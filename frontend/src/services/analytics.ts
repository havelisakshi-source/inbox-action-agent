import { api } from './api';

export interface DashboardStats {
  total_emails: number;
  unread_emails: number;
  high_priority_emails: number;
  categories: Record<string, number>;
}

export const analyticsService = {
  async getDashboardStats(): Promise<DashboardStats> {
    const { data } = await api.get<DashboardStats>('/analytics/dashboard');
    return data;
  }
};