export interface User {
  id: string;
  email: string;
  full_name: string | null;
  timezone: string;
  is_active: boolean;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface Email {
  id: string;
  gmail_message_id: string;
  sender_name: string | null;
  sender_email: string | null;
  subject: string | null;
  snippet: string | null;
  received_at: string | null;
  is_read: boolean;
  is_starred: boolean;
  has_attachment: boolean;
  
  // Add these AI fields:
  category: string | null;
  priority_score: number | null;
  priority_label: string | null;
  summary_short: string | null;
}