from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.core.config import settings
from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    generate_opaque_token,
    hash_opaque_token,
    hash_password,
    verify_password,
    encrypt_token,
)
from app.integrations.gmail.authentication import create_oauth_flow
from app.models.user import RefreshToken, UserPreference, OAuthCredential
from app.repositories.user_repo import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.audit_service import AuditService

router = APIRouter()


def _client_meta(request: Request) -> tuple[str | None, str | None]:
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    return ip, ua


async def _issue_tokens(db, user_id: str, request: Request) -> TokenResponse:
    access = create_access_token(user_id)
    refresh_plain = generate_opaque_token()
    refresh_hash = hash_opaque_token(refresh_plain)
    ip, ua = _client_meta(request)

    token = RefreshToken(
        user_id=user_id,
        token_hash=refresh_hash,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        user_agent=ua,
        ip=ip,
    )
    db.add(token)
    await db.flush()

    return TokenResponse(
        access_token=access,
        refresh_token=refresh_plain,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(payload: RegisterRequest, request: Request, db: DbSession) -> TokenResponse:
    repo = UserRepository(db)
    existing = await repo.get_by_email(payload.email)
    if existing is not None:
        raise ConflictError("An account with this email already exists")

    user = await repo.create(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
    )
    db.add(UserPreference(user_id=user.id))

    audit = AuditService(db)
    ip, ua = _client_meta(request)
    await audit.log(
        operation="auth.register",
        user_id=user.id,
        actor="user",
        resource_type="user",
        resource_id=user.id,
        ip=ip,
        user_agent=ua,
    )
    tokens = await _issue_tokens(db, user.id, request)
    await db.commit()
    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request, db: DbSession) -> TokenResponse:
    repo = UserRepository(db)
    user = await repo.get_by_email(payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")
    if not user.is_active:
        raise UnauthorizedError("Account is inactive")

    audit = AuditService(db)
    ip, ua = _client_meta(request)
    await audit.log(
        operation="auth.login",
        user_id=user.id,
        actor="user",
        resource_type="user",
        resource_id=user.id,
        ip=ip,
        user_agent=ua,
    )
    tokens = await _issue_tokens(db, user.id, request)
    await db.commit()
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, request: Request, db: DbSession) -> TokenResponse:
    token_hash = hash_opaque_token(payload.refresh_token)
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
    record = result.scalar_one_or_none()

    if record is None or record.revoked_at is not None:
        raise UnauthorizedError("Invalid refresh token")

    now = datetime.now(timezone.utc)
    if record.expires_at.tzinfo is None:
        record_expires = record.expires_at.replace(tzinfo=timezone.utc)
    else:
        record_expires = record.expires_at

    if record_expires <= now:
        record.revoked_at = now
        await db.commit()
        raise UnauthorizedError("Refresh token expired")

    record.revoked_at = now
    tokens = await _issue_tokens(db, record.user_id, request)
    await db.commit()
    return tokens


@router.post("/logout", status_code=204)
async def logout(payload: RefreshRequest, db: DbSession) -> None:
    token_hash = hash_opaque_token(payload.refresh_token)
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
    record = result.scalar_one_or_none()
    if record is not None and record.revoked_at is None:
        record.revoked_at = datetime.now(timezone.utc)
        await db.commit()


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)


# ---------------------------------------------------------------------------
# Google OAuth Endpoints
# ---------------------------------------------------------------------------

@router.get("/google/connect")
async def google_connect(current_user: CurrentUser) -> dict:
    flow = create_oauth_flow()
    auth_url, _ = flow.authorization_url(
        access_type="offline", 
        prompt="consent",
        state=current_user.id
    )
    return {"auth_url": auth_url}


@router.get("/google/callback")
async def google_callback(code: str, state: str, db: DbSession):
    user_id = state
    flow = create_oauth_flow()
    flow.fetch_token(code=code)
    creds = flow.credentials

    encrypted_access = encrypt_token(creds.token)
    encrypted_refresh = encrypt_token(creds.refresh_token) if creds.refresh_token else None

    res = await db.execute(select(OAuthCredential).where(OAuthCredential.user_id == user_id))
    existing = res.scalar_one_or_none()

    if existing:
        existing.encrypted_access_token = encrypted_access
        existing.encrypted_refresh_token = encrypted_refresh
        existing.token_expiry = creds.expiry
    else:
        new_cred = OAuthCredential(
            user_id=user_id,
            encrypted_access_token=encrypted_access,
            encrypted_refresh_token=encrypted_refresh,
            token_expiry=creds.expiry,
        )
        db.add(new_cred)

    await db.commit()
    
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/settings?gmail=connected")


@router.get("/google/status")
async def google_status(current_user: CurrentUser, db: DbSession):
    res = await db.execute(select(OAuthCredential).where(OAuthCredential.user_id == current_user.id))
    cred = res.scalar_one_or_none()
    return {"connected": cred is not None}