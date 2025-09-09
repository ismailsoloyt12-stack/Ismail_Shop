"""
Database Migration Script - From JSON to SQLite
This script sets up SQLite database and migrates data from JSON files
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
import shutil

# Get the project directory
PROJECT_DIR = Path(__file__).parent.absolute()

def create_database():
    """Create SQLite database with proper schema"""
    conn = sqlite3.connect('app_store.db')
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            avatar TEXT,
            bio TEXT,
            location TEXT,
            website TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            auth_provider TEXT DEFAULT 'local'
        )
    ''')
    
    # Create Apps table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            developer TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            version TEXT,
            size TEXT,
            icon TEXT,
            banner TEXT,
            rating REAL DEFAULT 0,
            downloads INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            price REAL DEFAULT 0,
            app_file TEXT,
            download_link TEXT,
            is_external_download BOOLEAN DEFAULT 0,
            featured BOOLEAN DEFAULT 0,
            mod_features TEXT,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id TEXT PRIMARY KEY,
            app_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            username TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            helpful_votes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (app_id) REFERENCES apps (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Screenshots table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS screenshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_id TEXT NOT NULL,
            image_url TEXT NOT NULL,
            display_order INTEGER DEFAULT 0,
            FOREIGN KEY (app_id) REFERENCES apps (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Favorites table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            user_id TEXT NOT NULL,
            app_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, app_id),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (app_id) REFERENCES apps (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Wishlist table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wishlist (
            user_id TEXT NOT NULL,
            app_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, app_id),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (app_id) REFERENCES apps (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Downloads History table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS downloads_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            app_id TEXT NOT NULL,
            app_name TEXT,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (app_id) REFERENCES apps (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Collections table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collections (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            is_public BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Collection Apps table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collection_apps (
            collection_id TEXT NOT NULL,
            app_id TEXT NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (collection_id, app_id),
            FOREIGN KEY (collection_id) REFERENCES collections (id) ON DELETE CASCADE,
            FOREIGN KEY (app_id) REFERENCES apps (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT,
            type TEXT DEFAULT 'info',
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create User Settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id TEXT PRIMARY KEY,
            profile_public BOOLEAN DEFAULT 1,
            show_downloads BOOLEAN DEFAULT 1,
            show_collections BOOLEAN DEFAULT 1,
            notify_updates BOOLEAN DEFAULT 1,
            notify_reviews BOOLEAN DEFAULT 1,
            notify_followers BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Followers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS followers (
            follower_id TEXT NOT NULL,
            following_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (follower_id, following_id),
            FOREIGN KEY (follower_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (following_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_apps_category ON apps(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_apps_downloads ON apps(downloads DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_apps_rating ON apps(rating DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reviews_app_id ON reviews(app_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id)')
    
    conn.commit()
    conn.close()
    print("✅ Database schema created successfully!")

def migrate_users():
    """Migrate users from users.json to database"""
    users_file = PROJECT_DIR / 'users.json'
    if not users_file.exists():
        print("⚠️ users.json not found, skipping user migration")
        return
    
    with open(users_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    conn = sqlite3.connect('app_store.db')
    cursor = conn.cursor()
    
    for user_id, user_data in users_data.items():
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (id, username, email, password, is_admin, avatar, bio, location, website, created_at, auth_provider)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                user_data.get('username'),
                user_data.get('email'),
                user_data.get('password'),
                user_data.get('is_admin', False),
                user_data.get('avatar'),
                user_data.get('bio'),
                user_data.get('location'),
                user_data.get('website'),
                user_data.get('created_at', datetime.now().isoformat()),
                user_data.get('auth_provider', 'local')
            ))
            
            # Migrate user settings
            settings = user_data.get('settings', {})
            if settings:
                cursor.execute('''
                    INSERT OR REPLACE INTO user_settings 
                    (user_id, profile_public, show_downloads, show_collections, 
                     notify_updates, notify_reviews, notify_followers)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    settings.get('profile_public', True),
                    settings.get('show_downloads', True),
                    settings.get('show_collections', True),
                    settings.get('notify_updates', True),
                    settings.get('notify_reviews', True),
                    settings.get('notify_followers', True)
                ))
            
            # Migrate favorites
            for app_id in user_data.get('favorites', []):
                cursor.execute('''
                    INSERT OR IGNORE INTO favorites (user_id, app_id) VALUES (?, ?)
                ''', (user_id, app_id))
            
            # Migrate wishlist
            for app_id in user_data.get('wishlist', []):
                cursor.execute('''
                    INSERT OR IGNORE INTO wishlist (user_id, app_id) VALUES (?, ?)
                ''', (user_id, app_id))
            
            # Migrate downloads history
            for download in user_data.get('downloads_history', []):
                cursor.execute('''
                    INSERT INTO downloads_history (user_id, app_id, app_name, downloaded_at)
                    VALUES (?, ?, ?, ?)
                ''', (
                    user_id,
                    download.get('app_id'),
                    download.get('app_name'),
                    download.get('date', datetime.now().isoformat())
                ))
            
            # Migrate followers/following
            for follower_id in user_data.get('followers', []):
                cursor.execute('''
                    INSERT OR IGNORE INTO followers (follower_id, following_id) VALUES (?, ?)
                ''', (follower_id, user_id))
            
            # Migrate notifications
            for notification in user_data.get('notifications', []):
                cursor.execute('''
                    INSERT OR IGNORE INTO notifications 
                    (id, user_id, title, message, type, is_read, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    notification.get('id'),
                    user_id,
                    notification.get('title'),
                    notification.get('message'),
                    notification.get('type', 'info'),
                    notification.get('read', False),
                    notification.get('timestamp', datetime.now().isoformat())
                ))
                
        except Exception as e:
            print(f"❌ Error migrating user {user_id}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Migrated {len(users_data)} users successfully!")

def migrate_apps():
    """Migrate apps from apps_data.json to database"""
    apps_file = PROJECT_DIR / 'apps_data.json'
    if not apps_file.exists():
        print("⚠️ apps_data.json not found, skipping apps migration")
        return
    
    with open(apps_file, 'r', encoding='utf-8') as f:
        apps_data = json.load(f)
    
    conn = sqlite3.connect('app_store.db')
    cursor = conn.cursor()
    
    for app in apps_data:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO apps 
                (id, name, developer, category, description, version, size, icon, 
                 rating, downloads, views, price, app_file, download_link, 
                 is_external_download, featured, mod_features, added_date, updated_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                app.get('id'),
                app.get('name'),
                app.get('developer'),
                app.get('category'),
                app.get('description'),
                app.get('version'),
                app.get('size'),
                app.get('icon'),
                app.get('rating', 0),
                app.get('downloads', 0),
                app.get('views', 0),
                app.get('price', 0),
                app.get('app_file'),
                app.get('download_link'),
                app.get('is_external_download', False),
                app.get('featured', False),
                app.get('mod_features'),
                app.get('added_date', datetime.now().isoformat()),
                app.get('updated_date', datetime.now().isoformat())
            ))
            
            # Migrate screenshots
            for idx, screenshot in enumerate(app.get('screenshots', [])):
                cursor.execute('''
                    INSERT INTO screenshots (app_id, image_url, display_order)
                    VALUES (?, ?, ?)
                ''', (app.get('id'), screenshot, idx))
            
            # Migrate reviews
            for review in app.get('reviews', []):
                cursor.execute('''
                    INSERT OR IGNORE INTO reviews 
                    (id, app_id, user_id, username, rating, comment, helpful_votes, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    review.get('id'),
                    app.get('id'),
                    review.get('user_id'),
                    review.get('user'),
                    review.get('rating'),
                    review.get('comment'),
                    review.get('helpful_votes', 0),
                    review.get('date', datetime.now().isoformat())
                ))
                
        except Exception as e:
            print(f"❌ Error migrating app {app.get('name')}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Migrated {len(apps_data)} apps successfully!")

def migrate_collections():
    """Migrate collections from collections.json to database"""
    collections_file = PROJECT_DIR / 'collections.json'
    if not collections_file.exists():
        print("⚠️ collections.json not found, skipping collections migration")
        return
    
    with open(collections_file, 'r', encoding='utf-8') as f:
        collections_data = json.load(f)
    
    conn = sqlite3.connect('app_store.db')
    cursor = conn.cursor()
    
    for collection_id, collection in collections_data.items():
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO collections 
                (id, user_id, name, description, is_public, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                collection.get('id', collection_id),
                collection.get('user_id'),
                collection.get('name'),
                collection.get('description'),
                collection.get('is_public', True),
                collection.get('created_at', datetime.now().isoformat()),
                collection.get('updated_at', datetime.now().isoformat())
            ))
            
            # Add apps to collection
            for app_id in collection.get('apps', []):
                cursor.execute('''
                    INSERT OR IGNORE INTO collection_apps (collection_id, app_id)
                    VALUES (?, ?)
                ''', (collection.get('id', collection_id), app_id))
                
        except Exception as e:
            print(f"❌ Error migrating collection {collection_id}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Migrated {len(collections_data)} collections successfully!")

def migrate_activities():
    """Migrate activities from activities.json to database"""
    activities_file = PROJECT_DIR / 'activities.json'
    if not activities_file.exists():
        print("⚠️ activities.json not found, skipping activities migration")
        return
    
    with open(activities_file, 'r', encoding='utf-8') as f:
        activities_data = json.load(f)
    
    conn = sqlite3.connect('app_store.db')
    cursor = conn.cursor()
    
    for user_id, activities in activities_data.items():
        for activity in activities:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO activities 
                    (id, user_id, activity_type, description, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    activity.get('id'),
                    user_id,
                    activity.get('type'),
                    activity.get('description'),
                    activity.get('timestamp', datetime.now().isoformat())
                ))
            except Exception as e:
                print(f"❌ Error migrating activity: {e}")
    
    conn.commit()
    conn.close()
    print("✅ Activities migrated successfully!")

def backup_json_files():
    """Create backup of all JSON files before migration"""
    backup_dir = PROJECT_DIR / 'backups' / 'json_backup'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    json_files = [
        'users.json',
        'apps_data.json',
        'collections.json',
        'activities.json',
        'analytics.json'
    ]
    
    for file in json_files:
        src = PROJECT_DIR / file
        if src.exists():
            dst = backup_dir / f"{file}.backup"
            shutil.copy2(src, dst)
            print(f"📁 Backed up {file}")
    
    print("✅ All JSON files backed up successfully!")

def verify_migration():
    """Verify that migration was successful"""
    conn = sqlite3.connect('app_store.db')
    cursor = conn.cursor()
    
    tables = [
        'users', 'apps', 'reviews', 'favorites', 'wishlist',
        'downloads_history', 'collections', 'activities', 'notifications'
    ]
    
    print("\n📊 Migration Verification:")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table.capitalize()}: {count} records")
    
    conn.close()
    print("-" * 40)
    print("✅ Migration verification complete!")

def main():
    """Main migration function"""
    print("🚀 Starting Database Migration...")
    print("=" * 50)
    
    # Step 1: Backup existing JSON files
    print("\n📦 Step 1: Backing up JSON files...")
    backup_json_files()
    
    # Step 2: Create database schema
    print("\n🏗️ Step 2: Creating database schema...")
    create_database()
    
    # Step 3: Migrate data
    print("\n📤 Step 3: Migrating data...")
    migrate_users()
    migrate_apps()
    migrate_collections()
    migrate_activities()
    
    # Step 4: Verify migration
    print("\n✔️ Step 4: Verifying migration...")
    verify_migration()
    
    print("\n" + "=" * 50)
    print("🎉 Migration completed successfully!")
    print("\nNext steps:")
    print("1. Update app.py to use SQLite instead of JSON files")
    print("2. Test all functionality with the new database")
    print("3. Keep JSON backups until you're sure everything works")

if __name__ == "__main__":
    main()
