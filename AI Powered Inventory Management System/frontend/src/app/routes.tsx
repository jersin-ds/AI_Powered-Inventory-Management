import { createBrowserRouter, Navigate } from 'react-router';
import { RootLayout } from './components/layout/root-layout';
import { ProtectedRoute } from './components/auth/protected-route';
import { LoginPage } from './pages/login-page';
import { DashboardPage } from './pages/dashboard-page';
import { ProductsPage } from './pages/products-page';
import { ProductDetailPage } from './pages/product-detail-page';
import { CategoriesPage } from './pages/categories-page';
import { SuppliersPage } from './pages/suppliers-page';
import { WarehousesPage } from './pages/warehouses-page';
import { StockPage } from './pages/stock-page';
import { PurchasesPage } from './pages/purchases-page';
import { NewPurchasePage } from './pages/new-purchase-page';
import { SalesPage } from './pages/sales-page';
import { NewSalePage } from './pages/new-sale-page';
import { ReportsPage } from './pages/reports-page';
import { AnalyticsPage } from './pages/analytics-page';
import { AIInsightsPage } from './pages/ai-insights-page';
import { SettingsPage } from './pages/settings-page';
import { UsersPage } from './pages/users-page';
import { UnauthorizedPage } from './pages/unauthorized-page';

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/unauthorized',
    element: <UnauthorizedPage />,
  },
  {
    path: '/',
    element: <RootLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: 'dashboard',
        element: (
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'products',
        element: (
          <ProtectedRoute requiredPermission="products.view">
            <ProductsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'products/:id',
        element: (
          <ProtectedRoute requiredPermission="products.view">
            <ProductDetailPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'categories',
        element: (
          <ProtectedRoute requiredPermission="products.view">
            <CategoriesPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'suppliers',
        element: (
          <ProtectedRoute requiredPermission="products.view">
            <SuppliersPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'warehouses',
        element: (
          <ProtectedRoute requiredPermission="warehouses.view">
            <WarehousesPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'stock',
        element: (
          <ProtectedRoute requiredPermission="stock.view">
            <StockPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'purchases',
        element: (
          <ProtectedRoute requiredPermission="purchases.view">
            <PurchasesPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'purchases/new',
        element: (
          <ProtectedRoute requiredPermission="purchases.create">
            <NewPurchasePage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'sales',
        element: (
          <ProtectedRoute requiredPermission="sales.view">
            <SalesPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'sales/new',
        element: (
          <ProtectedRoute requiredPermission="sales.create">
            <NewSalePage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'reports',
        element: (
          <ProtectedRoute requiredPermission="reports.view">
            <ReportsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'analytics',
        element: (
          <ProtectedRoute requiredPermission="reports.view">
            <AnalyticsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'ai-insights',
        element: (
          <ProtectedRoute requiredPermission="ai.view">
            <AIInsightsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'settings',
        element: (
          <ProtectedRoute>
            <SettingsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'users',
        element: (
          <ProtectedRoute requiredPermission="all">
            <UsersPage />
          </ProtectedRoute>
        ),
      },
    ],
  },
]);