// Shared TypeScript interfaces for the application

export interface Product {
  id: string;
  sku: string;
  name: string;
  category: string;
  subcategory: string;
  supplier: string;
  costPrice: number;
  sellPrice: number;
  stockQty: number;
  minLevel: number;
  barcode: string;
  image?: string;
  status: 'active' | 'low_stock' | 'out_of_stock';
  createdAt: string;
}

export interface Warehouse {
  id: string;
  name: string;
  location: string;
  capacity: number;
  currentStock: number;
  manager: string;
  status: 'active' | 'inactive';
}

export interface Purchase {
  id: string;
  poNumber: string;
  supplier: string;
  date: string;
  status: 'pending' | 'received' | 'cancelled';
  totalAmount: number;
  items: Array<{
    productId: string;
    productName: string;
    quantity: number;
    price: number;
  }>;
}

export interface Sale {
  id: string;
  invoiceNumber: string;
  customer: string;
  date: string;
  status: 'completed' | 'pending' | 'cancelled';
  totalAmount: number;
  profit: number;
  items: Array<{
    productId: string;
    productName: string;
    quantity: number;
    price: number;
  }>;
}

export interface AIInsight {
  id: string;
  type: 'demand_forecast' | 'dead_stock' | 'anomaly' | 'price_optimization' | 'expiry_risk' | 'stockout_prediction';
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  actionable: boolean;
  data?: any;
  createdAt: string;
}

export interface DashboardSummary {
  summary: string;
  generatedAt: string;
}

export interface HealthScore {
  score: number;
  grade: string;
  breakdown: Record<string, any>;
  recommendation: string;
}

export interface ReorderSuggestion {
  productId: string;
  productName: string;
  currentStock: number;
  minLevel: number;
  dailySalesRate: number;
  suggestedQuantity: number;
  daysUntilStockout: number;
  reasoning: string;
}

export interface ReorderSuggestionsResponse {
  suggestions: ReorderSuggestion[];
  generatedAt: string;
}

export interface ReportNarrative {
  narrative: string;
  generatedAt: string;
}

export interface StockoutPrediction {
  productId: string;
  productName: string;
  currentStock: number;
  dailySalesRate: number;
  daysUntilStockout: number;
  urgency: 'critical' | 'warning' | 'watch';
  recommendation: string;
}

export interface StockoutPredictionsResponse {
  predictions: StockoutPrediction[];
  generatedAt: string;
}

export interface SalesSummary {
  summary: string;
  metrics: Record<string, any>;
  generatedAt: string;
}

export interface Category {
  id: string;
  name: string;
  description: string;
  productCount: number;
  subcategories: string[];
  status: 'active' | 'inactive';
  createdAt: string;
}

export interface Supplier {
  id: string;
  name: string;
  contactPerson: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  country: string;
  productsSupplied: number;
  totalOrders: number;
  totalValue: number;
  rating: number;
  status: 'active' | 'inactive';
  paymentTerms: string;
  createdAt: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'inventory_manager' | 'sales_staff';
  avatar?: string;
  status: 'active' | 'inactive';
  lastLogin: string;
  createdAt: string;
}
