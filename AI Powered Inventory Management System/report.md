# AI-Powered Inventory Management System
## Final Year UG Project Report (Draft)

Department of Computer Science and Engineering  
Academic Year: 2025-2026

Prepared by: [Student Name], [Roll Number]  
Under the Guidance of: [Guide Name], [Designation]  
Co-Author: [Co-Author Name], [Designation]

---

## Certificate

This is to certify that the project report titled "AI-Powered Inventory Management System" is a bonafide record of work carried out by [Student Name], [Roll Number], under my guidance and supervision in partial fulfillment of the requirements for the award of the Degree of Bachelor of Engineering in Computer Science and Engineering.

Guide Signature: ____________________  
Head of Department Signature: ____________________  
Date: ____________________

---

## Declaration

I hereby declare that this project report titled "AI-Powered Inventory Management System" is my original work and has not been submitted to any other university or institution for the award of any degree or diploma. Wherever reference has been made to the work of others, due acknowledgment has been given.

Student Signature: ____________________  
Name: ____________________  
Date: ____________________

---

## Acknowledgement

I express my sincere gratitude to my project guide [Guide Name] for continuous support, motivation, and technical guidance throughout this project. I thank the Head of the Department and all faculty members of the Department of Computer Science and Engineering for their encouragement.

I am grateful to my co-author [Co-Author Name] for valuable suggestions and feedback. I also thank my classmates and family members for their support during the successful completion of this project.

---

## Table of Contents

INTRODUCTION  
	1.1 Description  
	1.2 Objective  
	1.3 Problem Definition  
		1.3.1 Purpose  
		1.3.2 Scope  
		1.3.3 Contributions  

LITERATURE REVIEW  

PROPOSED SYSTEM  
	3.1 Overview  
		3.1.1 Disadvantages  
	3.2 Proposed System  
		3.2.1 Advantages  
	3.3 Architecture Diagram  
	3.4 Modules  
		3.4.1 User Interface Module  
		3.4.2 Authentication Module  
		3.4.3 Backend API Module  
		3.4.4 AI Query Processing Module  
		3.4.5 Database Module  

SYSTEM REQUIREMENTS  
	4.1 System Description  
	4.2 Components/Tools Required  
	4.3 Software Tools  
		4.3.1 Visual Studio Code  
		4.3.2 Version Control with GitHub  
		4.3.3 Cerebras API Key  
	4.4 Software Packages  
		4.4.1 FastAPI  
		4.4.2 Uvicorn  
		4.4.3 SQLAlchemy  
		4.4.4 Pydantic  
		4.4.5 Python-Jose  
		4.4.6 Passlib  
		4.4.7 Python-Dotenv  
		4.4.8 HTTPX  
		4.4.9 Python-Multipart  
		4.4.10 Cerebras-Cloud-SDK  
		4.4.11 Bcrypt  
	4.5 Comparison with Existing System vs Proposed System  

## 4.1 System Description

This chapter provides a detailed overview of the hardware and software requirements, tools, and components used in the implementation of the AI-Powered Inventory Management System. It covers the essential specifications for development and deployment, ensuring the system can handle inventory operations, AI integrations, and multi-user interactions efficiently.

### Technical Feasibility

Technically feasible due to mature stack components: FastAPI, SQLAlchemy, React, and Cerebras SDK. The architecture is modular and maintainable.

### Economic Feasibility

Open-source framework stack reduces licensing cost. The system can run on modest development hardware and supports incremental deployment.

### Operational Feasibility

Role-based UI and AI-assisted recommendations improve usability for non-technical users. Existing workflow maps to common inventory operations.

### Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | User login with JWT authentication |
| FR-02 | Role and permission based route access |
| FR-03 | Product CRUD with SKU and status handling |
| FR-04 | Category and supplier management |
| FR-05 | Warehouse and stock operations |
| FR-06 | Purchase and sale management |
| FR-07 | Dashboard KPIs and charts |
| FR-08 | AI insight generation and retrieval |
| FR-09 | AI chat with inventory context |
| FR-10 | Alerts retrieval and update |
| FR-11 | Reports and analytics endpoints |
| FR-12 | User management for authorized roles |

### Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-01 | Secure password hashing and token handling |
| NFR-02 | Modular, maintainable architecture |
| NFR-03 | Input and schema validation |
| NFR-04 | Responsive frontend experience |
| NFR-05 | Configurable environment-based settings |
| NFR-06 | Graceful fallback for AI/API failures |

### User Roles and Permissions

| Role | Typical Access |
|---|---|
| Admin | Full system administration, user and module access |
| Inventory Manager | Product, stock, warehouse, purchases, reports, AI insights |
| Sales Staff | Sales-oriented operations, limited reports, AI view |

