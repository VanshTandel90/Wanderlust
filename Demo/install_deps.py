#!/usr/bin/env python3
"""
Simple dependency installer for Python 3.12 compatibility
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install all required dependencies"""
    print("🚀 Installing Dependencies for Python 3.12...")
    print("=" * 50)
    
    # List of packages to install
    packages = [
        "numpy",
        "Pillow", 
        "scikit-learn"
    ]
    
    success_count = 0
    total_packages = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"📊 Installation Results: {success_count}/{total_packages} packages installed")
    
    if success_count == total_packages:
        print("🎉 All dependencies installed successfully!")
        print("\n🚀 You can now run:")
        print("   python test_demo.py")
    else:
        print("⚠️  Some packages failed to install. Please check the errors above.")
    
    return success_count == total_packages

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 