// src/layouts/AuthLayout.tsx
import { Outlet } from 'react-router-dom';

export function AuthLayout() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-brand-600 dark:text-brand-500">Inbox Agent</h1>
          <p className="text-slate-500 mt-2 text-sm">AI-powered email management</p>
        </div>
        <Outlet />
      </div>
    </div>
  );
}