## 4.2 Components/Tools Required

### Hardware Specification
- A PC or Laptop with Windows OS (10 or above)
- 8 GB RAM (recommended for smooth AI processing)
- 10 GB free storage (for code, database, and dependencies)

### Software Tools
- Code Editor (e.g., Visual Studio Code)
- Version Control with GitHub
- Cerebras API Key

### Software Packages
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Python-Jose
- Passlib
- Python-Dotenv
- HTTPX
- Python-Multipart
- Cerebras-Cloud-SDK
- Bcrypt

## 4.3 Software Tools

### 4.3.1 Visual Studio Code

Visual Studio Code (VS Code) is a versatile, open-source code editor developed by Microsoft, serving as the primary development environment for the AI-Powered Inventory Management System. It supports multiple programming languages and frameworks, making it ideal for full-stack development involving React, FastAPI, and Python scripting. In this project, VS Code is used to write, debug, and manage code for frontend components (React with TypeScript), backend APIs (FastAPI), and AI integration scripts.

Key features include IntelliSense for smart code suggestions, auto-completion, and real-time error detection, which enhance productivity and reduce bugs. Syntax highlighting, integrated debugging, built-in terminal, and Git support streamline the workflow. Extensibility via plugins, such as Python and React extensions, further boosts capabilities—e.g., enabling live previews of UI changes and efficient API testing with tools like REST Client.

Its lightweight design ensures performance even with complex projects. VS Code's organized folder structure helps maintain code cleanliness, making it essential for building and managing the scalable inventory system.

### 4.3.2 Version Control with GitHub

GitHub is a critical platform for version control and collaboration in software development, functioning as a distributed version control system (DVCS). It allows tracking codebase changes, managing milestones, and enabling global team collaboration. Cloud-based repositories ensure secure, remote access to code, supporting decentralized workflows.

Branching and merging enable concurrent feature development, ensuring stability. Pull requests facilitate code reviews and feedback integration. Issue tracking centralizes task management, bugs, and features, promoting transparency. Integrated tools like wikis, project boards, and discussions enhance communication.

CI/CD integration automates builds, tests, and deployments, delivering reliable software. In this inventory project, GitHub supports collaborative development of AI features and multi-user modules.

### 4.3.3 Cerebras API Key

The Cerebras API Key is a secure token for accessing Cerebras Cloud's LLaMA 3.1-8B model via the Inference API. In the AI-Powered Inventory Management System, it's used in the FastAPI backend for authorized requests to generate insights like demand forecasting and anomaly detection. The key ensures secure access, tracks usage (requests and tokens), and prevents unauthorized interactions.

It enables fine-tuned AI responses for inventory queries, with pricing based on usage. For security, the key is stored in environment variables, not exposed in code. If compromised, it can be regenerated via the Cerebras dashboard. Overall, it's vital for real-time, intelligent inventory assistance.

## 4.4 Software Packages

### 4.4.1 FastAPI

FastAPI is a modern Python web framework for building high-performance RESTful APIs, leveraging type hints for automatic data validation and OpenAPI documentation. In this inventory system, it's used for backend APIs handling CRUD operations, AI insights, and user authentication. Its async support ensures efficient concurrent requests, with automatic schema generation improving development and testing.

### 4.4.2 Uvicorn

Uvicorn is a high-performance ASGI server for deploying FastAPI applications, built on uvloop and httptools for optimized networking. It handles HTTP requests asynchronously, enabling non-blocking operations crucial for real-time AI interactions in the inventory system. Lightweight and configurable, it integrates seamlessly for scalable deployment.

### 4.4.3 SQLAlchemy

SQLAlchemy is a powerful ORM library for database interactions, supporting SQLite and other engines. In the project, it manages inventory entities like products and sales, enabling efficient queries and relationships. Its abstraction layer simplifies data persistence, ensuring maintainability and performance in multi-user environments.

### 4.4.4 Pydantic

Pydantic is a Python library for data validation and modeling, defining schemas with type safety. In the inventory system, it validates API inputs/outputs for products and users, preventing errors and generating documentation. It enhances reliability in FastAPI integrations, maintaining data integrity across modules.

### 4.4.5 Python-Jose

Python-Jose is a library for JWT encoding/decoding, used for secure authentication. In the system, it handles token generation for user sessions and role-based access, ensuring encrypted, verifiable claims. It's essential for protecting endpoints and managing multi-user permissions.

### 4.4.6 Passlib

Passlib provides password hashing utilities, supporting bcrypt for secure storage. In the inventory project, it hashes user passwords, protecting against breaches. Combined with JWT, it ensures robust authentication for admins and staff.

### 4.4.7 Python-Dotenv

