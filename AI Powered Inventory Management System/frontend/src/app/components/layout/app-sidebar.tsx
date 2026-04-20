import { Link, useLocation } from 'react-router';
import {
  LayoutDashboard,
  Package,
  Warehouse,
  ShoppingCart,
  TrendingUp,
  BarChart3,
  Brain,
  Settings,
  Users,
  ChevronLeft,
  ChevronRight,
  Layers,
  Truck,
  IndianRupee,
  X,
} from 'lucide-react';
import { useUIStore } from '../../store/ui-store';
import { useAuthStore } from '../../store/auth-store';
import { cn } from '../ui/utils';

interface NavItem {
  name: string;
  path: string;
  icon: React.ElementType;
  permission?: string;
}

const navItems: NavItem[] = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Products', path: '/products', icon: Package, permission: 'products.view' },
  { name: 'Categories', path: '/categories', icon: Layers, permission: 'products.view' },
  { name: 'Suppliers', path: '/suppliers', icon: Truck, permission: 'products.view' },
  { name: 'Warehouses', path: '/warehouses', icon: Warehouse, permission: 'warehouses.view' },
  { name: 'Stock', path: '/stock', icon: Package, permission: 'stock.view' },
  { name: 'Purchases', path: '/purchases', icon: ShoppingCart, permission: 'purchases.view' },
  { name: 'Sales', path: '/sales', icon: IndianRupee, permission: 'sales.view' },
  { name: 'Reports', path: '/reports', icon: BarChart3, permission: 'reports.view' },
  { name: 'Analytics', path: '/analytics', icon: TrendingUp, permission: 'reports.view' },
  { name: 'AI Insights', path: '/ai-insights', icon: Brain, permission: 'ai.view' },
  { name: 'Users', path: '/users', icon: Users, permission: 'all' },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export function AppSidebar() {
  const { sidebarCollapsed, toggleSidebar, mobileSidebarOpen, toggleMobileSidebar } = useUIStore();
  const { hasPermission } = useAuthStore();
  const location = useLocation();

  const filteredNavItems = navItems.filter(
    (item) => !item.permission || hasPermission(item.permission)
  );

  const handleNavClick = () => {
    // Close mobile sidebar on navigation
    if (mobileSidebarOpen) {
      toggleMobileSidebar();
    }
  };

  return (
    <>
      {/* Mobile Overlay */}
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={toggleMobileSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed left-0 top-0 h-screen glass z-50 transition-all duration-300',
          // Desktop - always visible
          'hidden lg:block',
          sidebarCollapsed ? 'lg:w-16' : 'lg:w-64',
          // Mobile - show/hide based on state
          mobileSidebarOpen ? 'block translate-x-0 w-64' : 'translate-x-full lg:translate-x-0'
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="h-16 flex items-center justify-between px-4 border-b border-white/10">
            {!sidebarCollapsed && (
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <span className="font-semibold text-sm">AI Inventory</span>
              </div>
            )}
            {/* Desktop toggle */}
            <button
              onClick={toggleSidebar}
              className="hidden lg:block p-1.5 hover:bg-white/10 rounded-lg transition-colors"
            >
              {sidebarCollapsed ? (
                <ChevronRight className="w-5 h-5" />
              ) : (
                <ChevronLeft className="w-5 h-5" />
              )}
            </button>
            {/* Mobile close */}
            <button
              onClick={toggleMobileSidebar}
              className="lg:hidden p-1.5 hover:bg-white/10 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto py-4 px-2">
            <div className="space-y-1">
              {filteredNavItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;

                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={handleNavClick}
                    className={cn(
                      'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all',
                      'hover:bg-white/10',
                      isActive && 'bg-blue-500/20 text-blue-400 border border-blue-500/30',
                      sidebarCollapsed && 'lg:justify-center'
                    )}
                    title={sidebarCollapsed ? item.name : undefined}
                  >
                    <Icon className="w-5 h-5 flex-shrink-0" />
                    <span className={cn(
                      'text-sm font-medium',
                      sidebarCollapsed && 'lg:hidden'
                    )}>
                      {item.name}
                    </span>
                  </Link>
                );
              })}
            </div>
          </nav>
        </div>
      </aside>
    </>
  );
}