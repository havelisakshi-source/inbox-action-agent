import { api } from './api';
import type { DashboardStats } from '../types/api';

export const analyticsService = {
  async getDashboardStats(): Promise<DashboardStats> {
    const { data } = await api.get<DashboardStats>('/analytics/dashboard');
    return data;
  }
};