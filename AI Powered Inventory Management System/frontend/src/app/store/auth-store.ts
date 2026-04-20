import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import api from '../services/api';

export type UserRole = 'admin' | 'inventory_manager' | 'sales_staff';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  avatar?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
  hasPermission: (permission: string) => boolean;
}

// Role permissions mapping
const rolePermissions: Record<UserRole, string[]> = {
  admin: ['all'],
  inventory_manager: [
    'products.view',
    'products.create',
    'products.edit',
    'products.delete',
    'stock.view',
    'stock.manage',
    'warehouses.view',
    'warehouses.manage',
    'purchases.view',
    'purchases.create',
    'reports.view',
    'ai.view',
    'ai.suggestions',
  ],
  sales_staff: [
    'products.view',
    'sales.view',
    'sales.create',
    'reports.view-limited',
    'ai.view',
  ],
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        const response = await api.post('/auth/login', { email, password });
        const { user, token } = response.data;

        set({
          user,
          token,
          isAuthenticated: true,
        });
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },

      setUser: (user: User) => {
        set({ user });
      },

      hasPermission: (permission: string) => {
        const { user } = get();
        if (!user) return false;
        
        const permissions = rolePermissions[user.role];
        return permissions.includes('all') || permissions.includes(permission);
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
