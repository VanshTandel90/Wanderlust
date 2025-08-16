#!/usr/bin/env python3
"""
Simple test script to verify basic Python functionality
"""

def test_basic_python():
    """Test basic Python functionality"""
    print("🧪 Testing Basic Python...")
    
    try:
        # Test basic operations
        result = 2 + 2
        assert result == 4, "Basic math failed"
        print("✅ Basic math operations work")
        
        # Test string operations
        text = "Hello, World!"
        assert len(text) == 13, "String operations failed"
        print("✅ String operations work")
        
        # Test list operations
        numbers = [1, 2, 3, 4, 5]
        assert sum(numbers) == 15, "List operations failed"
        print("✅ List operations work")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic Python test failed: {e}")
        return False

def test_imports():
    """Test if we can import basic modules"""
    print("\n🧪 Testing Basic Imports...")
    
    try:
        import os
        print("✅ os module imported")
        
        import sys
        print("✅ sys module imported")
        
        import json
        print("✅ json module imported")
        
        import datetime
        print("✅ datetime module imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_python_version():
    """Check Python version"""
    print("\n🧪 Checking Python Version...")
    
    import sys
    version = sys.version_info
    
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python version too old. Need 3.8+")
        return False

def main():
    """Run all basic tests"""
    print("🚀 Starting Basic Python Tests...\n")
    
    tests = [
        ("Basic Python", test_basic_python),
        ("Basic Imports", test_imports),
        ("Python Version", test_python_version)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed\n")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}\n")
    
    print("=" * 50)
    print(f"📊 Basic Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Basic Python functionality is working!")
        print("\n🚀 Next steps:")
        print("   1. Run: python install_deps.py")
        print("   2. Then run: python test_demo.py")
    else:
        print("⚠️  Some basic tests failed. Please check your Python installation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 