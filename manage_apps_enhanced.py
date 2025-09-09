"""
Ultra-Enhanced App Management System for Game & App Store
Advanced features including analytics, AI recommendations, promotional campaigns,
customer management, backup systems, and much more!
"""

import json
import os
import shutil
from datetime import datetime, timedelta
import uuid
from pathlib import Path
import random
import string
import hashlib
import re
import csv
import sqlite3
from collections import defaultdict, Counter
import statistics
import zipfile
import time
from typing import Dict, List, Optional, Tuple, Any
import pickle
import threading
import queue
import base64
import secrets
import math
from enum import Enum
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.request
import urllib.parse
import socket
import ssl
import certifi
from dataclasses import dataclass, field
from decimal import Decimal
import asyncio
import sys

# Define directories
STATIC_DIR = Path("static")
IMAGES_DIR = STATIC_DIR / "images"
APP_ICONS_DIR = IMAGES_DIR / "app_icons"
APP_BANNERS_DIR = IMAGES_DIR / "app_banners"
SCREENSHOTS_DIR = IMAGES_DIR / "screenshots"
APPS_LINK_DIR = Path("Apps_Link")

# New directories for enhanced features
BACKUP_DIR = Path("backups")
ANALYTICS_DIR = Path("analytics")
EXPORT_DIR = Path("exports")
CACHE_DIR = Path("cache")
LOGS_DIR = Path("logs")
DATA_DIR = Path("data")
TEMPLATES_DIR = Path("templates")

# Database files
CUSTOMERS_DB = DATA_DIR / "customers.db"
ANALYTICS_DB = DATA_DIR / "analytics.db"
PROMO_DB = DATA_DIR / "promotions.db"
INVENTORY_DB = DATA_DIR / "inventory.db"
SECURITY_DB = DATA_DIR / "security.db"
SOCIAL_DB = DATA_DIR / "social.db"
PAYMENT_DB = DATA_DIR / "payments.db"
SUPPORT_DB = DATA_DIR / "support.db"
BETA_DB = DATA_DIR / "beta_testing.db"
QUALITY_DB = DATA_DIR / "quality_assurance.db"
CLOUD_DB = DATA_DIR / "cloud_sync.db"
MONITORING_DB = DATA_DIR / "monitoring.db"

# Configuration
CONFIG = {
    'currency': '$',
    'tax_rate': 0.10,
    'default_language': 'en',
    'max_backup_files': 10,
    'analytics_retention_days': 90,
    'review_moderation': True,
    'auto_backup': True,
    'backup_interval_hours': 24,
    'loyalty_points_per_dollar': 10,
    'ai_recommendations': True,
    'smart_pricing': True,
    'inventory_alert_threshold': 10,
    'cloud_sync_enabled': True,
    'voice_search_enabled': True,
    'live_chat_enabled': True,
    'beta_testing_enabled': True,
    'auto_quality_check': True,
    'social_features_enabled': True,
    'advanced_security': True,
    'delta_updates_enabled': True,
    'multi_language_support': True,
    'gamification_enabled': True,
    'app_performance_monitoring': True,
    'developer_analytics_pro': True,
    'smart_notifications': True,
    'fraud_detection': True,
    'blockchain_verification': False,
    'ar_preview_enabled': True,
    'video_trailers_enabled': True,
    'supported_languages': ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ar'],
    'supported_currencies': ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'INR', 'BRL'],
    'payment_processors': ['stripe', 'paypal', 'razorpay', 'square', 'crypto'],
    'max_file_size_mb': 5000,
    'enable_cdn': True,
    'enable_app_streaming': True
}

def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        APP_ICONS_DIR, APP_BANNERS_DIR, SCREENSHOTS_DIR, APPS_LINK_DIR,
        BACKUP_DIR, ANALYTICS_DIR, EXPORT_DIR, CACHE_DIR, LOGS_DIR, DATA_DIR, TEMPLATES_DIR
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory ready: {directory}")

# ============== ANALYTICS & REPORTING SYSTEM ==============

