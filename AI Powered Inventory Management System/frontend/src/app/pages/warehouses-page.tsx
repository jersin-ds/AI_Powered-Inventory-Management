import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Warehouse, Plus, Edit, Trash2 } from 'lucide-react';
import api from '../services/api';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
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
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../components/ui/dialog';
import { Skeleton } from '../components/ui/skeleton';
import { toast } from 'sonner';

interface WarehouseFormData {
  name: string;
  location: string;
  capacity: number;
  currentStock: number;
  manager: string;
  status: string;
}

const emptyForm: WarehouseFormData = {
  name: '',
  location: '',
  capacity: 1000,
  currentStock: 0,
  manager: '',
  status: 'active',
};

export function WarehousesPage() {
  const queryClient = useQueryClient();
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [editingWarehouse, setEditingWarehouse] = useState<any>(null);

  const { data: warehouses = [], isLoading } = useQuery({
    queryKey: ['warehouses'],
    queryFn: async () => {
      const { data } = await api.get('/warehouses');
      return data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/warehouses/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['warehouses'] });
      toast.success('Warehouse deleted successfully');
    },
    onError: (err: any) => {
      toast.error(err?.response?.data?.detail || 'Failed to delete warehouse');
    },
  });

  const handleDelete = (id: string, name: string) => {
    if (confirm(`Are you sure you want to delete "${name}"?`)) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Warehouse className="h-8 w-8" />
            Warehouses
          </h1>
          <p className="text-muted-foreground mt-1">Manage warehouse locations and stock</p>
        </div>
        <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add Warehouse
            </Button>
          </DialogTrigger>
          <DialogContent className="glass max-w-lg">
            <WarehouseForm
              onClose={() => setIsAddOpen(false)}
              onSuccess={() => {
                queryClient.invalidateQueries({ queryKey: ['warehouses'] });
                setIsAddOpen(false);
              }}
            />
          </DialogContent>
        </Dialog>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(3)].map((_, i) => (
            <Skeleton key={i} className="h-64 w-full" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {warehouses.map((warehouse: any) => {
            const utilization = (warehouse.currentStock / warehouse.capacity) * 100;
            return (
              <Card key={warehouse.id} className="glass card-hover">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>{warehouse.name}</CardTitle>
                    <Badge className={warehouse.status === 'active' ? 'bg-green-500' : 'bg-gray-500'}>
                      {warehouse.status}
                    </Badge>
                  </div>
                  <CardDescription>{warehouse.location}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-muted-foreground">Capacity Utilization</span>
                      <span className="font-medium">{utilization.toFixed(0)}%</span>
                    </div>
                    <Progress value={utilization} className="h-2" />
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-muted-foreground">Current Stock</p>
                      <p className="font-bold text-lg">{warehouse.currentStock.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">Capacity</p>
                      <p className="font-bold text-lg">{warehouse.capacity.toLocaleString()}</p>
                    </div>
                  </div>
                  <div>
                    <p className="text-muted-foreground text-sm">Manager</p>
                    <p className="font-medium">{warehouse.manager}</p>
                  </div>
                  <div className="flex gap-2 pt-2 border-t border-white/10">
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button
                          variant="outline"
                          size="sm"
                          className="flex-1"
                          onClick={() => setEditingWarehouse(warehouse)}
                        >
                          <Edit className="mr-2 h-4 w-4" />
                          Edit
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="glass max-w-lg">
                        <WarehouseForm
                          warehouse={editingWarehouse}
                          onClose={() => setEditingWarehouse(null)}
                          onSuccess={() => {
                            queryClient.invalidateQueries({ queryKey: ['warehouses'] });
                            setEditingWarehouse(null);
                          }}
                        />
                      </DialogContent>
                    </Dialog>
                    <Button
                      variant="outline"
                      size="sm"
                      className="text-red-500 hover:text-red-600"
                      onClick={() => handleDelete(warehouse.id, warehouse.name)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}

// Warehouse Form Component (same pattern as ProductForm)
interface WarehouseFormProps {
  warehouse?: any;
  onClose: () => void;
  onSuccess: () => void;
}

function WarehouseForm({ warehouse, onClose, onSuccess }: WarehouseFormProps) {
  const [formData, setFormData] = useState<WarehouseFormData>(
    warehouse
      ? {
          name: warehouse.name,
          location: warehouse.location,
          capacity: warehouse.capacity,
          currentStock: warehouse.currentStock,
          manager: warehouse.manager,
          status: warehouse.status,
        }
      : emptyForm,
  );
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name.trim() || !formData.location.trim()) {
      toast.error('Name and location are required');
      return;
    }
    setSaving(true);
    try {
      if (warehouse) {
        await api.put(`/warehouses/${warehouse.id}`, formData);
        toast.success('Warehouse updated successfully');
      } else {
        await api.post('/warehouses', formData);
        toast.success('Warehouse created successfully');
      }
      onSuccess();
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to save warehouse');
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <DialogHeader>
        <DialogTitle>{warehouse ? 'Edit Warehouse' : 'Add New Warehouse'}</DialogTitle>
        <DialogDescription>
          {warehouse ? 'Update warehouse information' : 'Add a new warehouse location'}
        </DialogDescription>
      </DialogHeader>
      <div className="grid grid-cols-2 gap-4 py-4">
        <div className="space-y-2">
          <Label htmlFor="wh-name">Warehouse Name</Label>
          <Input
            id="wh-name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="bg-white/5 border-white/10"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="wh-location">Location</Label>
          <Input
            id="wh-location"
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            className="bg-white/5 border-white/10"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="wh-capacity">Capacity</Label>
          <Input
            id="wh-capacity"
            type="number"
            min={1}
            value={formData.capacity}
            onChange={(e) => setFormData({ ...formData, capacity: parseInt(e.target.value) || 0 })}
            className="bg-white/5 border-white/10"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="wh-stock">Current Stock</Label>
          <Input
            id="wh-stock"
            type="number"
            min={0}
            value={formData.currentStock}
            onChange={(e) => setFormData({ ...formData, currentStock: parseInt(e.target.value) || 0 })}
            className="bg-white/5 border-white/10"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="wh-manager">Manager</Label>
          <Input
            id="wh-manager"
            value={formData.manager}
            onChange={(e) => setFormData({ ...formData, manager: e.target.value })}
            className="bg-white/5 border-white/10"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="wh-status">Status</Label>
          <Select value={formData.status} onValueChange={(v) => setFormData({ ...formData, status: v })}>
            <SelectTrigger className="bg-white/5 border-white/10">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="inactive">Inactive</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
      <DialogFooter>
        <Button type="button" variant="outline" onClick={onClose}>
          Cancel
        </Button>
        <Button type="submit" disabled={saving}>
          {saving ? 'Saving...' : warehouse ? 'Update' : 'Create'}
        </Button>
      </DialogFooter>
    </form>
  );
}
