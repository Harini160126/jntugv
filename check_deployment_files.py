#!/usr/bin/env python3
"""
Check for missing files in last site deploy
"""

import os
import sys
import requests
from urllib.parse import urljoin

def check_local_files():
    """Check local project files"""
    
    print("🔍 Checking Local Project Files")
    print("=" * 50)
    
    # Essential files for deployment
    essential_files = {
        'app.py': 'Main Flask application',
        'requirements.txt': 'Python dependencies',
        'templates/login.html': 'Login template',
        'templates/login_fixed.html': 'Fixed login template',
        'templates/admin_login.html': 'Admin login template',
        'templates/register.html': 'Registration template',
        'templates/base.html': 'Base template',
        'static/css/': 'CSS stylesheets',
        'static/js/': 'JavaScript files',
        'static/images/': 'Image assets',
        'database_manager.py': 'Database abstraction',
        'firebase_config.py': 'Firebase configuration',
        '.env': 'Environment variables',
        '.gitignore': 'Git ignore rules'
    }
    
    missing_files = []
    found_files = []
    
    for file_path, description in essential_files.items():
        if os.path.exists(file_path):
            found_files.append(f"✅ {file_path} - {description}")
        else:
            missing_files.append(f"❌ {file_path} - {description}")
    
    print("📋 Essential Files Status:")
    for item in found_files + missing_files:
        print(f"   {item}")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Found: {len(found_files)} files")
    print(f"   ❌ Missing: {len(missing_files)} files")
    
    return len(missing_files) == 0

def check_deployment_status():
    """Check deployment status for common platforms"""
    
    print("\n🌐 Checking Deployment Status")
    print("=" * 50)
    
    # Common deployment URLs
    deployment_urls = [
        'https://teamx-seven.vercel.app',
        'https://pytech-arena.netlify.app',
        'https://pytech-arena.onrender.com',
        'https://pytech-arena.pythonanywhere.com'
    ]
    
    for url in deployment_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {url} - LIVE (Status: {response.status_code})")
            elif response.status_code == 404:
                print(f"   ❌ {url} - NOT FOUND (Status: {response.status_code})")
            elif response.status_code == 500:
                print(f"   ⚠️  {url} - SERVER ERROR (Status: {response.status_code})")
            else:
                print(f"   ⚠️  {url} - ISSUE (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {url} - UNREACHABLE ({str(e)[:50]}...)")

def check_serverless_functions():
    """Check serverless function files for Vercel"""
    
    print("\n🔧 Checking Serverless Functions")
    print("=" * 50)
    
    api_files = {
        'api/index.py': 'Main API function',
        'api/minimal.py': 'Minimal serverless function',
        'api/working.py': 'Working serverless function',
        'vercel.json': 'Vercel configuration',
        'package.json': 'Node.js configuration'
    }
    
    missing_api = []
    found_api = []
    
    for file_path, description in api_files.items():
        if os.path.exists(file_path):
            found_api.append(f"✅ {file_path} - {description}")
        else:
            missing_api.append(f"❌ {file_path} - {description}")
    
    print("📋 Serverless Files Status:")
    for item in found_api + missing_api:
        print(f"   {item}")
    
    print(f"\n📊 Serverless Summary:")
    print(f"   ✅ Found: {len(found_api)} files")
    print(f"   ❌ Missing: {len(missing_api)} files")
    
    return len(missing_api) == 0

def check_database_files():
    """Check database-related files"""
    
    print("\n🗄️ Checking Database Files")
    print("=" * 50)
    
    db_files = {
        'placement.db': 'SQLite database',
        'models.py': 'Database models',
        'database_manager.py': 'Database manager',
        'firebase_config.py': 'Firebase config'
    }
    
    missing_db = []
    found_db = []
    
    for file_path, description in db_files.items():
        if os.path.exists(file_path):
            found_db.append(f"✅ {file_path} - {description}")
        else:
            missing_db.append(f"❌ {file_path} - {description}")
    
    print("📋 Database Files Status:")
    for item in found_db + missing_db:
        print(f"   {item}")
    
    print(f"\n📊 Database Summary:")
    print(f"   ✅ Found: {len(found_db)} files")
    print(f"   ❌ Missing: {len(missing_db)} files")

def check_static_assets():
    """Check static assets"""
    
    print("\n🎨 Checking Static Assets")
    print("=" * 50)
    
    static_dirs = {
        'static/css/': 'CSS stylesheets',
        'static/js/': 'JavaScript files',
        'static/images/': 'Image assets'
    }
    
    missing_static = []
    found_static = []
    
    for dir_path, description in static_dirs.items():
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            count = len(files)
            if count > 0:
                found_static.append(f"✅ {dir_path} - {description} ({count} files)")
            else:
                missing_static.append(f"⚠️  {dir_path} - {description} (empty)")
        else:
            missing_static.append(f"❌ {dir_path} - {description}")
    
    print("📋 Static Assets Status:")
    for item in found_static + missing_static:
        print(f"   {item}")
    
    print(f"\n📊 Static Summary:")
    print(f"   ✅ Found: {len(found_static)} directories")
    print(f"   ❌ Missing: {len(missing_static)} directories")

def generate_deployment_report():
    """Generate comprehensive deployment report"""
    
    print("\n📊 DEPLOYMENT READINESS REPORT")
    print("=" * 60)
    
    # Check all components
    local_ok = check_local_files()
    api_ok = check_serverless_functions()
    check_database_files()
    check_static_assets()
    
    # Check deployment status
    check_deployment_status()
    
    print(f"\n🎯 OVERALL STATUS:")
    if local_ok and api_ok:
        print("   ✅ PROJECT IS READY FOR DEPLOYMENT")
        print("   🚀 All essential files are present")
        print("   🌐 Ready to deploy to any platform")
    else:
        print("   ⚠️  PROJECT NEEDS ATTENTION")
        print("   🔧 Fix missing files before deployment")
    
    print(f"\n📋 RECOMMENDATIONS:")
    print("   1. Fix any missing essential files")
    print("   2. Ensure static assets are included")
    print("   3. Test serverless functions locally")
    print("   4. Verify database connectivity")
    print("   5. Check deployment platform requirements")

if __name__ == "__main__":
    print("🚀 PyTech Arena - Deployment File Checker")
    print("=" * 60)
    
    try:
        generate_deployment_report()
    except KeyboardInterrupt:
        print("\n\n⚠️  Check interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during check: {str(e)}")
    
    print("\n🎉 Deployment check completed!")
