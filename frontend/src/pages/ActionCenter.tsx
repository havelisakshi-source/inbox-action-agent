import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { Card } from '../components/ui/Card';
import { CheckSquare, CheckCircle2, Clock } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export function ActionCenter() {
  const { data: actions = [], isLoading } = useQuery({
    queryKey: ['actions'],
    queryFn: async () => {
      const { data } = await api.get('/actions');
      return data;
    }
  });

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Action Center</h1>
        <p className="text-slate-500 text-sm mt-1">View all AI-executed actions.</p>
      </div>

      <Card className="divide-y divide-slate-100 dark:divide-slate-800">
        {isLoading ? (
          <div className="p-8 text-center text-slate-500">Loading actions...</div>
        ) : actions.length === 0 ? (
          <div className="p-12 text-center flex flex-col items-center">
            <CheckSquare className="w-12 h-12 text-slate-300 mb-4" />
            <h3 className="text-lg font-medium text-slate-900 dark:text-slate-100">No actions yet</h3>
            <p className="text-slate-500 mt-2">When the AI drafts an email, it will appear here.</p>
          </div>
        ) : (
          actions.map((action: any) => (
            <div key={action.id} className="p-4 flex items-start gap-4 hover:bg-slate-50 dark:hover:bg-slate-800/50">
              <div className={`mt-1 p-2 rounded-full ${action.status === 'executed' ? 'bg-green-100 text-green-600 dark:bg-green-500/20' : 'bg-amber-100 text-amber-600'}`}>
                {action.status === 'executed' ? <CheckCircle2 className="w-5 h-5" /> : <Clock className="w-5 h-5" />}
              </div>
              <div className="flex-1">
                <p className="font-medium text-slate-900 dark:text-slate-100 capitalize">{action.action_type.replace('_', ' ')}</p>
                <p className="text-sm text-slate-500 mt-1">{action.reason}</p>
                <div className="flex items-center gap-4 mt-2 text-xs text-slate-400">
                  <span className="capitalize px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800">{action.status}</span>
                  <span>{formatDistanceToNow(new Date(action.created_at), { addSuffix: true })}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </Card>
    </div>
  );
}