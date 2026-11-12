import { api } from './api';
import type { Email } from '../types/api';

export const inboxService = {
  async getEmails(): Promise<Email[]> {
    const { data } = await api.get<Email[]>('/inbox');
    return data;
  },
  
  async syncEmails(): Promise<{ status: string; synced: number }> {
    const { data } = await api.post('/inbox/sync');
    return data;
  },

  async getGoogleAuthUrl(): Promise<string> {
    const { data } = await api.get<{ auth_url: string }>('/auth/google/connect');
    return data.auth_url;
  }
};