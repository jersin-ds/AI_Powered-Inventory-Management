import { useState } from 'react';
import { Bell, Search, Moon, Sun, LogOut, User, Menu, Check } from 'lucide-react';
import { useAuthStore } from '../../store/auth-store';
import { useUIStore } from '../../store/ui-store';
import { useNavigate } from 'react-router';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import api from '../../services/api';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';

export function AppNavbar() {
  const { user, logout } = useAuthStore();
  const { theme, setTheme, toggleMobileSidebar } = useUIStore();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState('');

  const { data: alerts = [] } = useQuery({
    queryKey: ['alerts'],
    queryFn: async () => {
      const { data } = await api.get('/alerts', { params: { unread_only: true } });
      return data;
    },
    refetchInterval: 30000,
  });

  const unreadCount = alerts.length;

  const handleMarkRead = async (alertId: string) => {
    try {
      await api.put(`/alerts/${alertId}/read`);
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    } catch {}
  };

  const handleMarkAllRead = async () => {
    try {
      await api.put('/alerts/read-all');
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    } catch {}
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const handleSearch = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && searchQuery.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchQuery.trim())}`);
      setSearchQuery('');
    }
  };

  const getAlertColor = (type: string) => {
    switch (type) {
      case 'low_stock':
        return { bg: 'bg-amber-500/10', border: 'border-amber-500/20', text: 'text-amber-600' };
      case 'out_of_stock':
        return { bg: 'bg-red-500/10', border: 'border-red-500/20', text: 'text-red-600' };
      case 'expiry':
        return { bg: 'bg-purple-500/10', border: 'border-purple-500/20', text: 'text-purple-600' };
      default:
        return { bg: 'bg-blue-500/10', border: 'border-blue-500/20', text: 'text-blue-600' };
    }
  };

  const getAlertLabel = (type: string) => {
    switch (type) {
      case 'low_stock': return 'Low Stock Alert';
      case 'out_of_stock': return 'Out of Stock';
      case 'expiry': return 'Expiry Warning';
      default: return type.replace('_', ' ');
    }
  };

  return (
    <header className="h-16 glass border-b border-white/10 px-4 sm:px-6 flex items-center justify-between gap-4">
      {/* Mobile Menu Button */}
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden"
        onClick={toggleMobileSidebar}
      >
        <Menu className="h-5 w-5" />
      </Button>

      {/* Search */}
      <div className="flex-1 max-w-md hidden sm:block">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search products, orders, customers..."
            className="pl-10 bg-white/5 border-white/10"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleSearch}
          />
        </div>
      </div>

      {/* Mobile Search Button */}
      <Button
        variant="ghost"
        size="icon"
        className="sm:hidden"
      >
        <Search className="h-5 w-5" />
      </Button>

      {/* Actions */}
      <div className="flex items-center gap-2 sm:gap-4">
        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 hover:bg-white/10 rounded-lg transition-colors"
        >
          {theme === 'dark' ? (
            <Sun className="w-5 h-5" />
          ) : (
            <Moon className="w-5 h-5" />
          )}
        </button>

        {/* Notifications */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="relative p-2 hover:bg-white/10 rounded-lg transition-colors">
              <Bell className="w-5 h-5" />
              {unreadCount > 0 && (
                <Badge className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0 bg-red-500 text-white text-xs">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </Badge>
              )}
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-80 glass">
            <div className="flex items-center justify-between px-2">
              <DropdownMenuLabel>Notifications</DropdownMenuLabel>
              {unreadCount > 0 && (
                <Button variant="ghost" size="sm" className="text-xs h-7" onClick={handleMarkAllRead}>
                  <Check className="h-3 w-3 mr-1" />
                  Mark all read
                </Button>
              )}
            </div>
            <DropdownMenuSeparator />
            <div className="space-y-2 p-2 max-h-80 overflow-y-auto">
              {alerts.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">
                  No new notifications
                </p>
              ) : (
                alerts.slice(0, 8).map((alert: any) => {
                  const colors = getAlertColor(alert.type);
                  return (
                    <div
                      key={alert.id}
                      className={`p-3 rounded-lg ${colors.bg} border ${colors.border} cursor-pointer hover:opacity-80 transition-opacity`}
                      onClick={() => handleMarkRead(alert.id)}
                    >
                      <p className={`text-sm font-medium ${colors.text}`}>
                        {getAlertLabel(alert.type)}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {alert.message || alert.title}
                      </p>
                    </div>
                  );
                })
              )}
            </div>
          </DropdownMenuContent>
        </DropdownMenu>

        {/* User Menu */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="flex items-center gap-3 p-2 hover:bg-white/10 rounded-lg transition-colors">
              <Avatar className="h-8 w-8">
                <AvatarImage src={user?.avatar} />
                <AvatarFallback>{user?.name.charAt(0)}</AvatarFallback>
              </Avatar>
              <div className="text-left hidden md:block">
                <p className="text-sm font-medium">{user?.name}</p>
                <p className="text-xs text-muted-foreground capitalize">
                  {user?.role.replace('_', ' ')}
                </p>
              </div>
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56 glass">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => navigate('/settings')}>
              <User className="mr-2 h-4 w-4" />
              <span>Profile Settings</span>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout} className="text-red-600">
              <LogOut className="mr-2 h-4 w-4" />
              <span>Logout</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}