Python-Dotenv loads environment variables from a .env file, securing sensitive data like API keys. In the system, it manages configurations for Cerebras and database credentials, keeping secrets out of source code for safe deployment and collaboration.

### 4.4.8 HTTPX

HTTPX is an async HTTP client for API interactions, used for Cerebras requests. In the inventory backend, it enables non-blocking calls for AI insights, improving responsiveness. Its compatibility with async frameworks ensures efficient external integrations.

### 4.4.9 Python-Multipart

Python-Multipart handles multipart form data, useful for file uploads. In the system, it supports potential document uploads for reports, integrating with FastAPI for secure, validated handling.

### 4.4.10 Cerebras-Cloud-SDK

The Cerebras-Cloud-SDK is the official SDK for LLaMA model integration. In the project, it facilitates AI queries for forecasting and chat, with built-in error handling. It streamlines backend-AI communication for intelligent inventory features.

### 4.4.11 Bcrypt

Bcrypt is a password hashing algorithm, used with Passlib for encryption. In the system, it secures user credentials, preventing unauthorized access and ensuring compliance with security standards.

## 4.5 Comparison with Existing System vs Proposed System

| Aspect | Existing Systems | Proposed System |
|---|---|---|
| AI Integration | None | Integrated LLM for insights |
| User Interaction | Static reports | Natural-language chat |
| Forecasting | Manual or basic | AI-powered demand forecasting |
| Security | Basic | RBAC with JWT |
| Scalability | Limited | Modular architecture |

SYSTEM DESIGN AND IMPLEMENTATION  
	5.1 Introduction  
	5.2 Admin Module  
		5.2.1 Login Page  
		5.2.2 User Creation  
		5.2.3 Admin Dashboard  
		5.2.4 Product Creation  
		5.2.5 Category Management  
		5.2.6 Supplier Management  
		5.2.7 Warehouse Management  
	5.3 User Module  
	5.4 Backend Module  
	5.5 Sample Code  

TESTING AND RESULTS  

CONCLUSION AND FUTURE ENHANCEMENT  
	7.1 Conclusion  
	7.2 Future Enhancement  

REFERENCES  

APPENDICES

---

## List of Figures

Figure 1: High-Level System Architecture  
Figure 2: Backend Layered Architecture  
Figure 3: Data Flow Diagram (Level 0 and Level 1)  
Figure 4: ER Diagram (Text Representation)  
Figure 5: Use Case Overview  
Figure 6: AI Insight Generation Workflow

---

## List of Abbreviations

API - Application Programming Interface  
LLM - Large Language Model  
RBAC - Role-Based Access Control  
JWT - JSON Web Token  
CRUD - Create, Read, Update, Delete  
SQL - Structured Query Language  
ORM - Object-Relational Mapping  

---

## List of Tables

Table 1: Existing System Comparison  
Table 2: Functional Requirements  
Table 3: Non-Functional Requirements  
Table 4: Role and Permission Matrix  
Table 5: Major Backend Modules  
Table 6: Database Entity Summary  
Table 7: Test Cases and Expected Results  
Table 8: Literature Survey Summary

---

## ABSTRACT

Inventory management is a critical business function where inaccuracies lead to overstocking, stockouts, and financial losses. Most low-cost inventory solutions provide only CRUD operations and static analytics, with limited intelligent decision support. This project presents an AI-Powered Inventory Management System that combines a full-stack inventory platform with Large Language Model (LLM) based insights.

The system is implemented using React 18 and TypeScript on the frontend, FastAPI and SQLAlchemy on the backend, and SQLite as the primary data store. The AI layer integrates Cerebras Cloud (LLaMA 3.1-8B) to deliver demand forecasting, dead-stock detection, sales anomaly analysis, price optimization suggestions, expiry-risk alerts, stockout prediction, and natural-language inventory chat.

The architecture follows a layered approach: routes, services, repositories, and ORM models. Role-Based Access Control (RBAC) is enforced through JWT authentication and permission-based endpoint protection. Business modules include products, categories, suppliers, warehouses, stock, purchases, sales, reports, dashboards, analytics, alerts, users, and AI insights.

The final system provides a practical, scalable, and affordable solution for small and medium businesses by combining operational inventory workflows with intelligent recommendations. This report documents literature survey, requirement analysis, architecture, detailed implementation, testing strategy, observed outcomes, limitations, and future scope.

Keywords: Inventory Management, LLM, AI Insights, FastAPI, React, Demand Forecasting, Anomaly Detection, RBAC.

---

# INTRODUCTION

## 1.1 Description

Inventory management directly impacts profitability, customer satisfaction, and cash flow for product-based businesses. Traditional tools often provide only record-keeping and static reports. They do not offer context-aware forecasting, anomaly detection, or AI-assisted decision support.

