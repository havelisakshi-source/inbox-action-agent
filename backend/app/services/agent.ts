import { api } from './api';

export const agentService = {
  async chat(message: string): Promise<string> {
    const { data } = await api.post<{ response: string }>('/agent/chat', { message });
    return data.response;
  }
};