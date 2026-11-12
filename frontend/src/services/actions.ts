import { api } from './api';

export const actionsService = {
  async draftReply(emailId: string): Promise<string> {
    const { data } = await api.post<{ status: string; draft_text: string }>('/actions/draft', { email_id: emailId });
    return data.draft_text;
  }
};