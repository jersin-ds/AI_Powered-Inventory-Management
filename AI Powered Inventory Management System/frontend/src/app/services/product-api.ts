import api from './api';
import type { Product } from './types';

export const productApi = {
  getAll: async (): Promise<Product[]> => {
    const { data } = await api.get('/products');
    return data;
  },

  getById: async (id: string): Promise<Product> => {
    const { data } = await api.get(`/products/${id}`);
    return data;
  },

  create: async (product: Omit<Product, 'id' | 'createdAt'>): Promise<Product> => {
    const { data } = await api.post('/products', product);
    return data;
  },

  update: async (id: string, updates: Partial<Product>): Promise<Product> => {
    const { data } = await api.put(`/products/${id}`, updates);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/products/${id}`);
  },

  search: async (query: string): Promise<Product[]> => {
    const { data } = await api.get('/products/search', { params: { q: query } });
    return data;
  },
};
