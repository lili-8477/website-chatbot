#!/usr/bin/env python3
"""
Setup script for Website Chatbot
"""
import os
import shutil
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_env_file():
    """Copy .env.example to .env if it doesn't exist"""
    if os.path.exists(".env"):
        print("ℹ️  .env file already exists")
        return True
    
    if os.path.exists(".env.example"):
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from .env.example")
        print("⚠️  Please edit .env file and add your OpenAI API key")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def validate_setup():
    """Validate the setup"""
    print("\n🔍 Validating setup...")
    
    try:
        # Test imports
        from dotenv import load_dotenv
        load_dotenv()
        
        from utils.call_llm import call_llm
        from utils.web_scraper import scrape_website
        from flow import run_chatbot
        
        print("✅ All imports successful")
        
        # Check API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your-openai-api-key-here":
            print("⚠️  OpenAI API key not set. Please update .env file")
            return False
        
        print("✅ OpenAI API key configured")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Website Chatbot Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup .env file
    if not setup_env_file():
        return False
    
    # Validate setup
    if not validate_setup():
        print("\n⚠️  Setup completed with warnings.")
        print("Please update your .env file with a valid OpenAI API key")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Make sure your OpenAI API key is set in .env")
    print("2. Run: python test_chatbot.py (to test)")
    print("3. Run: python main.py (to start the server)")
    print("4. Open: http://localhost:8000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)