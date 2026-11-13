import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, Inbox, Star, Mail, RefreshCw, MessageSquare, 
  CheckSquare, ListTodo, BarChart2, History, Settings, X
} from 'lucide-react';
import { cn } from '../../utils/cn';

const navItems = [
  { to: '/', label: 'Overview', icon: LayoutDashboard },
  { to: '/inbox', label: 'Inbox', icon: Inbox },
  { to: '/important', label: 'Important', icon: Star },
  { to: '/unread', label: 'Unread', icon: Mail },
  { to: '/followups', label: 'Follow-ups', icon: RefreshCw },
  { to: '/assistant', label: 'AI Assistant', icon: MessageSquare },
  { to: '/actions', label: 'Action Center', icon: CheckSquare },
  { to: '/tasks', label: 'Tasks & Deadlines', icon: ListTodo },
  { to: '/analytics', label: 'Analytics', icon: BarChart2 },
  { to: '/history', label: 'Activity History', icon: History },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export function Sidebar({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  return (
    <>
      {/* Mobile Backdrop */}
      <div 
        className={cn(
          "fixed inset-0 z-[90] bg-slate-900/60 backdrop-blur-sm transition-opacity md:hidden",
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        onClick={onClose}
      />

      {/* Sidebar */}
      <aside className={cn(
        "fixed inset-y-0 left-0 z-[100] w-64 border-r border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900 flex flex-col transform transition-transform duration-200 ease-in-out md:relative md:translate-x-0",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="h-16 flex items-center justify-between px-6 border-b border-slate-200 dark:border-slate-800">
          <span className="text-xl font-bold text-brand-600 dark:text-brand-500 tracking-tight">Inbox Agent</span>
          <button onClick={onClose} className="md:hidden p-1 text-slate-500 hover:bg-slate-100 rounded-md dark:hover:bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>
        <nav className="flex-1 overflow-y-auto p-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={() => { if (window.innerWidth < 768) onClose(); }}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400'
                    : 'text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800'
                )
              }
            >
              <item.icon className="w-5 h-5" />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
    </>
  );
}