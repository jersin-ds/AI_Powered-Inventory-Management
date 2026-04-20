import { useState } from 'react';
import { motion } from 'motion/react';
import {
  BarChart3,
  Download,
  FileText,
  Calendar,
  TrendingUp,
  Package,
  ShoppingCart,
  IndianRupee,
  Sparkles,
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Label } from '../components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table';
import { Skeleton } from '../components/ui/skeleton';
import api from '../services/api';
import { aiApi } from '../services/ai-api';
import { toast } from 'sonner';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import * as XLSX from 'xlsx';

type ReportType = 'sales' | 'purchases' | 'inventory' | 'profit';
type DateRange = '7days' | '30days' | '90days' | 'year';

export function ReportsPage() {
  const [reportType, setReportType] = useState<ReportType>('sales');
  const [dateRange, setDateRange] = useState<DateRange>('30days');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedReport, setGeneratedReport] = useState<any>(null);
  const [narrative, setNarrative] = useState<string | null>(null);
  const [narrativeLoading, setNarrativeLoading] = useState(false);

  const handleGenerateReport = async () => {
    setIsGenerating(true);
    setNarrative(null);
    try {
      const { data } = await api.get(`/reports/${reportType}`, {
        params: { range: dateRange },
      });
      setGeneratedReport(data);
      toast.success('Report generated successfully');

      // Auto-generate AI narrative
      setNarrativeLoading(true);
      try {
        const narrativeData = await aiApi.getReportNarrative(reportType, data.summary);
        setNarrative(narrativeData.narrative);
      } catch {
        // Narrative is optional
      } finally {
        setNarrativeLoading(false);
      }
    } catch {
      toast.error('Failed to generate report');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExportReport = (format: 'pdf' | 'excel' | 'csv') => {
    if (!generatedReport?.data || generatedReport.data.length === 0) {
      toast.error('No report data to export');
      return;
    }

    try {
      const rows = generatedReport.data;
      const headers = Object.keys(rows[0]).filter((k) => k !== 'id' && k !== 'items');
      const fileName = generatedReport.title.replace(/\s+/g, '_');

      if (format === 'pdf') {
        const doc = new jsPDF();
        doc.setFontSize(16);
        doc.text(generatedReport.title, 14, 20);
        doc.setFontSize(10);
        doc.text(`Period: ${getDateRangeLabel(generatedReport.period)}`, 14, 28);
        autoTable(doc, {
          head: [headers.map((h) => h.replace(/([A-Z])/g, ' $1').trim())],
          body: rows.map((row: any) => headers.map((h) => row[h] ?? '')),
          startY: 35,
          styles: { fontSize: 8 },
          headStyles: { fillColor: [37, 99, 235] },
        });
        doc.save(`${fileName}.pdf`);
      } else if (format === 'excel') {
        const wsData = [headers, ...rows.map((row: any) => headers.map((h) => row[h] ?? ''))];
        const ws = XLSX.utils.aoa_to_sheet(wsData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, 'Report');
        XLSX.writeFile(wb, `${fileName}.xlsx`);
      } else {
        const csvHeader = headers.join(',');
        const csvBody = rows
          .map((row: any) =>
            headers.map((h) => {
              const val = row[h];
              if (typeof val === 'string' && val.includes(',')) return `"${val}"`;
              return val;
            }).join(',')
          )
          .join('\n');
        const csv = csvHeader + '\n' + csvBody;
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${fileName}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }
      toast.success(`Report exported as ${format.toUpperCase()}`);
    } catch {
      toast.error('Failed to export report');
    }
  };

  const getDateRangeLabel = (range: DateRange) => {
    const labels = {
      '7days': 'Last 7 Days',
      '30days': 'Last 30 Days',
      '90days': 'Last 90 Days',
      'year': 'Last Year',
    };
    return labels[range];
  };

  const reportTemplates = [
    {
      type: 'sales' as ReportType,
      title: 'Sales Report',
      description: 'Detailed sales performance and revenue analysis',
      icon: ShoppingCart,
      color: 'text-blue-500',
    },
    {
      type: 'purchases' as ReportType,
      title: 'Purchase Report',
      description: 'Purchase orders and supplier transactions',
      icon: Package,
      color: 'text-green-500',
    },
    {
      type: 'inventory' as ReportType,
      title: 'Inventory Report',
      description: 'Stock levels and product valuation',
      icon: FileText,
      color: 'text-purple-500',
    },
    {
      type: 'profit' as ReportType,
      title: 'Profit & Loss',
      description: 'Financial performance and profit margins',
      icon: IndianRupee,
      color: 'text-amber-500',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold flex items-center gap-2">
          <BarChart3 className="h-6 w-6 sm:h-8 sm:w-8" />
          Reports
        </h1>
        <p className="text-muted-foreground mt-1 text-sm sm:text-base">
          Generate and view comprehensive reports
        </p>
      </div>

      {/* Report Templates */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {reportTemplates.map((template, index) => {
          const Icon = template.icon;
          return (
            <motion.div
              key={template.type}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card
                className={`glass card-hover cursor-pointer ${
                  reportType === template.type ? 'ring-2 ring-blue-500' : ''
                }`}
                onClick={() => setReportType(template.type)}
              >
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Icon className={`h-8 w-8 ${template.color}`} />
                    {reportType === template.type && (
                      <Badge className="bg-blue-500">Selected</Badge>
                    )}
                  </div>
                  <CardTitle className="text-base mt-2">{template.title}</CardTitle>
                  <CardDescription className="text-xs mt-1">
                    {template.description}
                  </CardDescription>
                </CardHeader>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Report Configuration */}
      <Card className="glass">
        <CardHeader>
          <CardTitle>Report Configuration</CardTitle>
          <CardDescription>Select parameters for your report</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="space-y-2">
              <Label htmlFor="reportType">Report Type</Label>
              <Select value={reportType} onValueChange={(value: ReportType) => setReportType(value)}>
                <SelectTrigger className="bg-white/5">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="sales">Sales Report</SelectItem>
                  <SelectItem value="purchases">Purchase Report</SelectItem>
                  <SelectItem value="inventory">Inventory Report</SelectItem>
                  <SelectItem value="profit">Profit & Loss</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="dateRange">Date Range</Label>
              <Select value={dateRange} onValueChange={(value: DateRange) => setDateRange(value)}>
                <SelectTrigger className="bg-white/5">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7days">Last 7 Days</SelectItem>
                  <SelectItem value="30days">Last 30 Days</SelectItem>
                  <SelectItem value="90days">Last 90 Days</SelectItem>
                  <SelectItem value="year">Last Year</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-end">
              <Button
                onClick={handleGenerateReport}
                disabled={isGenerating}
                className="bg-blue-500 hover:bg-blue-600 w-full"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                    Generating...
                  </>
                ) : (
                  <>
                    <FileText className="mr-2 h-4 w-4" />
                    Generate Report
                  </>
                )}
              </Button>
            </div>
            {generatedReport && (
              <div className="flex items-end">
                <Button
                  variant="outline"
                  onClick={() => handleExportReport('pdf')}
                  className="w-full"
                >
                  <Download className="mr-2 h-4 w-4" />
                  Export PDF
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Generated Report */}
      {generatedReport && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Report Header */}
          <Card className="glass">
            <CardHeader>
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <CardTitle className="text-xl">{generatedReport.title}</CardTitle>
                  <CardDescription className="mt-1 flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    {getDateRangeLabel(generatedReport.period)}
                  </CardDescription>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleExportReport('pdf')}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    PDF
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleExportReport('excel')}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Excel
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleExportReport('csv')}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    CSV
                  </Button>
                </div>
              </div>
            </CardHeader>
          </Card>

          {/* Report Summary */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(generatedReport.summary).map(([key, value], index) => (
              <motion.div
                key={key}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="glass">
                  <CardContent className="pt-6">
                    <div className="space-y-2">
                      <p className="text-xs text-muted-foreground capitalize">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </p>
                      <p className="text-xl sm:text-2xl font-bold">
                        {typeof value === 'number'
                          ? key.toLowerCase().includes('total') ||
                            key.toLowerCase().includes('value') ||
                            key.toLowerCase().includes('revenue') ||
                            key.toLowerCase().includes('profit')
                            ? `₹${value.toLocaleString('en-IN')}`
                            : key.toLowerCase().includes('margin')
                            ? `${value}%`
                            : value.toLocaleString()
                          : value}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* AI Report Narrative */}
          <Card className="glass border-blue-500/20 bg-gradient-to-r from-blue-500/5 to-purple-500/5">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-blue-500" />
                <CardTitle className="text-lg">AI Analysis</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              {narrativeLoading ? (
                <div className="space-y-2">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-5/6" />
                  <Skeleton className="h-4 w-3/4" />
                </div>
              ) : narrative ? (
                <p className="text-sm leading-relaxed text-muted-foreground">{narrative}</p>
              ) : (
                <p className="text-sm text-muted-foreground">AI narrative unavailable for this report.</p>
              )}
            </CardContent>
          </Card>

          {/* Report Data Table */}
          {generatedReport.data && (
            <Card className="glass">
              <CardHeader>
                <CardTitle>Detailed Data</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  {reportType === 'sales' && (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Invoice</TableHead>
                          <TableHead>Customer</TableHead>
                          <TableHead>Date</TableHead>
                          <TableHead>Status</TableHead>
                          <TableHead className="text-right">Amount</TableHead>
                          <TableHead className="text-right">Profit</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {generatedReport.data.map((sale: any) => (
                          <TableRow key={sale.id}>
                            <TableCell className="font-medium">{sale.invoiceNumber}</TableCell>
                            <TableCell>{sale.customer}</TableCell>
                            <TableCell>{new Date(sale.date).toLocaleDateString()}</TableCell>
                            <TableCell>
                              <Badge
                                variant={
                                  sale.status === 'completed'
                                    ? 'default'
                                    : sale.status === 'pending'
                                    ? 'secondary'
                                    : 'destructive'
                                }
                              >
                                {sale.status}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-right">₹{sale.totalAmount.toLocaleString('en-IN')}</TableCell>
                            <TableCell className="text-right text-green-500">
                              ₹{sale.profit.toLocaleString('en-IN')}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}

                  {reportType === 'purchases' && (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>PO Number</TableHead>
                          <TableHead>Supplier</TableHead>
                          <TableHead>Date</TableHead>
                          <TableHead>Status</TableHead>
                          <TableHead className="text-right">Amount</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {generatedReport.data.map((purchase: any) => (
                          <TableRow key={purchase.id}>
                            <TableCell className="font-medium">{purchase.poNumber}</TableCell>
                            <TableCell>{purchase.supplier}</TableCell>
                            <TableCell>{new Date(purchase.date).toLocaleDateString()}</TableCell>
                            <TableCell>
                              <Badge
                                variant={
                                  purchase.status === 'received'
                                    ? 'default'
                                    : purchase.status === 'pending'
                                    ? 'secondary'
                                    : 'destructive'
                                }
                              >
                                {purchase.status}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-right">
                              ₹{purchase.totalAmount.toLocaleString('en-IN')}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}

                  {reportType === 'inventory' && (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>SKU</TableHead>
                          <TableHead>Product</TableHead>
                          <TableHead>Category</TableHead>
                          <TableHead className="text-right">Stock</TableHead>
                          <TableHead className="text-right">Value</TableHead>
                          <TableHead>Status</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {generatedReport.data.map((product: any) => (
                          <TableRow key={product.id}>
                            <TableCell className="font-medium">{product.sku}</TableCell>
                            <TableCell>{product.name}</TableCell>
                            <TableCell>{product.category}</TableCell>
                            <TableCell className="text-right">{product.stockQty}</TableCell>
                            <TableCell className="text-right">
                              ₹{(product.stockQty * product.costPrice).toLocaleString('en-IN')}
                            </TableCell>
                            <TableCell>
                              <Badge
                                variant={
                                  product.status === 'active'
                                    ? 'default'
                                    : product.status === 'low_stock'
                                    ? 'secondary'
                                    : 'destructive'
                                }
                              >
                                {product.status.replace('_', ' ')}
                              </Badge>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Profit & Loss Breakdown */}
          {reportType === 'profit' && (
            <Card className="glass">
              <CardHeader>
                <CardTitle>Financial Breakdown</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between py-3 border-b border-white/10">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5 text-green-500" />
                      <span className="font-medium">Total Revenue</span>
                    </div>
                    <span className="text-lg font-bold text-green-500">
                      ₹{generatedReport.summary.totalRevenue.toLocaleString('en-IN')}
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b border-white/10">
                    <div className="flex items-center gap-2">
                      <IndianRupee className="h-5 w-5 text-blue-500" />
                      <span className="font-medium">Total Profit</span>
                    </div>
                    <span className="text-lg font-bold text-blue-500">
                      ₹{generatedReport.summary.totalProfit.toLocaleString('en-IN')}
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b border-white/10">
                    <div className="flex items-center gap-2">
                      <BarChart3 className="h-5 w-5 text-purple-500" />
                      <span className="font-medium">Profit Margin</span>
                    </div>
                    <span className="text-lg font-bold text-purple-500">
                      {generatedReport.summary.profitMargin}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-3">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5 text-amber-500" />
                      <span className="font-medium">Growth Rate</span>
                    </div>
                    <span className="text-lg font-bold text-amber-500">
                      {generatedReport.summary.growth >= 0 ? '+' : ''}{generatedReport.summary.growth}%
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </motion.div>
      )}

      {!generatedReport && (
        <Card className="glass">
          <CardContent className="py-12 text-center">
            <BarChart3 className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Report Generated</h3>
            <p className="text-muted-foreground">
              Select a report type and date range, then click Generate Report
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