In many small and medium businesses, stock decisions are made manually based on static reorder levels or staff experience. This leads to common problems:

1. Overstocking, causing inventory carrying costs and dead stock.
2. Understocking, causing missed sales and customer dissatisfaction.
3. Delayed detection of abnormal trends in sales or stock movement.
4. Inability of non-technical staff to query business data quickly.

Recent advances in LLMs enable structured reasoning over operational business data through prompt engineering. This project leverages these capabilities to build a practical inventory intelligence platform.

## 1.2 Objective

Primary objectives of this project are:

1. To build a complete inventory management web application with role-based access control.
2. To implement core business modules: products, stock, warehouses, purchases, sales, reports, and analytics.
3. To integrate Cerebras-hosted LLaMA 3.1-8B for inventory-focused AI insights.
4. To enable natural-language AI chat constrained to inventory context.
5. To provide actionable recommendations for reordering, pricing, expiry risks, and stockouts.

## 1.3 Problem Definition

### 1.3.1 Purpose

Existing affordable inventory systems lack integrated AI capabilities such as demand forecasting, dead stock identification, and natural-language operational assistance. Businesses require an end-to-end platform that combines daily inventory operations with explainable AI recommendations.

### 1.3.2 Scope

#### In Scope

1. Multi-module inventory operations across product lifecycle.
2. JWT-based authentication and permission-driven authorization.
3. AI insight generation and storage.
4. Dashboard and analytics visualization.
5. Report generation and AI narrative support.

#### Out of Scope (Current Phase)

1. Multi-tenant cloud deployment and Kubernetes orchestration.
2. Advanced external integrations (ERP, accounting gateways).
3. Full automated benchmarking infrastructure.
4. Mobile native application.

### 1.3.3 Contributions

This project contributes:

1. A practical architecture combining traditional inventory services with LLM-driven intelligence.
2. Prompt templates with strict output constraints for structured AI responses.
3. A safety-constrained inventory chat assistant that avoids off-domain responses.
4. A reusable backend module pattern (routes -> services -> repositories -> models).
5. A production-style frontend with role-based navigation and protected routes.

---

# LITERATURE REVIEW

## 2.1 Overview

This chapter reviews foundational and recent work in inventory optimization, machine learning-based forecasting, anomaly detection, conversational enterprise systems, and secure role-based systems.

## 2.2 Review of Existing Research

### 2.2.1 Inventory and Supply Chain Foundations

Silver et al. [1] and Chopra and Meindl [2] provide classical approaches for inventory policies, service levels, and replenishment planning. These methods form baseline logic but do not adapt quickly to changing market behavior.

### 2.2.2 Forecasting Models in Inventory

Hyndman and Athanasopoulos [3] describe statistical forecasting models including ARIMA and ETS. Seyedan and Mafakheri [4] and Punia et al. [5] report improved accuracy from ML/deep learning methods but highlight dependence on historical data volume and feature engineering.

### 2.2.3 Anomaly Detection and Demand Signals

Fahim and Sillitti [6] discuss anomaly detection approaches in operational systems. While effective for numerical outliers, these models often struggle to incorporate context such as promotions, local events, or category-specific behavior.

### 2.2.4 LLMs for Structured Reasoning

Brown et al. [7], Wei et al. [8], and Ouyang et al. [9] establish that LLMs can perform instruction-following and reasoning when prompts are designed with constraints. Recent studies indicate that LLMs can reason over structured/tabular summaries when input is transformed appropriately.

### 2.2.5 Conversational Systems in Enterprise Software

Gnewuch et al. [10] demonstrate productivity benefits of conversational interfaces in enterprise scenarios. However, earlier chatbot systems are usually intent-limited. LLM-based assistants can provide richer contextual interaction if domain boundaries are enforced.

### 2.2.6 Security and Access Control

Ferraiolo et al. [11] describe RBAC principles that are now standard in enterprise software. Permission-based API protection is necessary to prevent unauthorized operational changes.

## 2.3 Research Gap

From reviewed literature and market tools, the following gap is identified:

1. Most inventory systems provide transaction management but limited AI-assisted recommendations.
2. Forecasting models are often separate from operational systems.
3. Conversational interfaces are either absent or not context-grounded to live inventory data.
4. Affordable, open, end-to-end implementations combining operations + AI + role security are limited.

## 2.4 How This Project Addresses the Gap

The proposed system combines:

1. Full inventory operational modules.
2. Integrated AI insight generation using structured prompts.
3. Context-aware AI chat constrained to inventory scope.
4. RBAC-enforced APIs and role-based frontend access.

## 2.5 Literature Summary Table

