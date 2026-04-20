import { useQuery } from '@tanstack/react-query';
import { motion } from 'motion/react';
import {
  TrendingUp,
  TrendingDown,
  Package,
  IndianRupee,
  AlertTriangle,
  ShoppingCart,
  ArrowUpRight,
  Sparkles,
  Activity,
  Brain,
  Clock,
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Skeleton } from '../components/ui/skeleton';
import { Progress } from '../components/ui/progress';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import api from '../services/api';
import { aiApi } from '../services/ai-api';
import { useNavigate } from 'react-router';

const COLORS = ['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd'];

function parseJsonLikeDescription(text: string): unknown {
  const trimmed = text.trim();
  const codeBlockMatch = trimmed.match(/```(?:json)?\s*([\s\S]*?)\s*```/i);
  const candidate = codeBlockMatch ? codeBlockMatch[1].trim() : trimmed;

  try {
    return JSON.parse(candidate);
  } catch {
    return null;
  }
}

function extractReasoningFromData(data: unknown): string | null {
  if (!data) return null;

  if (Array.isArray(data)) {
    const first = data[0] as Record<string, unknown> | undefined;
    if (first && typeof first.reasoning === 'string' && first.reasoning.trim()) {
      return data.length > 1
        ? `${first.reasoning} (+${data.length - 1} more recommendations)`
        : first.reasoning;
    }
    return data.length > 0 ? `Generated ${data.length} recommendations.` : null;
  }

  if (typeof data === 'object') {
    const obj = data as Record<string, unknown>;

    if (typeof obj.reasoning === 'string' && obj.reasoning.trim()) {
      return obj.reasoning;
    }

    if (Array.isArray(obj.suggestions) && obj.suggestions.length > 0) {
      const first = obj.suggestions[0] as Record<string, unknown>;
      if (typeof first.reasoning === 'string' && first.reasoning.trim()) {
        return obj.suggestions.length > 1
          ? `${first.reasoning} (+${obj.suggestions.length - 1} more recommendations)`
          : first.reasoning;
      }
      return `Generated ${obj.suggestions.length} recommendations.`;
    }
  }

  return null;
}

function formatInsightDescription(insight: { description: string; data?: unknown }): string {
  const raw = insight.description?.trim() ?? '';
  if (!raw) return 'AI-generated recommendation based on your inventory data.';

  const parsed = parseJsonLikeDescription(raw);
  const parsedReasoning = extractReasoningFromData(parsed);
  if (parsedReasoning) return parsedReasoning;

  const dataReasoning = extractReasoningFromData(insight.data);
  if (dataReasoning) return dataReasoning;

  if (raw.toLowerCase().startsWith('ai analysis for') || raw.includes('{') || raw.includes('[') || raw.includes('```')) {
    return 'AI-generated recommendation based on current inventory and sales patterns.';
  }

  return raw.replace(/```json|```/gi, '').trim();
}

