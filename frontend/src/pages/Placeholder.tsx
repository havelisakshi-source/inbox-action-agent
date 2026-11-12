// src/pages/Placeholder.tsx
export function Placeholder({ title }: { title: string }) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">{title}</h2>
      <p className="text-slate-500 mt-2">This page will be implemented in a future milestone.</p>
    </div>
  );
}