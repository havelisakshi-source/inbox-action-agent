// src/components/layout/Header.tsx
import { useAuth } from '../../hooks/useAuth';
import { LogOut } from 'lucide-react';
import { Button } from '../ui/Button';

export function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="h-16 border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900 flex items-center justify-between px-6 flex-shrink-0">
      <div className="font-medium text-slate-700 dark:text-slate-300">
        Welcome back, {user?.full_name || user?.email.split('@')[0]}
      </div>
      <Button variant="ghost" size="sm" onClick={logout} className="text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200">
        <LogOut className="w-4 h-4 mr-2" />
        Sign out
      </Button>
    </header>
  );
}