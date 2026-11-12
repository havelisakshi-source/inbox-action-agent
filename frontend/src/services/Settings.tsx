import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { inboxService } from '../services/inbox';
import { CheckCircle2, Mail, ShieldAlert } from 'lucide-react';

export function Settings() {
  const [searchParams] = useSearchParams();
  const [isConnecting, setIsConnecting] = useState(false);
  
  // Check if we just returned from Google OAuth
  const justConnected = searchParams.get('gmail') === 'connected';

  const handleConnect = async () => {
    try {
      setIsConnecting(true);
      const url = await inboxService.getGoogleAuthUrl();
      window.location.href = url; // Redirect to Google
    } catch (err) {
      console.error(err);
      setIsConnecting(false);
      alert('Failed to get Google Auth URL');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Settings</h1>
        <p className="text-slate-500 text-sm mt-1">Manage your integrations and preferences.</p>
      </div>

      {justConnected && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 rounded-xl flex items-start gap-3">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 mt-0.5" />
          <div>
            <h4 className="font-medium text-emerald-900 dark:text-emerald-100">Gmail Connected!</h4>
            <p className="text-sm text-emerald-700 dark:text-emerald-300 mt-1">
              Your account is successfully linked. Go to the Inbox to sync your emails.
            </p>
          </div>
        </div>
      )}

      <Card className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex gap-4">
            <div className="p-3 bg-red-50 dark:bg-red-500/10 rounded-xl text-red-500">
              <Mail className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Gmail Integration</h3>
              <p className="text-sm text-slate-500 mt-1 max-w-md">
                Connect your Gmail account to allow the AI to read, classify, and manage your inbox.
              </p>
            </div>
          </div>
          <Button onClick={handleConnect} isLoading={isConnecting}>
            {justConnected ? 'Reconnect Gmail' : 'Connect Gmail'}
          </Button>
        </div>

        <div className="mt-6 pt-6 border-t border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <ShieldAlert className="w-4 h-4" />
            <span>We use secure OAuth 2.0. We never see or store your password.</span>
          </div>
        </div>
      </Card>
    </div>
  );
}