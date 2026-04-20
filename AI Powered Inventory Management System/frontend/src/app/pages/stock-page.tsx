import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Package, AlertTriangle, RefreshCw, Plus, Minus, Sparkles, Clock, Brain } from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import { aiApi } from '../services/ai-api';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Skeleton } from '../components/ui/skeleton';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogTrigger } from '../components/ui/dialog';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from 'sonner';

export function StockPage() {
  const queryClient = useQueryClient();
  const [adjustOpen, setAdjustOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<any>(null);
  const [adjustQty, setAdjustQty] = useState('');
  const [adjustReason, setAdjustReason] = useState('');
  const [adjustType, setAdjustType] = useState<'add' | 'remove'>('add');

  const { data: lowStockProducts = [] } = useQuery({
    queryKey: ['stock', 'low'],
    queryFn: async () => {
      const { data } = await api.get('/stock/low');
      return data;
    },
  });
  const { data: outOfStockProducts = [] } = useQuery({
    queryKey: ['stock', 'out'],
    queryFn: async () => {
      const { data } = await api.get('/stock/out');
      return data;
    },
  });

  const { data: reorderData, isLoading: reorderLoading } = useQuery({
    queryKey: ['ai-reorder-suggestions'],
    queryFn: () => aiApi.getReorderSuggestions(),
    staleTime: 5 * 60 * 1000,
  });

  const { data: stockoutData, isLoading: stockoutLoading } = useQuery({
    queryKey: ['ai-stockout-predictions'],
    queryFn: () => aiApi.getStockoutPredictions(),
    staleTime: 5 * 60 * 1000,
  });

  const autoReorderMutation = useMutation({
    mutationFn: async () => {
      const { data } = await api.post('/stock/auto-reorder');
      return data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['stock'] });
      queryClient.invalidateQueries({ queryKey: ['purchases'] });
      toast.success(data.message);
    },
    onError: () => {
      toast.error('Failed to create auto-reorder');
    },
  });

  const adjustMutation = useMutation({
    mutationFn: async () => {
      const qty = adjustType === 'remove' ? -Math.abs(Number(adjustQty)) : Math.abs(Number(adjustQty));
      const { data } = await api.post('/stock/adjust', {
        product_id: selectedProduct.id,
        quantity: qty,
        reason: adjustReason,
      });
      return data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['stock'] });
      queryClient.invalidateQueries({ queryKey: ['products'] });
      toast.success(`Stock adjusted: ${data.name} → ${data.newQty} units`);
      setAdjustOpen(false);
      setAdjustQty('');
      setAdjustReason('');
    },
    onError: () => {
      toast.error('Failed to adjust stock');
    },
  });

  const openAdjustDialog = (product: any) => {
    setSelectedProduct(product);
    setAdjustQty('');
    setAdjustReason('');
    setAdjustType('add');
    setAdjustOpen(true);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Package className="h-8 w-8" />
            Stock Management
          </h1>
          <p className="text-muted-foreground mt-1">Monitor and manage inventory levels</p>
        </div>
        <Button
          onClick={() => autoReorderMutation.mutate()}
          disabled={autoReorderMutation.isPending}
          className="bg-gradient-to-r from-blue-500 to-blue-600"
        >
          {autoReorderMutation.isPending ? (
            <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <RefreshCw className="mr-2 h-4 w-4" />
          )}
          Auto-Reorder
        </Button>
      </div>

      {/* Stock Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="glass">
          <CardContent className="pt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-amber-500">{lowStockProducts.length}</div>
              <div className="text-sm text-muted-foreground mt-1">Low Stock Items</div>
            </div>
          </CardContent>
        </Card>
        <Card className="glass">
          <CardContent className="pt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-red-500">{outOfStockProducts.length}</div>
              <div className="text-sm text-muted-foreground mt-1">Out of Stock</div>
            </div>
          </CardContent>
        </Card>
        <Card className="glass">
          <CardContent className="pt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-green-500">{lowStockProducts.length + outOfStockProducts.length}</div>
              <div className="text-sm text-muted-foreground mt-1">Total Alerts</div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="glass border-amber-500/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-amber-500">
              <AlertTriangle className="h-5 w-5" />
              Low Stock Items
            </CardTitle>
            <CardDescription>{lowStockProducts.length} items need attention</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product</TableHead>
                  <TableHead>Current</TableHead>
                  <TableHead>Min</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {lowStockProducts.map((product: any) => (
                  <TableRow key={product.id}>
                    <TableCell>
                      <div>
                        <div className="font-medium">{product.name}</div>
                        <div className="text-xs text-muted-foreground">{product.sku}</div>
                      </div>
                    </TableCell>
                    <TableCell>{product.stockQty}</TableCell>
                    <TableCell>{product.minLevel}</TableCell>
                    <TableCell>
                      <Button size="sm" variant="outline" onClick={() => openAdjustDialog(product)}>
                        <Plus className="h-3 w-3 mr-1" /> Adjust
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card className="glass border-red-500/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-500">
              <AlertTriangle className="h-5 w-5" />
              Out of Stock
            </CardTitle>
            <CardDescription>{outOfStockProducts.length} items unavailable</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product</TableHead>
                  <TableHead>Min Level</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {outOfStockProducts.map((product: any) => (
                  <TableRow key={product.id}>
                    <TableCell>
                      <div>
                        <div className="font-medium">{product.name}</div>
                        <div className="text-xs text-muted-foreground">{product.sku}</div>
                      </div>
                    </TableCell>
                    <TableCell>{product.minLevel}</TableCell>
                    <TableCell>
                      <Button size="sm" variant="outline" onClick={() => openAdjustDialog(product)}>
                        <Plus className="h-3 w-3 mr-1" /> Adjust
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      {/* AI Smart Reorder Suggestions */}
      <Card className="glass border-blue-500/20 bg-gradient-to-r from-blue-500/5 to-purple-500/5">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-blue-500" />
            <CardTitle>AI Reorder Suggestions</CardTitle>
          </div>
          <CardDescription>Smart recommendations based on sales velocity and stock levels</CardDescription>
        </CardHeader>
        <CardContent>
          {reorderLoading ? (
            <div className="space-y-3">
              <Skeleton className="h-12 w-full" />
              <Skeleton className="h-12 w-full" />
              <Skeleton className="h-12 w-full" />
            </div>
          ) : reorderData?.suggestions && reorderData.suggestions.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product</TableHead>
                  <TableHead className="text-right">Stock</TableHead>
                  <TableHead className="text-right">Daily Sales</TableHead>
                  <TableHead className="text-right">Days Left</TableHead>
                  <TableHead className="text-right">Order Qty</TableHead>
                  <TableHead>AI Reasoning</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {reorderData.suggestions.map((s) => (
                  <TableRow key={s.productId}>
                    <TableCell className="font-medium">{s.productName}</TableCell>
                    <TableCell className="text-right">
                      <span className={s.currentStock <= s.minLevel ? 'text-red-500 font-semibold' : ''}>
                        {s.currentStock}
                      </span>
                      <span className="text-muted-foreground text-xs"> / {s.minLevel}</span>
                    </TableCell>
                    <TableCell className="text-right">{s.dailySalesRate}</TableCell>
                    <TableCell className="text-right">
                      <Badge className={`${
                        s.daysUntilStockout <= 7 ? 'bg-red-500' :
                        s.daysUntilStockout <= 14 ? 'bg-amber-500' : 'bg-yellow-500'
                      }`}>
                        {s.daysUntilStockout > 900 ? '∞' : `${s.daysUntilStockout}d`}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right font-semibold text-blue-500">
                      {s.suggestedQuantity} units
                    </TableCell>
                    <TableCell className="text-xs text-muted-foreground max-w-[200px] truncate">
                      {s.reasoning}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <p className="text-sm text-muted-foreground text-center py-4">
              All products are well-stocked. No reorder suggestions at this time.
            </p>
          )}
        </CardContent>
      </Card>

      {/* AI Stockout Predictions */}
      {stockoutData?.predictions && stockoutData.predictions.length > 0 && (
        <Card className="glass border-amber-500/20">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-amber-500" />
              <CardTitle>Predicted Stockouts</CardTitle>
            </div>
            <CardDescription>AI-predicted products at risk of running out</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {stockoutData.predictions.map((pred) => (
                <div
                  key={pred.productId}
                  className={`p-4 rounded-lg border ${
                    pred.urgency === 'critical' ? 'bg-red-500/10 border-red-500/20' :
                    pred.urgency === 'warning' ? 'bg-amber-500/10 border-amber-500/20' :
                    'bg-yellow-500/10 border-yellow-500/20'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-medium">{pred.productName}</span>
                        <Badge className={`text-xs ${
                          pred.urgency === 'critical' ? 'bg-red-500' :
                          pred.urgency === 'warning' ? 'bg-amber-500' : 'bg-yellow-500'
                        }`}>
                          {pred.urgency} — {pred.daysUntilStockout}d left
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">{pred.recommendation}</p>
                    </div>
                    <div className="text-right shrink-0">
                      <div className="text-sm font-medium">{pred.currentStock} units</div>
                      <div className="text-xs text-muted-foreground">{pred.dailySalesRate}/day</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Stock Adjustment Dialog */}
      <Dialog open={adjustOpen} onOpenChange={setAdjustOpen}>
        <DialogContent className="glass">
          <DialogHeader>
            <DialogTitle>Adjust Stock — {selectedProduct?.name}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              Current stock: <span className="font-semibold text-foreground">{selectedProduct?.stockQty} units</span>
            </div>
            <div className="space-y-2">
              <Label>Type</Label>
              <Select value={adjustType} onValueChange={(v: any) => setAdjustType(v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="add">Add Stock</SelectItem>
                  <SelectItem value="remove">Remove Stock</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Quantity</Label>
              <Input
                type="number"
                min="1"
                value={adjustQty}
                onChange={(e) => setAdjustQty(e.target.value)}
                placeholder="Enter quantity"
                className="bg-white/5 border-white/10"
              />
            </div>
            <div className="space-y-2">
              <Label>Reason</Label>
              <Input
                value={adjustReason}
                onChange={(e) => setAdjustReason(e.target.value)}
                placeholder="e.g. Physical count correction"
                className="bg-white/5 border-white/10"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setAdjustOpen(false)}>Cancel</Button>
            <Button
              onClick={() => adjustMutation.mutate()}
              disabled={!adjustQty || adjustMutation.isPending}
            >
              {adjustType === 'add' ? <Plus className="h-4 w-4 mr-1" /> : <Minus className="h-4 w-4 mr-1" />}
              {adjustType === 'add' ? 'Add' : 'Remove'} Stock
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
