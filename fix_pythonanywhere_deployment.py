#!/usr/bin/env python3
"""
PythonAnywhere Deployment Fix Script
Fixes common issues when deploying the app store to PythonAnywhere
"""

import json
import os
import shutil
from pathlib import Path
import stat

def fix_file_paths():
    """Fix Windows-style paths to Unix-style paths"""
    print("🔧 Fixing file paths for Linux compatibility...")
    
    if not os.path.exists('apps_data.json'):
        print("❌ apps_data.json not found!")
        return False
    
    # Read the apps data
    with open('apps_data.json', 'r', encoding='utf-8') as f:
        apps = json.load(f)
    
    # Fix paths in apps data
    changes_made = False
    for app in apps:
        # Fix app_file_path if it exists
        if 'app_file_path' in app:
            old_path = app['app_file_path']
            # Convert Windows paths to Unix paths
            if '\\\\' in old_path or '\\' in old_path:
                # Replace Windows backslashes with forward slashes
                new_path = old_path.replace('\\\\', '/').replace('\\', '/')
                app['app_file_path'] = new_path
                changes_made = True
                print(f"  Fixed path: {old_path} -> {new_path}")
    
    # Save the fixed data
    if changes_made:
        with open('apps_data.json', 'w', encoding='utf-8') as f:
            json.dump(apps, f, indent=2, ensure_ascii=False)
        print("✅ File paths fixed and saved!")
    else:
        print("✅ No file path issues found")
    
    return True

def create_directory_structure():
    """Create necessary directories if they don't exist"""
    print("🔧 Creating directory structure...")
    
    directories = [
        'static',
        'static/images',
        'static/images/app_icons',
        'static/images/app_banners', 
        'static/images/screenshots',
        'Apps_Link',
        'data',
        'templates'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"  Created directory: {directory}")
        else:
            print(f"  ✅ Directory exists: {directory}")

