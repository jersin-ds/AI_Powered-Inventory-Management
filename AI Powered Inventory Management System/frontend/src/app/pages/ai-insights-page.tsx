import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Sparkles, TrendingUp, AlertTriangle, IndianRupee, Calendar, RefreshCw, Clock } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Skeleton } from '../components/ui/skeleton';
import { aiApi } from '../services/ai-api';
import { motion } from 'motion/react';
import { useNavigate } from 'react-router';
import { toast } from 'sonner';
import api from '../services/api';

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

export function AIInsightsPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: insights, isLoading } = useQuery({
    queryKey: ['ai-insights'],
    queryFn: aiApi.getInsights,
  });

  const { data: stockoutData } = useQuery({
    queryKey: ['ai-stockout-predictions'],
    queryFn: () => aiApi.getStockoutPredictions(),
    staleTime: 5 * 60 * 1000,
  });

  const generateMutation = useMutation({
    mutationFn: async () => {
      const { data } = await api.post('/ai/generate-insights');
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ai-insights'] });
      toast.success('New insights generated successfully!');
    },
    onError: () => {
      toast.error('Failed to generate insights');
    },
  });

  const handleTakeAction = (type: string) => {
    switch (type) {
      case 'demand_forecast':
        navigate('/stock');
        break;
      case 'dead_stock':
        navigate('/products');
        break;
      case 'price_optimization':
        navigate('/products');
        break;
      case 'anomaly':
        navigate('/analytics');
        break;
      case 'expiry_risk':
        navigate('/stock');
        break;
      default:
        navigate('/dashboard');
    }
  };

  const getIcon = (type: string) => {
    switch (type) {
      case 'demand_forecast':
        return <TrendingUp className="h-5 w-5" />;
      case 'price_optimization':
        return <IndianRupee className="h-5 w-5" />;
      case 'expiry_risk':
        return <Calendar className="h-5 w-5" />;
      case 'stockout_prediction':
        return <Clock className="h-5 w-5" />;
      default:
        return <AlertTriangle className="h-5 w-5" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-500';
      case 'medium':
        return 'bg-amber-500';
      default:
        return 'bg-blue-500';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Sparkles className="h-8 w-8 text-blue-500" />
            AI Insights
          </h1>
          <p className="text-muted-foreground mt-1">
            Intelligent recommendations powered by AI
          </p>
        </div>
        <Button
          onClick={() => generateMutation.mutate()}
          disabled={generateMutation.isPending}
          className="bg-gradient-to-r from-blue-500 to-purple-600"
        >
          {generateMutation.isPending ? (
            <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <Sparkles className="mr-2 h-4 w-4" />
          )}
          Generate Insights
        </Button>
      </div>

      <Tabs defaultValue="all" className="space-y-4">
        <TabsList className="glass flex-wrap">
          <TabsTrigger value="all">All Insights</TabsTrigger>
          <TabsTrigger value="demand_forecast">Demand Forecast</TabsTrigger>
          <TabsTrigger value="dead_stock">Dead Stock</TabsTrigger>
          <TabsTrigger value="anomaly">Anomalies</TabsTrigger>
          <TabsTrigger value="price_optimization">Pricing</TabsTrigger>
          <TabsTrigger value="expiry_risk">Expiry Risk</TabsTrigger>
          <TabsTrigger value="stockout">Stockout Alerts</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          <div className="grid gap-4">
            {isLoading && (
              Array.from({ length: 3 }).map((_, idx) => (
                <Card key={`insight-skeleton-${idx}`} className="glass">
                  <CardHeader>
                    <Skeleton className="h-5 w-48" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-3/4" />
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-4 w-32" />
                  </CardContent>
                </Card>
              ))
            )}

            {!isLoading && (!insights || insights.length === 0) && (
              <Card className="glass">
                <CardContent className="py-8 text-center">
                  <Sparkles className="h-10 w-10 mx-auto mb-3 text-muted-foreground" />
                  <p className="text-muted-foreground">No AI insights found yet. Click Generate Insights to create recommendations.</p>
                </CardContent>
              </Card>
            )}

            {insights?.map((insight, index) => (
              <motion.div
                key={insight.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="glass card-hover">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3">
                        <div className="p-2 rounded-lg bg-blue-500/20">
                          {getIcon(insight.type)}
                        </div>
                        <div>
                          <CardTitle className="text-lg">{insight.title}</CardTitle>
                          <CardDescription className="mt-1">
                            {formatInsightDescription(insight)}
                          </CardDescription>
                        </div>
                      </div>
                      <Badge className={getPriorityColor(insight.priority)}>
                        {insight.priority}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <div className="text-sm text-muted-foreground">
                        {new Date(insight.createdAt).toLocaleDateString()}
                      </div>
                      {insight.actionable && (
                        <Button size="sm" onClick={() => handleTakeAction(insight.type)}>Take Action</Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>

        {['demand_forecast', 'dead_stock', 'anomaly', 'price_optimization', 'expiry_risk'].map((type) => (
          <TabsContent key={type} value={type} className="space-y-4">
            <div className="grid gap-4">
              {!isLoading && insights?.filter((i) => i.type === type).length === 0 && (
                <Card className="glass">
                  <CardContent className="py-8 text-center">
                    <p className="text-muted-foreground">No insights available for this category.</p>
                  </CardContent>
                </Card>
              )}

              {insights
                ?.filter((i) => i.type === type)
                .map((insight, index) => (
                  <motion.div
                    key={insight.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Card className="glass card-hover">
                      <CardHeader>
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-3">
                            <div className="p-2 rounded-lg bg-blue-500/20">
                              {getIcon(insight.type)}
                            </div>
                            <div>
                              <CardTitle className="text-lg">{insight.title}</CardTitle>
                              <CardDescription className="mt-1">
                                {formatInsightDescription(insight)}
                              </CardDescription>
                            </div>
                          </div>
                          <Badge className={getPriorityColor(insight.priority)}>
                            {insight.priority}
                          </Badge>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center justify-between">
                          <div className="text-sm text-muted-foreground">
                            {new Date(insight.createdAt).toLocaleDateString()}
                          </div>
                          {insight.actionable && (
                            <Button size="sm" onClick={() => handleTakeAction(insight.type)}>Take Action</Button>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
            </div>
          </TabsContent>
        ))}

        {/* Stockout Predictions Tab */}
        <TabsContent value="stockout" className="space-y-4">
          <div className="grid gap-4">
            {stockoutData?.predictions && stockoutData.predictions.length > 0 ? (
              stockoutData.predictions.map((pred, index) => (
                <motion.div
                  key={pred.productId}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card className={`glass card-hover border-l-4 ${
                    pred.urgency === 'critical' ? 'border-l-red-500' :
                    pred.urgency === 'warning' ? 'border-l-amber-500' : 'border-l-yellow-500'
                  }`}>
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3">
                          <div className={`p-2 rounded-lg ${
                            pred.urgency === 'critical' ? 'bg-red-500/20' :
                            pred.urgency === 'warning' ? 'bg-amber-500/20' : 'bg-yellow-500/20'
                          }`}>
                            <Clock className="h-5 w-5" />
                          </div>
                          <div>
                            <CardTitle className="text-lg">{pred.productName}</CardTitle>
                            <CardDescription className="mt-1">{pred.recommendation}</CardDescription>
                          </div>
                        </div>
                        <Badge className={
                          pred.urgency === 'critical' ? 'bg-red-500' :
                          pred.urgency === 'warning' ? 'bg-amber-500' : 'bg-yellow-500'
                        }>
                          {pred.urgency}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex gap-4">
                          <span className="text-muted-foreground">Current: <strong>{pred.currentStock}</strong> units</span>
                          <span className="text-muted-foreground">Sales: <strong>{pred.dailySalesRate}</strong>/day</span>
                          <span className={`font-semibold ${
                            pred.daysUntilStockout <= 7 ? 'text-red-500' :
                            pred.daysUntilStockout <= 14 ? 'text-amber-500' : 'text-yellow-500'
                          }`}>
                            ~{pred.daysUntilStockout} days left
                          </span>
                        </div>
                        <Button size="sm" onClick={() => navigate('/stock')}>View Stock</Button>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))
            ) : (
              <Card className="glass">
                <CardContent className="py-8 text-center">
                  <Clock className="h-10 w-10 mx-auto mb-3 text-muted-foreground" />
                  <p className="text-muted-foreground">No stockout risks detected. All products are well-stocked.</p>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