class AnalyticsEngine:
    """Advanced analytics and reporting system"""
    
    def __init__(self):
        self.ensure_analytics_db()
    
    def ensure_analytics_db(self):
        """Create analytics database if it doesn't exist"""
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                session_id TEXT,
                source TEXT,
                device_type TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                revenue REAL,
                payment_method TEXT,
                country TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                start_time DATETIME,
                end_time DATETIME,
                pages_viewed INTEGER,
                apps_viewed INTEGER,
                total_spent REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_view(self, app_id: str, user_id: str = None, source: str = "organic"):
        """Track app view"""
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()
        session_id = str(uuid.uuid4())
        device_type = random.choice(['mobile', 'desktop', 'tablet'])
        
        cursor.execute('''
            INSERT INTO app_views (app_id, user_id, session_id, source, device_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (app_id, user_id, session_id, source, device_type))
        
        conn.commit()
        conn.close()
    
    def track_download(self, app_id: str, revenue: float = 0, user_id: str = None):
        """Track app download"""
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()
        payment_method = random.choice(['credit_card', 'paypal', 'crypto', 'gift_card'])
        country = random.choice(['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP'])
        
        cursor.execute('''
            INSERT INTO downloads (app_id, user_id, revenue, payment_method, country)
            VALUES (?, ?, ?, ?, ?)
        ''', (app_id, user_id, revenue, payment_method, country))
        
        conn.commit()
        conn.close()
    
    def get_app_stats(self, app_id: str) -> Dict:
        """Get comprehensive statistics for an app"""
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()
        
        # Get view count
        cursor.execute('SELECT COUNT(*) FROM app_views WHERE app_id = ?', (app_id,))
        views = cursor.fetchone()[0]
        
        # Get download count
        cursor.execute('SELECT COUNT(*) FROM downloads WHERE app_id = ?', (app_id,))
        downloads = cursor.fetchone()[0]
        
        # Get revenue
        cursor.execute('SELECT SUM(revenue) FROM downloads WHERE app_id = ?', (app_id,))
        revenue = cursor.fetchone()[0] or 0
        
        # Get conversion rate
        conversion_rate = (downloads / views * 100) if views > 0 else 0
        
        # Get top countries
        cursor.execute('''
            SELECT country, COUNT(*) as count 
            FROM downloads 
            WHERE app_id = ? 
            GROUP BY country 
            ORDER BY count DESC 
            LIMIT 5
        ''', (app_id,))
        top_countries = cursor.fetchall()
        
        conn.close()
        
        return {
            'views': views,
            'downloads': downloads,
            'revenue': revenue,
            'conversion_rate': conversion_rate,
            'top_countries': top_countries,
            'avg_revenue_per_download': revenue / downloads if downloads > 0 else 0
        }
    
    def generate_report(self, period: str = 'monthly') -> Dict:
        """Generate comprehensive analytics report"""
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()
        
        # Calculate date range
        end_date = datetime.now()
        if period == 'daily':
            start_date = end_date - timedelta(days=1)
        elif period == 'weekly':
            start_date = end_date - timedelta(weeks=1)
        elif period == 'monthly':
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=365)
        
        # Total revenue
        cursor.execute('''
            SELECT SUM(revenue) FROM downloads 
            WHERE timestamp BETWEEN ? AND ?
        ''', (start_date, end_date))
        total_revenue = cursor.fetchone()[0] or 0
        
        # Total downloads
        cursor.execute('''
            SELECT COUNT(*) FROM downloads 
            WHERE timestamp BETWEEN ? AND ?
        ''', (start_date, end_date))
        total_downloads = cursor.fetchone()[0]
        
        # Total views
        cursor.execute('''
            SELECT COUNT(*) FROM app_views 
            WHERE timestamp BETWEEN ? AND ?
        ''', (start_date, end_date))
        total_views = cursor.fetchone()[0]
        
        # Top performing apps
        cursor.execute('''
            SELECT app_id, COUNT(*) as download_count, SUM(revenue) as total_revenue
            FROM downloads
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY app_id
            ORDER BY total_revenue DESC
            LIMIT 10
        ''', (start_date, end_date))
        top_apps = cursor.fetchall()
        
        conn.close()
        
        return {
            'period': period,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'total_revenue': total_revenue,
            'total_downloads': total_downloads,
            'total_views': total_views,
            'conversion_rate': (total_downloads / total_views * 100) if total_views > 0 else 0,
            'avg_revenue_per_download': total_revenue / total_downloads if total_downloads > 0 else 0,
            'top_performing_apps': top_apps
        }

# ============== CUSTOMER MANAGEMENT SYSTEM ==============

class CustomerManager:
    """Advanced customer relationship management system"""
    
    def __init__(self):
        self.ensure_customers_db()
    
    def ensure_customers_db(self):
        """Create customers database if it doesn't exist"""
        conn = sqlite3.connect(CUSTOMERS_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME,
                total_spent REAL DEFAULT 0,
                loyalty_points INTEGER DEFAULT 0,
                tier TEXT DEFAULT 'Bronze',
                preferences TEXT,
                country TEXT,
                language TEXT DEFAULT 'en'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wishlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                app_id TEXT,
                added_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                app_id TEXT,
                purchase_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                amount REAL,
                payment_method TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_customer(self, email: str, username: str, full_name: str = None) -> str:
        """Add a new customer"""
        customer_id = str(uuid.uuid4())
        conn = sqlite3.connect(CUSTOMERS_DB)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO customers (customer_id, email, username, full_name)
                VALUES (?, ?, ?, ?)
            ''', (customer_id, email, username, full_name))
            conn.commit()
            print(f"✅ Customer {username} added successfully!")
        except sqlite3.IntegrityError:
            print(f"❌ Customer with email {email} or username {username} already exists!")
            customer_id = None
        finally:
            conn.close()
        
        return customer_id
    
    def update_loyalty_tier(self, customer_id: str):
        """Update customer loyalty tier based on spending"""
        conn = sqlite3.connect(CUSTOMERS_DB)
        cursor = conn.cursor()
        
        cursor.execute('SELECT total_spent FROM customers WHERE customer_id = ?', (customer_id,))
        result = cursor.fetchone()
        
        if result:
            total_spent = result[0]
            
            if total_spent >= 1000:
                tier = 'Platinum'
            elif total_spent >= 500:
                tier = 'Gold'
            elif total_spent >= 100:
                tier = 'Silver'
            else:
                tier = 'Bronze'
            
            cursor.execute('''
                UPDATE customers SET tier = ? WHERE customer_id = ?
            ''', (tier, customer_id))
            conn.commit()
        
        conn.close()
    
    def add_to_wishlist(self, customer_id: str, app_id: str):
        """Add app to customer's wishlist"""
        conn = sqlite3.connect(CUSTOMERS_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO wishlists (customer_id, app_id)
            VALUES (?, ?)
        ''', (customer_id, app_id))
        
        conn.commit()
        conn.close()
    
    def get_customer_profile(self, customer_id: str) -> Dict:
        """Get comprehensive customer profile"""
        conn = sqlite3.connect(CUSTOMERS_DB)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,))
        customer = cursor.fetchone()
        
        if not customer:
            return None
        
        # Get wishlist
        cursor.execute('SELECT app_id FROM wishlists WHERE customer_id = ?', (customer_id,))
        wishlist = [row[0] for row in cursor.fetchall()]
        
        # Get purchase history
        cursor.execute('''
            SELECT app_id, purchase_date, amount 
            FROM purchase_history 
            WHERE customer_id = ? 
            ORDER BY purchase_date DESC
        ''', (customer_id,))
        purchases = cursor.fetchall()
        
        conn.close()
        
        return {
            'customer_id': customer[0],
            'email': customer[1],
            'username': customer[2],
            'full_name': customer[3],
            'created_date': customer[4],
            'total_spent': customer[6],
            'loyalty_points': customer[7],
            'tier': customer[8],
            'wishlist': wishlist,
            'purchase_history': purchases
        }

# ============== PROMOTIONAL CAMPAIGN SYSTEM ==============

class PromotionManager:
    """Advanced promotional campaign management"""
    
    def __init__(self):
        self.ensure_promo_db()
    
    def ensure_promo_db(self):
        """Create promotions database if it doesn't exist"""
        conn = sqlite3.connect(PROMO_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotions (
                promo_id TEXT PRIMARY KEY,
                code TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                value REAL NOT NULL,
                min_purchase REAL DEFAULT 0,
                max_uses INTEGER,
                current_uses INTEGER DEFAULT 0,
                start_date DATETIME,
                end_date DATETIME,
                applicable_apps TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bundles (
                bundle_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                apps TEXT NOT NULL,
                original_price REAL,
                bundle_price REAL,
                savings_percent REAL,
                active BOOLEAN DEFAULT 1,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_discount_code(self, discount_type: str, value: float, 
                            code: str = None, max_uses: int = None) -> str:
        """Create a new discount code"""
        if not code:
            code = self.generate_promo_code()
        
        promo_id = str(uuid.uuid4())
        conn = sqlite3.connect(PROMO_DB)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO promotions (promo_id, code, type, value, max_uses)
                VALUES (?, ?, ?, ?, ?)
            ''', (promo_id, code, discount_type, value, max_uses))
            conn.commit()
            print(f"✅ Discount code '{code}' created successfully!")
        except sqlite3.IntegrityError:
            print(f"❌ Code '{code}' already exists!")
            code = None
        finally:
            conn.close()
        
        return code
    
    def generate_promo_code(self, length: int = 8) -> str:
        """Generate a random promo code"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def create_bundle(self, name: str, app_ids: List[str], bundle_price: float) -> str:
        """Create an app bundle deal"""
        bundle_id = str(uuid.uuid4())
        apps_json = json.dumps(app_ids)
        
        # Calculate original price and savings
        apps = load_apps()
        original_price = sum(float(app.get('price', 0)) for app in apps 
                           if app['id'] in app_ids)
        savings_percent = ((original_price - bundle_price) / original_price * 100) \
                         if original_price > 0 else 0
        
        conn = sqlite3.connect(PROMO_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bundles (bundle_id, name, apps, original_price, bundle_price, savings_percent)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (bundle_id, name, apps_json, original_price, bundle_price, savings_percent))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Bundle '{name}' created with {savings_percent:.1f}% savings!")
        return bundle_id
    
    def run_flash_sale(self, app_ids: List[str], discount_percent: float, duration_hours: int):
        """Create a time-limited flash sale"""
        promo_id = str(uuid.uuid4())
        code = f"FLASH{random.randint(1000, 9999)}"
        start_date = datetime.now()
        end_date = start_date + timedelta(hours=duration_hours)
        
        conn = sqlite3.connect(PROMO_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO promotions (promo_id, code, type, value, start_date, end_date, applicable_apps)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (promo_id, code, 'percentage', discount_percent, start_date, end_date, json.dumps(app_ids)))
        
        conn.commit()
        conn.close()
        
        print(f"🎯 Flash Sale Started!")
        print(f"   Code: {code}")
        print(f"   Discount: {discount_percent}%")
        print(f"   Duration: {duration_hours} hours")
        print(f"   Ends: {end_date.strftime('%Y-%m-%d %H:%M')}")
        
        return code

# ============== AI RECOMMENDATION ENGINE ==============

class RecommendationEngine:
    """AI-powered app recommendation system"""
    
    def __init__(self):
        self.cache_file = CACHE_DIR / "recommendations.pkl"
    
    def calculate_similarity(self, app1: Dict, app2: Dict) -> float:
        """Calculate similarity score between two apps"""
        score = 0.0
        
        # Category match
        if app1.get('category') == app2.get('category'):
            score += 0.3
        
        # Tag overlap
        tags1 = set(app1.get('tags', []))
        tags2 = set(app2.get('tags', []))
        if tags1 and tags2:
            overlap = len(tags1.intersection(tags2)) / len(tags1.union(tags2))
            score += overlap * 0.3
        
        # Rating similarity
        rating_diff = abs(app1.get('rating', 0) - app2.get('rating', 0))
        score += (5 - rating_diff) / 5 * 0.2
        
        # Price range similarity
        price1 = float(app1.get('price', 0))
        price2 = float(app2.get('price', 0))
        if price1 == 0 and price2 == 0:
            score += 0.2
        elif price1 > 0 and price2 > 0:
            price_ratio = min(price1, price2) / max(price1, price2)
            score += price_ratio * 0.2
        
        return score
    
    def get_recommendations(self, app_id: str, limit: int = 5) -> List[Dict]:
        """Get app recommendations based on similarity"""
        apps = load_apps()
        target_app = next((app for app in apps if app['id'] == app_id), None)
        
        if not target_app:
            return []
        
        # Calculate similarity scores
        recommendations = []
        for app in apps:
            if app['id'] != app_id:
                score = self.calculate_similarity(target_app, app)
                recommendations.append((app, score))
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [app for app, score in recommendations[:limit]]
    
    def get_trending_apps(self, days: int = 7) -> List[Dict]:
        """Get trending apps based on recent activity"""
        apps = load_apps()
        analytics = AnalyticsEngine()
        
        trending = []
        for app in apps:
            stats = analytics.get_app_stats(app['id'])
            # Calculate trend score
            trend_score = (
                stats['views'] * 0.3 + 
                stats['downloads'] * 0.5 + 
                app.get('rating', 0) * 0.2
            )
            trending.append((app, trend_score))
        
        trending.sort(key=lambda x: x[1], reverse=True)
        return [app for app, score in trending[:10]]
    
    def get_personalized_recommendations(self, customer_id: str) -> List[Dict]:
        """Get personalized recommendations for a customer"""
        customer_mgr = CustomerManager()
        profile = customer_mgr.get_customer_profile(customer_id)
        
        if not profile:
            return self.get_trending_apps()
        
        # Get apps from purchase history
        purchased_apps = [p[0] for p in profile['purchase_history']]
        
        # Find similar apps to purchased ones
        recommendations = []
        for app_id in purchased_apps[:5]:  # Use last 5 purchases
            recs = self.get_recommendations(app_id, limit=3)
            recommendations.extend(recs)
        
        # Remove duplicates and already purchased apps
        seen = set(purchased_apps)
        unique_recs = []
        for app in recommendations:
            if app['id'] not in seen:
                unique_recs.append(app)
                seen.add(app['id'])
        
        return unique_recs[:10]

# ============== BACKUP & RECOVERY SYSTEM ==============

class BackupManager:
    """Comprehensive backup and recovery system"""
    
    def __init__(self):
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Ensure backup directory exists"""
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, backup_name: str = None) -> str:
        """Create a complete backup of all data"""
        if not backup_name:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = BACKUP_DIR / f"{backup_name}.zip"
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            # Backup JSON data
            if os.path.exists('apps_data.json'):
                backup_zip.write('apps_data.json')
            
            # Backup databases
            for db_file in [CUSTOMERS_DB, ANALYTICS_DB, PROMO_DB, INVENTORY_DB]:
                if db_file.exists():
                    backup_zip.write(db_file)
            
            # Backup images
            for img_dir in [APP_ICONS_DIR, APP_BANNERS_DIR, SCREENSHOTS_DIR]:
                if img_dir.exists():
                    for file in img_dir.iterdir():
                        if file.is_file():
                            backup_zip.write(file)
        
        # Clean old backups
        self.clean_old_backups()
        
        print(f"✅ Backup created: {backup_path}")
        return str(backup_path)
    
    def restore_backup(self, backup_file: str) -> bool:
        """Restore data from backup"""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            print(f"❌ Backup file not found: {backup_file}")
            return False
        
        try:
            with zipfile.ZipFile(backup_path, 'r') as backup_zip:
                backup_zip.extractall()
            print(f"✅ Backup restored successfully from {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False
    
    def clean_old_backups(self):
        """Remove old backup files beyond retention limit"""
        backups = sorted(BACKUP_DIR.glob("backup_*.zip"), key=lambda x: x.stat().st_mtime)
        
        while len(backups) > CONFIG['max_backup_files']:
            oldest = backups.pop(0)
            oldest.unlink()
            print(f"🗑️ Removed old backup: {oldest.name}")
    
    def export_data(self, format: str = 'csv') -> str:
        """Export data in various formats"""
        export_file = EXPORT_DIR / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        apps = load_apps()
        
        if format == 'csv':
            with open(export_file, 'w', newline='', encoding='utf-8') as f:
                if apps:
                    writer = csv.DictWriter(f, fieldnames=apps[0].keys())
                    writer.writeheader()
                    writer.writerows(apps)
        elif format == 'json':
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(apps, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data exported to: {export_file}")
        return str(export_file)

# ============== ADVANCED SEARCH & FILTERING ==============

class SearchEngine:
    """Advanced search and filtering system"""
    
    def __init__(self):
        self.index_cache = CACHE_DIR / "search_index.pkl"
        self.build_index()
    
    def build_index(self):
        """Build search index for faster queries"""
        apps = load_apps()
        index = defaultdict(set)
        
        for app in apps:
            # Index by name
            for word in app['name'].lower().split():
                index[word].add(app['id'])
            
            # Index by developer
            for word in app['developer'].lower().split():
                index[word].add(app['id'])
            
            # Index by category
            index[app['category'].lower()].add(app['id'])
            
            # Index by tags
            for tag in app.get('tags', []):
                index[tag.lower()].add(app['id'])
        
        # Save index
        with open(self.index_cache, 'wb') as f:
            pickle.dump(dict(index), f)
    
    def fuzzy_search(self, query: str, threshold: float = 0.7) -> List[Dict]:
        """Perform fuzzy search with typo tolerance"""
        apps = load_apps()
        query_lower = query.lower()
        results = []
        
        for app in apps:
            # Calculate similarity scores
            name_score = self.string_similarity(query_lower, app['name'].lower())
            dev_score = self.string_similarity(query_lower, app['developer'].lower())
            desc_score = self.string_similarity(query_lower, app.get('description', '').lower())
            
            max_score = max(name_score, dev_score * 0.8, desc_score * 0.6)
            
            if max_score >= threshold:
                results.append((app, max_score))
        
        # Sort by relevance
        results.sort(key=lambda x: x[1], reverse=True)
        return [app for app, score in results]
    
    def string_similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity using Levenshtein distance"""
        if not s1 or not s2:
            return 0.0
        
        # Simple character overlap for now
        s1_chars = set(s1)
        s2_chars = set(s2)
        
        if not s1_chars or not s2_chars:
            return 0.0
        
        intersection = len(s1_chars.intersection(s2_chars))
        union = len(s1_chars.union(s2_chars))
        
        # Check for substring match
        if s1 in s2 or s2 in s1:
            return 0.9
        
        return intersection / union
    
    def advanced_filter(self, **criteria) -> List[Dict]:
        """Filter apps by multiple criteria"""
        apps = load_apps()
        filtered = apps
        
        # Price range
        if 'min_price' in criteria:
            filtered = [app for app in filtered 
                       if float(app.get('price', 0)) >= criteria['min_price']]
        if 'max_price' in criteria:
            filtered = [app for app in filtered 
                       if float(app.get('price', 0)) <= criteria['max_price']]
        
        # Rating
        if 'min_rating' in criteria:
            filtered = [app for app in filtered 
                       if app.get('rating', 0) >= criteria['min_rating']]
        
        # Category
        if 'category' in criteria:
            filtered = [app for app in filtered 
                       if app.get('category', '').lower() == criteria['category'].lower()]
        
        # Age rating
        if 'age_rating' in criteria:
            filtered = [app for app in filtered 
                       if app.get('age_rating', '') == criteria['age_rating']]
        
        # Features
        if 'no_ads' in criteria and criteria['no_ads']:
            filtered = [app for app in filtered 
                       if not app.get('contains_ads', False)]
        
        if 'free_only' in criteria and criteria['free_only']:
            filtered = [app for app in filtered 
                       if float(app.get('price', 0)) == 0]
        
        return filtered

# ============== REVIEW & RATING MANAGEMENT ==============

class ReviewManager:
    """Advanced review and rating management system"""
    
    def __init__(self):
        self.spam_keywords = ['scam', 'fake', 'virus', 'malware', 'spam']
        self.positive_keywords = ['great', 'awesome', 'excellent', 'love', 'perfect', 'amazing']
        self.negative_keywords = ['bad', 'terrible', 'awful', 'hate', 'worst', 'useless']
    
    def add_review(self, app_id: str, user_id: str, rating: int, 
                   comment: str, verified_purchase: bool = False) -> bool:
        """Add a new review with moderation"""
        apps = load_apps()
        app = next((a for a in apps if a['id'] == app_id), None)
        
        if not app:
            return False
        
        # Check for spam
        if CONFIG['review_moderation'] and self.is_spam(comment):
            print("⚠️ Review flagged as potential spam and requires moderation")
            # In production, this would go to a moderation queue
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(comment)
        
        review = {
            'review_id': str(uuid.uuid4()),
            'user_id': user_id,
            'rating': rating,
            'comment': comment,
            'date': datetime.now().isoformat(),
            'verified_purchase': verified_purchase,
            'helpful_count': 0,
            'sentiment': sentiment,
            'developer_response': None
        }
        
        # Add review to app
        if 'reviews' not in app:
            app['reviews'] = []
        app['reviews'].append(review)
        
        # Update app rating
        self.update_app_rating(app)
        
        save_apps(apps)
        return True
    
    def is_spam(self, text: str) -> bool:
        """Detect potential spam reviews"""
        text_lower = text.lower()
        
        # Check for spam keywords
        spam_count = sum(1 for keyword in self.spam_keywords if keyword in text_lower)
        
        # Check for excessive caps
        if len(text) > 10:
            caps_ratio = sum(1 for c in text if c.isupper()) / len(text)
            if caps_ratio > 0.5:
                return True
        
        # Check for repetitive characters
        for i in range(len(text) - 2):
            if text[i] == text[i+1] == text[i+2] and text[i] != ' ':
                return True
        
        return spam_count >= 2
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze review sentiment"""
        text_lower = text.lower()
        
        positive_score = sum(1 for keyword in self.positive_keywords if keyword in text_lower)
        negative_score = sum(1 for keyword in self.negative_keywords if keyword in text_lower)
        
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'
    
    def update_app_rating(self, app: Dict):
        """Update app's overall rating based on reviews"""
        if not app.get('reviews'):
            return
        
        ratings = [r['rating'] for r in app['reviews']]
        app['rating'] = statistics.mean(ratings)
        app['review_count'] = len(ratings)
        
        # Calculate rating distribution
        rating_dist = Counter(ratings)
        app['rating_distribution'] = {
            '5_star': rating_dist.get(5, 0),
            '4_star': rating_dist.get(4, 0),
            '3_star': rating_dist.get(3, 0),
            '2_star': rating_dist.get(2, 0),
            '1_star': rating_dist.get(1, 0)
        }
    
    def add_developer_response(self, app_id: str, review_id: str, response: str):
        """Add developer response to a review"""
        apps = load_apps()
        app = next((a for a in apps if a['id'] == app_id), None)
        
        if app and 'reviews' in app:
            review = next((r for r in app['reviews'] if r['review_id'] == review_id), None)
            if review:
                review['developer_response'] = {
                    'text': response,
                    'date': datetime.now().isoformat()
                }
                save_apps(apps)
                return True
        
        return False

# ============== INVENTORY MANAGEMENT ==============

class InventoryManager:
    """Inventory and stock management system"""
    
    def __init__(self):
        self.ensure_inventory_db()
    
    def ensure_inventory_db(self):
        """Create inventory database if it doesn't exist"""
        conn = sqlite3.connect(INVENTORY_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                app_id TEXT PRIMARY KEY,
                stock_quantity INTEGER DEFAULT -1,
                reserved_quantity INTEGER DEFAULT 0,
                reorder_level INTEGER DEFAULT 10,
                supplier TEXT,
                unit_cost REAL,
                last_restock_date DATETIME,
                notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT,
                movement_type TEXT,
                quantity INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                reference TEXT,
                FOREIGN KEY (app_id) REFERENCES inventory(app_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def set_stock_level(self, app_id: str, quantity: int):
        """Set stock level for an app (for physical media)"""
        conn = sqlite3.connect(INVENTORY_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO inventory (app_id, stock_quantity)
            VALUES (?, ?)
        ''', (app_id, quantity))
        
        # Log movement
        cursor.execute('''
            INSERT INTO stock_movements (app_id, movement_type, quantity)
            VALUES (?, ?, ?)
        ''', (app_id, 'adjustment', quantity))
        
        conn.commit()
        conn.close()
    
    def check_stock_alerts(self) -> List[Dict]:
        """Check for low stock alerts"""
        conn = sqlite3.connect(INVENTORY_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT app_id, stock_quantity, reorder_level
            FROM inventory
            WHERE stock_quantity >= 0 AND stock_quantity <= reorder_level
        ''')
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'app_id': row[0],
                'current_stock': row[1],
                'reorder_level': row[2],
                'status': 'critical' if row[1] == 0 else 'low'
            })
        
        conn.close()
        return alerts

# ============== CLOUD SYNC & MULTI-DEVICE SUPPORT ==============

class CloudSyncManager:
    """Cloud synchronization and multi-device support system"""
    
    def __init__(self):
        self.ensure_cloud_db()
        self.sync_queue = queue.Queue()
        self.sync_thread = None
        
    def ensure_cloud_db(self):
        """Create cloud sync database"""
        conn = sqlite3.connect(CLOUD_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_status (
                device_id TEXT PRIMARY KEY,
                device_name TEXT,
                last_sync DATETIME,
                sync_token TEXT,
                platform TEXT,
                app_version TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT,
                data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                synced BOOLEAN DEFAULT 0,
                device_id TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conflict_resolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_id TEXT,
                conflict_type TEXT,
                local_version TEXT,
                cloud_version TEXT,
                resolution TEXT,
                resolved_at DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_device(self, device_name: str, platform: str) -> str:
        """Register a new device for sync"""
        device_id = str(uuid.uuid4())
        sync_token = secrets.token_urlsafe(32)
        
        conn = sqlite3.connect(CLOUD_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sync_status (device_id, device_name, sync_token, platform, last_sync)
            VALUES (?, ?, ?, ?, ?)
        ''', (device_id, device_name, sync_token, platform, datetime.now()))
        
        conn.commit()
        conn.close()
        
        return device_id, sync_token
    
    def sync_data(self, device_id: str, data_type: str, data: Dict):
        """Sync data across devices"""
        conn = sqlite3.connect(CLOUD_DB)
        cursor = conn.cursor()
        
        # Add to sync queue
        cursor.execute('''
            INSERT INTO sync_queue (operation, data, device_id)
            VALUES (?, ?, ?)
        ''', (data_type, json.dumps(data), device_id))
        
        # Update last sync time
        cursor.execute('''
            UPDATE sync_status SET last_sync = ? WHERE device_id = ?
        ''', (datetime.now(), device_id))
        
        conn.commit()
        conn.close()
        
        # Trigger sync
        self.sync_queue.put((device_id, data_type, data))
    
    def start_auto_sync(self):
        """Start automatic synchronization in background"""
        if not self.sync_thread or not self.sync_thread.is_alive():
            self.sync_thread = threading.Thread(target=self._sync_worker, daemon=True)
            self.sync_thread.start()
            print("☁️ Cloud sync started!")
    
    def _sync_worker(self):
        """Background worker for syncing data"""
        while True:
            try:
                device_id, data_type, data = self.sync_queue.get(timeout=30)
                # Simulate cloud sync
                time.sleep(0.5)  # Simulate network delay
                print(f"✅ Synced {data_type} from device {device_id[:8]}...")
                self.sync_queue.task_done()
            except queue.Empty:
                # Periodic sync check
                self._check_pending_sync()
            except Exception as e:
                print(f"Sync error: {e}")
    
    def _check_pending_sync(self):
        """Check for pending sync operations"""
        conn = sqlite3.connect(CLOUD_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, operation, data, device_id FROM sync_queue
            WHERE synced = 0
            ORDER BY timestamp
            LIMIT 10
        ''')
        
        pending = cursor.fetchall()
        
        for sync_id, operation, data, device_id in pending:
            # Process sync
            cursor.execute('UPDATE sync_queue SET synced = 1 WHERE id = ?', (sync_id,))
        
        conn.commit()
        conn.close()
    
    def resolve_conflict(self, resource_id: str, strategy: str = 'last_write_wins'):
        """Resolve sync conflicts"""
        strategies = {
            'last_write_wins': self._resolve_last_write,
            'merge': self._resolve_merge,
            'user_choice': self._resolve_user_choice
        }
        
        if strategy in strategies:
            return strategies[strategy](resource_id)
        return False
    
    def _resolve_last_write(self, resource_id: str):
        """Resolve conflict using last write wins strategy"""
        # Implementation for last write wins
        return True
    
    def _resolve_merge(self, resource_id: str):
        """Resolve conflict by merging changes"""
        # Implementation for merge strategy
        return True
    
    def _resolve_user_choice(self, resource_id: str):
        """Let user choose conflict resolution"""
        print("\nConflict detected! Choose resolution:")
        print("1. Keep local version")
        print("2. Keep cloud version")
        print("3. Merge both")
        choice = input("Select (1-3): ")
        return choice in ['1', '2', '3']

# ============== ADVANCED SEARCH WITH VOICE INPUT ==============

class AdvancedSearchEngine:
    """Enhanced search with voice input and AI capabilities"""
    
    def __init__(self):
        self.search_history = []
        self.voice_enabled = CONFIG['voice_search_enabled']
        self.search_suggestions = self._load_suggestions()
    
    def _load_suggestions(self) -> List[str]:
        """Load search suggestions"""
        suggestions_file = DATA_DIR / "search_suggestions.json"
        if suggestions_file.exists():
            with open(suggestions_file, 'r') as f:
                return json.load(f)
        return []
    
    def voice_search(self) -> str:
        """Simulate voice search input"""
        print("🎤 Voice Search Active (Simulated)")
        print("Speak your search query...")
        time.sleep(2)  # Simulate voice processing
        
        # Simulate voice recognition result
        sample_queries = [
            "action games",
            "free photo editor",
            "best racing games",
            "productivity apps",
            "music player"
        ]
        
        query = random.choice(sample_queries)
        print(f"Recognized: '{query}'")
        return query
    
    def smart_search(self, query: str, filters: Dict = None) -> List[Dict]:
        """Perform smart search with AI enhancements"""
        apps = load_apps()
        results = []
        
        # Tokenize and process query
        tokens = self._tokenize_query(query)
        
        # Search with scoring
        for app in apps:
            score = self._calculate_search_score(app, tokens, query)
            
            if filters:
                if not self._apply_filters(app, filters):
                    continue
            
            if score > 0:
                results.append((app, score))
        
        # Sort by relevance
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Store search history
        self.search_history.append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results_count': len(results)
        })
        
        return [app for app, score in results]
    
    def _tokenize_query(self, query: str) -> List[str]:
        """Tokenize search query"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        tokens = query.lower().split()
        return [t for t in tokens if t not in stop_words]
    
    def _calculate_search_score(self, app: Dict, tokens: List[str], query: str) -> float:
        """Calculate search relevance score"""
        score = 0.0
        
        # Exact match in name
        if query.lower() in app['name'].lower():
            score += 10.0
        
        # Token matches
        for token in tokens:
            if token in app['name'].lower():
                score += 5.0
            if token in app.get('description', '').lower():
                score += 2.0
            if token in app.get('developer', '').lower():
                score += 3.0
            if token in app.get('category', '').lower():
                score += 4.0
            for tag in app.get('tags', []):
                if token in tag.lower():
                    score += 3.0
        
        # Boost for popular apps
        score += app.get('downloads', 0) / 1000
        score += app.get('rating', 0) * 2
        
        return score
    
    def _apply_filters(self, app: Dict, filters: Dict) -> bool:
        """Apply search filters"""
        for key, value in filters.items():
            if key == 'min_rating' and app.get('rating', 0) < value:
                return False
            if key == 'max_price' and float(app.get('price', 0)) > value:
                return False
            if key == 'category' and app.get('category', '').lower() != value.lower():
                return False
            if key == 'free_only' and value and float(app.get('price', 0)) > 0:
                return False
        return True
    
    def get_search_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions as user types"""
        suggestions = []
        
        # From search history
        for history_item in self.search_history[-50:]:
            if partial_query.lower() in history_item['query'].lower():
                suggestions.append(history_item['query'])
        
        # From app names
        apps = load_apps()
        for app in apps:
            if partial_query.lower() in app['name'].lower():
                suggestions.append(app['name'])
        
        # Remove duplicates and limit
        return list(set(suggestions))[:10]

# ============== LIVE CHAT SUPPORT SYSTEM ==============

class LiveSupportSystem:
    """Real-time chat support system"""
    
    def __init__(self):
        self.ensure_support_db()
        self.chat_sessions = {}
        self.support_agents = self._load_agents()
    
    def ensure_support_db(self):
        """Create support database"""
        conn = sqlite3.connect(SUPPORT_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id TEXT PRIMARY KEY,
                customer_id TEXT,
                agent_id TEXT,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                ended_at DATETIME,
                status TEXT DEFAULT 'active',
                rating INTEGER,
                category TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                sender_type TEXT,
                sender_id TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                read_status BOOLEAN DEFAULT 0,
                FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS support_tickets (
                ticket_id TEXT PRIMARY KEY,
                customer_id TEXT,
                subject TEXT,
                description TEXT,
                priority TEXT DEFAULT 'normal',
                status TEXT DEFAULT 'open',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                resolved_at DATETIME,
                assigned_to TEXT,
                category TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faq_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT,
                category TEXT,
                views INTEGER DEFAULT 0,
                helpful_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_agents(self) -> List[Dict]:
        """Load support agents"""
        return [
            {'id': 'agent1', 'name': 'Alex Support', 'status': 'online', 'specialization': 'technical'},
            {'id': 'agent2', 'name': 'Sarah Helper', 'status': 'online', 'specialization': 'billing'},
            {'id': 'agent3', 'name': 'Mike Assist', 'status': 'away', 'specialization': 'general'},
            {'id': 'bot', 'name': 'AI Assistant', 'status': 'online', 'specialization': 'all'}
        ]
    
    def start_chat_session(self, customer_id: str, category: str = 'general') -> str:
        """Start a new chat session"""
        session_id = str(uuid.uuid4())
        
        # Find available agent
        available_agents = [a for a in self.support_agents if a['status'] == 'online']
        
        if not available_agents:
            # Use AI bot if no agents available
            agent = next(a for a in self.support_agents if a['id'] == 'bot')
        else:
            # Match by specialization
            agent = next((a for a in available_agents if a['specialization'] == category), available_agents[0])
        
        conn = sqlite3.connect(SUPPORT_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_sessions (session_id, customer_id, agent_id, category)
            VALUES (?, ?, ?, ?)
        ''', (session_id, customer_id, agent['id'], category))
        
        conn.commit()
        conn.close()
        
        self.chat_sessions[session_id] = {
            'customer_id': customer_id,
            'agent': agent,
            'started': datetime.now()
        }
        
        print(f"\n💬 Chat started with {agent['name']}")
        return session_id
    
    def send_message(self, session_id: str, sender_type: str, sender_id: str, message: str):
        """Send a chat message"""
        conn = sqlite3.connect(SUPPORT_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_messages (session_id, sender_type, sender_id, message)
            VALUES (?, ?, ?, ?)
        ''', (session_id, sender_type, sender_id, message))
        
        conn.commit()
        conn.close()
        
        # Simulate agent response if it's a bot
        if sender_type == 'customer' and session_id in self.chat_sessions:
            if self.chat_sessions[session_id]['agent']['id'] == 'bot':
                self._generate_bot_response(session_id, message)
    
    def _generate_bot_response(self, session_id: str, customer_message: str):
        """Generate AI bot response"""
        responses = {
            'refund': "I understand you're asking about refunds. Our refund policy allows returns within 30 days of purchase. Would you like me to help you start a refund request?",
            'download': "For download issues, please try: 1) Check your internet connection, 2) Clear app cache, 3) Ensure sufficient storage space. Is the issue resolved?",
            'payment': "For payment issues, please verify your payment method is valid and has sufficient funds. You can also try an alternative payment method. Need more help?",
            'update': "App updates are released regularly. Go to 'My Apps' and check for available updates. Enable auto-update for convenience. Anything else?",
            'default': "I'm here to help! Could you please provide more details about your issue? You can also check our FAQ section for quick answers."
        }
        
        # Simple keyword matching for demo
        bot_response = responses['default']
        for keyword, response in responses.items():
            if keyword in customer_message.lower():
                bot_response = response
                break
        
        time.sleep(1)  # Simulate thinking
        self.send_message(session_id, 'agent', 'bot', bot_response)
        print(f"🤖 Bot: {bot_response}")
    
    def create_support_ticket(self, customer_id: str, subject: str, description: str, priority: str = 'normal') -> str:
        """Create a support ticket"""
        ticket_id = f"TICKET-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        conn = sqlite3.connect(SUPPORT_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO support_tickets (ticket_id, customer_id, subject, description, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (ticket_id, customer_id, subject, description, priority))
        
        conn.commit()
        conn.close()
        
        print(f"\n🎫 Support Ticket Created: {ticket_id}")
        print(f"   Subject: {subject}")
        print(f"   Priority: {priority}")
        print(f"   Status: Open")
        
        return ticket_id
    
    def add_faq_entry(self, question: str, answer: str, category: str = 'general'):
        """Add FAQ entry"""
        conn = sqlite3.connect(SUPPORT_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO faq_entries (question, answer, category)
            VALUES (?, ?, ?)
        ''', (question, answer, category))
        
        conn.commit()
        conn.close()

# ============== SOCIAL FEATURES ==============

class SocialPlatform:
    """Social features for the app store"""
    
    def __init__(self):
        self.ensure_social_db()
    
    def ensure_social_db(self):
        """Create social features database"""
        conn = sqlite3.connect(SOCIAL_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE,
                display_name TEXT,
                bio TEXT,
                avatar_url TEXT,
                followers_count INTEGER DEFAULT 0,
                following_count INTEGER DEFAULT 0,
                verified BOOLEAN DEFAULT 0,
                developer_account BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_id TEXT,
                following_id TEXT,
                followed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(follower_id, following_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT,
                user_id TEXT,
                platform TEXT,
                shared_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                message TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_collections (
                collection_id TEXT PRIMARY KEY,
                user_id TEXT,
                name TEXT,
                description TEXT,
                public BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_apps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collection_id TEXT,
                app_id TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (collection_id) REFERENCES user_collections(collection_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                achievement_type TEXT,
                achievement_name TEXT,
                earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                points INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user_profile(self, username: str, display_name: str, bio: str = "") -> str:
        """Create a social profile"""
        user_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(SOCIAL_DB)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_profiles (user_id, username, display_name, bio)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, display_name, bio))
            conn.commit()
            print(f"✅ Profile created for @{username}")
        except sqlite3.IntegrityError:
            print(f"❌ Username @{username} already taken!")
            user_id = None
        finally:
            conn.close()
        
        return user_id
    
    def follow_user(self, follower_id: str, following_id: str):
        """Follow another user"""
        conn = sqlite3.connect(SOCIAL_DB)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO follows (follower_id, following_id)
                VALUES (?, ?)
            ''', (follower_id, following_id))
            
            # Update follower counts
            cursor.execute('''
                UPDATE user_profiles 
                SET followers_count = followers_count + 1 
                WHERE user_id = ?
            ''', (following_id,))
            
            cursor.execute('''
                UPDATE user_profiles 
                SET following_count = following_count + 1 
                WHERE user_id = ?
            ''', (follower_id,))
            
            conn.commit()
            print("✅ Successfully followed user!")
        except sqlite3.IntegrityError:
            print("Already following this user!")
        finally:
            conn.close()
    
    def share_app(self, app_id: str, user_id: str, platform: str, message: str = ""):
        """Share an app on social media"""
        conn = sqlite3.connect(SOCIAL_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO app_shares (app_id, user_id, platform, message)
            VALUES (?, ?, ?, ?)
        ''', (app_id, user_id, platform, message))
        
        conn.commit()
        conn.close()
        
        # Award achievement
        self.award_achievement(user_id, 'social', 'First Share', 10)
        
        print(f"\n📱 App shared on {platform}!")
        if message:
            print(f"   Message: {message}")
    
    def create_collection(self, user_id: str, name: str, description: str = "", public: bool = True) -> str:
        """Create an app collection"""
        collection_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(SOCIAL_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_collections (collection_id, user_id, name, description, public)
            VALUES (?, ?, ?, ?, ?)
        ''', (collection_id, user_id, name, description, public))
        
        conn.commit()
        conn.close()
        
        print(f"\n📚 Collection '{name}' created!")
        return collection_id
    
    def add_to_collection(self, collection_id: str, app_id: str, notes: str = ""):
        """Add app to collection"""
        conn = sqlite3.connect(SOCIAL_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO collection_apps (collection_id, app_id, notes)
            VALUES (?, ?, ?)
        ''', (collection_id, app_id, notes))
        
        conn.commit()
        conn.close()
    
    def award_achievement(self, user_id: str, achievement_type: str, achievement_name: str, points: int):
        """Award achievement to user"""
        conn = sqlite3.connect(SOCIAL_DB)
        cursor = conn.cursor()
        
        # Check if already earned
        cursor.execute('''
            SELECT id FROM achievements 
            WHERE user_id = ? AND achievement_name = ?
        ''', (user_id, achievement_name))
        
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO achievements (user_id, achievement_type, achievement_name, points)
                VALUES (?, ?, ?, ?)
            ''', (user_id, achievement_type, achievement_name, points))
            
            conn.commit()
            print(f"\n🏆 Achievement Unlocked: {achievement_name} (+{points} points)")
        
        conn.close()
    
    def get_user_achievements(self, user_id: str) -> List[Dict]:
        """Get user's achievements"""
        conn = sqlite3.connect(SOCIAL_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT achievement_type, achievement_name, points, earned_at
            FROM achievements
            WHERE user_id = ?
            ORDER BY earned_at DESC
        ''', (user_id,))
        
        achievements = []
        for row in cursor.fetchall():
            achievements.append({
                'type': row[0],
                'name': row[1],
                'points': row[2],
                'earned_at': row[3]
            })
        
        conn.close()
        return achievements

# ============== PUSH NOTIFICATION SYSTEM FOR WEB ==============

class WebPushNotificationManager:
    """Push notification system for web users"""
    
    def __init__(self):
        self.web_notifications_file = Path("static") / "notifications" / "push_notifications.json"
        self.ensure_notification_directory()
        self.load_web_notifications()
    
    def ensure_notification_directory(self):
        """Create notification directory if it doesn't exist"""
        notif_dir = Path("static") / "notifications"
        notif_dir.mkdir(parents=True, exist_ok=True)
    
    def load_web_notifications(self):
        """Load existing web notifications"""
        if self.web_notifications_file.exists():
            with open(self.web_notifications_file, 'r', encoding='utf-8') as f:
                self.web_notifications = json.load(f)
        else:
            self.web_notifications = []
    
    def save_web_notifications(self):
        """Save notifications to file that web can access"""
        with open(self.web_notifications_file, 'w', encoding='utf-8') as f:
            json.dump(self.web_notifications, f, indent=2, ensure_ascii=False)
    
    def push_notification(self, title: str, message: str, type: str = 'info', 
                         target_audience: str = 'all', link: str = '', 
                         icon: str = '🔔', expires_in_hours: int = 24):
        """Push a notification to web users"""
        notification = {
            'id': str(uuid.uuid4()),
            'title': title,
            'message': message,
            'type': type,  # info, success, warning, error, special
            'icon': icon,
            'link': link,  # Optional link for click action
            'target_audience': target_audience,  # all, new_users, premium, specific_region
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=expires_in_hours)).isoformat(),
            'display_after': (datetime.now() + timedelta(minutes=1)).isoformat(),  # Show after 1 minute
            'priority': 'high' if type in ['error', 'special'] else 'normal',
            'read_by': [],  # Track which users have seen it
            'click_count': 0,
            'dismiss_count': 0,
            'active': True
        }
        
        self.web_notifications.insert(0, notification)
        self.save_web_notifications()
        
        # Also create a backup in data directory
        self._backup_notification(notification)
        
        return notification['id']
    
    def _backup_notification(self, notification: Dict):
        """Backup notification to data directory"""
        backup_file = DATA_DIR / "push_notifications_backup.json"
        backups = []
        
        if backup_file.exists():
            with open(backup_file, 'r', encoding='utf-8') as f:
                backups = json.load(f)
        
        backups.insert(0, notification)
        
        # Keep only last 100 notifications in backup
        backups = backups[:100]
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backups, f, indent=2, ensure_ascii=False)
    
    def get_active_notifications(self) -> List[Dict]:
        """Get all active notifications for display"""
        current_time = datetime.now()
        active_notifs = []
        
        for notif in self.web_notifications:
            if notif['active']:
                expires_at = datetime.fromisoformat(notif['expires_at'])
                display_after = datetime.fromisoformat(notif['display_after'])
                
                if display_after <= current_time <= expires_at:
                    active_notifs.append(notif)
        
        return active_notifs
    
    def update_notification(self, notif_id: str, **updates):
        """Update an existing notification"""
        for notif in self.web_notifications:
            if notif['id'] == notif_id:
                notif.update(updates)
                self.save_web_notifications()
                return True
        return False
    
    def deactivate_notification(self, notif_id: str):
        """Deactivate a notification"""
        return self.update_notification(notif_id, active=False)
    
    def get_notification_analytics(self, notif_id: str) -> Dict:
        """Get analytics for a specific notification"""
        for notif in self.web_notifications:
            if notif['id'] == notif_id:
                return {
                    'title': notif['title'],
                    'created_at': notif['created_at'],
                    'expires_at': notif['expires_at'],
                    'views': len(notif['read_by']),
                    'clicks': notif['click_count'],
                    'dismissals': notif['dismiss_count'],
                    'active': notif['active']
                }
        return {}
    
    def create_campaign_notification(self, campaign_name: str, apps: List[str], 
                                    discount_percent: int, duration_hours: int):
        """Create a special campaign notification"""
        message = f"Limited time offer! Get {discount_percent}% off on selected apps. Hurry, offer ends in {duration_hours} hours!"
        
        return self.push_notification(
            title=f"🎉 {campaign_name}",
            message=message,
            type='special',
            link='/deals',
            icon='🎁',
            expires_in_hours=duration_hours
        )
    
    def create_update_notification(self, app_name: str, version: str, features: List[str]):
        """Create app update notification"""
        feature_list = ', '.join(features[:3]) if features else 'bug fixes and improvements'
        
        return self.push_notification(
            title=f"Update Available: {app_name}",
            message=f"Version {version} is now available with {feature_list}",
            type='info',
            icon='🔄',
            expires_in_hours=48
        )
    
    def create_announcement(self, title: str, message: str, important: bool = False):
        """Create a general announcement"""
        return self.push_notification(
            title=title,
            message=message,
            type='special' if important else 'info',
            icon='📢' if important else '📣',
            expires_in_hours=72 if important else 24
        )
    
    def cleanup_expired_notifications(self):
        """Remove expired notifications"""
        current_time = datetime.now()
        active_count = 0
        
        for notif in self.web_notifications:
            if notif['active']:
                expires_at = datetime.fromisoformat(notif['expires_at'])
                if current_time > expires_at:
                    notif['active'] = False
                else:
                    active_count += 1
        
        # Keep only last 50 notifications total
        self.web_notifications = self.web_notifications[:50]
        self.save_web_notifications()
        
        return active_count

# ============== NOTIFICATION SYSTEM ==============

class NotificationManager:
    """Notification and alert system"""
    
    def __init__(self):
        self.notifications = []
        self.load_notifications()
    
    def load_notifications(self):
        """Load notifications from file"""
        notif_file = DATA_DIR / "notifications.json"
        if notif_file.exists():
            with open(notif_file, 'r') as f:
                self.notifications = json.load(f)
    
    def save_notifications(self):
        """Save notifications to file"""
        notif_file = DATA_DIR / "notifications.json"
        with open(notif_file, 'w') as f:
            json.dump(self.notifications, f, indent=2)
    
    def add_notification(self, title: str, message: str, type: str = 'info', priority: str = 'normal'):
        """Add a new notification"""
        notification = {
            'id': str(uuid.uuid4()),
            'title': title,
            'message': message,
            'type': type,  # info, warning, error, success
            'priority': priority,  # low, normal, high, critical
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        
        self.notifications.insert(0, notification)
        self.save_notifications()
        
        # Show immediate notification for critical items
        if priority == 'critical':
            print(f"\n🚨 CRITICAL ALERT: {title}")
            print(f"   {message}")
    
    def get_unread_notifications(self) -> List[Dict]:
        """Get all unread notifications"""
        return [n for n in self.notifications if not n['read']]
    
    def mark_as_read(self, notification_id: str):
        """Mark notification as read"""
        for notif in self.notifications:
            if notif['id'] == notification_id:
                notif['read'] = True
                break
        self.save_notifications()
    
    def check_system_alerts(self):
        """Check for system-wide alerts"""
        # Check inventory
        inv_mgr = InventoryManager()
        stock_alerts = inv_mgr.check_stock_alerts()
        
        for alert in stock_alerts:
            if alert['status'] == 'critical':
                self.add_notification(
                    "Stock Alert",
                    f"App {alert['app_id']} is out of stock!",
                    "error",
                    "critical"
                )
            else:
                self.add_notification(
                    "Low Stock Warning",
                    f"App {alert['app_id']} has only {alert['current_stock']} units left",
                    "warning",
                    "high"
                )

# ============== ENHANCED HELPER FUNCTIONS ==============

def generate_analytics_report():
    """Generate and display analytics report"""
    analytics = AnalyticsEngine()
    
    print("\n" + "="*60)
    print("📊 ANALYTICS REPORT")
    print("="*60)
    
    # Get report for different periods
    for period in ['daily', 'weekly', 'monthly']:
        report = analytics.generate_report(period)
        print(f"\n📅 {period.upper()} REPORT:")
        print(f"   Period: {report['start_date'][:10]} to {report['end_date'][:10]}")
        print(f"   Total Revenue: {CONFIG['currency']}{report['total_revenue']:.2f}")
        print(f"   Total Downloads: {report['total_downloads']}")
        print(f"   Total Views: {report['total_views']}")
        print(f"   Conversion Rate: {report['conversion_rate']:.2f}%")
        print(f"   Avg Revenue/Download: {CONFIG['currency']}{report['avg_revenue_per_download']:.2f}")
    
    print("\n" + "="*60)

def manage_promotions():
    """Manage promotional campaigns"""
    promo_mgr = PromotionManager()
    
    print("\n=== PROMOTIONAL CAMPAIGNS ===")
    print("1. Create Discount Code")
    print("2. Create Bundle Deal")
    print("3. Run Flash Sale")
    print("4. View Active Promotions")
    print("5. Back to Main Menu")
    
    choice = input("\nSelect option (1-5): ")
    
    if choice == '1':
        print("\n📱 CREATE DISCOUNT CODE")
        discount_type = input("Type (percentage/fixed): ")
        value = float(input("Value (e.g., 20 for 20% or $20): "))
        code = input("Custom code (or press Enter for auto): ") or None
        max_uses = input("Max uses (or press Enter for unlimited): ")
        max_uses = int(max_uses) if max_uses else None
        
        promo_code = promo_mgr.create_discount_code(discount_type, value, code, max_uses)
        if promo_code:
            print(f"\n✅ Discount code created: {promo_code}")
    
    elif choice == '2':
        print("\n📦 CREATE BUNDLE DEAL")
        apps = load_apps()
        
        if len(apps) < 2:
            print("Need at least 2 apps to create a bundle")
            return
        
        print("\nAvailable apps:")
        for i, app in enumerate(apps, 1):
            print(f"{i}. {app['name']} ({CONFIG['currency']}{app.get('price', '0')})")
        
        app_indices = input("\nSelect app numbers (comma-separated): ")
        selected_indices = [int(i.strip())-1 for i in app_indices.split(',')]
        app_ids = [apps[i]['id'] for i in selected_indices if 0 <= i < len(apps)]
        
        if len(app_ids) >= 2:
            bundle_name = input("Bundle name: ")
            bundle_price = float(input("Bundle price: "))
            promo_mgr.create_bundle(bundle_name, app_ids, bundle_price)
    
    elif choice == '3':
        print("\n⚡ RUN FLASH SALE")
        apps = load_apps()
        
        print("\nSelect apps for flash sale:")
        print("1. All apps")
        print("2. Featured apps only")
        print("3. Select specific apps")
        
        sale_choice = input("\nChoice (1-3): ")
        
        if sale_choice == '1':
            app_ids = [app['id'] for app in apps]
        elif sale_choice == '2':
            app_ids = [app['id'] for app in apps if app.get('featured')]
        else:
            print("\nAvailable apps:")
            for i, app in enumerate(apps, 1):
                print(f"{i}. {app['name']}")
            
            indices = input("\nSelect app numbers (comma-separated): ")
            selected = [int(i.strip())-1 for i in indices.split(',')]
            app_ids = [apps[i]['id'] for i in selected if 0 <= i < len(apps)]
        
        if app_ids:
            discount = float(input("Discount percentage: "))
            duration = int(input("Duration (hours): "))
            promo_mgr.run_flash_sale(app_ids, discount, duration)

def show_ai_recommendations():
    """Show AI-powered recommendations"""
    rec_engine = RecommendationEngine()
    apps = load_apps()
    
    if not apps:
        print("No apps available for recommendations")
        return
    
    print("\n=== AI RECOMMENDATIONS ===")
    print("1. Get recommendations for an app")
    print("2. Show trending apps")
    print("3. Get personalized recommendations")
    print("4. Back")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == '1':
        print("\nSelect app:")
        for i, app in enumerate(apps, 1):
            print(f"{i}. {app['name']}")
        
        try:
            app_idx = int(input("\nApp number: ")) - 1
            if 0 <= app_idx < len(apps):
                recommendations = rec_engine.get_recommendations(apps[app_idx]['id'])
                
                print(f"\n🤖 Recommendations based on '{apps[app_idx]['name']}':")
                for i, rec in enumerate(recommendations, 1):
                    print(f"{i}. {rec['name']} - {rec['category']} ({CONFIG['currency']}{rec.get('price', '0')})")
        except (ValueError, IndexError):
            print("Invalid selection")
    
    elif choice == '2':
        trending = rec_engine.get_trending_apps()
        print("\n🔥 TRENDING APPS:")
        for i, app in enumerate(trending, 1):
            print(f"{i}. {app['name']} - {app['category']} ⭐{app.get('rating', 0):.1f}")
    
    elif choice == '3':
        customer_id = input("\nEnter customer ID (or 'demo' for demo): ")
        if customer_id == 'demo':
            # Create demo customer
            cust_mgr = CustomerManager()
            customer_id = cust_mgr.add_customer("demo@example.com", "demo_user", "Demo User")
        
        if customer_id:
            recommendations = rec_engine.get_personalized_recommendations(customer_id)
            print("\n🎯 PERSONALIZED RECOMMENDATIONS:")
            for i, app in enumerate(recommendations, 1):
                print(f"{i}. {app['name']} - {app['category']}")

def perform_advanced_search():
    """Perform advanced search and filtering"""
    search_engine = SearchEngine()
    
    print("\n=== ADVANCED SEARCH ===")
    print("1. Fuzzy search (typo-tolerant)")
    print("2. Filter by criteria")
    print("3. Combined search & filter")
    print("4. Back")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == '1':
        query = input("\nEnter search query: ")
        results = search_engine.fuzzy_search(query)
        
        if results:
            print(f"\n🔍 Found {len(results)} results:")
            for i, app in enumerate(results[:10], 1):
                print(f"{i}. {app['name']} by {app['developer']}")
        else:
            print("No results found")
    
    elif choice == '2':
        print("\n📋 FILTER CRITERIA (press Enter to skip):")
        criteria = {}
        
        min_price = input("Min price: ")
        if min_price:
            criteria['min_price'] = float(min_price)
        
        max_price = input("Max price: ")
        if max_price:
            criteria['max_price'] = float(max_price)
        
        min_rating = input("Min rating (0-5): ")
        if min_rating:
            criteria['min_rating'] = float(min_rating)
        
        category = input("Category: ")
        if category:
            criteria['category'] = category
        
        free_only = input("Free apps only? (yes/no): ")
        if free_only.lower() == 'yes':
            criteria['free_only'] = True
        
        no_ads = input("No ads? (yes/no): ")
        if no_ads.lower() == 'yes':
            criteria['no_ads'] = True
        
        results = search_engine.advanced_filter(**criteria)
        
        if results:
            print(f"\n📊 Found {len(results)} apps matching criteria:")
            for i, app in enumerate(results[:10], 1):
                print(f"{i}. {app['name']} - {CONFIG['currency']}{app.get('price', '0')} - ⭐{app.get('rating', 0):.1f}")
        else:
            print("No apps match the criteria")

def load_apps():
    """Load apps from the JSON file"""
    if os.path.exists('apps_data.json'):
        with open('apps_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_apps(apps):
    """Save apps to the JSON file"""
    with open('apps_data.json', 'w', encoding='utf-8') as f:
        json.dump(apps, f, indent=2, ensure_ascii=False)
    print("✅ Apps data saved successfully!")

def list_files_in_directory(directory, extensions):
    """List files with specific extensions in a directory"""
    files = []
    if directory.exists():
        for ext in extensions:
            files.extend([f.name for f in directory.glob(f"*.{ext}")])
    return sorted(files)

def copy_image_to_directory(source_path, target_directory, prefix=""):
    """Copy an image file to the target directory with optional prefix"""
    source = Path(source_path)
    if not source.exists():
        return None
    
    # Generate unique filename if prefix is provided
    if prefix:
        ext = source.suffix
        filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
    else:
        filename = source.name
    
    target = target_directory / filename
    try:
        shutil.copy2(source, target)
        return filename
    except Exception as e:
        print(f"Error copying file: {e}")
        return None

def show_available_images():
    """Show available images in the directories"""
    print("\n📁 Available Images in Directories:")
    print("="*50)
    
    print("\n🎨 App Icons (static/images/app_icons/):")
    icons = list_files_in_directory(APP_ICONS_DIR, ['png', 'jpg', 'jpeg', 'gif', 'webp'])
    if icons:
        for i, icon in enumerate(icons, 1):
            print(f"  {i}. {icon}")
    else:
        print("  (No icons found)")
    
    print("\n🖼️ Banners (static/images/app_banners/):")
    banners = list_files_in_directory(APP_BANNERS_DIR, ['png', 'jpg', 'jpeg', 'gif', 'webp'])
    if banners:
        for i, banner in enumerate(banners, 1):
            print(f"  {i}. {banner}")
    else:
        print("  (No banners found)")
    
    print("\n📸 Screenshots (static/images/screenshots/):")
    screenshots = list_files_in_directory(SCREENSHOTS_DIR, ['png', 'jpg', 'jpeg', 'gif', 'webp'])
    if screenshots:
        for i, screenshot in enumerate(screenshots, 1):
            print(f"  {i}. {screenshot}")
    else:
        print("  (No screenshots found)")
    
    print("\n📦 App Files (Apps_Link/):")
    app_files = list_files_in_directory(APPS_LINK_DIR, ['apk', 'zip', 'exe', 'dmg', 'rar'])
    if app_files:
        for i, app_file in enumerate(app_files, 1):
            print(f"  {i}. {app_file}")
    else:
        print("  (No app files found)")
    
    print("="*50)

def select_or_add_image(image_type, directory, required=False):
    """Let user select existing image or add new one"""
    extensions = ['png', 'jpg', 'jpeg', 'gif', 'webp']
    existing_files = list_files_in_directory(directory, extensions)
    
    print(f"\n{image_type}:")
    print("1. Select from existing images")
    print("2. Add new image from path")
    print("3. Use default" if not required else "3. Skip (not recommended)")
    
    choice = input("Choose option (1-3): ")
    
    if choice == "1":
        if not existing_files:
            print("No existing images found!")
            return select_or_add_image(image_type, directory, required)
        
        print("\nAvailable images:")
        for i, file in enumerate(existing_files, 1):
            print(f"{i}. {file}")
        
        try:
            selection = int(input("Select image number: ")) - 1
            if 0 <= selection < len(existing_files):
                return existing_files[selection]
        except (ValueError, IndexError):
            print("Invalid selection!")
            return select_or_add_image(image_type, directory, required)
            
    elif choice == "2":
        source_path = input("Enter full path to image file: ").strip('"')
        if os.path.exists(source_path):
            filename = copy_image_to_directory(source_path, directory)
            if filename:
                print(f"✅ Image copied successfully: {filename}")
                return filename
            else:
                print("Failed to copy image!")
                return select_or_add_image(image_type, directory, required)
        else:
            print("File not found!")
            return select_or_add_image(image_type, directory, required)
            
    elif choice == "3":
        if image_type == "App Icon":
            return "default_icon.png"
        elif image_type == "Banner":
            return "default_banner.jpg"
        else:
            return "" if not required else select_or_add_image(image_type, directory, required)
    
    return ""

def add_app():
    """Add a new app to the store with image management"""
    ensure_directories()
    print("\n=== ADD NEW APP WITH IMAGES ===")
    
    # Ask if this is a Premium Unlocked app
    print("\n🔓 Is this a Premium Unlocked app (external app from other sources)?")
    is_premium = input("Enter 'yes' for Premium Unlocked, 'no' for regular app: ").lower() == 'yes'
    
    if not is_premium:
        show_available_images()
    
    app_id = str(uuid.uuid4())
    print(f"\nApp ID: {app_id}")
    print("="*50)
    
    app = {
        'id': app_id,
        'name': input("\n📱 App Name: "),
        'developer': input("👤 Developer Name: "),
        'is_premium_unlocked': is_premium,
    }
    
    if is_premium:
        app['category'] = 'Premium Unlocked'
        app['original_source'] = input("🌐 Original Source/Website: ")
        app['mod_features'] = input("✨ Mod Features (e.g., Pro Unlocked, No Ads, etc.): ")
    else:
        app['category'] = input("📂 Category (e.g., Games, Tools, Social, etc.): ")
    
    app['description'] = input("📝 Short Description: ")
    app['long_description'] = input("📄 Long Description (About this app): ")
    
    # Handle App Icon
    print("\n🎨 APP ICON SELECTION")
    if is_premium:
        icon_url = input("Enter external icon URL (http://...): ")
        if icon_url.startswith('http'):
            app['app_icon'] = icon_url
            app['icon'] = icon_url
            app['is_external_icon'] = True
        else:
            print("Invalid URL. Using default icon.")
            app['app_icon'] = "default_icon.png"
            app['icon'] = "default_icon.png"
            app['is_external_icon'] = False
    else:
        app['app_icon'] = select_or_add_image("App Icon", APP_ICONS_DIR)
        app['icon'] = app['app_icon']  # Legacy field
        app['is_external_icon'] = False
    
    # Handle Banner
    print("\n🖼️ BANNER SELECTION")
    if is_premium:
        banner_url = input("Enter external banner URL (http://...): ")
        if banner_url.startswith('http'):
            app['banner'] = banner_url
            app['is_external_banner'] = True
        else:
            print("Invalid URL. Using default banner.")
            app['banner'] = "default_banner.jpg"
            app['is_external_banner'] = False
    else:
        app['banner'] = select_or_add_image("Banner", APP_BANNERS_DIR)
        app['is_external_banner'] = False
    
    # Basic app info
    app.update({
        'size': input("\n💾 App Size (e.g., 50MB): "),
        'version': input("🔢 Version (e.g., 1.0.0): "),
        'min_android': input("📱 Minimum Android Version (e.g., 5.0): "),
        'age_rating': input("👶 Age Rating (e.g., 3+, 7+, 12+, 16+, 18+): "),
        'downloads': 0,
        'views': 0,
        'rating': 0,
        'review_count': 0,
        'reviews': [],
        'featured': input("⭐ Featured app? (yes/no): ").lower() == 'yes',
        'release_date': input("📅 Release Date (YYYY-MM-DD) or press Enter for today: ") or datetime.now().strftime('%Y-%m-%d'),
        'added_date': datetime.now().isoformat(),
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
    })
    
    # Handle Screenshots
    print("\n📸 SCREENSHOTS (Regular screenshots for details page)")
    app['screenshots'] = []
    if is_premium:
        screenshot_count = int(input("How many external screenshot URLs to add? (0-10): ") or "0")
        for i in range(screenshot_count):
            screenshot_url = input(f"Screenshot {i+1} URL (http://...): ")
            if screenshot_url.startswith('http'):
                app['screenshots'].append(screenshot_url)
    else:
        screenshot_count = int(input("How many screenshots to add? (0-10): ") or "0")
        for i in range(screenshot_count):
            screenshot = select_or_add_image(f"Screenshot {i+1}", SCREENSHOTS_DIR)
            if screenshot:
                app['screenshots'].append(screenshot)
    
    # Handle App Preview Photos (minimum 2 required)
    print("\n🖼️ APP PREVIEW PHOTOS (Main preview images shown in store)")
    print("⚠️ Minimum 2 preview photos required for publishing!")
    app['app_preview_photos'] = []
    
    if is_premium:
        for i in range(2):
            preview_url = input(f"Preview Photo {i+1} URL (Required) (http://...): ")
            if preview_url.startswith('http'):
                app['app_preview_photos'].append(preview_url)
        
        # Optional additional previews
        while len(app['app_preview_photos']) < 5:
            add_more = input(f"\nAdd preview photo {len(app['app_preview_photos'])+1}? (yes/no): ")
            if add_more.lower() != 'yes':
                break
            preview_url = input(f"Preview Photo {len(app['app_preview_photos'])+1} URL (http://...): ")
            if preview_url.startswith('http'):
                app['app_preview_photos'].append(preview_url)
    else:
        for i in range(2):
            preview = select_or_add_image(f"Preview Photo {i+1} (Required)", SCREENSHOTS_DIR, required=True)
            if preview:
                app['app_preview_photos'].append(preview)
        
        # Optional additional previews
        while len(app['app_preview_photos']) < 5:
            add_more = input(f"\nAdd preview photo {len(app['app_preview_photos'])+1}? (yes/no): ")
            if add_more.lower() != 'yes':
                break
            preview = select_or_add_image(f"Preview Photo {len(app['app_preview_photos'])+1}", SCREENSHOTS_DIR)
            if preview:
                app['app_preview_photos'].append(preview)
    
    # Tags
    tags_input = input("\n🏷️ Tags (comma-separated): ")
    app['tags'] = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
    
    # Download link and app file
    print("\n📦 APP FILE")
    if is_premium:
        print("Choose how to specify the download:")
        print("1. Enter external download URL")
        print("2. Upload to file hosting service later")
        print("3. Skip (no download)")
        
        file_choice = input("\nSelect option (1-3): ")
        if file_choice == "1":
            download_url = input("Enter external download URL (http://...): ")
            if download_url.startswith('http'):
                app['download_link'] = download_url
                app['is_external_download'] = True
                app['app_file'] = "External"
                app['app_file_path'] = download_url
            else:
                print("Invalid URL.")
                app['download_link'] = "#"
                app['is_external_download'] = False
                app['app_file'] = ""
                app['app_file_path'] = ""
        elif file_choice == "2":
            app['download_link'] = "#pending"
            app['is_external_download'] = True
            app['app_file'] = "Pending"
            app['app_file_path'] = ""
        else:
            app['download_link'] = "#"
            app['is_external_download'] = False
            app['app_file'] = ""
            app['app_file_path'] = ""
        file_choice = "skip"  # Skip the regular file handling
    else:
        print("Choose how to specify the app file:")
        print("1. Select from existing files in Apps_Link folder")
        print("2. Copy a new file to Apps_Link folder")
        print("3. Enter file name (file should already exist in Apps_Link)")
        print("4. Skip (no download)")
        
        file_choice = input("\nSelect option (1-4): ")
    
    if file_choice == "1":
        app_files = list_files_in_directory(APPS_LINK_DIR, ['apk', 'zip', 'exe', 'dmg', 'rar', 'msi', 'deb', 'pkg'])
        if app_files:
            print("\nAvailable app files in Apps_Link folder:")
            for i, file in enumerate(app_files, 1):
                file_path = APPS_LINK_DIR / file
                file_size = file_path.stat().st_size / (1024 * 1024)  # Convert to MB
                print(f"{i}. {file} ({file_size:.2f} MB)")
            
            try:
                choice = int(input("\nSelect app file number: "))
                if 1 <= choice <= len(app_files):
                    app['app_file'] = app_files[choice-1]
                    app['app_file_path'] = str(APPS_LINK_DIR / app_files[choice-1])
                    print(f"✅ Selected: {app['app_file']}")
                else:
                    print("Invalid selection, skipping file.")
                    app['app_file'] = ""
                    app['app_file_path'] = ""
            except ValueError:
                app['app_file'] = ""
                app['app_file_path'] = ""
        else:
            print("No app files found in Apps_Link folder.")
            app['app_file'] = ""
            app['app_file_path'] = ""
    
    elif file_choice == "2":
        source_path = input("Enter full path to your app file: ").strip('"')
        if os.path.exists(source_path):
            source = Path(source_path)
            # Copy file to Apps_Link folder
            target_filename = f"{app['id'][:8]}_{source.name}"
            target_path = APPS_LINK_DIR / target_filename
            
            try:
                print(f"Copying {source.name} to Apps_Link folder...")
                shutil.copy2(source, target_path)
                app['app_file'] = target_filename
                app['app_file_path'] = str(target_path)
                file_size = target_path.stat().st_size / (1024 * 1024)
                print(f"✅ File copied successfully! Size: {file_size:.2f} MB")
            except Exception as e:
                print(f"Error copying file: {e}")
                app['app_file'] = ""
                app['app_file_path'] = ""
        else:
            print("File not found!")
            app['app_file'] = ""
            app['app_file_path'] = ""
    
    elif file_choice == "3":
        filename = input("Enter app file name (must exist in Apps_Link folder): ")
        file_path = APPS_LINK_DIR / filename
        if file_path.exists():
            app['app_file'] = filename
            app['app_file_path'] = str(file_path)
            file_size = file_path.stat().st_size / (1024 * 1024)
            print(f"✅ File found! Size: {file_size:.2f} MB")
        else:
            print(f"Warning: File '{filename}' not found in Apps_Link folder!")
            app['app_file'] = filename
            app['app_file_path'] = str(file_path)
    
    else:
        if not is_premium:
            app['app_file'] = ""
            app['app_file_path'] = ""
            print("No app file specified.")
    
    # Set download link for regular apps
    if not is_premium and file_choice != "skip":
        app['download_link'] = f"/download/{app['id']}" if app.get('app_file') else "#"
        app['is_external_download'] = False
    
    # Pricing and monetization
    app['price'] = input("\n💰 Price (0 for free, or amount): ") or "0"
    app['in_app_purchases'] = input("💳 Has in-app purchases? (yes/no): ").lower() == 'yes'
    app['contains_ads'] = input("📢 Contains ads? (yes/no): ").lower() == 'yes'
    
    # Technical requirements
    app['requirements'] = {
        'storage': input("\n💾 Storage Required (e.g., 100MB): "),
        'ram': input("🧠 RAM Required (e.g., 2GB): ") or "1GB",
        'internet': input("🌐 Internet Required? (yes/no): ").lower() == 'yes'
    }
    
    # Additional info
    app['additional_info'] = {
        'content_rating': input("\n📋 Content Rating Description: ") or "Suitable for all ages",
        'permissions': [],
        'whats_new': input("✨ What's new in this version: ") or "Initial release"
    }
    
    # Add permissions
    if input("\n🔒 Add permissions? (yes/no): ").lower() == 'yes':
        permissions = input("Enter permissions (comma-separated): ")
        app['additional_info']['permissions'] = [p.strip() for p in permissions.split(',') if p.strip()]
    
    # Save the app
    apps = load_apps()
    apps.append(app)
    save_apps(apps)
    
    print(f"\n✅ App '{app['name']}' added successfully!")
    print(f"📱 App ID: {app['id']}")
    print("\n📋 Summary:")
    print(f"  - Icon: {app['app_icon']}")
    print(f"  - Banner: {app['banner']}")
    print(f"  - Screenshots: {len(app['screenshots'])} files")
    print(f"  - Preview Photos: {len(app['app_preview_photos'])} files")
    print(f"  - App File: {app.get('app_file', 'None')}")

def edit_app():
    """Edit an existing app with image management"""
    ensure_directories()
    apps = load_apps()
    
    if not apps:
        print("No apps found in the store.")
        return
    
    print("\n=== EDIT APP ===")
    print("Available apps:")
    for i, app in enumerate(apps, 1):
        print(f"{i}. {app['name']} (ID: {app['id']})")
    
    try:
        choice = int(input("\nSelect app number to edit: ")) - 1
        if 0 <= choice < len(apps):
            app = apps[choice]
            print(f"\nEditing: {app['name']}")
            show_available_images()
            print("\nPress Enter to keep current value")
            
            # Edit basic info
            app['name'] = input(f"Name [{app['name']}]: ") or app['name']
            app['developer'] = input(f"Developer [{app['developer']}]: ") or app['developer']
            app['category'] = input(f"Category [{app['category']}]: ") or app['category']
            app['description'] = input(f"Description [{app['description'][:50]}...]: ") or app['description']
            app['version'] = input(f"Version [{app['version']}]: ") or app['version']
            app['size'] = input(f"Size [{app['size']}]: ") or app['size']
            app['price'] = input(f"Price [{app['price']}]: ") or app['price']
            
            # Update images
            if input(f"\nUpdate App Icon? Current: [{app.get('app_icon', 'default_icon.png')}] (yes/no): ").lower() == 'yes':
                app['app_icon'] = select_or_add_image("App Icon", APP_ICONS_DIR)
                app['icon'] = app['app_icon']
            
            if input(f"Update Banner? Current: [{app.get('banner', 'default_banner.jpg')}] (yes/no): ").lower() == 'yes':
                app['banner'] = select_or_add_image("Banner", APP_BANNERS_DIR)
            
            # Update screenshots
            if input(f"Update Screenshots? Currently {len(app.get('screenshots', []))} files (yes/no): ").lower() == 'yes':
                app['screenshots'] = []
                screenshot_count = int(input("How many screenshots? (0-10): ") or "0")
                for i in range(screenshot_count):
                    screenshot = select_or_add_image(f"Screenshot {i+1}", SCREENSHOTS_DIR)
                    if screenshot:
                        app['screenshots'].append(screenshot)
            
            # Update preview photos
            if input(f"Update Preview Photos? Currently {len(app.get('app_preview_photos', []))} files (yes/no): ").lower() == 'yes':
                app['app_preview_photos'] = []
                for i in range(2):
                    preview = select_or_add_image(f"Preview Photo {i+1} (Required)", SCREENSHOTS_DIR, required=True)
                    if preview:
                        app['app_preview_photos'].append(preview)
                
                while len(app['app_preview_photos']) < 5:
                    add_more = input(f"Add preview photo {len(app['app_preview_photos'])+1}? (yes/no): ")
                    if add_more.lower() != 'yes':
                        break
                    preview = select_or_add_image(f"Preview Photo {len(app['app_preview_photos'])+1}", SCREENSHOTS_DIR)
                    if preview:
                        app['app_preview_photos'].append(preview)
            
            # Update app file
            if input(f"Update App File? Current: [{app.get('app_file', '')}] (yes/no): ").lower() == 'yes':
                print("\n📦 UPDATE APP FILE")
                print("1. Select from existing files in Apps_Link folder")
                print("2. Copy a new file to Apps_Link folder")
                print("3. Enter file name manually")
                print("4. Remove app file")
                
                file_choice = input("\nSelect option (1-4): ")
                
                if file_choice == "1":
                    app_files = list_files_in_directory(APPS_LINK_DIR, ['apk', 'zip', 'exe', 'dmg', 'rar', 'msi', 'deb', 'pkg'])
                    if app_files:
                        print("\nAvailable app files:")
                        for i, file in enumerate(app_files, 1):
                            file_path = APPS_LINK_DIR / file
                            file_size = file_path.stat().st_size / (1024 * 1024)
                            print(f"{i}. {file} ({file_size:.2f} MB)")
                        try:
                            choice = int(input("Select app file: ")) - 1
                            if 0 <= choice < len(app_files):
                                app['app_file'] = app_files[choice]
                                app['app_file_path'] = str(APPS_LINK_DIR / app_files[choice])
                        except ValueError:
                            pass
                    else:
                        print("No files found in Apps_Link folder.")
                
                elif file_choice == "2":
                    source_path = input("Enter full path to your app file: ").strip('"')
                    if os.path.exists(source_path):
                        source = Path(source_path)
                        target_filename = f"{app['id'][:8]}_{source.name}"
                        target_path = APPS_LINK_DIR / target_filename
                        try:
                            shutil.copy2(source, target_path)
                            app['app_file'] = target_filename
                            app['app_file_path'] = str(target_path)
                            print(f"✅ File copied successfully!")
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        print("File not found!")
                
                elif file_choice == "3":
                    filename = input("Enter app file name: ")
                    app['app_file'] = filename
                    app['app_file_path'] = str(APPS_LINK_DIR / filename)
                
                elif file_choice == "4":
                    app['app_file'] = ""
                    app['app_file_path'] = ""
                    print("App file removed.")
                
                # Update download link
                app['download_link'] = f"/download/{app['id']}" if app.get('app_file') else "#"
            
            featured = input(f"Featured [{app.get('featured', False)}] (yes/no/keep): ")
            if featured.lower() == 'yes':
                app['featured'] = True
            elif featured.lower() == 'no':
                app['featured'] = False
            
            app['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            
            save_apps(apps)
            print(f"\n✅ App '{app['name']}' updated successfully!")
        else:
            print("Invalid selection.")
    except (ValueError, IndexError):
        print("Invalid input.")

def remove_app():
    """Remove an app from the store"""
    apps = load_apps()
    
    if not apps:
        print("No apps found in the store.")
        return
    
    print("\n=== REMOVE APP ===")
    print("Available apps:")
    for i, app in enumerate(apps, 1):
        print(f"{i}. {app['name']} (ID: {app['id']})")
    
    try:
        choice = int(input("\nSelect app number to remove: ")) - 1
        if 0 <= choice < len(apps):
            app = apps[choice]
            confirm = input(f"Are you sure you want to remove '{app['name']}'? (yes/no): ")
            
            if confirm.lower() == 'yes':
                # Optional: Ask if user wants to delete associated images
                delete_images = input("Delete associated image files? (yes/no): ").lower() == 'yes'
                
                if delete_images:
                    print("Note: This would delete image files (not implemented for safety)")
                    # In production, you might want to delete orphaned images
                
                apps.pop(choice)
                save_apps(apps)
                print(f"\n✅ App '{app['name']}' removed successfully!")
            else:
                print("Removal cancelled.")
        else:
            print("Invalid selection.")
    except (ValueError, IndexError):
        print("Invalid input.")

def list_apps():
    """List all apps in the store with image info"""
    apps = load_apps()
    
    if not apps:
        print("\n📱 No apps in the store yet.")
        print("Use option 1 to add your first app!")
        return
    
    print(f"\n=== APPS IN STORE ({len(apps)} total) ===")
    for i, app in enumerate(apps, 1):
        print(f"\n{i}. {app['name']}")
        print(f"   Developer: {app['developer']}")
        print(f"   Category: {app['category']}")
        print(f"   Version: {app.get('version', 'N/A')}")
        print(f"   Downloads: {app.get('downloads', 0)}")
        print(f"   Rating: {app.get('rating', 0):.1f} ⭐ ({app.get('review_count', 0)} reviews)")
        print(f"   Featured: {'Yes' if app.get('featured', False) else 'No'}")
        print(f"   Images: Icon={app.get('app_icon', 'None')}, "
              f"Screenshots={len(app.get('screenshots', []))}, "
              f"Previews={len(app.get('app_preview_photos', []))}")
        print(f"   App File: {app.get('app_file', 'None')}")
        print(f"   ID: {app['id']}")

def quick_add_sample():
    """Quickly add a sample app for testing"""
    ensure_directories()
    
    # Create default images if they don't exist
    default_icon = APP_ICONS_DIR / "default_icon.png"
    default_banner = APP_BANNERS_DIR / "default_banner.jpg"
    
    if not default_icon.exists():
        print("Creating default_icon.png...")
        # In a real scenario, you'd copy actual default images here
    
    if not default_banner.exists():
        print("Creating default_banner.jpg...")
        # In a real scenario, you'd copy actual default images here
    
    sample_app = {
        'id': str(uuid.uuid4()),
        'name': 'Sample App',
        'developer': 'Test Developer',
        'category': 'Tools',
        'description': 'This is a sample app for testing the store.',
        'long_description': 'This sample app demonstrates all the features of the app store. It includes reviews, screenshots, and all other metadata fields.',
        'app_icon': 'default_icon.png',
        'icon': 'default_icon.png',
        'banner': 'default_banner.jpg',
        'size': '10MB',
        'version': '1.0.0',
        'min_android': '5.0',
        'age_rating': '3+',
        'downloads': 0,
        'views': 0,
        'rating': 0,
        'review_count': 0,
        'reviews': [],
        'featured': True,
        'release_date': datetime.now().strftime('%Y-%m-%d'),
        'added_date': datetime.now().isoformat(),
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'screenshots': ['screenshot1.png', 'screenshot2.png'],
        'app_preview_photos': ['preview1.png', 'preview2.png'],
        'tags': ['sample', 'test', 'demo'],
        'download_link': '#',
        'app_file': 'app_sample.apk',
        'price': '0',
        'in_app_purchases': False,
        'contains_ads': False,
        'requirements': {
            'storage': '50MB',
            'ram': '1GB',
            'internet': False
        },
        'additional_info': {
            'content_rating': 'Suitable for all ages',
            'permissions': [],
            'whats_new': 'Initial release'
        }
    }
    
    apps = load_apps()
    apps.append(sample_app)
    save_apps(apps)
    print(f"\n✅ Sample app added successfully!")
    print(f"App ID: {sample_app['id']}")

def manage_images():
    """Manage image files in the directories"""
    ensure_directories()
    
    print("\n=== IMAGE MANAGEMENT ===")
    print("1. View all images")
    print("2. Add images to directories")
    print("3. Create default images")
    print("4. Back to main menu")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == "1":
        show_available_images()
        input("\nPress Enter to continue...")
        
    elif choice == "2":
        print("\nSelect directory to add images to:")
        print("1. App Icons")
        print("2. Banners")
        print("3. Screenshots")
        
        dir_choice = input("Select (1-3): ")
        
        if dir_choice == "1":
            target_dir = APP_ICONS_DIR
        elif dir_choice == "2":
            target_dir = APP_BANNERS_DIR
        elif dir_choice == "3":
            target_dir = SCREENSHOTS_DIR
        else:
            return
        
        source_path = input("Enter full path to image file: ").strip('"')
        if os.path.exists(source_path):
            filename = copy_image_to_directory(source_path, target_dir)
            if filename:
                print(f"✅ Image copied successfully: {filename}")
            else:
                print("Failed to copy image!")
        else:
            print("File not found!")
            
    elif choice == "3":
        print("\nCreating default placeholder images...")
        # Here you would create actual default images
        print("Note: In production, actual default images would be created here")
        print("For now, please add your own default_icon.png and default_banner.jpg")

# ============== ADVANCED SECURITY & ANTI-PIRACY ==============

class SecurityManager:
    """Advanced security and anti-piracy system"""
    
    def __init__(self):
        self.ensure_security_db()
        self.encryption_key = self._generate_encryption_key()
    
    def ensure_security_db(self):
        """Create security database"""
        conn = sqlite3.connect(SECURITY_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_licenses (
                license_id TEXT PRIMARY KEY,
                app_id TEXT,
                user_id TEXT,
                license_key TEXT UNIQUE,
                activation_date DATETIME,
                expiry_date DATETIME,
                device_fingerprint TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                user_id TEXT,
                app_id TEXT,
                ip_address TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                details TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocked_users (
                user_id TEXT PRIMARY KEY,
                reason TEXT,
                blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                blocked_until DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key"""
        return secrets.token_bytes(32)
    
    def generate_license_key(self, app_id: str, user_id: str) -> str:
        """Generate unique license key"""
        license_id = str(uuid.uuid4())
        
        # Generate license key
        key_parts = [
            secrets.token_hex(4).upper(),
            secrets.token_hex(4).upper(),
            secrets.token_hex(4).upper(),
            secrets.token_hex(4).upper()
        ]
        license_key = '-'.join(key_parts)
        
        # Get device fingerprint
        device_fingerprint = self._get_device_fingerprint()
        
        conn = sqlite3.connect(SECURITY_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO app_licenses (license_id, app_id, user_id, license_key, 
                                     activation_date, device_fingerprint)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (license_id, app_id, user_id, license_key, datetime.now(), device_fingerprint))
        
        conn.commit()
        conn.close()
        
        return license_key
    
    def _get_device_fingerprint(self) -> str:
        """Generate device fingerprint"""
        # Combine various system attributes
        fingerprint_data = [
            socket.gethostname(),
            str(uuid.getnode()),  # MAC address
            sys.platform
        ]
        
        fingerprint_str = '|'.join(fingerprint_data)
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()
    
    def verify_license(self, license_key: str, app_id: str) -> bool:
        """Verify license key"""
        conn = sqlite3.connect(SECURITY_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT status, device_fingerprint, expiry_date
            FROM app_licenses
            WHERE license_key = ? AND app_id = ?
        ''', (license_key, app_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            self.log_security_event('invalid_license', None, app_id, f"Invalid key: {license_key[:8]}...")
            return False
        
        status, stored_fingerprint, expiry_date = result
        
        # Check status
        if status != 'active':
            return False
        
        # Check expiry
        if expiry_date and datetime.fromisoformat(expiry_date) < datetime.now():
            return False
        
        # Verify device fingerprint
        current_fingerprint = self._get_device_fingerprint()
        if stored_fingerprint != current_fingerprint:
            self.log_security_event('device_mismatch', None, app_id, "Device fingerprint mismatch")
            return False
        
        return True
    
    def log_security_event(self, event_type: str, user_id: str = None, app_id: str = None, details: str = ""):
        """Log security event"""
        conn = sqlite3.connect(SECURITY_DB)
        cursor = conn.cursor()
        
        # Get IP address (simulated)
        ip_address = socket.gethostbyname(socket.gethostname())
        
        cursor.execute('''
            INSERT INTO security_logs (event_type, user_id, app_id, ip_address, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (event_type, user_id, app_id, ip_address, details))
        
        conn.commit()
        conn.close()
    
    def check_fraud_indicators(self, user_id: str) -> Dict:
        """Check for fraud indicators"""
        conn = sqlite3.connect(SECURITY_DB)
        cursor = conn.cursor()
        
        # Check security logs for suspicious activity
        cursor.execute('''
            SELECT COUNT(*) FROM security_logs
            WHERE user_id = ? AND event_type IN ('invalid_license', 'device_mismatch')
            AND timestamp > datetime('now', '-1 day')
        ''', (user_id,))
        
        suspicious_attempts = cursor.fetchone()[0]
        
        # Check if user is blocked
        cursor.execute('''
            SELECT reason, blocked_until FROM blocked_users
            WHERE user_id = ?
        ''', (user_id,))
        
        blocked_info = cursor.fetchone()
        conn.close()
        
        risk_score = min(suspicious_attempts * 20, 100)
        
        return {
            'risk_score': risk_score,
            'suspicious_attempts': suspicious_attempts,
            'is_blocked': blocked_info is not None,
            'blocked_reason': blocked_info[0] if blocked_info else None,
            'risk_level': 'high' if risk_score > 70 else 'medium' if risk_score > 30 else 'low'
        }

# ============== BETA TESTING PROGRAM ==============

class BetaTestingManager:
    """Beta testing program management"""
    
    def __init__(self):
        self.ensure_beta_db()
    
    def ensure_beta_db(self):
        """Create beta testing database"""
        conn = sqlite3.connect(BETA_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS beta_programs (
                program_id TEXT PRIMARY KEY,
                app_id TEXT,
                version TEXT,
                start_date DATETIME,
                end_date DATETIME,
                max_testers INTEGER,
                current_testers INTEGER DEFAULT 0,
                status TEXT DEFAULT 'recruiting',
                requirements TEXT,
                rewards TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS beta_testers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT,
                user_id TEXT,
                joined_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                feedback_count INTEGER DEFAULT 0,
                bugs_reported INTEGER DEFAULT 0,
                rating INTEGER,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (program_id) REFERENCES beta_programs(program_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS beta_feedback (
                feedback_id TEXT PRIMARY KEY,
                program_id TEXT,
                user_id TEXT,
                feedback_type TEXT,
                title TEXT,
                description TEXT,
                severity TEXT,
                status TEXT DEFAULT 'new',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                resolved_at DATETIME,
                FOREIGN KEY (program_id) REFERENCES beta_programs(program_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_beta_program(self, app_id: str, version: str, duration_days: int, max_testers: int) -> str:
        """Create a beta testing program"""
        program_id = str(uuid.uuid4())
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)
        
        conn = sqlite3.connect(BETA_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO beta_programs (program_id, app_id, version, start_date, end_date, max_testers)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (program_id, app_id, version, start_date, end_date, max_testers))
        
        conn.commit()
        conn.close()
        
        print(f"\n🧪 Beta Program Created!")
        print(f"   Version: {version}")
        print(f"   Duration: {duration_days} days")
        print(f"   Max Testers: {max_testers}")
        
        return program_id
    
    def join_beta_program(self, program_id: str, user_id: str) -> bool:
        """Join a beta testing program"""
        conn = sqlite3.connect(BETA_DB)
        cursor = conn.cursor()
        
        # Check if program is open
        cursor.execute('''
            SELECT max_testers, current_testers, status
            FROM beta_programs
            WHERE program_id = ?
        ''', (program_id,))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False
        
        max_testers, current_testers, status = result
        
        if status != 'recruiting' or current_testers >= max_testers:
            conn.close()
            return False
        
        # Add tester
        cursor.execute('''
            INSERT INTO beta_testers (program_id, user_id)
            VALUES (?, ?)
        ''', (program_id, user_id))
        
        # Update tester count
        cursor.execute('''
            UPDATE beta_programs
            SET current_testers = current_testers + 1
            WHERE program_id = ?
        ''', (program_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Successfully joined beta program!")
        return True
    
    def submit_beta_feedback(self, program_id: str, user_id: str, feedback_type: str, 
                            title: str, description: str, severity: str = 'medium'):
        """Submit beta testing feedback"""
        feedback_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(BETA_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO beta_feedback (feedback_id, program_id, user_id, feedback_type, 
                                      title, description, severity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (feedback_id, program_id, user_id, feedback_type, title, description, severity))
        
        # Update tester stats
        if feedback_type == 'bug':
            cursor.execute('''
                UPDATE beta_testers
                SET bugs_reported = bugs_reported + 1
                WHERE program_id = ? AND user_id = ?
            ''', (program_id, user_id))
        
        cursor.execute('''
            UPDATE beta_testers
            SET feedback_count = feedback_count + 1
            WHERE program_id = ? AND user_id = ?
        ''', (program_id, user_id))
        
        conn.commit()
        conn.close()
        
        print(f"\n📝 Feedback submitted!")
        print(f"   Type: {feedback_type}")
        print(f"   Severity: {severity}")

# ============== DEVELOPER DASHBOARD ==============

class DeveloperDashboard:
    """Advanced developer dashboard with analytics"""
    
    def __init__(self):
        self.analytics = AnalyticsEngine()
        self.revenue_calculator = RevenueCalculator()
    
    def get_developer_stats(self, developer_name: str) -> Dict:
        """Get comprehensive developer statistics"""
        apps = load_apps()
        developer_apps = [app for app in apps if app.get('developer') == developer_name]
        
        if not developer_apps:
            return {}
        
        total_downloads = sum(app.get('downloads', 0) for app in developer_apps)
        total_revenue = sum(float(app.get('price', 0)) * app.get('downloads', 0) for app in developer_apps)
        avg_rating = statistics.mean([app.get('rating', 0) for app in developer_apps if app.get('rating', 0) > 0] or [0])
        
        # Get trending apps
        trending = sorted(developer_apps, key=lambda x: x.get('downloads', 0), reverse=True)[:3]
        
        # Revenue by category
        revenue_by_category = defaultdict(float)
        for app in developer_apps:
            category = app.get('category', 'Other')
            revenue = float(app.get('price', 0)) * app.get('downloads', 0)
            revenue_by_category[category] += revenue
        
        return {
            'total_apps': len(developer_apps),
            'total_downloads': total_downloads,
            'total_revenue': total_revenue,
            'average_rating': avg_rating,
            'trending_apps': trending,
            'revenue_by_category': dict(revenue_by_category),
            'best_performing_app': max(developer_apps, key=lambda x: x.get('downloads', 0)) if developer_apps else None,
            'growth_rate': self._calculate_growth_rate(developer_apps)
        }
    
    def _calculate_growth_rate(self, apps: List[Dict]) -> float:
        """Calculate growth rate for developer"""
        # Simulated growth calculation
        return random.uniform(5, 25)  # Percentage growth
    
    def generate_revenue_report(self, developer_name: str, period: str = 'monthly') -> Dict:
        """Generate detailed revenue report"""
        stats = self.get_developer_stats(developer_name)
        
        if not stats:
            return {}
        
        # Calculate projections
        current_revenue = stats['total_revenue']
        growth_rate = stats['growth_rate'] / 100
        
        projections = {
            'next_month': current_revenue * (1 + growth_rate),
            'next_quarter': current_revenue * (1 + growth_rate) ** 3,
            'next_year': current_revenue * (1 + growth_rate) ** 12
        }
        
        return {
            'period': period,
            'current_revenue': current_revenue,
            'growth_rate': stats['growth_rate'],
            'projections': projections,
            'top_earning_apps': stats['trending_apps'][:3],
            'revenue_breakdown': stats['revenue_by_category'],
            'recommendations': self._generate_recommendations(stats)
        }
    
    def _generate_recommendations(self, stats: Dict) -> List[str]:
        """Generate actionable recommendations for developers"""
        recommendations = []
        
        if stats['average_rating'] < 4.0:
            recommendations.append("Focus on improving app quality to increase ratings")
        
        if stats['total_apps'] < 5:
            recommendations.append("Consider developing more apps to diversify revenue")
        
        if stats['growth_rate'] < 10:
            recommendations.append("Implement marketing campaigns to boost growth")
        
        recommendations.append("Enable in-app purchases for additional revenue streams")
        recommendations.append("Consider seasonal promotions to increase downloads")
        
        return recommendations

class RevenueCalculator:
    """Calculate and predict revenue"""
    
    def calculate_net_revenue(self, gross_revenue: float) -> Dict:
        """Calculate net revenue after fees and taxes"""
        platform_fee = gross_revenue * 0.30  # 30% platform fee
        tax = (gross_revenue - platform_fee) * CONFIG['tax_rate']
        net_revenue = gross_revenue - platform_fee - tax
        
        return {
            'gross_revenue': gross_revenue,
            'platform_fee': platform_fee,
            'tax': tax,
            'net_revenue': net_revenue,
            'take_home_percentage': (net_revenue / gross_revenue * 100) if gross_revenue > 0 else 0
        }
    
    def predict_revenue(self, historical_data: List[float], months_ahead: int = 3) -> List[float]:
        """Predict future revenue based on historical data"""
        if len(historical_data) < 2:
            return [historical_data[-1] if historical_data else 0] * months_ahead
        
        # Simple linear prediction
        avg_growth = statistics.mean([
            (historical_data[i] - historical_data[i-1]) / historical_data[i-1] 
            for i in range(1, len(historical_data)) 
            if historical_data[i-1] > 0
        ] or [0.1])
        
        predictions = []
        last_value = historical_data[-1]
        
        for _ in range(months_ahead):
            last_value *= (1 + avg_growth)
            predictions.append(last_value)
        
        return predictions

# ============== APP PERFORMANCE MONITORING ==============

class PerformanceMonitor:
    """Monitor app performance and health"""
    
    def __init__(self):
        self.ensure_monitoring_db()
    
    def ensure_monitoring_db(self):
        """Create monitoring database"""
        conn = sqlite3.connect(MONITORING_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT,
                metric_type TEXT,
                value REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crash_reports (
                report_id TEXT PRIMARY KEY,
                app_id TEXT,
                version TEXT,
                crash_type TEXT,
                stack_trace TEXT,
                device_info TEXT,
                reported_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                resolved BOOLEAN DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions_metrics (
                session_id TEXT PRIMARY KEY,
                app_id TEXT,
                user_id TEXT,
                session_duration INTEGER,
                screens_viewed INTEGER,
                actions_performed INTEGER,
                errors_encountered INTEGER,
                session_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_performance_metric(self, app_id: str, metric_type: str, value: float):
        """Track performance metric"""
        conn = sqlite3.connect(MONITORING_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_metrics (app_id, metric_type, value)
            VALUES (?, ?, ?)
        ''', (app_id, metric_type, value))
        
        conn.commit()
        conn.close()
    
    def report_crash(self, app_id: str, version: str, crash_type: str, stack_trace: str):
        """Report app crash"""
        report_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(MONITORING_DB)
        cursor = conn.cursor()
        
        device_info = json.dumps({
            'platform': sys.platform,
            'python_version': sys.version,
            'hostname': socket.gethostname()
        })
        
        cursor.execute('''
            INSERT INTO crash_reports (report_id, app_id, version, crash_type, stack_trace, device_info)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (report_id, app_id, version, crash_type, stack_trace, device_info))
        
        conn.commit()
        conn.close()
        
        print(f"\n🔴 Crash reported: {crash_type}")
        return report_id
    
    def get_app_health_score(self, app_id: str) -> Dict:
        """Calculate app health score"""
        conn = sqlite3.connect(MONITORING_DB)
        cursor = conn.cursor()
        
        # Get crash rate
        cursor.execute('''
            SELECT COUNT(*) FROM crash_reports
            WHERE app_id = ? AND reported_at > datetime('now', '-7 days')
        ''', (app_id,))
        recent_crashes = cursor.fetchone()[0]
        
        # Get average session metrics
        cursor.execute('''
            SELECT AVG(session_duration), AVG(errors_encountered)
            FROM user_sessions_metrics
            WHERE app_id = ? AND session_date > datetime('now', '-7 days')
        ''', (app_id,))
        
        result = cursor.fetchone()
        avg_session_duration = result[0] or 0
        avg_errors = result[1] or 0
        
        conn.close()
        
        # Calculate health score (0-100)
        crash_penalty = min(recent_crashes * 10, 50)
        error_penalty = min(avg_errors * 5, 30)
        health_score = max(0, 100 - crash_penalty - error_penalty)
        
        return {
            'health_score': health_score,
            'recent_crashes': recent_crashes,
            'avg_session_duration': avg_session_duration,
            'avg_errors_per_session': avg_errors,
            'status': 'healthy' if health_score > 80 else 'warning' if health_score > 50 else 'critical'
        }

def main():
    """Main menu for enhanced app management"""
    ensure_directories()
    
    # Initialize advanced systems
    cloud_sync = CloudSyncManager()
    social_platform = SocialPlatform()
    support_system = LiveSupportSystem()
    security_mgr = SecurityManager()
    
    # Start background services
    if CONFIG['cloud_sync_enabled']:
        cloud_sync.start_auto_sync()
    
    while True:
        print("\n" + "="*60)
        print("🎮 ULTRA-ENHANCED APP STORE MANAGEMENT SYSTEM 🎮")
        print("="*60)
        print("📱 BASIC OPERATIONS:")
        print("1. ➕ Add New App")
        print("2. ✏️  Edit Existing App")
        print("3. ❌ Remove App")
        print("4. 📋 List All Apps")
        print("\n🌟 ADVANCED FEATURES:")
        print("5. 📊 Analytics & Reports")
        print("6. 💰 Promotions & Campaigns")
        print("7. 🤖 AI Recommendations")
        print("8. 🔍 Advanced Search")
        print("9. 💬 Live Support System")
        print("10. 👥 Social Features")
        print("11. 🔐 Security & Licensing")
        print("12. 🧪 Beta Testing Program")
        print("13. 📈 Developer Dashboard")
        print("14. 🏆 Gamification & Achievements")
        print("15. ☁️  Cloud Sync Status")
        print("16. 📸 Manage Images")
        print("17. 💾 Backup & Export")
        print("18. 🔔 Notifications")
        print("19. 📢 Push Web Notifications")
        print("20. 🚀 Quick Actions")
        print("21. 🚪 Exit")
        print("="*60)
        
        choice = input("\nSelect an option (1-21): ")
        
        if choice == '1':
            add_app()
        elif choice == '2':
            edit_app()
        elif choice == '3':
            remove_app()
        elif choice == '4':
            list_apps()
        elif choice == '5':
            show_analytics_menu()
        elif choice == '6':
            manage_promotions()
        elif choice == '7':
            show_ai_recommendations()
        elif choice == '8':
            show_advanced_search_menu()
        elif choice == '9':
            show_support_menu(support_system)
        elif choice == '10':
            show_social_menu(social_platform)
        elif choice == '11':
            show_security_menu(security_mgr)
        elif choice == '12':
            show_beta_testing_menu()
        elif choice == '13':
            show_developer_dashboard()
        elif choice == '14':
            show_gamification_menu(social_platform)
        elif choice == '15':
            show_cloud_sync_status(cloud_sync)
        elif choice == '16':
            manage_images()
        elif choice == '17':
            show_backup_menu()
        elif choice == '18':
            show_notifications_menu()
        elif choice == '19':
            show_push_notifications_menu()
        elif choice == '20':
            show_quick_actions_menu()
        elif choice == '21':
            print("\n👋 Thank you for using the Ultra-Enhanced App Store System!")
            print("✨ May your store be as successful as the Play Store!")
            break
        else:
            print("❌ Invalid option. Please try again.")

# ============== NEW MENU FUNCTIONS ==============

def show_analytics_menu():
    """Show analytics menu"""
    print("\n=== ANALYTICS & REPORTS ===")
    print("1. Generate Analytics Report")
    print("2. View App Statistics")
    print("3. Revenue Analysis")
    print("4. User Behavior Insights")
    print("5. Export Reports")
    print("6. Back")
    
    choice = input("\nSelect option (1-6): ")
    
    if choice == '1':
        generate_analytics_report()
    elif choice == '2':
        apps = load_apps()
        if apps:
            print("\nSelect app:")
            for i, app in enumerate(apps, 1):
                print(f"{i}. {app['name']}")
            try:
                app_idx = int(input("App number: ")) - 1
                if 0 <= app_idx < len(apps):
                    analytics = AnalyticsEngine()
                    stats = analytics.get_app_stats(apps[app_idx]['id'])
                    print(f"\n📊 Stats for {apps[app_idx]['name']}:")
                    print(f"   Views: {stats['views']}")
                    print(f"   Downloads: {stats['downloads']}")
                    print(f"   Revenue: ${stats['revenue']:.2f}")
                    print(f"   Conversion Rate: {stats['conversion_rate']:.2f}%")
            except (ValueError, IndexError):
                print("Invalid selection")

def show_advanced_search_menu():
    """Show advanced search menu"""
    search_engine = AdvancedSearchEngine()
    
    print("\n=== ADVANCED SEARCH ===")
    print("1. Voice Search (Simulated)")
    print("2. Smart Search")
    print("3. Search with Filters")
    print("4. Search History")
    print("5. Back")
    
    choice = input("\nSelect option (1-5): ")
    
    if choice == '1':
        query = search_engine.voice_search()
        results = search_engine.smart_search(query)
        display_search_results(results)
    elif choice == '2':
        query = input("\nEnter search query: ")
        results = search_engine.smart_search(query)
        display_search_results(results)
    elif choice == '3':
        perform_advanced_search()
    elif choice == '4':
        print("\n📜 Recent Searches:")
        for item in search_engine.search_history[-10:]:
            print(f"   • {item['query']} ({item['results_count']} results)")

def show_support_menu(support_system: LiveSupportSystem):
    """Show support menu"""
    print("\n=== LIVE SUPPORT SYSTEM ===")
    print("1. Start Chat Session")
    print("2. Create Support Ticket")
    print("3. View FAQ")
    print("4. Chat Bot Demo")
    print("5. Back")
    
    choice = input("\nSelect option (1-5): ")
    
    if choice == '1' or choice == '4':
        customer_id = f"user_{random.randint(1000, 9999)}"
        session_id = support_system.start_chat_session(customer_id)
        
        print("\n💬 Chat Session Started")
        print("Type 'exit' to end chat\n")
        
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                break
            support_system.send_message(session_id, 'customer', customer_id, message)
    
    elif choice == '2':
        customer_id = f"user_{random.randint(1000, 9999)}"
        subject = input("\nTicket Subject: ")
        description = input("Description: ")
        priority = input("Priority (low/normal/high/critical): ") or 'normal'
        support_system.create_support_ticket(customer_id, subject, description, priority)

def show_social_menu(social_platform: SocialPlatform):
    """Show social features menu"""
    print("\n=== SOCIAL FEATURES ===")
    print("1. Create Profile")
    print("2. Follow Developer")
    print("3. Share App")
    print("4. Create Collection")
    print("5. View Achievements")
    print("6. Back")
    
    choice = input("\nSelect option (1-6): ")
    
    if choice == '1':
        username = input("\nUsername: ")
        display_name = input("Display Name: ")
        bio = input("Bio: ")
        user_id = social_platform.create_user_profile(username, display_name, bio)
        if user_id:
            print(f"\n✅ Profile created! User ID: {user_id[:8]}...")
    
    elif choice == '3':
        apps = load_apps()
        if apps:
            print("\nSelect app to share:")
            for i, app in enumerate(apps[:5], 1):
                print(f"{i}. {app['name']}")
            try:
                app_idx = int(input("App number: ")) - 1
                if 0 <= app_idx < len(apps):
                    platform = input("Share on (twitter/facebook/instagram): ")
                    message = input("Message (optional): ")
                    user_id = f"user_{random.randint(1000, 9999)}"
                    social_platform.share_app(apps[app_idx]['id'], user_id, platform, message)
            except (ValueError, IndexError):
                print("Invalid selection")

def show_security_menu(security_mgr: SecurityManager):
    """Show security menu"""
    print("\n=== SECURITY & LICENSING ===")
    print("1. Generate License Key")
    print("2. Verify License")
    print("3. Check Fraud Indicators")
    print("4. View Security Logs")
    print("5. Back")
    
    choice = input("\nSelect option (1-5): ")
    
    if choice == '1':
        apps = load_apps()
        if apps:
            print("\nSelect app:")
            for i, app in enumerate(apps[:5], 1):
                print(f"{i}. {app['name']}")
            try:
                app_idx = int(input("App number: ")) - 1
                if 0 <= app_idx < len(apps):
                    user_id = f"user_{random.randint(1000, 9999)}"
                    license_key = security_mgr.generate_license_key(apps[app_idx]['id'], user_id)
                    print(f"\n🔑 License Key Generated: {license_key}")
            except (ValueError, IndexError):
                print("Invalid selection")
    
    elif choice == '3':
        user_id = input("\nEnter user ID: ")
        indicators = security_mgr.check_fraud_indicators(user_id)
        print(f"\n🔍 Fraud Analysis for {user_id}:")
        print(f"   Risk Score: {indicators['risk_score']}/100")
        print(f"   Risk Level: {indicators['risk_level']}")
        print(f"   Suspicious Attempts: {indicators['suspicious_attempts']}")

def show_beta_testing_menu():
    """Show beta testing menu"""
    beta_mgr = BetaTestingManager()
    
    print("\n=== BETA TESTING PROGRAM ===")
    print("1. Create Beta Program")
    print("2. Join Beta Program")
    print("3. Submit Feedback")
    print("4. View Active Programs")
    print("5. Back")
    
    choice = input("\nSelect option (1-5): ")
    
    if choice == '1':
        apps = load_apps()
        if apps:
            print("\nSelect app for beta:")
            for i, app in enumerate(apps[:5], 1):
                print(f"{i}. {app['name']}")
            try:
                app_idx = int(input("App number: ")) - 1
                if 0 <= app_idx < len(apps):
                    version = input("Beta version: ")
                    duration = int(input("Duration (days): "))
                    max_testers = int(input("Max testers: "))
                    beta_mgr.create_beta_program(apps[app_idx]['id'], version, duration, max_testers)
            except (ValueError, IndexError):
                print("Invalid input")

def show_developer_dashboard():
    """Show developer dashboard"""
    dashboard = DeveloperDashboard()
    
    print("\n=== DEVELOPER DASHBOARD ===")
    developer_name = input("Enter developer name: ")
    
    stats = dashboard.get_developer_stats(developer_name)
    if stats:
        print(f"\n📊 Dashboard for {developer_name}:")
        print(f"   Total Apps: {stats['total_apps']}")
        print(f"   Total Downloads: {stats['total_downloads']:,}")
        print(f"   Total Revenue: ${stats['total_revenue']:,.2f}")
        print(f"   Average Rating: ⭐ {stats['average_rating']:.1f}")
        print(f"   Growth Rate: {stats['growth_rate']:.1f}%")
        
        if input("\nGenerate revenue report? (yes/no): ").lower() == 'yes':
            report = dashboard.generate_revenue_report(developer_name)
            print(f"\n💰 Revenue Report:")
            print(f"   Current: ${report['current_revenue']:,.2f}")
            print(f"   Projected (1 month): ${report['projections']['next_month']:,.2f}")
            print(f"   Projected (1 year): ${report['projections']['next_year']:,.2f}")
            print(f"\n📌 Recommendations:")
            for rec in report['recommendations']:
                print(f"   • {rec}")
    else:
        print(f"No apps found for developer '{developer_name}'")

def show_gamification_menu(social_platform: SocialPlatform):
    """Show gamification menu"""
    print("\n=== GAMIFICATION & ACHIEVEMENTS ===")
    print("1. View Leaderboard")
    print("2. Check Achievements")
    print("3. Daily Challenges")
    print("4. Reward Store")
    print("5. Back")
    
    choice = input("\nSelect option (1-5): ")
    
    if choice == '2':
        user_id = input("\nEnter user ID (or 'demo' for demo): ")
        if user_id == 'demo':
            user_id = f"user_{random.randint(1000, 9999)}"
            # Award some demo achievements
            social_platform.award_achievement(user_id, 'milestone', 'First Download', 10)
            social_platform.award_achievement(user_id, 'social', 'Community Member', 5)
            social_platform.award_achievement(user_id, 'reviewer', 'Helpful Reviewer', 15)
        
        achievements = social_platform.get_user_achievements(user_id)
        if achievements:
            print(f"\n🏆 Achievements for {user_id}:")
            total_points = 0
            for ach in achievements:
                print(f"   • {ach['name']} - {ach['points']} points")
                total_points += ach['points']
            print(f"\n   Total Points: {total_points}")
        else:
            print("No achievements yet!")

def show_cloud_sync_status(cloud_sync: CloudSyncManager):
    """Show cloud sync status"""
    print("\n=== CLOUD SYNC STATUS ===")
    print("☁️  Cloud Sync: ACTIVE" if CONFIG['cloud_sync_enabled'] else "☁️  Cloud Sync: DISABLED")
    
    # Register a demo device
    device_name = socket.gethostname()
    device_id, sync_token = cloud_sync.register_device(device_name, sys.platform)
    
    print(f"\n📱 Registered Devices:")
    print(f"   • {device_name} ({sys.platform})")
    print(f"   Device ID: {device_id[:8]}...")
    print(f"   Sync Token: {sync_token[:16]}...")
    
    # Simulate sync
    if input("\nPerform sync now? (yes/no): ").lower() == 'yes':
        cloud_sync.sync_data(device_id, 'apps', {'action': 'sync', 'timestamp': datetime.now().isoformat()})
        print("✅ Sync initiated!")

def show_backup_menu():
    """Show backup menu"""
    backup_mgr = BackupManager()
    
    print("\n=== BACKUP & EXPORT ===")
    print("1. Create Backup")
    print("2. Restore Backup")
    print("3. Export Data (CSV)")
    print("4. Export Data (JSON)")
    print("5. Schedule Auto-Backup")
    print("6. Back")
    
    choice = input("\nSelect option (1-6): ")
    
    if choice == '1':
        backup_name = input("\nBackup name (or Enter for auto): ") or None
        backup_mgr.create_backup(backup_name)
    elif choice == '2':
        backup_file = input("\nEnter backup file path: ")
        backup_mgr.restore_backup(backup_file)
    elif choice == '3':
        backup_mgr.export_data('csv')
    elif choice == '4':
        backup_mgr.export_data('json')

def show_push_notifications_menu():
    """Show push notifications menu for web users"""
    push_mgr = WebPushNotificationManager()
    
    print("\n" + "="*60)
    print("📢 PUSH NOTIFICATIONS FOR WEB USERS")
    print("="*60)
    print("\nThis system pushes notifications to your web store.")
    print("Notifications appear on the website 1 minute after creation.")
    print("Works with Netlify hosting!\n")
    
    print("1. 📤 Push New Notification")
    print("2. 🎉 Create Campaign Notification")
    print("3. 📣 Make Announcement")
    print("4. 🔄 App Update Notification")
    print("5. 📊 View Active Notifications")
    print("6. 📈 Notification Analytics")
    print("7. 🗑️ Cleanup Expired")
    print("8. 🔙 Back")
    
    choice = input("\nSelect option (1-8): ")
    
    if choice == '1':
        print("\n📤 PUSH NEW NOTIFICATION")
        print("-" * 40)
        
        title = input("\n📝 Notification Title: ")
        message = input("💬 Message: ")
        
        print("\n🎨 Select Type:")
        print("1. ℹ️ Info (Blue)")
        print("2. ✅ Success (Green)")
        print("3. ⚠️ Warning (Yellow)")
        print("4. 🔴 Error (Red)")
        print("5. 🌟 Special (Purple with animation)")
        
        type_choice = input("\nType (1-5): ")
        types = ['info', 'success', 'warning', 'error', 'special']
        notif_type = types[int(type_choice)-1] if type_choice.isdigit() and 1 <= int(type_choice) <= 5 else 'info'
        
        print("\n🎯 Target Audience:")
        print("1. All Users")
        print("2. New Users")
        print("3. Premium Users")
        print("4. Specific Region")
        
        audience_choice = input("\nAudience (1-4): ")
        audiences = ['all', 'new_users', 'premium', 'specific_region']
        target = audiences[int(audience_choice)-1] if audience_choice.isdigit() and 1 <= int(audience_choice) <= 4 else 'all'
        
        link = input("\n🔗 Click Action Link (optional, press Enter to skip): ")
        
        print("\n⏰ Expiration Time:")
        print("1. 6 hours")
        print("2. 12 hours")
        print("3. 24 hours (1 day)")
        print("4. 48 hours (2 days)")
        print("5. 72 hours (3 days)")
        print("6. 168 hours (1 week)")
        
        expire_choice = input("\nExpiration (1-6): ")
        expire_hours = [6, 12, 24, 48, 72, 168]
        expires_in = expire_hours[int(expire_choice)-1] if expire_choice.isdigit() and 1 <= int(expire_choice) <= 6 else 24
        
        # Select icon
        icons = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '🚨',
            'special': '🎉'
        }
        icon = icons.get(notif_type, '🔔')
        
        # Push the notification
        notif_id = push_mgr.push_notification(
            title=title,
            message=message,
            type=notif_type,
            target_audience=target,
            link=link,
            icon=icon,
            expires_in_hours=expires_in
        )
        
        print("\n" + "="*50)
        print("✅ NOTIFICATION PUSHED SUCCESSFULLY!")
        print("="*50)
        print(f"📋 Notification ID: {notif_id[:8]}...")
        print(f"⏱️ Will appear on website in: 1 minute")
        print(f"🎯 Target: {target}")
        print(f"⏳ Expires in: {expires_in} hours")
        print(f"📁 Saved to: static/notifications/push_notifications.json")
        print("\n💡 The web app will automatically fetch and display this!")
        
    elif choice == '2':
        print("\n🎉 CREATE CAMPAIGN NOTIFICATION")
        print("-" * 40)
        
        campaign_name = input("\n🏷️ Campaign Name: ")
        discount = int(input("💰 Discount Percentage: "))
        duration = int(input("⏱️ Duration (hours): "))
        
        apps = load_apps()
        if apps:
            print("\n📱 Select Apps for Campaign:")
            for i, app in enumerate(apps[:10], 1):
                print(f"{i}. {app['name']}")
            
            app_indices = input("\nApp numbers (comma-separated): ")
            selected = [int(i.strip())-1 for i in app_indices.split(',') if i.strip().isdigit()]
            app_names = [apps[i]['name'] for i in selected if 0 <= i < len(apps)]
            
            notif_id = push_mgr.create_campaign_notification(
                campaign_name=campaign_name,
                apps=app_names,
                discount_percent=discount,
                duration_hours=duration
            )
            
            print(f"\n✅ Campaign notification created!")
            print(f"📋 ID: {notif_id[:8]}...")
            print(f"🎁 {discount}% off on {len(app_names)} apps")
    
    elif choice == '3':
        print("\n📣 MAKE ANNOUNCEMENT")
        print("-" * 40)
        
        title = input("\n📢 Announcement Title: ")
        message = input("📝 Message: ")
        important = input("⭐ Mark as Important? (yes/no): ").lower() == 'yes'
        
        notif_id = push_mgr.create_announcement(title, message, important)
        
        print(f"\n✅ Announcement created!")
        print(f"📋 ID: {notif_id[:8]}...")
        print(f"Priority: {'HIGH' if important else 'NORMAL'}")
    
    elif choice == '4':
        print("\n🔄 APP UPDATE NOTIFICATION")
        print("-" * 40)
        
        apps = load_apps()
        if apps:
            print("\n📱 Select App:")
            for i, app in enumerate(apps[:10], 1):
                print(f"{i}. {app['name']} (v{app.get('version', '1.0.0')})")
            
            try:
                app_idx = int(input("\nApp number: ")) - 1
                if 0 <= app_idx < len(apps):
                    app = apps[app_idx]
                    new_version = input(f"New Version (current: {app.get('version', '1.0.0')}): ")
                    
                    print("\n✨ What's New (comma-separated):")
                    features_input = input("Features: ")
                    features = [f.strip() for f in features_input.split(',') if f.strip()]
                    
                    notif_id = push_mgr.create_update_notification(
                        app_name=app['name'],
                        version=new_version,
                        features=features
                    )
                    
                    print(f"\n✅ Update notification created!")
                    print(f"📋 ID: {notif_id[:8]}...")
            except (ValueError, IndexError):
                print("Invalid selection")
    
    elif choice == '5':
        print("\n📊 ACTIVE NOTIFICATIONS")
        print("="*50)
        
        active_notifs = push_mgr.get_active_notifications()
        
        if active_notifs:
            print(f"\nFound {len(active_notifs)} active notification(s):\n")
            
            for i, notif in enumerate(active_notifs[:10], 1):
                created = datetime.fromisoformat(notif['created_at'])
                expires = datetime.fromisoformat(notif['expires_at'])
                time_left = expires - datetime.now()
                
                print(f"{i}. {notif['icon']} {notif['title']}")
                print(f"   Message: {notif['message'][:50]}...")
                print(f"   Type: {notif['type'].upper()}")
                print(f"   Target: {notif['target_audience']}")
                print(f"   Created: {created.strftime('%Y-%m-%d %H:%M')}")
                print(f"   Expires in: {time_left.total_seconds()/3600:.1f} hours")
                print(f"   Views: {len(notif.get('read_by', []))}")
                print()
        else:
            print("No active notifications")
    
    elif choice == '6':
        print("\n📈 NOTIFICATION ANALYTICS")
        print("="*50)
        
        # Show recent notifications with analytics
        push_mgr.load_web_notifications()
        
        if push_mgr.web_notifications:
            print("\nRecent Notifications:\n")
            for i, notif in enumerate(push_mgr.web_notifications[:5], 1):
                analytics = push_mgr.get_notification_analytics(notif['id'])
                print(f"{i}. {notif.get('icon', '🔔')} {analytics.get('title', 'Unknown')}")
                print(f"   Status: {'🟢 Active' if analytics.get('active') else '🔴 Inactive'}")
                print(f"   Views: {analytics.get('views', 0)}")
                print(f"   Clicks: {analytics.get('clicks', 0)}")
                print(f"   Dismissals: {analytics.get('dismissals', 0)}")
                
                if analytics.get('views', 0) > 0:
                    ctr = (analytics.get('clicks', 0) / analytics.get('views', 0)) * 100
                    print(f"   CTR: {ctr:.1f}%")
                print()
        else:
            print("No notifications to analyze")
    
    elif choice == '7':
        print("\n🗑️ CLEANUP EXPIRED NOTIFICATIONS")
        active_count = push_mgr.cleanup_expired_notifications()
        print(f"✅ Cleanup complete!")
        print(f"   Active notifications: {active_count}")
        print(f"   File optimized: static/notifications/push_notifications.json")
    
    input("\nPress Enter to continue...")

def show_notifications_menu():
    """Show notifications menu"""
    notif_mgr = NotificationManager()
    
    print("\n=== SYSTEM NOTIFICATIONS ===")
    
    # Check system alerts
    notif_mgr.check_system_alerts()
    
    # Show unread notifications
    unread = notif_mgr.get_unread_notifications()
    if unread:
        print(f"\n🔔 You have {len(unread)} unread notifications:")
        for notif in unread[:5]:
            icon = {'error': '🔴', 'warning': '⚠️', 'success': '✅', 'info': 'ℹ️'}.get(notif['type'], '📌')
            print(f"{icon} {notif['title']}")
            print(f"   {notif['message']}")
            notif_mgr.mark_as_read(notif['id'])
    else:
        print("\n✨ No new notifications")
    
    input("\nPress Enter to continue...")

def show_quick_actions_menu():
    """Show quick actions menu"""
    print("\n=== QUICK ACTIONS ===")
    print("1. 🚀 Add Sample Apps (5 apps)")
    print("2. 🎯 Run Flash Sale")
    print("3. 📊 Quick Stats")
    print("4. 🔍 Health Check")
    print("5. Back")
    
    choice = input("\nSelect option (1-5): ")
    
    if choice == '1':
        for i in range(5):
            quick_add_sample()
        print("\n✅ Added 5 sample apps!")
    elif choice == '2':
        promo_mgr = PromotionManager()
        apps = load_apps()
        if apps:
            app_ids = [app['id'] for app in apps]
            code = promo_mgr.run_flash_sale(app_ids, 50, 24)
    elif choice == '3':
        apps = load_apps()
        print(f"\n📊 Quick Stats:")
        print(f"   Total Apps: {len(apps)}")
        print(f"   Total Downloads: {sum(app.get('downloads', 0) for app in apps):,}")
        print(f"   Average Rating: ⭐ {statistics.mean([app.get('rating', 0) for app in apps if app.get('rating', 0) > 0] or [0]):.1f}")
    elif choice == '4':
        monitor = PerformanceMonitor()
        apps = load_apps()
        if apps:
            app = apps[0]
            health = monitor.get_app_health_score(app['id'])
            print(f"\n🏥 Health Check for {app['name']}:")
            print(f"   Health Score: {health['health_score']}/100")
            print(f"   Status: {health['status'].upper()}")

def display_search_results(results: List[Dict]):
    """Display search results"""
    if results:
        print(f"\n🔍 Found {len(results)} results:")
        for i, app in enumerate(results[:10], 1):
            print(f"{i}. {app['name']} - {app['category']} (⭐ {app.get('rating', 0):.1f})")
    else:
        print("\n No results found.")

if __name__ == "__main__":
    # Create empty apps_data.json if it doesn't exist
    if not os.path.exists('apps_data.json'):
        with open('apps_data.json', 'w') as f:
            json.dump([], f)
        print("📱 Created new apps_data.json file")
    
    print("\n" + "="*60)
    print("📸 IMPORTANT: Image Management System Active!")
    print("="*60)
    print("This enhanced version includes:")
    print("✓ Image selection from existing files")
    print("✓ Image upload from your computer")
    print("✓ Organized image directories")
    print("✓ Preview of all available images")
    print("="*60)
    
    main()