| Ref | Focus Area | Key Contribution | Limitation | Relevance to Project |
|---|---|---|---|---|
| [1], [2] | Inventory theory | Replenishment and policy foundations | Not AI-native | Business logic baseline |
| [3] | Forecasting | Statistical model framework | Needs stable historical trends | Forecasting benchmark context |
| [4], [5] | ML forecasting | Better accuracy than classical models | Data-intensive and model training heavy | Motivation for LLM-based reasoning |
| [6] | Anomaly detection | Outlier detection patterns | Context limitations | Motivates context-aware AI anomaly insights |
| [7], [8], [9] | LLM reasoning | Strong instruction-following and reasoning | Output control required | Basis for prompt-structured AI outputs |
| [10] | Conversational enterprise UX | Better user productivity | Intent-limited in classic bots | Justifies inventory AI chat |
| [11] | RBAC | Secure permission modeling | Requires strict implementation | Applied to API/route protection |

---

# PROPOSED SYSTEM

## 3.1 Overview

Conventional systems include spreadsheets and standard inventory packages. They provide CRUD and reports but typically lack integrated predictive intelligence and contextual chat support.

### 3.1.1 Disadvantages

1. Static thresholds for reorder alerts.
2. Limited anomaly awareness.
3. No direct natural-language operational interaction.
4. Fragmented analytics and decision support.

## 3.2 Proposed System

The proposed AI-Powered Inventory Management System provides:

1. Centralized inventory operations across modules.
2. Real-time dashboard and analytics.
3. AI-generated insights and narratives.
4. Role-aware secure access for multi-user environments.

### 3.2.1 Advantages

1. Integrated AI for intelligent decision support.
2. Natural-language interaction for operational queries.
3. Real-time insights and recommendations.
4. Secure, role-based access for multi-user environments.
5. Scalable and maintainable architecture.

## 3.3 Architecture Diagram

Figure 1 shows the three-tier architecture.

```text
+-------------------------------+
| Frontend (React + TypeScript) |
| Pages, Components, State, UI  |
+-------------------------------+
			|
			| REST (JSON)
			v
+-------------------------------+
| Backend (FastAPI)             |
| Routes -> Services -> Repos   |
| Auth, Analytics, AI, Reports  |
+-------------------------------+
			|
			| ORM
			v
+-------------------------------+
| SQLite Database               |
| Core business entities        |
+-------------------------------+
			|
			| AI API calls
			v
+-------------------------------+
| Cerebras LLaMA 3.1-8B         |
| Structured prompt reasoning   |
+-------------------------------+
```

## 3.4 Modules

### 3.4.1 User Interface Module

Frontend architecture includes:

1. Route-based page structure.
2. Protected routes with permission checks.
3. Axios service layer for API calls.
4. React Query for server data caching.
5. Zustand for client/global state.
6. Themed UI component system.

### 3.4.2 Authentication Module

JWT-based authentication and permission-driven authorization.

### 3.4.3 Backend API Module

FastAPI routes for all business operations.

### 3.4.4 AI Query Processing Module

AI service for insights and chat.

### 3.4.5 Database Module

SQLAlchemy ORM for persistence.

## 3.3 Feasibility Analysis

### 3.3.1 Technical Feasibility

Technically feasible due to mature stack components: FastAPI, SQLAlchemy, React, and Cerebras SDK. The architecture is modular and maintainable.

### 3.3.2 Economic Feasibility

Open-source framework stack reduces licensing cost. The system can run on modest development hardware and supports incremental deployment.

### 3.3.3 Operational Feasibility

Role-based UI and AI-assisted recommendations improve usability for non-technical users. Existing workflow maps to common inventory operations.

## 3.4 Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | User login with JWT authentication |
| FR-02 | Role and permission based route access |
| FR-03 | Product CRUD with SKU and status handling |
| FR-04 | Category and supplier management |
| FR-05 | Warehouse and stock operations |
| FR-06 | Purchase and sale management |
| FR-07 | Dashboard KPIs and charts |
| FR-08 | AI insight generation and retrieval |
| FR-09 | AI chat with inventory context |
| FR-10 | Alerts retrieval and update |
| FR-11 | Reports and analytics endpoints |
| FR-12 | User management for authorized roles |

## 3.5 Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-01 | Secure password hashing and token handling |
| NFR-02 | Modular, maintainable architecture |
| NFR-03 | Input and schema validation |
| NFR-04 | Responsive frontend experience |
| NFR-05 | Configurable environment-based settings |
| NFR-06 | Graceful fallback for AI/API failures |

## 3.6 User Roles and Permissions

| Role | Typical Access |
|---|---|
| Admin | Full system administration, user and module access |
| Inventory Manager | Product, stock, warehouse, purchases, reports, AI insights |
| Sales Staff | Sales-oriented operations, limited reports, AI view |

## 3.7 Use Case Overview

Primary use cases include:

