#!/usr/bin/env python3
"""
Quick Deployment Verification Script
Run this on PythonAnywhere to verify your deployment
"""

import json
import os
import sys

def check_deployment():
    """Check if deployment is correct"""
    print("🔍 PythonAnywhere Deployment Verification")
    print("=" * 40)
    
    issues = []
    success = []
    
    # Check critical files
    critical_files = [
        'apps_data.json',
        'app.py',
        'templates/index.html'
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            success.append(f"✅ {file_path} found")
        else:
            issues.append(f"❌ MISSING: {file_path}")
    
    # Check directories
    critical_dirs = [
        'templates',
        'static',
        'static/images',
        'static/images/app_icons'
    ]
    
    for dir_path in critical_dirs:
        if os.path.exists(dir_path):
            success.append(f"✅ {dir_path}/ directory exists")
        else:
            issues.append(f"❌ MISSING: {dir_path}/ directory")
    
    # Check apps data
    if os.path.exists('apps_data.json'):
        try:
            with open('apps_data.json', 'r', encoding='utf-8') as f:
                apps = json.load(f)
            
            success.append(f"✅ apps_data.json contains {len(apps)} apps")
            
            featured_count = len([app for app in apps if app.get('featured', False)])
            if featured_count > 0:
                success.append(f"✅ {featured_count} featured apps found")
            else:
                issues.append("⚠️  No featured apps (this is why 'Featured Apps' section is empty)")
            
            # Check for app icons
            for app in apps:
                icon_path = f"static/images/app_icons/{app.get('icon', '')}"
                if os.path.exists(icon_path):
                    success.append(f"✅ App icon found: {app.get('icon')}")
                else:
                    issues.append(f"❌ MISSING app icon: {icon_path}")
                    
        except Exception as e:
            issues.append(f"❌ Error reading apps_data.json: {e}")
    
    # Print results
    print("\n🎉 WORKING CORRECTLY:")
    for item in success:
        print(f"  {item}")
    
    if issues:
        print("\n🚨 ISSUES FOUND:")
        for item in issues:
            print(f"  {item}")
        print(f"\n📊 Summary: {len(success)} OK, {len(issues)} issues")
        return False
    else:
        print(f"\n🎉 ALL GOOD! {len(success)} checks passed")
        return True

def main():
    print("Current working directory:", os.getcwd())
    print("Python version:", sys.version)
    print("Files in current directory:", sorted(os.listdir('.')))
    print()
    
    if check_deployment():
        print("\n✅ Your deployment looks correct!")
        print("If apps still don't show, check your web app error logs.")
    else:
        print("\n🔧 Fix the issues above and restart your web app.")

if __name__ == "__main__":
    main()
