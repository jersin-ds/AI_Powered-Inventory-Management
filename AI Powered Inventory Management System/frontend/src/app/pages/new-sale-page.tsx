import { useState } from 'react';
import { useNavigate } from 'react-router';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { IndianRupee, Plus, Trash2, ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';
import api from '../services/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table';

interface SaleLineItem {
  productId: string;
  productName: string;
  quantity: number;
  price: number;
}

export function NewSalePage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [customer, setCustomer] = useState('');
  const [items, setItems] = useState<SaleLineItem[]>([]);
  const [selectedProductId, setSelectedProductId] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [submitting, setSubmitting] = useState(false);

  const { data: products = [] } = useQuery({
    queryKey: ['products'],
    queryFn: async () => {
      const { data } = await api.get('/products');
      return data;
    },
  });

  const addItem = () => {
    const product = products.find((p: any) => p.id === selectedProductId);
    if (!product) return;
    if (items.some((i) => i.productId === selectedProductId)) {
      toast.error('Product already added — update the quantity instead');
      return;
    }
    setItems([
      ...items,
      {
        productId: product.id,
        productName: product.name,
        quantity,
        price: product.sellPrice,
      },
    ]);
    setSelectedProductId('');
    setQuantity(1);
  };

  const removeItem = (productId: string) => {
    setItems(items.filter((i) => i.productId !== productId));
  };

  const updateItemQty = (productId: string, qty: number) => {
    setItems(items.map((i) => (i.productId === productId ? { ...i, quantity: Math.max(1, qty) } : i)));
  };

  const total = items.reduce((sum, i) => sum + i.quantity * i.price, 0);

  const handleSubmit = async () => {
    if (!customer.trim()) {
      toast.error('Please enter a customer name');
      return;
    }
    if (items.length === 0) {
      toast.error('Please add at least one product');
      return;
    }
    setSubmitting(true);
    try {
      await api.post('/sales', {
        customer: customer.trim(),
        items: items.map((i) => ({
          productId: i.productId,
          productName: i.productName,
          quantity: i.quantity,
          price: i.price,
        })),
      });
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast.success('Sale created successfully');
      navigate('/sales');
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to create sale');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate('/sales')}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold flex items-center gap-2">
            <IndianRupee className="h-6 w-6 sm:h-8 sm:w-8" />
            New Sale
          </h1>
          <p className="text-muted-foreground mt-1 text-sm">Create a new sales order</p>
        </div>
      </div>

      {/* Customer */}
      <Card className="glass">
        <CardHeader>
          <CardTitle>Customer Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 max-w-md">
            <Label htmlFor="customer">Customer Name</Label>
            <Input
              id="customer"
              placeholder="e.g. Acme Corp"
              value={customer}
              onChange={(e) => setCustomer(e.target.value)}
              className="bg-white/5 border-white/10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Add Product */}
      <Card className="glass">
        <CardHeader>
          <CardTitle>Add Products</CardTitle>
          <CardDescription>Select products and quantities for this sale</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 space-y-2">
              <Label>Product</Label>
              <Select value={selectedProductId} onValueChange={setSelectedProductId}>
                <SelectTrigger className="bg-white/5 border-white/10">
                  <SelectValue placeholder="Select a product" />
                </SelectTrigger>
                <SelectContent>
                  {products
                    .filter((p: any) => p.status !== 'out_of_stock')
                    .map((p: any) => (
                      <SelectItem key={p.id} value={p.id}>
                        {p.name} — ₹{p.sellPrice} (Stock: {p.stockQty})
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
            </div>
            <div className="w-32 space-y-2">
              <Label>Quantity</Label>
              <Input
                type="number"
                min={1}
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                className="bg-white/5 border-white/10"
              />
            </div>
            <div className="flex items-end">
              <Button onClick={addItem} disabled={!selectedProductId}>
                <Plus className="h-4 w-4 mr-2" />
                Add
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Line Items */}
      {items.length > 0 && (
        <Card className="glass">
          <CardHeader>
            <CardTitle>Order Items</CardTitle>
            <CardDescription>{items.length} item(s)</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product</TableHead>
                  <TableHead className="w-32">Quantity</TableHead>
                  <TableHead>Unit Price</TableHead>
                  <TableHead>Subtotal</TableHead>
                  <TableHead className="w-16"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {items.map((item) => (
                  <TableRow key={item.productId}>
                    <TableCell className="font-medium">{item.productName}</TableCell>
                    <TableCell>
                      <Input
                        type="number"
                        min={1}
                        value={item.quantity}
                        onChange={(e) =>
                          updateItemQty(item.productId, parseInt(e.target.value) || 1)
                        }
                        className="w-20 bg-white/5 border-white/10"
                      />
                    </TableCell>
                    <TableCell>₹{item.price.toLocaleString('en-IN')}</TableCell>
                    <TableCell className="font-semibold">
                      ₹{(item.quantity * item.price).toLocaleString('en-IN')}
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => removeItem(item.productId)}
                        className="text-red-500 hover:text-red-600"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>

            <div className="flex justify-between items-center mt-6 pt-4 border-t border-white/10">
              <span className="text-lg font-semibold">Total</span>
              <span className="text-2xl font-bold">₹{total.toLocaleString('en-IN')}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Actions */}
      <div className="flex gap-4 justify-end">
        <Button variant="outline" onClick={() => navigate('/sales')}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          disabled={submitting || items.length === 0 || !customer.trim()}
          className="bg-blue-500 hover:bg-blue-600"
        >
          {submitting ? 'Creating...' : 'Create Sale'}
        </Button>
      </div>
    </div>
  );
}
