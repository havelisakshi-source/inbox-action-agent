import { api } from './api';
import type { User, TokenResponse } from '../types/api';

export const authService = {
  async login(email: string, password: string): Promise<TokenResponse> {
    const { data } = await api.post<TokenResponse>('/auth/login', { email, password });
    return data;
  },

  async register(email: string, password: string, fullName?: string): Promise<TokenResponse> {
    const { data } = await api.post<TokenResponse>('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return data;
  },

  async getMe(): Promise<User> {
    const { data } = await api.get<User>('/auth/me');
    return data;
  },

  async logout(refreshToken: string): Promise<void> {
    await api.post('/auth/logout', { refresh_token: refreshToken });
  },

  async getGoogleStatus(): Promise<boolean> {
    const { data } = await api.get<{ connected: boolean }>('/auth/google/status');
    return data.connected;
  }
};