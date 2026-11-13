import { useQuery } from '@tanstack/react-query';
import { analyticsService } from '../services/analytics';
import { Card } from '../components/ui/Card';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b', '#3b82f6'];

export function Analytics() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboardStats'],
    queryFn: analyticsService.getDashboardStats,
  });

  if (isLoading) return <div className="p-8 text-center text-slate-500">Loading analytics...</div>;

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Analytics</h1>
        <p className="text-slate-500 text-sm mt-1">Insights into your inbox activity.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Email Categories */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 text-slate-900 dark:text-slate-100">Email Categories</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats?.categories || []}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {(stats?.categories || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-wrap gap-4 mt-4 justify-center">
            {(stats?.categories || []).map((entry, index) => (
              <div key={entry.name} className="flex items-center gap-2 text-sm">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }} />
                <span className="text-slate-600 dark:text-slate-400">{entry.name} ({entry.value})</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Emails Over Time */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 text-slate-900 dark:text-slate-100">Emails (Last 7 Days)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.timeline || []}>
                <XAxis dataKey="date" stroke="#8884d8" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#8884d8" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip cursor={{ fill: 'transparent' }} />
                <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
}