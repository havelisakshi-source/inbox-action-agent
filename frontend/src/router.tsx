import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppLayout } from './layouts/AppLayout';
import { AuthLayout } from './layouts/AuthLayout';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Inbox } from './pages/Inbox';
import { Important } from './pages/Important';
import { Unread } from './pages/Unread';
import { Followups } from './pages/Followups';
import { ActionCenter } from './pages/ActionCenter';
import { History } from './pages/History';
import { Analytics } from './pages/Analytics';
import { Settings } from './pages/Settings';
import { Assistant } from './pages/Assistant';
import { Tasks } from './pages/Tasks';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'inbox', element: <Inbox /> },
      { path: 'important', element: <Important /> },
      { path: 'unread', element: <Unread /> },
      { path: 'followups', element: <Followups /> },
      { path: 'assistant', element: <Assistant /> },
      { path: 'actions', element: <ActionCenter /> },
      { path: 'tasks', element: <Tasks /> },
      { path: 'analytics', element: <Analytics /> },
      { path: 'history', element: <History /> },
      { path: 'settings', element: <Settings /> },
    ],
  },
  {
    path: '/',
    element: <AuthLayout />,
    children: [
      { path: 'login', element: <Login /> },
      { path: 'register', element: <Register /> },
    ],
  },
  { path: '*', element: <Navigate to="/" replace /> },
]);