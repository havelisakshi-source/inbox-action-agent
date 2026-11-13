import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { Card } from '../components/ui/Card';
import { ListTodo, Calendar } from 'lucide-react';
import { format } from 'date-fns';

export function Tasks() {
  const { data: tasks = [], isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: async () => {
      const { data } = await api.get('/tasks');
      return data;
    }
  });

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Tasks & Deadlines</h1>
        <p className="text-slate-500 text-sm mt-1">Manage action items extracted from your inbox.</p>
      </div>

      <Card className="divide-y divide-slate-100 dark:divide-slate-800">
        {isLoading ? (
          <div className="p-8 text-center text-slate-500">Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div className="p-12 text-center flex flex-col items-center">
            <ListTodo className="w-12 h-12 text-slate-300 mb-4" />
            <h3 className="text-lg font-medium text-slate-900 dark:text-slate-100">No tasks found</h3>
            <p className="text-slate-500 mt-2 max-w-sm">
              When the AI detects actionable items or deadlines in your emails, they will appear here.
            </p>
          </div>
        ) : (
          tasks.map((task: any) => (
            <div key={task.id} className="p-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-800/50">
              <div>
                <p className="font-medium text-slate-900 dark:text-slate-100">{task.description}</p>
                <div className="flex items-center gap-4 mt-1 text-xs text-slate-500">
                  <span className="capitalize">{task.status}</span>
                  {task.deadline && (
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {format(new Date(task.deadline), 'MMM d, yyyy')}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </Card>
    </div>
  );
}