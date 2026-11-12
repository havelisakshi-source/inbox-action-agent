# 📬 Inbox Action Agent

An intelligent, multi-agent email management and automation platform. It connects to your Gmail account, uses AI to classify and prioritize your emails, and allows you to chat with your inbox or generate context-aware drafts.

## 🚀 Features

- **Gmail Integration:** Secure OAuth 2.0 connection to read, sync, and draft emails.
- **AI Email Analysis:** Automatically categorizes emails (Work, Promotions, Education, etc.) and assigns a priority score with a 1-line summary.
- **AI Assistant:** A conversational LangGraph agent that can query your database and answer questions about your inbox.
- **Draft Generation:** Generates professional, context-aware replies and saves them directly to your Gmail Drafts folder.
- **Analytics Dashboard:** Real-time metrics on your email volume, unread counts, and category breakdown.
- **Premium UI:** A modern, responsive React dashboard with dark/light mode.

## 🛠️ Tech Stack

- **Frontend:** React, Vite, TypeScript, Tailwind CSS, TanStack Query
- **Backend:** Python, FastAPI, SQLAlchemy (Async)
- **Database:** PostgreSQL (Production) / SQLite (Local testing)
- **AI & Agents:** LangGraph, LangChain, Groq API (OpenAI OSS models)
- **Integrations:** Google Gmail API, Google OAuth 2.0
