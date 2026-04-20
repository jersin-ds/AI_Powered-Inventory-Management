"""
Database Seeder — Populates SQLite with rich, realistic initial data.

Usage:
    cd backend
    python -m inventory_backend.seed

This script is idempotent — it skips seeding if data already exists.
Safe to run on any machine, even after transferring the project.
"""

from __future__ import annotations

import sys
import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Ensure the backend directory is on the Python path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inventory_backend.app.database import engine, SessionLocal, Base
from inventory_backend.app.models import (
    User, Category, Supplier, Product,
    Warehouse, WarehouseStock, Batch,
    Purchase, PurchaseItem, Sale, SaleItem,
    Alert, AIPrediction,
)
from inventory_backend.app.auth.security import hash_password


def parse_date(date_str: str) -> datetime:
    """Parse a date string into a timezone-aware datetime."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            return datetime.now(timezone.utc)


def seed():
    """Seed the database with rich realistic data."""
    print("=" * 60)
    print("  AI Inventory Management — Database Seeder")
    print("=" * 60)

    # Create all tables
    print("\n[1/11] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("  ✓ Tables created")

    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).count() > 0:
            print("\n⚠️  Database already seeded (users exist). Skipping.")
            print("   To re-seed, delete inventory.db and run again.")
            return

        # ── USERS ──
        print("\n[2/11] Seeding users...")
        default_password = hash_password("password123")

        users = [
            User(id="1", name="Admin User", email="admin@inventory.com", password_hash=default_password, role="admin", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=admin", status="active", last_login=parse_date("2024-02-25T10:30:00Z"), created_at=parse_date("2022-01-01")),
            User(id="2", name="John Manager", email="manager@inventory.com", password_hash=default_password, role="inventory_manager", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=manager1", status="active", last_login=parse_date("2024-02-25T09:15:00Z"), created_at=parse_date("2022-03-15")),
            User(id="3", name="Sarah Sales", email="sales@inventory.com", password_hash=default_password, role="sales_staff", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=sales1", status="active", last_login=parse_date("2024-02-25T08:45:00Z"), created_at=parse_date("2022-05-20")),
            User(id="4", name="Emily Manager", email="emily.manager@inventory.com", password_hash=default_password, role="inventory_manager", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=manager2", status="active", last_login=parse_date("2024-02-24T16:30:00Z"), created_at=parse_date("2022-06-10")),
            User(id="5", name="Mike Sales", email="mike.sales@inventory.com", password_hash=default_password, role="sales_staff", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=sales2", status="active", last_login=parse_date("2024-02-24T14:20:00Z"), created_at=parse_date("2022-08-05")),
            User(id="6", name="Jessica Staff", email="jessica@inventory.com", password_hash=default_password, role="sales_staff", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=sales3", status="inactive", last_login=parse_date("2024-02-15T11:00:00Z"), created_at=parse_date("2023-01-12")),
            User(id="7", name="Robert Chen", email="robert@inventory.com", password_hash=default_password, role="inventory_manager", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=manager3", status="active", last_login=parse_date("2024-02-23T12:00:00Z"), created_at=parse_date("2023-02-01")),
            User(id="8", name="Lisa Wang", email="lisa@inventory.com", password_hash=default_password, role="sales_staff", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=sales4", status="active", last_login=parse_date("2024-02-22T09:30:00Z"), created_at=parse_date("2023-04-15")),
        ]
        db.add_all(users)
        db.flush()
        print(f"  ✓ {len(users)} users seeded (password: password123)")

        # ── CATEGORIES ──
        print("\n[3/11] Seeding categories...")
        categories = [
            Category(id="1", name="Electronics", description="Electronic devices, peripherals and accessories", product_count=0, subcategories=json.dumps(["Computer Accessories", "Cables", "Audio Equipment", "Mobile Accessories", "Networking"]), status="active", created_at=parse_date("2023-01-15")),
            Category(id="2", name="Furniture", description="Office and ergonomic furniture items", product_count=0, subcategories=json.dumps(["Desk Accessories", "Chairs", "Storage", "Tables", "Standing Desks"]), status="active", created_at=parse_date("2023-02-20")),
            Category(id="3", name="Office Supplies", description="General office supplies and stationery", product_count=0, subcategories=json.dumps(["Writing Tools", "Paper Products", "Organization", "Printing Supplies", "Labels"]), status="active", created_at=parse_date("2023-03-10")),
            Category(id="4", name="Software & Licenses", description="Software subscriptions and license keys", product_count=0, subcategories=json.dumps(["Productivity", "Security", "Design", "Development"]), status="active", created_at=parse_date("2023-04-05")),
            Category(id="5", name="Cleaning & Maintenance", description="Cleaning supplies and maintenance tools", product_count=0, subcategories=json.dumps(["Cleaning Kits", "Tools", "Safety Equipment"]), status="active", created_at=parse_date("2023-05-01")),
        ]
        db.add_all(categories)
        db.flush()
        print(f"  ✓ {len(categories)} categories seeded")

        # ── SUPPLIERS ──
        print("\n[4/11] Seeding suppliers...")
        suppliers = [
            Supplier(id="1", name="TechCorp Inc", contact_person="John Smith", email="john.smith@techcorp.com", phone="+91 98765 43210", address="123 Tech Park", city="Bangalore", country="India", products_supplied=245, total_orders=89, total_value=37912740, rating=4.8, status="active", payment_terms="Net 30", created_at=parse_date("2022-06-15")),
            Supplier(id="2", name="CableCo", contact_person="Sarah Johnson", email="sarah@cableco.com", phone="+91 98765 43211", address="456 Cable Avenue", city="Mumbai", country="India", products_supplied=120, total_orders=45, total_value=10246350, rating=4.5, status="active", payment_terms="Net 45", created_at=parse_date("2022-08-20")),
            Supplier(id="3", name="KeyMasters", contact_person="Michael Chen", email="michael@keymasters.com", phone="+91 98765 43212", address="789 Keyboard Lane", city="Delhi", country="India", products_supplied=87, total_orders=34, total_value=23895700, rating=4.9, status="active", payment_terms="Net 30", created_at=parse_date("2022-09-10")),
            Supplier(id="4", name="ErgoSupply", contact_person="Emily Davis", email="emily@ergosupply.com", phone="+91 98765 43213", address="321 Ergo Road", city="Hyderabad", country="India", products_supplied=156, total_orders=67, total_value=28690610, rating=4.7, status="active", payment_terms="Net 30", created_at=parse_date("2022-10-05")),
            Supplier(id="5", name="Global Tech Supplies", contact_person="David Brown", email="david@globaltech.com", phone="+91 98765 43214", address="654 Global Plaza", city="Chennai", country="India", products_supplied=312, total_orders=102, total_value=56350360, rating=4.6, status="active", payment_terms="Net 60", created_at=parse_date("2022-07-12")),
            Supplier(id="6", name="OfficePro Distributors", contact_person="Angela Wu", email="angela@officepro.com", phone="+91 98765 43215", address="22 Office Drive", city="Pune", country="India", products_supplied=198, total_orders=73, total_value=19463500, rating=4.3, status="active", payment_terms="Net 30", created_at=parse_date("2023-01-20")),
            Supplier(id="7", name="FurniWorld", contact_person="Mark Taylor", email="mark@furniworld.com", phone="+91 98765 43216", address="88 Furniture Blvd", city="Kolkata", country="India", products_supplied=95, total_orders=41, total_value=15711900, rating=4.4, status="active", payment_terms="Net 45", created_at=parse_date("2023-03-05")),
            Supplier(id="8", name="CleanTech Solutions", contact_person="Nina Patel", email="nina@cleantech.com", phone="+91 98765 43217", address="12 Green Street", city="Ahmedabad", country="India", products_supplied=68, total_orders=28, total_value=6341200, rating=4.1, status="active", payment_terms="Net 30", created_at=parse_date("2023-04-18")),
        ]
        db.add_all(suppliers)
        db.flush()
        print(f"  ✓ {len(suppliers)} suppliers seeded")

        # ── PRODUCTS ──
        print("\n[5/11] Seeding products...")
        products = [
            # Electronics (cat 1)
            Product(id="1", sku="ELC-001", name="Wireless Mouse", category_id="1", subcategory="Computer Accessories", supplier_id="1", cost_price=1245, sell_price=2075, stock_qty=150, min_level=20, barcode="1234567890001", status="active", created_at=parse_date("2024-01-15")),
            Product(id="2", sku="ELC-002", name="USB-C Cable 2m", category_id="1", subcategory="Cables", supplier_id="2", cost_price=415, sell_price=996, stock_qty=15, min_level=30, barcode="1234567890002", status="low_stock", created_at=parse_date("2024-01-16")),
            Product(id="3", sku="ELC-003", name="Mechanical Keyboard", category_id="1", subcategory="Computer Accessories", supplier_id="3", cost_price=4150, sell_price=7055, stock_qty=0, min_level=10, barcode="1234567890003", status="out_of_stock", created_at=parse_date("2024-01-17")),
            Product(id="5", sku="ELC-005", name="Webcam HD 1080p", category_id="1", subcategory="Computer Accessories", supplier_id="1", cost_price=2905, sell_price=4980, stock_qty=45, min_level=10, barcode="1234567890005", status="active", created_at=parse_date("2024-01-19")),
            Product(id="6", sku="ELC-006", name="Bluetooth Speaker", category_id="1", subcategory="Audio Equipment", supplier_id="5", cost_price=1826, sell_price=3735, stock_qty=80, min_level=15, barcode="1234567890006", status="active", created_at=parse_date("2024-01-20")),
            Product(id="7", sku="ELC-007", name="HDMI Cable 3m", category_id="1", subcategory="Cables", supplier_id="2", cost_price=664, sell_price=1494, stock_qty=200, min_level=40, barcode="1234567890007", status="active", created_at=parse_date("2024-01-21")),
            Product(id="8", sku="ELC-008", name="Wireless Earbuds", category_id="1", subcategory="Audio Equipment", supplier_id="1", cost_price=2324, sell_price=4565, stock_qty=60, min_level=12, barcode="1234567890008", status="active", created_at=parse_date("2024-01-22")),
            Product(id="9", sku="ELC-009", name="USB Hub 7-Port", category_id="1", subcategory="Computer Accessories", supplier_id="5", cost_price=1494, sell_price=2656, stock_qty=5, min_level=15, barcode="1234567890009", status="low_stock", created_at=parse_date("2024-01-23")),
            Product(id="10", sku="ELC-010", name="Phone Charger 65W", category_id="1", subcategory="Mobile Accessories", supplier_id="1", cost_price=996, sell_price=2324, stock_qty=120, min_level=25, barcode="1234567890010", status="active", created_at=parse_date("2024-01-24")),
            Product(id="11", sku="ELC-011", name="WiFi Router AC1200", category_id="1", subcategory="Networking", supplier_id="5", cost_price=3320, sell_price=5976, stock_qty=30, min_level=8, barcode="1234567890011", status="active", created_at=parse_date("2024-01-25")),

            # Furniture (cat 2)
            Product(id="4", sku="FRN-001", name="Laptop Stand", category_id="2", subcategory="Desk Accessories", supplier_id="4", cost_price=1660, sell_price=2905, stock_qty=75, min_level=15, barcode="1234567890004", status="active", created_at=parse_date("2024-01-18")),
            Product(id="12", sku="FRN-002", name="Ergonomic Office Chair", category_id="2", subcategory="Chairs", supplier_id="7", cost_price=14940, sell_price=28967, stock_qty=18, min_level=5, barcode="1234567890012", status="active", created_at=parse_date("2024-01-26")),
            Product(id="13", sku="FRN-003", name="Standing Desk Converter", category_id="2", subcategory="Standing Desks", supplier_id="4", cost_price=9960, sell_price=19007, stock_qty=12, min_level=4, barcode="1234567890013", status="active", created_at=parse_date("2024-01-27")),
            Product(id="14", sku="FRN-004", name="Monitor Arm Dual", category_id="2", subcategory="Desk Accessories", supplier_id="4", cost_price=3735, sell_price=7387, stock_qty=25, min_level=6, barcode="1234567890014", status="active", created_at=parse_date("2024-01-28")),
            Product(id="15", sku="FRN-005", name="Filing Cabinet 3-Drawer", category_id="2", subcategory="Storage", supplier_id="7", cost_price=5395, sell_price=9877, stock_qty=0, min_level=3, barcode="1234567890015", status="out_of_stock", created_at=parse_date("2024-01-29")),

            # Office Supplies (cat 3)
            Product(id="16", sku="OFS-001", name="A4 Copy Paper (5 Reams)", category_id="3", subcategory="Paper Products", supplier_id="6", cost_price=1494, sell_price=2656, stock_qty=300, min_level=50, barcode="1234567890016", status="active", created_at=parse_date("2024-01-30")),
            Product(id="17", sku="OFS-002", name="Ballpoint Pens (Box 50)", category_id="3", subcategory="Writing Tools", supplier_id="6", cost_price=664, sell_price=1245, stock_qty=150, min_level=30, barcode="1234567890017", status="active", created_at=parse_date("2024-02-01")),
            Product(id="18", sku="OFS-003", name="Sticky Notes Assorted", category_id="3", subcategory="Organization", supplier_id="6", cost_price=332, sell_price=747, stock_qty=220, min_level=40, barcode="1234567890018", status="active", created_at=parse_date("2024-02-02")),
            Product(id="19", sku="OFS-004", name="Printer Toner Cartridge", category_id="3", subcategory="Printing Supplies", supplier_id="6", cost_price=2905, sell_price=5395, stock_qty=8, min_level=10, barcode="1234567890019", status="low_stock", created_at=parse_date("2024-02-03")),
            Product(id="20", sku="OFS-005", name="Desk Organizer Set", category_id="3", subcategory="Organization", supplier_id="6", cost_price=996, sell_price=1992, stock_qty=45, min_level=10, barcode="1234567890020", status="active", created_at=parse_date("2024-02-04")),
            Product(id="21", sku="OFS-006", name="Shipping Labels (Roll 500)", category_id="3", subcategory="Labels", supplier_id="6", cost_price=1245, sell_price=2407, stock_qty=60, min_level=15, barcode="1234567890021", status="active", created_at=parse_date("2024-02-05")),

            # Software & Licenses (cat 4)
            Product(id="22", sku="SFT-001", name="Antivirus License (1yr)", category_id="4", subcategory="Security", supplier_id="5", cost_price=2075, sell_price=4067, stock_qty=100, min_level=20, barcode="1234567890022", status="active", created_at=parse_date("2024-02-06")),
            Product(id="23", sku="SFT-002", name="Office Suite License", category_id="4", subcategory="Productivity", supplier_id="5", cost_price=6640, sell_price=12367, stock_qty=50, min_level=10, barcode="1234567890023", status="active", created_at=parse_date("2024-02-07")),

            # Cleaning & Maintenance (cat 5)
            Product(id="24", sku="CLN-001", name="Screen Cleaning Kit", category_id="5", subcategory="Cleaning Kits", supplier_id="8", cost_price=498, sell_price=1162, stock_qty=90, min_level=20, barcode="1234567890024", status="active", created_at=parse_date("2024-02-08")),
            Product(id="25", sku="CLN-002", name="Compressed Air Duster (6pk)", category_id="5", subcategory="Cleaning Kits", supplier_id="8", cost_price=830, sell_price=1826, stock_qty=70, min_level=15, barcode="1234567890025", status="active", created_at=parse_date("2024-02-09")),
        ]
        db.add_all(products)
        db.flush()

        # Update category product counts
        for cat in categories:
            cat.product_count = db.query(Product).filter(Product.category_id == cat.id).count()
        db.flush()

        print(f"  ✓ {len(products)} products seeded")

        # ── WAREHOUSES ──
        print("\n[6/11] Seeding warehouses...")
        warehouses = [
            Warehouse(id="1", name="Main Warehouse", location="New York, NY", capacity=10000, current_stock=7500, manager="John Doe", status="active"),
            Warehouse(id="2", name="West Coast Hub", location="Los Angeles, CA", capacity=8000, current_stock=4200, manager="Jane Smith", status="active"),
            Warehouse(id="3", name="Southern Distribution", location="Houston, TX", capacity=6000, current_stock=3100, manager="Mike Johnson", status="active"),
            Warehouse(id="4", name="Midwest Center", location="Chicago, IL", capacity=7000, current_stock=2800, manager="Laura Garcia", status="active"),
        ]
        db.add_all(warehouses)
        db.flush()

        # Warehouse stock entries
        wh_stocks = []
        for prod in products:
            wh = random.choice(warehouses)
            qty = max(0, prod.stock_qty // 2)
            if qty > 0:
                wh_stocks.append(WarehouseStock(warehouse_id=wh.id, product_id=prod.id, quantity=qty))
        db.add_all(wh_stocks)
        db.flush()
        print(f"  ✓ {len(warehouses)} warehouses + {len(wh_stocks)} stock entries seeded")

        # ── PURCHASES ──
        print("\n[7/11] Seeding purchases...")
        now = datetime.now(timezone.utc)
        def _rel(days_ago: int) -> str:
            """Return ISO date string relative to today."""
            return (now - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        purchases_data = [
            ("PO-2024-001", "1", "TechCorp Inc",      _rel(150), "received", [("1", "Wireless Mouse", 200, 1245), ("5", "Webcam HD 1080p", 80, 2905)]),
            ("PO-2024-002", "2", "CableCo",            _rel(130), "received", [("2", "USB-C Cable 2m", 300, 415), ("7", "HDMI Cable 3m", 250, 664)]),
            ("PO-2024-003", "3", "KeyMasters",         _rel(110), "received", [("3", "Mechanical Keyboard", 60, 4150)]),
            ("PO-2024-004", "4", "ErgoSupply",         _rel(90), "received", [("4", "Laptop Stand", 100, 1660), ("14", "Monitor Arm Dual", 40, 3735)]),
            ("PO-2024-005", "5", "Global Tech Supplies",_rel(70), "received", [("6", "Bluetooth Speaker", 100, 1826), ("11", "WiFi Router AC1200", 40, 3320)]),
            ("PO-2024-006", "6", "OfficePro Distributors",_rel(55), "received", [("16", "A4 Copy Paper (5 Reams)", 400, 1494), ("17", "Ballpoint Pens (Box 50)", 200, 664), ("18", "Sticky Notes Assorted", 300, 332)]),
            ("PO-2024-007", "7", "FurniWorld",         _rel(45), "received", [("12", "Ergonomic Office Chair", 25, 14940), ("13", "Standing Desk Converter", 15, 9960)]),
            ("PO-2024-008", "1", "TechCorp Inc",       _rel(28), "received", [("8", "Wireless Earbuds", 80, 2324), ("10", "Phone Charger 65W", 150, 996)]),
            ("PO-2024-009", "8", "CleanTech Solutions", _rel(22), "received", [("24", "Screen Cleaning Kit", 100, 498), ("25", "Compressed Air Duster (6pk)", 80, 830)]),
            ("PO-2024-010", "5", "Global Tech Supplies",_rel(15), "received", [("22", "Antivirus License (1yr)", 120, 2075), ("23", "Office Suite License", 60, 6640)]),
            ("PO-2024-011", "6", "OfficePro Distributors",_rel(7), "pending", [("19", "Printer Toner Cartridge", 30, 2905), ("21", "Shipping Labels (Roll 500)", 80, 1245)]),
            ("PO-2024-012", "4", "ErgoSupply",         _rel(3), "pending",  [("15", "Filing Cabinet 3-Drawer", 10, 5395)]),
        ]
        purchase_objs = []
        for i, (po, sup_id, sup_name, date_str, status, items) in enumerate(purchases_data, 1):
            total = sum(q * p for _, _, q, p in items)
            pur = Purchase(id=str(i), po_number=po, supplier_id=sup_id, supplier_name=sup_name, date=parse_date(date_str), status=status, total_amount=total, created_by=random.choice(["1", "2", "4"]))
            pur.items = [PurchaseItem(product_id=pid, product_name=pname, quantity=qty, price=price) for pid, pname, qty, price in items]
            purchase_objs.append(pur)
        db.add_all(purchase_objs)
        db.flush()
        print(f"  ✓ {len(purchase_objs)} purchases seeded")

        # ── SALES ──
        print("\n[8/11] Seeding sales...")
        customers = ["Acme Corp", "Tech Solutions Ltd", "StartupXYZ", "Global Media Inc", "Pioneer Systems",
                      "Blue Ocean Ventures", "DataDriven Co", "NextGen Labs", "CloudPeak Inc", "Alpha Analytics",
                      "Metro Office Group", "Pinnacle Consulting", "Summit Enterprises", "Vertex Solutions", "Cascade Digital"]

        sales_data = [
            # ~5 months ago
            ("INV-2023-001", "Acme Corp",          _rel(145), "completed", [("1", "Wireless Mouse", 30, 2075), ("7", "HDMI Cable 3m", 20, 1494)]),
            ("INV-2023-002", "Tech Solutions Ltd",  _rel(138), "completed", [("5", "Webcam HD 1080p", 15, 4980)]),
            # ~4 months ago
            ("INV-2023-003", "Pioneer Systems",     _rel(120), "completed", [("6", "Bluetooth Speaker", 12, 3735), ("1", "Wireless Mouse", 25, 2075)]),
            ("INV-2023-004", "Global Media Inc",    _rel(108), "completed", [("4", "Laptop Stand", 20, 2905), ("14", "Monitor Arm Dual", 8, 7387)]),
            ("INV-2023-005", "Blue Ocean Ventures", _rel(97), "completed", [("2", "USB-C Cable 2m", 50, 996), ("7", "HDMI Cable 3m", 30, 1494)]),
            # ~3 months ago
            ("INV-2023-006", "NextGen Labs",        _rel(85), "completed", [("3", "Mechanical Keyboard", 10, 7055), ("8", "Wireless Earbuds", 15, 4565)]),
            ("INV-2023-007", "DataDriven Co",       _rel(78), "completed", [("11", "WiFi Router AC1200", 6, 5976), ("9", "USB Hub 7-Port", 10, 2656)]),
            ("INV-2023-008", "Acme Corp",           _rel(65), "completed", [("12", "Ergonomic Office Chair", 5, 28967)]),
            # ~2 months ago
            ("INV-2023-009", "CloudPeak Inc",       _rel(58), "completed", [("22", "Antivirus License (1yr)", 30, 4067), ("23", "Office Suite License", 15, 12367)]),
            ("INV-2023-010", "Metro Office Group",  _rel(50), "completed", [("16", "A4 Copy Paper (5 Reams)", 40, 2656), ("17", "Ballpoint Pens (Box 50)", 25, 1245), ("18", "Sticky Notes Assorted", 30, 747)]),
            ("INV-2023-011", "Alpha Analytics",     _rel(42), "completed", [("13", "Standing Desk Converter", 3, 19007), ("4", "Laptop Stand", 10, 2905)]),
            # ~1 month ago
            ("INV-2024-001", "Pinnacle Consulting", _rel(28), "completed", [("1", "Wireless Mouse", 40, 2075), ("10", "Phone Charger 65W", 20, 2324)]),
            ("INV-2024-002", "Summit Enterprises",  _rel(24), "completed", [("5", "Webcam HD 1080p", 25, 4980), ("8", "Wireless Earbuds", 20, 4565)]),
            ("INV-2024-003", "Cascade Digital",     _rel(20), "completed", [("6", "Bluetooth Speaker", 18, 3735), ("24", "Screen Cleaning Kit", 15, 1162)]),
            ("INV-2024-004", "Tech Solutions Ltd",  _rel(16), "completed", [("12", "Ergonomic Office Chair", 4, 28967), ("14", "Monitor Arm Dual", 6, 7387)]),
            # Recent (within last 2 weeks)
            ("INV-2024-005", "Acme Corp",           _rel(13), "completed", [("1", "Wireless Mouse", 50, 2075), ("2", "USB-C Cable 2m", 40, 996)]),
            ("INV-2024-006", "Global Media Inc",    _rel(11), "completed", [("22", "Antivirus License (1yr)", 25, 4067), ("23", "Office Suite License", 10, 12367)]),
            ("INV-2024-007", "Pioneer Systems",     _rel(9), "completed", [("3", "Mechanical Keyboard", 8, 7055), ("9", "USB Hub 7-Port", 12, 2656)]),
            ("INV-2024-008", "StartupXYZ",          _rel(7), "completed", [("16", "A4 Copy Paper (5 Reams)", 60, 2656), ("19", "Printer Toner Cartridge", 8, 5395)]),
            ("INV-2024-009", "NextGen Labs",        _rel(5), "completed", [("11", "WiFi Router AC1200", 10, 5976), ("25", "Compressed Air Duster (6pk)", 15, 1826)]),
            ("INV-2024-010", "Blue Ocean Ventures", _rel(4), "completed", [("5", "Webcam HD 1080p", 30, 4980), ("10", "Phone Charger 65W", 25, 2324)]),
            ("INV-2024-011", "DataDriven Co",       _rel(3), "completed", [("4", "Laptop Stand", 15, 2905), ("20", "Desk Organizer Set", 10, 1992)]),
            ("INV-2024-012", "Alpha Analytics",     _rel(2), "pending",   [("13", "Standing Desk Converter", 2, 19007), ("14", "Monitor Arm Dual", 5, 7387)]),
            ("INV-2024-013", "CloudPeak Inc",       _rel(1), "pending",   [("8", "Wireless Earbuds", 20, 4565), ("6", "Bluetooth Speaker", 10, 3735)]),
        ]

        # Product cost lookup for profit calculation
        cost_map = {p.id: p.cost_price for p in products}

        sale_objs = []
        for i, (inv, customer, date_str, status, items) in enumerate(sales_data, 1):
            total = sum(q * p for _, _, q, p in items)
            profit = sum((p - cost_map.get(pid, p * 0.6)) * q for pid, _, q, p in items)
            s = Sale(id=str(i), invoice_number=inv, customer=customer, date=parse_date(date_str), status=status, total_amount=total, profit=round(profit, 2), created_by=random.choice(["3", "5", "8"]))
            s.items = [SaleItem(product_id=pid, product_name=pname, quantity=qty, price=price) for pid, pname, qty, price in items]
            sale_objs.append(s)
        db.add_all(sale_objs)
        db.flush()
        print(f"  ✓ {len(sale_objs)} sales seeded")

        # ── BATCHES ──
        print("\n[9/11] Seeding batches...")
        today = datetime.now(timezone.utc).date()
        batches = [
            Batch(product_id="3",  batch_number="B2024-001", quantity=25,  expiry_date=today + timedelta(days=30)),
            Batch(product_id="19", batch_number="B2024-002", quantity=8,   expiry_date=today + timedelta(days=15)),
            Batch(product_id="24", batch_number="B2024-003", quantity=40,  expiry_date=today + timedelta(days=90)),
            Batch(product_id="25", batch_number="B2024-004", quantity=35,  expiry_date=today + timedelta(days=120)),
            Batch(product_id="17", batch_number="B2024-005", quantity=100, expiry_date=today + timedelta(days=365)),
            Batch(product_id="18", batch_number="B2024-006", quantity=80,  expiry_date=today + timedelta(days=300)),
            Batch(product_id="1",  batch_number="B2024-007", quantity=150, expiry_date=None),
            Batch(product_id="6",  batch_number="B2024-008", quantity=80,  expiry_date=None),
        ]
        db.add_all(batches)
        db.flush()
        print(f"  ✓ {len(batches)} batches seeded")

        # ── AI PREDICTIONS ──
        print("\n[10/11] Seeding AI predictions/insights...")
        predictions = [
            AIPrediction(id="1",  type="demand_forecast", title="High Demand Expected for Wireless Mouse", description="AI predicts 40% increase in demand for Wireless Mouse over the next 2 weeks based on seasonal trend and recent order velocity. Recommend ordering 200 additional units.", priority="high", actionable=True, data=json.dumps({"productId": "1", "predictedDemand": 280, "currentStock": 150, "recommendedOrder": 200}), created_at=parse_date("2024-02-23")),
            AIPrediction(id="2",  type="demand_forecast", title="Webcam HD Demand Surge Expected", description="Remote work trends indicate 25% increase in Webcam HD demand. Current stock may run low within 10 days.", priority="high", actionable=True, data=json.dumps({"productId": "5", "predictedDemand": 65, "currentStock": 45, "recommendedOrder": 50}), created_at=parse_date("2024-02-22")),
            AIPrediction(id="3",  type="dead_stock", title="Slow-Moving: USB-C Cable 2m", description="USB-C Cable has been moving slowly. Only 5 units sold in the last 30 days vs. 15-unit average. Consider 15% discount promotion.", priority="medium", actionable=True, data=json.dumps({"productId": "2", "averageMonthlySales": 5, "currentStock": 15, "suggestedDiscount": 15}), created_at=parse_date("2024-02-22")),
            AIPrediction(id="4",  type="dead_stock", title="Filing Cabinet Overstocked", description="Filing Cabinet 3-Drawer shows zero sales in 45 days. Consider bundling with standing desk offers or 20% markdown.", priority="medium", actionable=True, data=json.dumps({"productId": "15", "averageMonthlySales": 0, "currentStock": 0, "suggestedDiscount": 20}), created_at=parse_date("2024-02-21")),
            AIPrediction(id="5",  type="anomaly", title="Unusual Spike in Webcam Sales", description="Detected a 300% spike in Webcam HD sales compared to monthly average. This correlates with new remote work policies announced by enterprise clients.", priority="high", actionable=True, data=json.dumps({"productId": "5", "normalAverage": 15, "currentSales": 60, "percentageChange": 300}), created_at=parse_date("2024-02-21")),
            AIPrediction(id="6",  type="anomaly", title="Bluetooth Speaker Sales Drop", description="Bluetooth Speaker sales dropped 40% month-over-month. Market saturation or seasonal pattern possible.", priority="medium", actionable=True, data=json.dumps({"productId": "6", "normalAverage": 18, "currentSales": 10, "percentageChange": -44}), created_at=parse_date("2024-02-20")),
            AIPrediction(id="7",  type="price_optimization", title="Laptop Stand Can Support Price Increase", description="Market analysis and competitor pricing suggests Laptop Stand can support a 12% price increase to \u20b93,253 without affecting demand.", priority="low", actionable=True, data=json.dumps({"productId": "4", "currentPrice": 2905, "suggestedPrice": 3253, "expectedRevenue": 124500}), created_at=parse_date("2024-02-20")),
            AIPrediction(id="8",  type="price_optimization", title="Ergonomic Office Chair Pricing Opportunity", description="Competitor average price is \u20b932,287. Current price of \u20b928,967 leaves room for 8% increase while remaining competitive.", priority="low", actionable=True, data=json.dumps({"productId": "12", "currentPrice": 28967, "suggestedPrice": 31457, "expectedRevenue": 282200}), created_at=parse_date("2024-02-19")),
            AIPrediction(id="9",  type="expiry_risk", title="Printer Toner Nearing Expiry", description="Batch B2024-002 of Printer Toner Cartridge expires in 15 days. 8 units at risk — consider flash sale or internal allocation.", priority="high", actionable=True, data=json.dumps({"productId": "19", "batchNumber": "B2024-002", "expiryDate": str(today + timedelta(days=15)), "unitsAtRisk": 8}), created_at=parse_date("2024-02-23")),
            AIPrediction(id="10", type="expiry_risk", title="Mechanical Keyboard Batch Expiring Soon", description="Batch B2024-001 (25 units) expires in 30 days. Move to clearance pricing or redistribute to high-traffic warehouse.", priority="medium", actionable=True, data=json.dumps({"productId": "3", "batchNumber": "B2024-001", "expiryDate": str(today + timedelta(days=30)), "unitsAtRisk": 25}), created_at=parse_date("2024-02-23")),
        ]
        db.add_all(predictions)
        db.flush()
        print(f"  ✓ {len(predictions)} AI predictions seeded")

        # ── ALERTS ──
        print("\n[11/11] Seeding alerts...")
        alerts = [
            Alert(type="low_stock", title="USB-C Cable 2m Low Stock", message="USB-C Cable 2m stock is below minimum level (15 < 30)", priority="high", created_at=parse_date("2024-02-20")),
            Alert(type="out_of_stock", title="Mechanical Keyboard Out of Stock", message="Mechanical Keyboard is out of stock — 0 units remaining", priority="critical", created_at=parse_date("2024-02-19")),
            Alert(type="low_stock", title="USB Hub 7-Port Critically Low", message="USB Hub 7-Port stock critically low (5 < 15)", priority="high", created_at=parse_date("2024-02-22")),
            Alert(type="out_of_stock", title="Filing Cabinet Out of Stock", message="Filing Cabinet 3-Drawer is out of stock — reorder needed", priority="critical", created_at=parse_date("2024-02-21")),
            Alert(type="low_stock", title="Printer Toner Below Minimum", message="Printer Toner Cartridge below minimum (8 < 10)", priority="medium", created_at=parse_date("2024-02-23")),
            Alert(type="expiry", title="Toner Batch Expiring Soon", message="Printer Toner batch B2024-002 expires in 15 days", priority="high", created_at=parse_date("2024-02-23")),
        ]
        db.add_all(alerts)

        # Commit everything
        db.commit()

        # ── Summary ──
        print("\n" + "=" * 60)
        print("  ✅ Database seeded successfully!")
        print("=" * 60)
        print(f"\n  Users:           {db.query(User).count()}")
        print(f"  Categories:      {db.query(Category).count()}")
        print(f"  Suppliers:       {db.query(Supplier).count()}")
        print(f"  Products:        {db.query(Product).count()}")
        print(f"  Warehouses:      {db.query(Warehouse).count()}")
        print(f"  Warehouse Stock: {db.query(WarehouseStock).count()}")
        print(f"  Purchases:       {db.query(Purchase).count()}")
        print(f"  Purchase Items:  {db.query(PurchaseItem).count()}")
        print(f"  Sales:           {db.query(Sale).count()}")
        print(f"  Sale Items:      {db.query(SaleItem).count()}")
        print(f"  Batches:         {db.query(Batch).count()}")
        print(f"  AI Predictions:  {db.query(AIPrediction).count()}")
        print(f"  Alerts:          {db.query(Alert).count()}")
        print()
        print("  Demo accounts (all use password: password123):")
        print("    admin@inventory.com         → Admin (full access)")
        print("    manager@inventory.com       → Inventory Manager")
        print("    sales@inventory.com         → Sales Staff")
        print("    emily.manager@inventory.com → Inventory Manager")
        print("    mike.sales@inventory.com    → Sales Staff")
        print("    robert@inventory.com        → Inventory Manager")
        print("    lisa@inventory.com          → Sales Staff")
        print("    jessica@inventory.com       → Sales Staff (inactive)")
        print()

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
