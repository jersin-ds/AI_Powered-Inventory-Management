import { useParams, useNavigate } from 'react-router';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, Package, IndianRupee, TrendingUp, Warehouse } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Skeleton } from '../components/ui/skeleton';
import { productApi } from '../services/product-api';

export function ProductDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data: product, isLoading } = useQuery({
    queryKey: ['product', id],
    queryFn: () => productApi.getById(id!),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-12 w-64" />
        <div className="grid grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
      </div>
    );
  }

  if (!product) {
    return <div>Product not found</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate('/products')}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold">{product.name}</h1>
          <p className="text-muted-foreground">{product.sku}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="glass">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <Package className="h-4 w-4" />
              Stock Quantity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{product.stockQty}</div>
            <p className="text-xs text-muted-foreground">Min: {product.minLevel}</p>
          </CardContent>
        </Card>

        <Card className="glass">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <IndianRupee className="h-4 w-4" />
              Cost Price
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹{product.costPrice.toLocaleString('en-IN')}</div>
          </CardContent>
        </Card>

        <Card className="glass">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              Sell Price
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹{product.sellPrice.toLocaleString('en-IN')}</div>
            <p className="text-xs text-green-500">
              +{(((product.sellPrice - product.costPrice) / product.costPrice) * 100).toFixed(1)}%
              margin
            </p>
          </CardContent>
        </Card>

        <Card className="glass">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <Warehouse className="h-4 w-4" />
              Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Badge className={product.status === 'active' ? 'bg-green-500' : 'bg-red-500'}>
              {product.status.replace('_', ' ')}
            </Badge>
          </CardContent>
        </Card>
      </div>

      <Card className="glass">
        <CardHeader>
          <CardTitle>Product Details</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="grid grid-cols-2 gap-4">
            <div>
              <dt className="text-sm text-muted-foreground">Category</dt>
              <dd className="font-medium">{product.category}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">Subcategory</dt>
              <dd className="font-medium">{product.subcategory}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">Supplier</dt>
              <dd className="font-medium">{product.supplier}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">Barcode</dt>
              <dd className="font-medium font-mono">{product.barcode}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">Created Date</dt>
              <dd className="font-medium">{product.createdAt}</dd>
            </div>
          </dl>
        </CardContent>
      </Card>
    </div>
  );
}
