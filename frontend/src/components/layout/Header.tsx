import { useAuth } from '../../hooks/useAuth';
import { LogOut, Menu } from 'lucide-react';
import { Button } from '../ui/Button';

export function Header({ onMenuClick }: { onMenuClick: () => void }) {
  const { user, logout } = useAuth();

  return (
    <header className="h-16 border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900 flex items-center justify-between px-4 md:px-6 flex-shrink-0">
      <div className="flex items-center gap-4">
        <button onClick={onMenuClick} className="md:hidden p-2 -ml-2 text-slate-500 hover:bg-slate-100 rounded-md dark:hover:bg-slate-800">
          <Menu className="w-5 h-5" />
        </button>
        <div className="font-medium text-slate-700 dark:text-slate-300 truncate max-w-[200px] md:max-w-none">
          Welcome back, {user?.full_name || user?.email.split('@')[0]}
        </div>
      </div>
      <Button variant="ghost" size="sm" onClick={logout} className="text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200">
        <LogOut className="w-4 h-4 md:mr-2" />
        <span className="hidden md:inline">Sign out</span>
      </Button>
    </header>
  );
}