1. Authenticate user and establish session.
2. Manage products, categories, suppliers.
3. Track stock and warehouse quantities.
4. Record purchases and sales transactions.
5. Monitor dashboard and analytics.
6. Generate AI insights and ask AI chat questions.
7. Review alerts and business reports.

---

# SYSTEM DESIGN AND IMPLEMENTATION

## 5.1 Introduction

Backend is organized into route handlers, service layer, repository layer, model layer, and schemas.

Route modules expose domain APIs for auth, products, categories, suppliers, warehouses, stock, purchases, sales, dashboard, analytics, reports, AI, alerts, and users.

Services implement business logic, aggregation, and AI orchestration. This reduces route complexity and improves testability.

Repositories encapsulate database operations, reducing direct query duplication and improving maintainability.

SQLAlchemy models represent entities and relationships for operational and AI insight data.

Frontend architecture includes route-based page structure, protected routes with permission checks, Axios service layer for API calls, React Query for server data caching, Zustand for client/global state, and themed UI component system.

## 5.2 Admin Module

### 5.2.1 Login Page

Users authenticate using JWT-based login.

### 5.2.2 User Creation

Admins can create and manage user accounts with role assignment.

### 5.2.3 Admin Dashboard

Provides overview of system metrics and administrative controls.

### 5.2.4 Product Creation

Admins can add new products with categories and suppliers.

### 5.2.5 Category Management

CRUD operations for product categories.

### 5.2.6 Supplier Management

Management of supplier information.

### 5.2.7 Warehouse Management

Setup and management of warehouse locations.

## 5.3 User Module

Other roles like Inventory Manager and Sales Staff have access to relevant modules based on permissions.

## 5.4 Backend Module

Implemented using FastAPI with SQLAlchemy ORM and SQLite database.

## 5.5 Sample Code

```python
# Example: Product Model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    # ... other fields
```

## 4.4 Data Flow Design

### 4.4.1 DFD Level 0

```text
User <-> Inventory Web App <-> Database
			   |
			   v
		   Cerebras AI API
```

### 4.4.2 DFD Level 1

```text
1) User Auth Request -> Auth Module -> JWT Token
2) CRUD/Transactions -> Inventory Modules -> Database
3) Analytics/Reports -> Aggregation Services -> Database -> UI
4) AI Request -> AI Service -> Prompt Builder -> Cerebras -> Parsed Response -> DB/UI
```

## 4.5 ER Design (Entity Summary)

Primary entities include User, Product, Category, Supplier, Warehouse, WarehouseStock, Batch, Purchase, PurchaseItem, Sale, SaleItem, Alert, and AIPrediction.

### Key Relationships

1. Category 1:N Product.
2. Supplier 1:N Product and Supplier 1:N Purchase.
3. Product 1:N Batch.
4. Warehouse N:M Product through WarehouseStock.
5. Purchase 1:N PurchaseItem.
6. Sale 1:N SaleItem.

## 4.6 Algorithmic Design

### 4.6.1 Product Status Sync

```text
if stock_qty <= 0 -> out_of_stock
else if stock_qty < min_level -> low_stock
else -> active
```

### 4.6.2 AI Insight Generation

1. Collect product, sales, and batch data.
2. Build task-specific prompts.
3. Call Cerebras completion endpoint.
4. Parse structured JSON output.
5. Persist insights and return typed response.

### 4.6.3 JWT Permission Validation

1. Decode bearer token.
2. Validate signature and expiry.
3. Resolve user and role.
4. Enforce endpoint permission requirement.

---

# Chapter 5: Implementation Details

## 5.1 Technology Stack

### Frontend

1. React 18 with TypeScript.
2. Vite for fast build and development workflow.
3. Tailwind + SCSS for styling.
4. React Router for navigation.
5. TanStack Query for API state.
6. Zustand for auth/UI state.

### Backend

1. FastAPI for REST APIs.
2. SQLAlchemy ORM for persistence.
3. Pydantic for validation.
4. JWT + bcrypt/passlib for authentication.
5. Cerebras Cloud SDK for AI integration.

## 5.2 Backend Module Implementation

| Module | Major Responsibilities |
|---|---|
| Auth | Login, token issue, current user profile |
| Products | CRUD, stock status consistency, filtering |
| Categories | Category operations and grouping |
| Suppliers | Supplier profile and linkage |
| Warehouses | Location-level stock capacity operations |
| Stock | Low stock detection, adjustments, reorder helpers |
| Purchases | Purchase lifecycle and item management |
| Sales | Sales records and profit computations |
| Dashboard | KPI aggregation and charts |
| Analytics | Monthly and category performance summaries |
| Reports | Report datasets and period summaries |
| Alerts | Alert listing and status management |
| Users | User profile and role-aware operations |
| AI | Chat, insights, stockout/reorder/health analysis |

