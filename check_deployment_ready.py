#!/usr/bin/env python3
"""
Deployment readiness checker for ai-builders.space
"""
import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False

def check_dockerfile():
    """Check Dockerfile requirements"""
    print("\n🐳 Checking Dockerfile...")
    
    if not check_file_exists("Dockerfile", "Dockerfile exists"):
        return False
    
    with open("Dockerfile", "r") as f:
        content = f.read()
    
    checks = [
        ("python:3.11-slim" in content, "Uses Python 3.11 slim base image"),
        ("EXPOSE" in content, "Exposes port"),
        ('CMD sh -c' in content, "Uses shell form CMD for PORT expansion"),
        ("${PORT:-8000}" in content, "Uses PORT environment variable with fallback"),
        ("uvicorn main:app" in content, "Starts correct application"),
    ]
    
    all_passed = True
    for check, description in checks:
        if check:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            all_passed = False
    
    return all_passed

def check_main_py():
    """Check main.py configuration"""
    print("\n🐍 Checking main.py...")
    
    if not check_file_exists("main.py", "Main application file exists"):
        return False
    
    with open("main.py", "r") as f:
        content = f.read()
    
    checks = [
        ('os.getenv("PORT"' in content, "Reads PORT from environment"),
        ("FastAPI" in content, "Uses FastAPI framework"),
        ("StaticFiles" in content, "Serves static files"),
        ("uvicorn.run" in content, "Has uvicorn server setup"),
    ]
    
    all_passed = True
    for check, description in checks:
        if check:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            all_passed = False
    
    return all_passed

def check_static_files():
    """Check static file configuration"""
    print("\n📁 Checking static files...")
    
    if not os.path.exists("static"):
        print("❌ Static directory not found")
        return False
    
    static_files = ["index.html", "style.css", "script.js"]
    all_passed = True
    
    for file in static_files:
        filepath = f"static/{file}"
        if check_file_exists(filepath, f"Frontend file"):
            pass
        else:
            all_passed = False
    
    return all_passed

def check_requirements():
    """Check requirements.txt"""
    print("\n📦 Checking requirements.txt...")
    
    if not check_file_exists("requirements.txt", "Requirements file exists"):
        return False
    
    with open("requirements.txt", "r") as f:
        content = f.read()
    
    required_packages = ["fastapi", "uvicorn", "pocketflow", "requests", "beautifulsoup4"]
    all_found = True
    
    for package in required_packages:
        if package in content:
            print(f"✅ {package} found in requirements")
        else:
            print(f"❌ {package} NOT found in requirements")
            all_found = False
    
    return all_found

def check_git_status():
    """Check git status"""
    print("\n📡 Checking Git status...")
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            print("❌ Uncommitted changes found:")
            print(result.stdout)
            print("Please commit and push all changes before deployment")
            return False
        else:
            print("✅ No uncommitted changes")
        
        # Check if we have a remote
        remote_result = subprocess.run(["git", "remote", "-v"], 
                                     capture_output=True, text=True, check=True)
        
        if "github.com" in remote_result.stdout:
            print("✅ GitHub remote found")
            return True
        else:
            print("❌ No GitHub remote found")
            return False
            
    except subprocess.CalledProcessError:
        print("❌ Not a git repository or git not available")
        return False

def check_env_security():
    """Check environment file security"""
    print("\n🔒 Checking environment security...")
    
    # Check if .env is in .gitignore
    gitignore_ok = False
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
            if ".env" in gitignore_content:
                print("✅ .env files ignored in .gitignore")
                gitignore_ok = True
    
    if not gitignore_ok:
        print("❌ .env should be added to .gitignore")
    
    # Check if .env.example exists
    example_exists = check_file_exists(".env.example", "Environment example file")
    
    return gitignore_ok and example_exists

def main():
    """Main deployment readiness checker"""
    print("🚀 AI Builders Space Deployment Readiness Checker")
    print("=" * 50)
    
    checks = [
        ("Dockerfile", check_dockerfile),
        ("Main Application", check_main_py),
        ("Static Files", check_static_files),
        ("Requirements", check_requirements),
        ("Git Repository", check_git_status),
        ("Environment Security", check_env_security),
    ]
    
    all_passed = True
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append((name, False))
            all_passed = False
    
    print("\n" + "=" * 50)
    print("📋 DEPLOYMENT READINESS SUMMARY")
    print("=" * 50)
    
    for name, passed in results:
        status = "✅ READY" if passed else "❌ NEEDS FIX"
        print(f"{name:<20}: {status}")
    
    if all_passed:
        print("\n🎉 READY FOR DEPLOYMENT!")
        print("\nNext steps:")
        print("1. Ensure all changes are committed and pushed to GitHub")
        print("2. Prepare deployment information:")
        print("   - GitHub repository URL")
        print("   - Service name for your deployment")
        print("   - Git branch to deploy (e.g., 'main')")
        print("3. Contact your instructor or use the deployment API")
        return 0
    else:
        print("\n⚠️  NOT READY FOR DEPLOYMENT")
        print("Please fix the issues above before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())