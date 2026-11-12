import { useQuery } from '@tanstack/react-query';
import { useAuth } from '../hooks/useAuth';
import { analyticsService } from '../services/analytics';
import { Card } from '../components/ui/Card';
import { Inbox, Mail, AlertCircle, TrendingUp, Sparkles } from 'lucide-react';

export function Dashboard() {
  const { user } = useAuth();
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboardStats'],
    queryFn: analyticsService.getDashboardStats,
  });

  if (isLoading) {
    return <div className="p-8 text-center text-slate-500">Loading your dashboard...</div>;
  }

  const statCards = [
    { label: 'Total Emails', value: stats?.total_emails || 0, icon: Inbox, color: 'text-blue-500', bg: 'bg-blue-50 dark:bg-blue-500/10' },
    { label: 'Unread', value: stats?.unread_emails || 0, icon: Mail, color: 'text-amber-500', bg: 'bg-amber-50 dark:bg-amber-500/10' },
    { label: 'High Priority', value: stats?.high_priority_emails || 0, icon: AlertCircle, color: 'text-red-500', bg: 'bg-red-50 dark:bg-red-500/10' },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Dashboard Overview</h1>
        <p className="text-slate-500 text-sm mt-1">Welcome back, {user?.full_name || 'User'}.</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {statCards.map((stat) => (
          <Card key={stat.label} className="p-6 flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-500">{stat.label}</p>
              <p className="text-3xl font-bold mt-1 text-slate-900 dark:text-slate-100">{stat.value}</p>
            </div>
            <div className={`p-4 rounded-full ${stat.bg} ${stat.color}`}>
              <stat.icon className="w-6 h-6" />
            </div>
          </Card>
        ))}
      </div>

      {/* Category Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-brand-500" />
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Inbox Breakdown</h3>
          </div>
          <div className="space-y-4">
            {Object.entries(stats?.categories || {}).map(([category, count]) => (
              <div key={category}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium text-slate-700 dark:text-slate-300">{category}</span>
                  <span className="text-slate-500">{count}</span>
                </div>
                <div className="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2">
                  <div 
                    className="bg-brand-500 h-2 rounded-full" 
                    style={{ width: `${(count / (stats?.total_emails || 1)) * 100}%` }}
                  />
                </div>
              </div>
            ))}
            {Object.keys(stats?.categories || {}).length === 0 && (
              <p className="text-sm text-slate-500 text-center py-4">No emails analyzed yet.</p>
            )}
          </div>
        </Card>

        {/* AI Insights */}
        <Card className="p-6 bg-gradient-to-br from-brand-50 to-white dark:from-slate-900 dark:to-slate-950 border-brand-100 dark:border-brand-900/50">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-brand-500" />
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">AI Daily Summary</h3>
          </div>
          <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
            You have <strong className="text-slate-900 dark:text-slate-100">{stats?.unread_emails || 0} unread emails</strong>. 
            Based on the AI analysis, <strong className="text-red-500">{stats?.high_priority_emails || 0} emails require immediate attention</strong>. 
            Consider using the AI Assistant to draft replies for your most important messages.
          </p>
        </Card>
      </div>
    </div>
  );
}