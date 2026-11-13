import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { inboxService } from '../services/inbox';
import { actionsService } from '../services/actions';
import { api } from '../services/api';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { RefreshCw, Inbox as InboxIcon, Paperclip, Sparkles, Wand2 } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { cn } from '../utils/cn';
import type { Email } from '../types/api';

export function Inbox({ filterType = 'all' }: { filterType?: 'all' | 'important' | 'unread' }) {
  const queryClient = useQueryClient();
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);
  const [draftText, setDraftText] = useState<string | null>(null);

  const { data: emails = [], isLoading } = useQuery({
    queryKey: ['emails', filterType],
    queryFn: async () => {
      let url = '/inbox';
      if (filterType === 'important') url += '?priority=high';
      if (filterType === 'unread') url += '?is_read=false';
      const { data } = await api.get<Email[]>(url);
      return data;
    },
  });

  const syncMutation = useMutation({
    mutationFn: inboxService.syncEmails,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['emails'] });
      alert(`Sync complete! Synced ${data.synced} emails, analyzed ${data.analyzed}.`);
    },
    onError: (error: any) => {
      console.error(error);
      alert(`Sync failed: ${error.response?.data?.detail || error.message}`);
    }
  });

  const draftMutation = useMutation({
    mutationFn: (emailId: string) => actionsService.draftReply(emailId),
    onSuccess: (data) => {
      setDraftText(data);
    },
    onError: (error: any) => {
      console.error(error);
      alert(`Failed to generate draft: ${error.response?.data?.detail || error.message}`);
    }
  });

  const handleSelectEmail = (email: Email) => {
    setSelectedEmail(email);
    setDraftText(null); 
  };

  return (
    <div className="h-full flex flex-col space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 capitalize">
            {filterType === 'all' ? 'Inbox' : filterType}
          </h1>
          <p className="text-slate-500 text-sm mt-1">
            {filterType === 'all' ? 'Your recent emails, analyzed by AI.' : 
             filterType === 'important' ? 'Emails marked as high priority.' : 
             'Emails you haven\'t read yet.'}
          </p>
        </div>
        <Button 
          onClick={() => syncMutation.mutate()} 
          isLoading={syncMutation.isPending}
          variant="secondary"
        >
          <RefreshCw className={cn("w-4 h-4 mr-2", syncMutation.isPending && "animate-spin")} />
          {syncMutation.isPending ? 'Syncing & Analyzing...' : 'Sync Emails'}
        </Button>
      </div>

      <div className="flex-1 flex gap-4 min-h-0">
        <Card className="w-1/3 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto divide-y divide-slate-100 dark:divide-slate-800">
            {isLoading ? (
              <div className="p-4 text-center text-sm text-slate-500">Loading...</div>
            ) : emails.length === 0 ? (
              <div className="p-8 text-center flex flex-col items-center">
                <InboxIcon className="w-8 h-8 text-slate-300 mb-3" />
                <p className="text-sm text-slate-500">No emails found.</p>
                <p className="text-xs text-slate-400 mt-1">Click Sync to fetch from Gmail.</p>
              </div>
            ) : (
              emails.map((email) => (
                <button
                  key={email.id}
                  onClick={() => handleSelectEmail(email)}
                  className={cn(
                    "w-full text-left p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors",
                    selectedEmail?.id === email.id && "bg-brand-50 dark:bg-brand-500/10",
                    !email.is_read && "bg-blue-50/50 dark:bg-blue-500/5"
                  )}
                >
                  <div className="flex justify-between items-start mb-1">
                    <span className={cn("text-sm font-medium truncate pr-2", !email.is_read && "text-slate-900 dark:text-slate-100")}>
                      {email.sender_name || email.sender_email || 'Unknown Sender'}
                    </span>
                    <span className="text-xs text-slate-400 whitespace-nowrap">
                      {email.received_at ? formatDistanceToNow(new Date(email.received_at), { addSuffix: true }) : ''}
                    </span>
                  </div>
                  
                  <div className={cn("text-sm truncate", !email.is_read ? "font-semibold text-slate-800 dark:text-slate-200" : "text-slate-600 dark:text-slate-400")}>
                    {email.subject || '(No Subject)'}
                  </div>
                  
                  {email.summary_short && (
                    <div className="text-xs text-slate-500 truncate mt-1">
                      {email.summary_short}
                    </div>
                  )}

                  <div className="flex items-center gap-2 mt-2">
                    {email.category && (
                      <span className="px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider rounded-full bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                        {email.category}
                      </span>
                    )}
                    {email.priority_label && (
                      <span className={cn(
                        "px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider rounded-full",
                        email.priority_label === 'high' && "bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-400",
                        email.priority_label === 'normal' && "bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-400",
                        email.priority_label === 'low' && "bg-green-100 text-green-700 dark:bg-green-500/20 dark:text-green-400",
                      )}>
                        {email.priority_label}
                      </span>
                    )}
                    {email.has_attachment && <Paperclip className="w-3 h-3 text-slate-400" />}
                  </div>
                </button>
              ))
            )}
          </div>
        </Card>

        <Card className="flex-1 flex flex-col overflow-hidden">
          {selectedEmail ? (
            <div className="p-6 flex flex-col h-full overflow-y-auto">
              <div className="flex items-start justify-between gap-4 mb-4">
                <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
                  {selectedEmail.subject || '(No Subject)'}
                </h2>
                <Button 
                  onClick={() => draftMutation.mutate(selectedEmail.id)}
                  isLoading={draftMutation.isPending}
                  variant="secondary"
                  className="whitespace-nowrap"
                >
                  <Wand2 className="w-4 h-4 mr-2" />
                  {draftMutation.isPending ? 'Drafting...' : 'Draft Reply'}
                </Button>
              </div>

              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-slate-100 dark:border-slate-800">
                <div className="w-10 h-10 rounded-full bg-brand-100 dark:bg-brand-900/50 flex items-center justify-center text-brand-700 dark:text-brand-300 font-bold">
                  {(selectedEmail.sender_name?.[0] || selectedEmail.sender_email?.[0] || '?').toUpperCase()}
                </div>
                <div>
                  <div className="font-medium text-slate-900 dark:text-slate-100">{selectedEmail.sender_name || 'Unknown'}</div>
                  <div className="text-xs text-slate-500">{selectedEmail.sender_email}</div>
                </div>
              </div>

              {selectedEmail.summary_short && (
                <div className="mb-6 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-800">
                  <div className="flex items-center gap-2 mb-2 text-brand-600 dark:text-brand-400 font-medium text-sm">
                    <Sparkles className="w-4 h-4" />
                    AI Summary
                  </div>
                  <p className="text-sm text-slate-700 dark:text-slate-300">
                    {selectedEmail.summary_short}
                  </p>
                </div>
              )}

              <div className="prose dark:prose-invert max-w-none text-slate-700 dark:text-slate-300">
                <p className="whitespace-pre-wrap leading-relaxed">{selectedEmail.snippet}</p>
                <p className="text-sm text-slate-400 mt-8 italic">
                  (Full email body fetching will be implemented in a future milestone)
                </p>
              </div>

              {draftText && (
                <div className="mt-8 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-brand-100 dark:border-brand-500/20">
                  <div className="flex items-center gap-2 mb-3 text-brand-600 dark:text-brand-400 font-medium text-sm">
                    <Sparkles className="w-4 h-4" />
                    AI Generated Draft (Saved to Gmail Drafts)
                  </div>
                  <textarea
                    className="w-full h-40 p-3 text-sm bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 text-slate-900 dark:text-slate-100"
                    value={draftText}
                    onChange={(e) => setDraftText(e.target.value)}
                  />
                  <div className="mt-3 flex justify-end gap-2">
                    <Button variant="ghost" onClick={() => setDraftText(null)}>
                      Discard
                    </Button>
                    <Button onClick={() => alert('Sending will be implemented in the next update')}>
                      Send Email
                    </Button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-slate-400">
              <InboxIcon className="w-12 h-12 mb-4 opacity-20" />
              <p>Select an email to read</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}