## 5.3 AI Integration Implementation

AI implementation is organized with three core components:

1. `cerebras_client` for model communication and fallback handling.
2. `prompts` for strict instruction templates and output constraints.
3. `ai_service` for context building, orchestration, parsing, and response shaping.

### AI Features Implemented

1. Demand forecasting.
2. Dead stock identification.
3. Anomaly detection.
4. Price optimization suggestions.
5. Expiry risk assessment.
6. Dashboard summary generation.
7. Inventory health score recommendation.
8. Smart reorder suggestions.
9. Stockout prediction.
10. Sales summary narrative.
11. Inventory-constrained chat assistant.

### AI Safety and Reliability Controls

1. Inventory-only scope instructions.
2. Plain-text output constraints for chat summaries.
3. JSON output constraints for structured insight APIs.
4. Parsing fallback for malformed responses.
5. Error handling with meaningful fallback responses.

## 5.4 Frontend Implementation

Frontend includes route-driven pages for all operational modules. Key pages include dashboard, products, stock, purchases, sales, warehouses, categories, suppliers, reports, analytics, AI insights, user management, and settings.

### Frontend Security and Access

1. Protected routes wrap restricted pages.
2. Role-based permission checks control page-level access.
3. API token is attached through client interceptors.

### UX and Component System

1. Unified modern UI components.
2. Responsive layouts for desktop and mobile use.
3. Theme-aware styling and reusable design primitives.

## 5.5 Database Design and Persistence

Database uses SQLAlchemy models with UUID-centric entities and relation mappings. Startup lifecycle creates schema through metadata initialization. The model set supports operational records and AI prediction persistence.

---

# TESTING AND RESULTS

## 6.1 Testing Strategy

Testing was performed through:

1. API endpoint verification via Swagger/OpenAPI interface.
2. Frontend workflow validation against backend responses.
3. Role/permission checks for protected operations.
4. AI endpoint invocation with representative prompts.
5. Seeded data checks for dashboards and reports.

## 6.2 Representative Test Cases

| Test ID | Module | Test Scenario | Expected Result | Status |
|---|---|---|---|---|
| TC-01 | Auth | Valid login with known seeded user | JWT token returned; user profile available | Pass |
| TC-02 | Auth | Access protected endpoint without token | Unauthorized response | Pass |
| TC-03 | Products | Create product with valid payload | Product persisted and listed | Pass |
| TC-04 | Products | Stock falls below minimum | Status transitions to low_stock | Pass |
| TC-05 | Stock | Request low-stock list | Returns products with low_stock status | Pass |
| TC-06 | Purchases | Create purchase with items | Purchase and purchase_items created | Pass |
| TC-07 | Sales | Retrieve sales and totals | Correct response schema and data | Pass |
| TC-08 | Dashboard | Fetch KPI stats | Aggregated metrics returned | Pass |
| TC-09 | Reports | Generate report summary endpoint | Structured report response returned | Pass |
| TC-10 | AI Insights | Generate insights | Insight objects stored and returned | Pass |
| TC-11 | AI Chat | Ask inventory query | Contextual inventory-specific response | Pass |
| TC-12 | RBAC | Insufficient permission access | Forbidden response | Pass |

## 6.3 Observed Results

Observed outcomes from implementation-level validation:

1. Core inventory modules are integrated end-to-end through backend APIs and frontend pages.
2. Dashboard and analytics services return aggregated business metrics from transaction tables.
3. AI module successfully orchestrates multiple insight categories and stores generated predictions.
4. Chat assistant respects inventory-only domain constraints and provides fallback responses if external AI fails.
5. RBAC enforcement is active at route protection and API dependency levels.

## 6.4 Known Limitations

Based on project notes and current implementation phase:

1. Some frontend operations require completion for full parity with backend capabilities.
2. Certain UI workflows need additional integration and hardcoding cleanup.
3. Full performance benchmarking and stress-testing pipelines are yet to be formalized.

## 6.5 Discussion

The system demonstrates that combining standard inventory modules with prompt-structured LLM services provides practical intelligence without building separate ML training pipelines. The architecture is suitable for iterative improvement and production hardening.

---

# CONCLUSION AND FUTURE ENHANCEMENT

## 7.1 Conclusion

This project delivers a complete AI-Powered Inventory Management System with integrated operational modules and AI-assisted decision support. The solution successfully combines FastAPI backend services, React frontend workflows, secure role-based access control, and Cerebras-hosted LLM intelligence.

The implemented platform addresses critical gaps in traditional inventory software by adding forecasting, anomaly interpretation, expiry and stockout awareness, and natural-language assistant capabilities within a single system.

