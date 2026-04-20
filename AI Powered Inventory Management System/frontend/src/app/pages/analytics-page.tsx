import { useMemo } from 'react';
import { motion } from 'motion/react';
import {
  TrendingUp,
  TrendingDown,
  Activity,
  Users,
  Package,
  ShoppingCart,
  Sparkles,
  Brain,
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Badge } from '../components/ui/badge';
import { Skeleton } from '../components/ui/skeleton';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import { aiApi } from '../services/ai-api';

const COLORS = ['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'];
const SEGMENT_COLORS: Record<string, string> = {
  Enterprise: '#2563eb',
  SMB: '#3b82f6',
  Retail: '#60a5fa',
  Individual: '#93c5fd',
};
const RADAR_LINE_COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

export function AnalyticsPage() {
  const { data: dashboardStats } = useQuery({
    queryKey: ['dashboard', 'stats'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/stats');
      return data;
    },
  });
  const { data: revenueByCategory = [] } = useQuery({
    queryKey: ['dashboard', 'revenueByCategory'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/revenue-by-category');
      return data;
    },
  });
  const { data: topProducts = [] } = useQuery({
    queryKey: ['dashboard', 'topProducts'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/top-products');
      return data;
    },
  });
  const { data: monthlyData = [] } = useQuery({
    queryKey: ['dashboard', 'monthlyData'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/monthly-data');
      return data;
    },
  });
  const { data: categoryPerformance = [] } = useQuery({
    queryKey: ['dashboard', 'categoryPerformance'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/category-performance');
      return data;
    },
  });
  const { data: customerSegments = [] } = useQuery({
    queryKey: ['dashboard', 'customerSegments'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/customer-segments');
      return data;
    },
  });

  const { data: salesSummary, isLoading: salesSummaryLoading } = useQuery({
    queryKey: ['ai-sales-summary'],
    queryFn: () => aiApi.getSalesSummary(),
    staleTime: 5 * 60 * 1000,
  });

  // Derive radar chart data from category performance
  const radarCategories = useMemo(() => categoryPerformance.slice(0, 3).map((c: any) => c.category), [categoryPerformance]);
  const productPerformanceRadar = useMemo(() => {
    if (categoryPerformance.length === 0) return [];
    const cats = categoryPerformance.slice(0, 3);
    const maxSales = Math.max(...cats.map((c: any) => c.sales), 1);
    return [
      { metric: 'Sales Volume', ...Object.fromEntries(cats.map((c: any) => [c.category, Math.round((c.sales / maxSales) * 100)])) },
      { metric: 'Profit Margin', ...Object.fromEntries(cats.map((c: any) => [c.category, Math.round(c.margin)])) },
      { metric: 'Growth Rate', ...Object.fromEntries(cats.map((c: any) => [c.category, Math.max(0, Math.round(c.growth + 50))])) },
    ];
  }, [categoryPerformance]);

  const stats = [
    {
      title: 'Revenue Growth',
      value: dashboardStats ? `${dashboardStats.revenueGrowth >= 0 ? '+' : ''}${dashboardStats.revenueGrowth}%` : '—',
      subtitle: 'vs last 30 days',
      icon: TrendingUp,
      color: 'text-green-500',
      trend: dashboardStats?.revenueGrowth >= 0 ? 'up' : 'down',
    },
    {
      title: 'Active Products',
      value: dashboardStats?.totalProducts ?? '—',
      subtitle: `${dashboardStats?.lowStockItems ?? 0} low stock`,
      icon: Package,
      color: 'text-blue-500',
      trend: 'neutral',
    },
    {
      title: 'Total Orders',
      value: dashboardStats?.totalOrders ?? '—',
      subtitle: 'All time',
      icon: ShoppingCart,
      color: 'text-purple-500',
      trend: 'up',
    },
    {
      title: 'Profit Growth',
      value: dashboardStats ? `${dashboardStats.profitGrowth >= 0 ? '+' : ''}${dashboardStats.profitGrowth}%` : '—',
      subtitle: 'vs last 30 days',
      icon: Users,
      color: 'text-amber-500',
      trend: dashboardStats?.profitGrowth >= 0 ? 'up' : 'down',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold flex items-center gap-2">
          <Activity className="h-6 w-6 sm:h-8 sm:w-8" />
          Analytics
        </h1>
        <p className="text-muted-foreground mt-1 text-sm sm:text-base">
          Advanced analytics and insights
        </p>
      </div>

      {/* AI Sales Analysis */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <Card className="glass border-blue-500/20 bg-gradient-to-r from-blue-500/5 to-purple-500/5">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Brain className="h-5 w-5 text-blue-500" />
              <CardTitle className="text-lg">AI Sales Analysis</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            {salesSummaryLoading ? (
              <div className="space-y-2">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-5/6" />
                <Skeleton className="h-4 w-3/4" />
              </div>
            ) : salesSummary ? (
              <div className="space-y-4">
                <p className="text-sm leading-relaxed text-muted-foreground">{salesSummary.summary}</p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                    <div className="text-xs text-muted-foreground">7-Day Revenue</div>
                    <div className="text-lg font-bold">₹{(salesSummary.metrics?.last7Days?.revenue ?? 0).toLocaleString('en-IN')}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                    <div className="text-xs text-muted-foreground">30-Day Revenue</div>
                    <div className="text-lg font-bold">₹{(salesSummary.metrics?.last30Days?.revenue ?? 0).toLocaleString('en-IN')}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                    <div className="text-xs text-muted-foreground">30-Day Orders</div>
                    <div className="text-lg font-bold">{salesSummary.metrics?.last30Days?.orders ?? 0}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                    <div className="text-xs text-muted-foreground">30-Day Growth</div>
                    <div className={`text-lg font-bold ${(salesSummary.metrics?.growth30d ?? 0) >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                      {(salesSummary.metrics?.growth30d ?? 0) >= 0 ? '+' : ''}{salesSummary.metrics?.growth30d ?? 0}%
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">Sales analysis unavailable.</p>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="glass card-hover">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                  <Icon className={`h-4 w-4 ${stat.color}`} />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <div className="flex items-center gap-1 text-xs text-muted-foreground mt-1">
                    {stat.trend === 'up' && <TrendingUp className="h-3 w-3 text-green-500" />}
                    {stat.trend === 'down' && <TrendingDown className="h-3 w-3 text-red-500" />}
                    <span>{stat.subtitle}</span>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Analytics Tabs */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="glass">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="revenue">Revenue</TabsTrigger>
          <TabsTrigger value="products">Products</TabsTrigger>
          <TabsTrigger value="customers">Customers</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Revenue vs Profit Trend */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="glass">
              <CardHeader>
                <CardTitle>Revenue & Profit Trend</CardTitle>
                <CardDescription>Monthly performance over 6 months</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={monthlyData}>
                    <defs>
                      <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#2563eb" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                      </linearGradient>
                      <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis dataKey="month" stroke="rgba(255,255,255,0.5)" />
                    <YAxis stroke="rgba(255,255,255,0.5)" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px',
                      }}
                    />
                    <Legend />
                    <Area
                      type="monotone"
                      dataKey="revenue"
                      stroke="#2563eb"
                      fillOpacity={1}
                      fill="url(#colorRevenue)"
                    />
                    <Area
                      type="monotone"
                      dataKey="profit"
                      stroke="#10b981"
                      fillOpacity={1}
                      fill="url(#colorProfit)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Orders Trend */}
            <Card className="glass">
              <CardHeader>
                <CardTitle>Monthly Orders</CardTitle>
                <CardDescription>Order volume tracking</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={monthlyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis dataKey="month" stroke="rgba(255,255,255,0.5)" />
                    <YAxis stroke="rgba(255,255,255,0.5)" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px',
                      }}
                    />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="orders"
                      stroke="#8b5cf6"
                      strokeWidth={3}
                      dot={{ fill: '#8b5cf6', r: 5 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Category Performance */}
          <Card className="glass">
            <CardHeader>
              <CardTitle>Category Performance Analysis</CardTitle>
              <CardDescription>Sales, growth, and profit margins by category</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <div className="min-w-full space-y-4">
                  {categoryPerformance.map((cat, index) => (
                    <motion.div
                      key={cat.category}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="p-4 rounded-lg bg-white/5 border border-white/10"
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div className="flex-1">
                          <h4 className="font-semibold text-lg">{cat.category}</h4>
                          <div className="flex flex-wrap gap-4 mt-2 text-sm">
                            <div>
                              <span className="text-muted-foreground">Sales: </span>
                              <span className="font-semibold">{cat.sales}</span>
                            </div>
                            <div>
                              <span className="text-muted-foreground">Margin: </span>
                              <span className="font-semibold text-green-500">{cat.margin}%</span>
                            </div>
                          </div>
                        </div>
                        <Badge
                          variant={cat.growth >= 0 ? 'default' : 'destructive'}
                          className="flex items-center gap-1"
                        >
                          {cat.growth >= 0 ? (
                            <TrendingUp className="h-3 w-3" />
                          ) : (
                            <TrendingDown className="h-3 w-3" />
                          )}
                          {Math.abs(cat.growth)}%
                        </Badge>
                      </div>
                      <div className="mt-3 bg-white/5 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full transition-all"
                          style={{ width: `${cat.margin}%` }}
                        />
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Revenue Tab */}
        <TabsContent value="revenue" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Revenue by Category Pie */}
            <Card className="glass">
              <CardHeader>
                <CardTitle>Revenue Distribution</CardTitle>
                <CardDescription>By product category</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={revenueByCategory}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ category, percentage }) => `${category} (${percentage}%)`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {revenueByCategory.map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px',
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Revenue vs Expenses */}
            <Card className="glass">
              <CardHeader>
                <CardTitle>Revenue vs Expenses</CardTitle>
                <CardDescription>Monthly comparison</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={monthlyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis dataKey="month" stroke="rgba(255,255,255,0.5)" />
                    <YAxis stroke="rgba(255,255,255,0.5)" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px',
                      }}
                    />
                    <Legend />
                    <Bar dataKey="revenue" fill="#2563eb" radius={[8, 8, 0, 0]} />
                    <Bar dataKey="expenses" fill="#ef4444" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Products Tab */}
        <TabsContent value="products" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Top Products */}
            <Card className="glass">
              <CardHeader>
                <CardTitle>Top Selling Products</CardTitle>
                <CardDescription>By revenue generated</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={topProducts} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis type="number" stroke="rgba(255,255,255,0.5)" />
                    <YAxis type="category" dataKey="name" width={120} stroke="rgba(255,255,255,0.5)" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px',
                      }}
                    />
                    <Bar dataKey="revenue" fill="#10b981" radius={[0, 8, 8, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Product Performance Radar */}
            <Card className="glass">
              <CardHeader>
                <CardTitle>Product Performance Matrix</CardTitle>
                <CardDescription>Multi-dimensional analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={productPerformanceRadar}>
                    <PolarGrid stroke="rgba(255,255,255,0.2)" />
                    <PolarAngleAxis dataKey="metric" stroke="rgba(255,255,255,0.5)" />
                    <PolarRadiusAxis stroke="rgba(255,255,255,0.3)" />
                    {radarCategories.map((cat: string, i: number) => (
                      <Radar
                        key={cat}
                        name={cat}
                        dataKey={cat}
                        stroke={RADAR_LINE_COLORS[i % RADAR_LINE_COLORS.length]}
                        fill={RADAR_LINE_COLORS[i % RADAR_LINE_COLORS.length]}
                        fillOpacity={0.3}
                      />
                    ))}
                    <Legend />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px',
                      }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Customers Tab */}
        <TabsContent value="customers" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Customer Segments */}
            <Card className="glass">
              <CardHeader>
                <CardTitle>Customer Segmentation</CardTitle>
                <CardDescription>Distribution by customer type</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={customerSegments}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ segment, value }) => `${segment}: ${value}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {customerSegments.map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={SEGMENT_COLORS[entry.segment] || COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px',
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Customer Metrics */}
            <Card className="glass">
              <CardHeader>
                <CardTitle>Business Metrics</CardTitle>
                <CardDescription>Key performance indicators</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-muted-foreground">Total Orders</span>
                      <span className="text-sm font-semibold">{dashboardStats?.totalOrders ?? 0} orders</span>
                    </div>
                    <div className="bg-white/5 rounded-full h-2">
                      <div className="bg-green-500 h-2 rounded-full" style={{ width: `${Math.min((dashboardStats?.totalOrders ?? 0) / 2, 100)}%` }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-muted-foreground">Revenue Growth</span>
                      <span className="text-sm font-semibold">{dashboardStats?.revenueGrowth ?? 0}%</span>
                    </div>
                    <div className="bg-white/5 rounded-full h-2">
                      <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${Math.min(Math.max(dashboardStats?.revenueGrowth ?? 0, 0), 100)}%` }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-muted-foreground">Profit Margin</span>
                      <span className="text-sm font-semibold">{dashboardStats?.totalRevenue ? ((dashboardStats.totalProfit / dashboardStats.totalRevenue) * 100).toFixed(1) : '0'}%</span>
                    </div>
                    <div className="bg-white/5 rounded-full h-2">
                      <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${dashboardStats?.totalRevenue ? Math.min((dashboardStats.totalProfit / dashboardStats.totalRevenue) * 100, 100) : 0}%` }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-muted-foreground">Stock Health</span>
                      <span className="text-sm font-semibold">{dashboardStats?.totalProducts ? (((dashboardStats.totalProducts - (dashboardStats.lowStockItems ?? 0) - (dashboardStats.outOfStockItems ?? 0)) / dashboardStats.totalProducts) * 100).toFixed(0) : '0'}%</span>
                    </div>
                    <div className="bg-white/5 rounded-full h-2">
                      <div className="bg-amber-500 h-2 rounded-full" style={{ width: `${dashboardStats?.totalProducts ? ((dashboardStats.totalProducts - (dashboardStats.lowStockItems ?? 0) - (dashboardStats.outOfStockItems ?? 0)) / dashboardStats.totalProducts) * 100 : 0}%` }} />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