def fix_permissions():
    """Fix file permissions for web server"""
    print("🔧 Fixing file permissions...")
    
    files_to_check = [
        'app.py',
        'apps_data.json',
        'users.json'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            # Make file readable and writable
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            print(f"  Fixed permissions for: {file_path}")

def create_default_files():
    """Create default files if they don't exist"""
    print("🔧 Creating default files...")
    
    # Create users.json if it doesn't exist
    if not os.path.exists('users.json'):
        default_users = {}
        with open('users.json', 'w') as f:
            json.dump(default_users, f, indent=2)
        print("  Created default users.json")
    
    # Create collections.json if it doesn't exist
    if not os.path.exists('collections.json'):
        default_collections = {}
        with open('collections.json', 'w') as f:
            json.dump(default_collections, f, indent=2)
        print("  Created default collections.json")
    
    # Create activities.json if it doesn't exist
    if not os.path.exists('activities.json'):
        default_activities = {}
        with open('activities.json', 'w') as f:
            json.dump(default_activities, f, indent=2)
        print("  Created default activities.json")

def verify_apps_data():
    """Verify apps_data.json is valid and contains data"""
    print("🔍 Verifying apps data...")
    
    if not os.path.exists('apps_data.json'):
        print("❌ apps_data.json file is missing!")
        print("   This is likely the main cause of your issue.")
        print("   You need to upload this file to PythonAnywhere.")
        return False
    
    try:
        with open('apps_data.json', 'r', encoding='utf-8') as f:
            apps = json.load(f)
        
        print(f"✅ Found {len(apps)} apps in data file:")
        for i, app in enumerate(apps, 1):
            status = "✅" if not app.get('featured', False) else "⭐"
            print(f"  {status} {i}. {app.get('name', 'Unknown')} by {app.get('developer', 'Unknown')}")
            print(f"      Category: {app.get('category', 'Unknown')}")
            print(f"      Featured: {app.get('featured', False)}")
            print(f"      Downloads: {app.get('downloads', 0)}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error reading apps_data.json: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_debug_info():
    """Create a debug info file to help troubleshoot on PythonAnywhere"""
    print("🔧 Creating debug information...")
    
    debug_info = {
        'files_found': [],
        'directories_found': [],
        'apps_count': 0,
        'featured_apps': 0,
        'trending_apps': 0,
        'recent_apps': 0
    }
    
    # Check for files
    important_files = [
        'app.py', 
        'apps_data.json', 
        'users.json',
        'manage_apps_enhanced.py'
    ]
    
    for file_path in important_files:
        if os.path.exists(file_path):
            debug_info['files_found'].append(file_path)
    
    # Check directories
    important_dirs = [
        'static', 
        'static/images', 
        'static/images/app_icons',
        'templates',
        'Apps_Link'
    ]
    
    for dir_path in important_dirs:
        if os.path.exists(dir_path):
            debug_info['directories_found'].append(dir_path)
    
    # Analyze apps data
    if os.path.exists('apps_data.json'):
        try:
            with open('apps_data.json', 'r', encoding='utf-8') as f:
                apps = json.load(f)
            
            debug_info['apps_count'] = len(apps)
            debug_info['featured_apps'] = len([app for app in apps if app.get('featured', False)])
            debug_info['trending_apps'] = len([app for app in apps if app.get('downloads', 0) > 0])
            debug_info['recent_apps'] = len(apps)  # All apps are considered recent
            
        except Exception as e:
            debug_info['error'] = str(e)
    
    # Write debug info
    with open('debug_info.json', 'w') as f:
        json.dump(debug_info, f, indent=2)
    
    print("✅ Debug info created in debug_info.json")

def add_debug_to_app():
    """Add debugging code to app.py to help identify the issue"""
    print("🔧 Adding debug code to app.py...")
    
    debug_code = '''
# === DEBUG CODE FOR PYTHONANYWHERE DEPLOYMENT ===
import sys
print("DEBUG: Python version:", sys.version, file=sys.stderr)
print("DEBUG: Current working directory:", os.getcwd(), file=sys.stderr)
print("DEBUG: Files in current directory:", os.listdir('.'), file=sys.stderr)
print("DEBUG: apps_data.json exists:", os.path.exists('apps_data.json'), file=sys.stderr)

def debug_load_apps():
    """Debug version of load_apps function"""
    print("DEBUG: Loading apps...", file=sys.stderr)
    if os.path.exists('apps_data.json'):
        try:
            with open('apps_data.json', 'r', encoding='utf-8') as f:
                apps = json.load(f)
            print(f"DEBUG: Loaded {len(apps)} apps successfully", file=sys.stderr)
            for i, app in enumerate(apps[:3]):  # Show first 3 apps
                print(f"DEBUG: App {i+1}: {app.get('name')} - Featured: {app.get('featured', False)}", file=sys.stderr)
            return apps
        except Exception as e:
            print(f"DEBUG: Error loading apps: {e}", file=sys.stderr)
            return []
    else:
        print("DEBUG: apps_data.json file not found!", file=sys.stderr)
        return []

# Override the load_apps function temporarily
original_load_apps = load_apps
load_apps = debug_load_apps
'''
    
    # Read current app.py content
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if debug code is already added
    if 'DEBUG: Python version' in content:
        print("  Debug code already exists in app.py")
        return
    
    # Find where to insert debug code (after imports)
    lines = content.split('\n')
    insert_index = 0
    
    # Find the end of imports
    for i, line in enumerate(lines):
        if line.startswith('app = Flask(__name__)'):
            insert_index = i
            break
    
    # Insert debug code
    if insert_index > 0:
        debug_lines = debug_code.strip().split('\n')
        lines[insert_index:insert_index] = debug_lines
        
        # Write back to file
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print("✅ Debug code added to app.py")
        print("   Check your PythonAnywhere error logs after deployment!")
    else:
        print("❌ Could not add debug code to app.py")

def main():
    """Run all deployment fixes"""
    print("🚀 PythonAnywhere Deployment Fix Script")
    print("=" * 50)
    
    success = True
    
    # Step 1: Verify apps data
    if not verify_apps_data():
        success = False
        print("\n❌ CRITICAL: Missing or invalid apps_data.json")
        print("   Solution: Upload your apps_data.json file to PythonAnywhere")
    
    # Step 2: Create directory structure
    create_directory_structure()
    
    # Step 3: Fix file paths
    fix_file_paths()
    
    # Step 4: Fix permissions
    fix_permissions()
    
    # Step 5: Create default files
    create_default_files()
    
    # Step 6: Create debug info
    create_debug_info()
    
    # Step 7: Add debug code
    add_debug_to_app()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Deployment fixes completed!")
        print("\n📋 Next Steps for PythonAnywhere:")
        print("1. Upload all files to PythonAnywhere (especially apps_data.json)")
        print("2. Make sure static/images/app_icons/ contains your app icons")
        print("3. Check error logs in PythonAnywhere dashboard")
        print("4. Restart your web app")
    else:
        print("⚠️  Some issues found - check messages above")
        print("   Main issue: apps_data.json is missing or invalid")
    
    print("\n🔧 If issues persist, check the debug_info.json file")

if __name__ == "__main__":
    main()