## 7.2 Future Enhancement

Future enhancements include:

1. Complete pending frontend-backend parity for all operational flows.
2. Automated notification and alert orchestration.
3. Extended test automation and CI/CD quality gates.
4. Migration path to PostgreSQL for larger production scale.
5. Advanced forecasting ensembles combining statistical + LLM methods.
6. Audit trails and compliance reporting features.
7. External integrations (ERP/accounting/e-commerce connectors).

---

# References (IEEE Style)

[1] E. A. Silver, D. F. Pyke, and D. J. Thomas, *Inventory and Production Management in Supply Chains*, 4th ed. Boca Raton, FL, USA: CRC Press, 2016.  
[2] S. Chopra and P. Meindl, *Supply Chain Management: Strategy, Planning, and Operation*, 7th ed. New York, NY, USA: Pearson, 2021.  
[3] R. J. Hyndman and G. Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed. Melbourne, Australia: OTexts, 2021.  
[4] M. Seyedan and F. Mafakheri, "Predictive big data analytics for supply chain demand forecasting: methods, applications, and research opportunities," *J. Big Data*, vol. 7, no. 1, 2020.  
[5] S. Punia, S. Shankar, and S. P. Singh, "Demand forecasting using deep learning models: a comparative study," *Ann. Oper. Res.*, vol. 291, pp. 753-762, 2020.  
[6] M. Fahim and A. Sillitti, "Anomaly detection, analysis and prediction techniques in IoT environment: a systematic literature review," *IEEE Access*, vol. 7, pp. 81664-81681, 2019.  
[7] T. Brown et al., "Language models are few-shot learners," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2020.  
[8] J. Wei et al., "Chain-of-thought prompting elicits reasoning in large language models," in *NeurIPS*, 2022.  
[9] L. Ouyang et al., "Training language models to follow instructions with human feedback," in *NeurIPS*, 2022.  
[10] U. Gnewuch, S. Morana, and A. Maedche, "Towards designing cooperative and social conversational agents for customer service," in *Proc. ICIS*, 2017.  
[11] D. F. Ferraiolo, R. Sandhu, S. Gavrila, D. R. Kuhn, and R. Chandramouli, "Proposed NIST standard for role-based access control," *ACM Trans. Inf. Syst. Secur.*, vol. 4, no. 3, pp. 224-274, 2001.  
[12] S. Ramírez, "FastAPI Documentation," 2024. [Online]. Available: https://fastapi.tiangolo.com/  
[13] SQLAlchemy Authors, "SQLAlchemy Documentation," 2024. [Online]. Available: https://docs.sqlalchemy.org/  
[14] Cerebras Systems, "Cerebras Inference Documentation," 2024. [Online]. Available: https://inference-docs.cerebras.ai/  
[15] M. Touvron et al., "LLaMA: Open and efficient foundation language models," arXiv:2302.13971, 2023.  
[16] IHL Group, "Inventory Distortion: A Retail Industry Challenge," White Paper, 2023.  
[17] R. C. Martin, *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Boston, MA, USA: Prentice Hall, 2017.  
[18] M. Fowler, *Patterns of Enterprise Application Architecture*. Boston, MA, USA: Addison-Wesley, 2002.

---

# Appendices

## Appendix A: Major API Groups

1. `/api/auth` - authentication and profile.
2. `/api/products`, `/api/categories`, `/api/suppliers` - master data.
3. `/api/warehouses`, `/api/stock` - location and stock operations.
4. `/api/purchases`, `/api/sales` - transactions.
5. `/api/dashboard`, `/api/analytics`, `/api/reports` - analysis and reporting.
6. `/api/ai` - chat, insights, health score, stockout, summaries.
7. `/api/alerts`, `/api/users` - alerts and user administration.

## Appendix B: Sample AI Prompt Types

1. Demand forecasting prompt with JSON output schema.
2. Dead stock prompt with discount recommendation fields.
3. Anomaly prompt for spike/drop/trend classification.
4. Price optimization prompt with suggested price and reasoning.
5. Expiry risk prompt with batch-level action recommendation.

## Appendix C: User Manual (Quick Start)

1. Start backend and frontend services.
2. Login using seeded role credentials.
3. Navigate to dashboard, product, stock, purchase, and sales modules.
4. Open AI insights to generate recommendations.
5. Use AI chat for inventory-specific questions.
6. Access reports and analytics for business summary.

---

## Notes for Final Submission Formatting

1. Replace placeholders in title page, certificate, and declaration.
2. Add institution-specific formatting (font, spacing, margins) as per official template.
3. Insert screenshots and finalized diagrams where figure placeholders are given.
4. Update page numbers and preliminary-page numbering based on department format.
5. Ensure plagiarism check and final reference validation before print submission.
