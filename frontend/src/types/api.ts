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
  
  category: string | null;
  priority_score: number | null;
  priority_label: string | null;
  summary_short: string | null;
}

export interface DashboardStats {
  total_emails: number;
  unread_emails: number;
  high_priority_emails: number;
  categories: { name: string; value: number }[];
  timeline: { date: string; count: number }[];
}