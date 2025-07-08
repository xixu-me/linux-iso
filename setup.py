#!/usr/bin/env python3
"""
Setup script to help users get started with the Linux ISO downloader.
This script checks dependencies and provides initial setup guidance.
"""

import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("❌ Python 3.6 or higher is required.")
        print(f"   Current version: Python {version.major}.{version.minor}")
        return False

    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import requests

        print(f"✅ requests {requests.__version__} - Installed")
    except ImportError:
        print("❌ requests library not found")
        return False

    try:
        import tqdm

        print(f"✅ tqdm {tqdm.__version__} - Installed")
    except ImportError:
        print("❌ tqdm library not found")
        return False

    return True


def install_dependencies():
    """Install required dependencies."""
    print("\n🔧 Installing dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def create_output_directory():
    """Create the default output directory."""
    output_dir = Path("./isos")
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created output directory: {output_dir.absolute()}")
    else:
        print(f"✅ Output directory already exists: {output_dir.absolute()}")


def check_urls_file():
    """Check if the URLs file exists."""
    urls_file = Path("urls.txt")
    if urls_file.exists():
        with open(urls_file) as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"✅ Found {len(urls)} URLs in urls.txt")
        return True
    else:
        print("❌ urls.txt file not found")
        return False


def print_usage_examples():
    """Print usage examples."""
    print("\n" + "=" * 60)
    print("🚀 QUICK START EXAMPLES")
    print("=" * 60)

    print("\n1. Download all Linux ISOs:")
    print("   python download_isos.py")

    print("\n2. Download with custom settings:")
    print("   python download_isos.py --max-workers 3 --retries 5")

    print("\n3. Download to custom directory:")
    print("   python download_isos.py --output-dir /path/to/downloads")

    print("\n4. Run example scripts:")
    print("   python examples/download_specific.py")
    print("   python examples/create_custom_categories.py")

    print("\n5. Get help:")
    print("   python download_isos.py --help")

    print("\n" + "=" * 60)
    print("📋 WHAT'S INCLUDED")
    print("=" * 60)
    print("• 17 Linux distributions in urls.txt")
    print("• Parallel downloading with progress bars")
    print("• Automatic resume for interrupted downloads")
    print("• Example scripts in the examples/ directory")
    print("• Comprehensive error handling and retry logic")


def main():
    """Main setup function."""
    print("🐧 Linux ISO Downloader Setup")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Check if dependencies are already installed
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_dependencies():
            print("\n❌ Setup failed. Please install dependencies manually:")
            print("   pip install -r requirements.txt")
            sys.exit(1)

        # Verify installation
        print("\n🔍 Verifying installation...")
        if not check_dependencies():
            print("❌ Dependency verification failed")
            sys.exit(1)

    # Create output directory
    print("\n📁 Setting up directories...")
    create_output_directory()

    # Check URLs file
    print("\n🔗 Checking URL configuration...")
    check_urls_file()

    # Print usage examples
    print_usage_examples()

    print("\n✅ Setup complete! You're ready to download Linux ISOs.")
    print("\n💡 Tip: Start with 'python download_isos.py --help' to see all options.")


if __name__ == "__main__":
    main()
