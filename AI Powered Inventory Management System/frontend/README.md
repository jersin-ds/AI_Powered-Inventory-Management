# 🚀 AI-Powered Inventory Management System

A modern, enterprise-grade inventory management dashboard with AI-powered insights, built with React, TypeScript, and Tailwind CSS.

## ✨ Features

### 🎯 Core Functionality
- **Dashboard** - Real-time KPIs, charts, and analytics
- **Product Management** - Complete CRUD operations with search and filtering
- **Warehouse Management** - Multi-location inventory tracking
- **Stock Management** - Real-time stock levels with alerts
- **Purchase Orders** - Supplier order management
- **Sales Management** - Invoice generation and tracking
- **Reports & Analytics** - Comprehensive business insights

### 🤖 AI Features
- **Demand Forecasting** - AI-predicted inventory needs
- **Dead Stock Detection** - Identify slow-moving items
- **Anomaly Detection** - Unusual sales pattern alerts
- **Price Optimization** - AI-suggested pricing strategies
- **Expiry Risk Management** - Proactive expiry warnings
- **AI Chat Assistant** - Natural language inventory queries

### 🎨 Design System
- **Glassmorphism UI** - Modern frosted glass aesthetic
- **Dark/Light Mode** - System-aware theme switching
- **Responsive Design** - Mobile-first approach
- **Smooth Animations** - Motion-powered transitions
- **Custom Scrollbars** - Polished UI details

### 🔐 Role-Based Access Control (RBAC)
- **Admin** - Full system access
- **Inventory Manager** - Products, stock, purchases, AI insights
- **Sales Staff** - Sales operations and limited reports

## 🛠️ Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS v4** - Utility-first styling
- **React Router** - Client-side routing
- **TanStack Query** - Server state management
- **Zustand** - Client state management
- **Axios** - HTTP client
- **shadcn/ui** - UI component library
- **Recharts** - Data visualization
- **Motion (Framer Motion)** - Animations
- **Lucide Icons** - Icon library
- **SCSS** - Advanced styling

## 🚀 Quick Start

### Demo Accounts

**Admin Account:**
- Email: `admin@inventory.com`
- Password: any password

**Inventory Manager:**
- Email: `manager@inventory.com`
- Password: any password

**Sales Staff:**
- Email: `sales@inventory.com`
- Password: any password

> Note: The authentication is mocked for demo purposes. Any email containing the role name will grant that role's permissions.

## 📁 Project Structure

```
src/
├── app/
│   ├── components/
│   │   ├── ai/              # AI Chat Assistant
│   │   ├── auth/            # Authentication components
│   │   ├── layout/          # Sidebar, Navbar
│   │   ├── providers/       # Theme provider
│   │   └── ui/              # shadcn/ui components
│   ├── pages/               # All route pages
│   ├── services/            # API services & mock data
│   ├── store/               # Zustand stores
│   ├── lib/                 # Utilities
│   ├── routes.tsx           # Route configuration
│   └── App.tsx              # Root component
├── styles/
│   ├── global.scss          # Global SCSS styles
│   ├── theme.css            # CSS variables
│   └── index.css            # Style imports
```

## 🎨 Key Features Explained

### Glassmorphism Design
The entire UI uses a modern glassmorphism design system with:
- Frosted glass backgrounds
- Subtle borders and shadows
- Smooth color transitions
- Responsive blur effects

### AI Integration
All AI features are powered by mock responses that simulate:
- Real-time analysis
- Natural language processing
- Predictive analytics
- Intelligent recommendations

### State Management
- **Zustand** for UI state (theme, sidebar, AI chat)
- **TanStack Query** for server data caching
- **Local Storage** for persistence

### Routing & RBAC
- Protected routes based on user permissions
- Role-based sidebar navigation
- Unauthorized page handling

## 📊 Mock Data

The application uses comprehensive mock data including:
- 5 sample products with realistic data
- 3 warehouses with capacity tracking
- Purchase orders and sales records
- 5 AI insights across different categories
- Dashboard analytics and charts

## 🎯 Main Routes

- `/login` - Authentication
- `/dashboard` - Main overview
- `/products` - Product catalog
- `/warehouses` - Warehouse management
- `/stock` - Stock monitoring
- `/purchases` - Purchase orders
- `/sales` - Sales management
- `/ai-insights` - AI recommendations
- `/settings` - User settings
- `/users` - User management (Admin only)

## 🎨 Theme System

The application supports:
- **Light Mode** - Clean, bright interface
- **Dark Mode** - Eye-friendly dark theme
- **System Mode** - Follows OS preference

Theme persists across sessions and applies instantly.

## 🤖 AI Chat Assistant

Access the floating AI assistant from any page:
- Natural language queries
- Contextual responses
- Suggested prompts
- Chat history
- Expandable interface

## 📱 Responsive Design

Fully responsive across all devices:
- Desktop (1920px+)
- Laptop (1024px - 1919px)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🔧 Production Considerations

This is a **frontend-only demo**. For production:
1. Replace mock API calls with real backend
2. Implement actual authentication (JWT, OAuth)
3. Add real AI integration (OpenAI, custom ML models)
4. Set up proper error handling and logging
5. Implement data validation
6. Add unit and integration tests
7. Set up CI/CD pipeline

## 📝 License

This is a demonstration project for educational purposes.

---

Built with ❤️ for CSE Final Year Project