export function DashboardPage() {
  const navigate = useNavigate();

  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/stats');
      return data;
    },
  });

  const { data: salesChartData } = useQuery({
    queryKey: ['dashboard-sales-chart'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/sales-chart');
      return data;
    },
  });

  const { data: revenueByCategory } = useQuery({
    queryKey: ['dashboard-revenue-category'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/revenue-by-category');
      return data;
    },
  });

  const { data: topProducts } = useQuery({
    queryKey: ['dashboard-top-products'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/top-products');
      return data;
    },
  });

  const { data: aiInsights } = useQuery({
    queryKey: ['ai-insights'],
    queryFn: () => aiApi.getInsights(),
  });

  const { data: lowStockProducts } = useQuery({
    queryKey: ['stock-low'],
    queryFn: async () => {
      const { data } = await api.get('/stock/low');
      return data;
    },
  });

  const { data: outOfStockProducts } = useQuery({
    queryKey: ['stock-out'],
    queryFn: async () => {
      const { data } = await api.get('/stock/out');
      return data;
    },
  });

  const { data: aiSummary, isLoading: summaryLoading } = useQuery({
    queryKey: ['ai-dashboard-summary'],
    queryFn: () => aiApi.getDashboardSummary(),
    staleTime: 5 * 60 * 1000, // Cache for 5 min
  });

  const { data: healthScore, isLoading: healthLoading } = useQuery({
    queryKey: ['ai-health-score'],
    queryFn: () => aiApi.getHealthScore(),
    staleTime: 5 * 60 * 1000,
  });

  const { data: stockoutPredictions } = useQuery({
    queryKey: ['ai-stockout-predictions'],
    queryFn: () => aiApi.getStockoutPredictions(),
    staleTime: 5 * 60 * 1000,
  });

  const statCards = stats ? [
    {
      title: 'Total Revenue',
      value: `₹${stats.totalRevenue.toLocaleString('en-IN')}`,
      change: `${stats.revenueGrowth >= 0 ? '+' : ''}${stats.revenueGrowth}%`,
      trend: stats.revenueGrowth >= 0 ? 'up' : 'down',
      icon: IndianRupee,
      color: 'text-green-500',
    },
    {
      title: 'Total Profit',
      value: `₹${stats.totalProfit.toLocaleString('en-IN')}`,
      change: `${stats.profitGrowth >= 0 ? '+' : ''}${stats.profitGrowth}%`,
      trend: stats.profitGrowth >= 0 ? 'up' : 'down',
      icon: TrendingUp,
      color: 'text-blue-500',
    },
    {
      title: 'Total Products',
      value: stats.totalProducts.toLocaleString(),
      change: `${stats.lowStockItems} low stock`,
      trend: 'neutral',
      icon: Package,
      color: 'text-purple-500',
    },
    {
      title: 'Pending Orders',
      value: stats.pendingOrders.toString(),
      change: `${stats.outOfStockItems} out of stock`,
      trend: 'down',
      icon: ShoppingCart,
      color: 'text-amber-500',
    },
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground mt-1 text-sm sm:text-base">
            Welcome back! Here's what's happening with your inventory.
          </p>
        </div>
        <Button onClick={() => navigate('/ai-insights')} className="bg-gradient-to-r from-blue-500 to-purple-600 w-full sm:w-auto">
          <Sparkles className="mr-2 h-4 w-4" />
          AI Insights
        </Button>
      </div>

      {/* AI Dashboard Summary + Health Score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="lg:col-span-2"
        >
          <Card className="glass border-blue-500/20 bg-gradient-to-r from-blue-500/5 to-purple-500/5 h-full">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <Brain className="h-5 w-5 text-blue-500" />
                <CardTitle className="text-lg">AI Dashboard Summary</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              {summaryLoading ? (
                <div className="space-y-2">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-3/4" />
                  <Skeleton className="h-4 w-5/6" />
                </div>
              ) : aiSummary ? (
                <p className="text-sm leading-relaxed text-muted-foreground">
                  {aiSummary.summary}
                </p>
              ) : (
                <p className="text-sm text-muted-foreground">AI summary unavailable.</p>
              )}
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="glass border-green-500/20 h-full">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <Activity className="h-5 w-5 text-green-500" />
                <CardTitle className="text-lg">Health Score</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              {healthLoading ? (
                <div className="space-y-3">
                  <Skeleton className="h-16 w-16 rounded-full mx-auto" />
                  <Skeleton className="h-4 w-full" />
                </div>
              ) : healthScore ? (
                <div className="text-center space-y-3">
                  <div className="relative inline-flex items-center justify-center">
                    <div className={`text-4xl font-bold ${
                      healthScore.score >= 80 ? 'text-green-500' :
                      healthScore.score >= 60 ? 'text-amber-500' : 'text-red-500'
                    }`}>
                      {healthScore.score}
                    </div>
                    <span className={`ml-1 text-lg font-semibold ${
                      healthScore.score >= 80 ? 'text-green-500' :
                      healthScore.score >= 60 ? 'text-amber-500' : 'text-red-500'
                    }`}>
                      / {healthScore.grade}
                    </span>
                  </div>
                  <Progress
                    value={healthScore.score}
                    className="h-2"
                  />
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {healthScore.recommendation}
                  </p>
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">Score unavailable.</p>
              )}
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, index) => {
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
                    {stat.trend === 'up' ? (
                      <TrendingUp className="h-3 w-3 text-green-500" />
                    ) : stat.trend === 'down' ? (
                      <TrendingDown className="h-3 w-3 text-red-500" />
                    ) : null}
                    <span>{stat.change}</span>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sales Chart */}
        <Card className="glass">
          <CardHeader>
            <CardTitle>Sales & Profit Trend</CardTitle>
            <CardDescription>Daily sales and profit over time</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={salesChartData || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="date" stroke="rgba(255,255,255,0.5)" />
                <YAxis stroke="rgba(255,255,255,0.5)" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '8px',
                  }}
                />
                <Legend />
                <Line type="monotone" dataKey="sales" stroke="#2563eb" strokeWidth={2} />
                <Line type="monotone" dataKey="profit" stroke="#10b981" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Revenue by Category */}
        <Card className="glass">
          <CardHeader>
            <CardTitle>Revenue by Category</CardTitle>
            <CardDescription>Distribution of revenue across categories</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={revenueByCategory || []}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ category, percentage }) => `${category} ${percentage}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {(revenueByCategory || []).map((entry: any, index: number) => (
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
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top Products */}
        <Card className="glass lg:col-span-2">
          <CardHeader>
            <CardTitle>Top Selling Products</CardTitle>
            <CardDescription>Best performers this month</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={topProducts || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="name" stroke="rgba(255,255,255,0.5)" />
                <YAxis stroke="rgba(255,255,255,0.5)" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '8px',
                  }}
                />
                <Bar dataKey="revenue" fill="#2563eb" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Stock Alerts + Stockout Predictions */}
        <Card className="glass">
          <CardHeader>
            <CardTitle>Stock Alerts</CardTitle>
            <CardDescription>Items needing attention</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {/* Stockout Predictions */}
              {stockoutPredictions?.predictions?.slice(0, 2).map((pred) => (
                <div
                  key={pred.productId}
                  className={`flex items-center justify-between p-3 rounded-lg border ${
                    pred.urgency === 'critical'
                      ? 'bg-red-500/10 border-red-500/20'
                      : pred.urgency === 'warning'
                      ? 'bg-amber-500/10 border-amber-500/20'
                      : 'bg-yellow-500/10 border-yellow-500/20'
                  }`}
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5">
                      <Clock className="h-3 w-3 text-muted-foreground shrink-0" />
                      <p className="text-sm font-medium truncate">{pred.productName}</p>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      ~{pred.daysUntilStockout} days left
                    </p>
                  </div>
                  <Badge className={`ml-2 shrink-0 ${
                    pred.urgency === 'critical' ? 'bg-red-500' :
                    pred.urgency === 'warning' ? 'bg-amber-500' : 'bg-yellow-500'
                  }`}>
                    {pred.urgency}
                  </Badge>
                </div>
              ))}
              {(outOfStockProducts || []).map((product: any) => (
                <div
                  key={product.id}
                  className="flex items-center justify-between p-3 rounded-lg bg-red-500/10 border border-red-500/20"
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{product.name}</p>
                    <p className="text-xs text-muted-foreground">{product.sku}</p>
                  </div>
                  <Badge variant="destructive" className="ml-2 shrink-0">Out of Stock</Badge>
                </div>
              ))}
              {(lowStockProducts || []).slice(0, 2).map((product: any) => (
                <div
                  key={product.id}
                  className="flex items-center justify-between p-3 rounded-lg bg-amber-500/10 border border-amber-500/20"
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{product.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {product.stockQty} units left
                    </p>
                  </div>
                  <Badge className="bg-amber-500 ml-2 shrink-0">Low Stock</Badge>
                </div>
              ))}
              <Button
                variant="outline"
                className="w-full"
                onClick={() => navigate('/stock')}
              >
                View All Alerts
                <ArrowUpRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI Insights Preview */}
      {aiInsights && aiInsights.length > 0 && (
        <Card className="glass border-blue-500/20 bg-gradient-to-r from-blue-500/10 to-purple-500/10">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-blue-500" />
                <CardTitle>AI Insights</CardTitle>
              </div>
              <Button variant="ghost" size="sm" onClick={() => navigate('/ai-insights')}>
                View All <ArrowUpRight className="ml-1 h-3 w-3" />
              </Button>
            </div>
            <CardDescription>Key insights from AI analysis</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {aiInsights.slice(0, 2).map((insight) => (
                <div
                  key={insight.id}
                  className="p-4 rounded-lg bg-white/5 border border-white/10"
                >
                  <div className="flex items-start justify-between mb-2 gap-2">
                    <Badge
                      className={
                        insight.priority === 'high'
                          ? 'bg-red-500'
                          : insight.priority === 'medium'
                          ? 'bg-amber-500'
                          : 'bg-blue-500'
                      }
                    >
                      {insight.priority}
                    </Badge>
                    <AlertTriangle className="h-4 w-4 text-amber-500 shrink-0" />
                  </div>
                  <h4 className="font-medium mb-1">{insight.title}</h4>
                  <p className="text-sm text-muted-foreground">{formatInsightDescription(insight)}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}