import { Outlet } from 'react-router';
import { AppSidebar } from './app-sidebar';
import { AppNavbar } from './app-navbar';
import { AIChat } from '../ai/ai-chat';
import { useUIStore } from '../../store/ui-store';

export function RootLayout() {
  const { sidebarCollapsed } = useUIStore();

  return (
    <div className="min-h-screen bg-gradient-primary">
      <AppSidebar />
      <div
        className={`transition-all duration-300 ${
          sidebarCollapsed ? 'lg:ml-16' : 'lg:ml-64'
        } ml-0`}
      >
        <AppNavbar />
        <main className="p-4 sm:p-6">
          <Outlet />
        </main>
      </div>
      <AIChat />
    </div>
  );
}