import api from './api';
import type {
  AIInsight,
  DashboardSummary,
  HealthScore,
  ReorderSuggestionsResponse,
  ReportNarrative,
  StockoutPredictionsResponse,
  SalesSummary,
} from './types';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export const aiApi = {
  getInsights: async (): Promise<AIInsight[]> => {
    const { data } = await api.get('/ai/insights');
    return data;
  },

  getInsightsByType: async (type: AIInsight['type']): Promise<AIInsight[]> => {
    const { data } = await api.get('/ai/insights', { params: { type } });
    return data;
  },

  chat: async (message: string, history: ChatMessage[]): Promise<string> => {
    const { data } = await api.post('/ai/chat', {
      message,
      history: history.map((m) => ({ role: m.role, content: m.content })),
    });
    return data.response;
  },

  getSuggestedPrompts: async (): Promise<string[]> => {
    const { data } = await api.get('/ai/prompts');
    return data;
  },

  getDashboardSummary: async (): Promise<DashboardSummary> => {
    const { data } = await api.get('/ai/dashboard-summary');
    return data;
  },

  getHealthScore: async (): Promise<HealthScore> => {
    const { data } = await api.get('/ai/health-score');
    return data;
  },

  getReorderSuggestions: async (): Promise<ReorderSuggestionsResponse> => {
    const { data } = await api.get('/ai/reorder-suggestions');
    return data;
  },

  getReportNarrative: async (reportType: string, summary: Record<string, any>): Promise<ReportNarrative> => {
    const { data } = await api.post('/ai/report-narrative', {
      report_type: reportType,
      summary,
    });
    return data;
  },

  getStockoutPredictions: async (): Promise<StockoutPredictionsResponse> => {
    const { data } = await api.get('/ai/stockout-predictions');
    return data;
  },

  getSalesSummary: async (): Promise<SalesSummary> => {
    const { data } = await api.get('/ai/sales-summary');
    return data;
  },
};
