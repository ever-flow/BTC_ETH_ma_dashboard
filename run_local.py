#!/usr/bin/env python3
"""
Local development runner script
Provides easy commands for local development and testing
"""

import subprocess
import sys
import os
import argparse
import time
from pathlib import Path

def run_command(command, shell=True):
    """Run shell command and return result"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def setup_environment():
    """Setup local development environment"""
    print("🔧 Setting up local development environment...")

    # Create virtual environment if it doesn't exist
    if not Path("venv").exists():
        print("Creating virtual environment...")
        if not run_command("python -m venv venv"):
            return False

    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate && "
    else:
        activate_cmd = "source venv/bin/activate && "

    print("Installing dependencies...")
    if not run_command(f"{activate_cmd}pip install -r requirements.txt"):
        return False

    print("✅ Environment setup complete!")
    return True

def run_analysis():
    """Run crypto analysis"""
    print("📊 Running crypto analysis...")
    if not run_command("python data_processor.py"):
        return False
    print("✅ Analysis complete!")
    return True

def start_app():
    """Start Streamlit app"""
    print("🚀 Starting Streamlit app...")
    print("Opening in browser at http://localhost:8501")
    os.system("streamlit run enhanced_app.py")

def run_tests():
    """Run test suite"""
    print("🧪 Running tests...")
    if Path("tests").exists():
        return run_command("python -m pytest tests/ -v")
    else:
        print("No tests directory found. Creating basic test structure...")
        create_test_structure()
        return True

def create_test_structure():
    """Create basic test structure"""
    test_dir = Path("tests")
    test_dir.mkdir(exist_ok=True)

    # Create __init__.py
    (test_dir / "__init__.py").write_text("")

    # Create basic test file
    test_content = """import pytest
import pandas as pd
from data_processor import CryptoStrategyAnalyzer
from config import Config

def test_config_loading():
    \"\"\"Test configuration loading\"\"\"
    config = Config()
    assert config.DATA_START_DATE is not None
    assert config.STRATEGIES is not None

def test_analyzer_initialization():
    \"\"\"Test analyzer initialization\"\"\"
    analyzer = CryptoStrategyAnalyzer()
    assert analyzer is not None
    assert hasattr(analyzer, 'strategies')

def test_crypto_data_structure():
    \"\"\"Test crypto data structure\"\"\"
    analyzer = CryptoStrategyAnalyzer()
    # Mock test - in real implementation, test with sample data
    assert analyzer.strategies is not None

if __name__ == "__main__":
    pytest.main([__file__])
"""

    (test_dir / "test_basic.py").write_text(test_content)
    print("✅ Test structure created!")

def clean_data():
    """Clean generated data files"""
    print("🧹 Cleaning data files...")
    files_to_remove = [
        "strategy_results.json",
        "crypto_analyzer.log",
        "scheduler.log"
    ]

    for file in files_to_remove:
        if Path(file).exists():
            os.remove(file)
            print(f"Removed {file}")

    print("✅ Cleanup complete!")

def deploy_check():
    """Check deployment readiness"""
    print("🔍 Checking deployment readiness...")

    required_files = [
        "enhanced_app.py",
        "data_processor.py", 
        "config.py",
        "requirements.txt",
        "Dockerfile"
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False

    # Check if analysis can run
    try:
        from data_processor import CryptoStrategyAnalyzer
        analyzer = CryptoStrategyAnalyzer()
        print("✅ Data processor imports successfully")
    except Exception as e:
        print(f"❌ Data processor import failed: {e}")
        return False

    # Check if app can import
    try:
        import enhanced_app
        print("✅ Enhanced app imports successfully")
    except Exception as e:
        print(f"❌ Enhanced app import failed: {e}")
        return False

    print("✅ Deployment check passed!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Local development helper")
    parser.add_argument("command", choices=[
        "setup", "analysis", "app", "test", "clean", "deploy-check", "all"
    ], help="Command to run")

    args = parser.parse_args()

    if args.command == "setup":
        setup_environment()
    elif args.command == "analysis":
        run_analysis()
    elif args.command == "app":
        start_app()
    elif args.command == "test":
        run_tests()
    elif args.command == "clean":
        clean_data()
    elif args.command == "deploy-check":
        deploy_check()
    elif args.command == "all":
        print("🚀 Running complete setup and test...")
        if (setup_environment() and 
            run_analysis() and 
            deploy_check()):
            print("✅ All checks passed! Ready to start app.")
            print("Run: python run_local.py app")
        else:
            print("❌ Setup failed. Please check errors above.")

if __name__ == "__main__":
    main()
