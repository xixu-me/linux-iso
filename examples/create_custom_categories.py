#!/usr/bin/env python3
"""
Example script demonstrating how to create custom URL files and download
specific sets of distributions.
This example shows how to create different categories of Linux distributions.
"""

import os

from download_isos import ISODownloader


def create_lightweight_distros():
    """Create a URL file for lightweight Linux distributions."""
    lightweight_urls = [
        "https://geo.mirror.pkgbuild.com/iso/2025.07.01/archlinux-x86_64.iso",
        "https://mirrors.gigenet.com/endeavouros/iso/EndeavourOS_Mercury-Neo-2025.03.19.iso",
        "https://download.manjaro.org/gnome/25.0.4/manjaro-gnome-25.0.4-250623-linux612.iso",
    ]

    with open("examples/lightweight_distros.txt", "w") as f:
        for url in lightweight_urls:
            f.write(url + "\n")

    print("✅ Created lightweight_distros.txt")


def create_enterprise_distros():
    """Create a URL file for enterprise Linux distributions."""
    enterprise_urls = [
        "https://repo.almalinux.org/almalinux/10/isos/x86_64/AlmaLinux-10.0-x86_64-dvd.iso",
        "https://download.rockylinux.org/pub/rocky/10/isos/x86_64/Rocky-10.0-x86_64-dvd1.iso",
        "https://yum.oracle.com/ISOS/OracleLinux/OL10/u0/x86_64/OracleLinux-R10-U0-x86_64-dvd.iso",
    ]

    with open("examples/enterprise_distros.txt", "w") as f:
        for url in enterprise_urls:
            f.write(url + "\n")

    print("✅ Created enterprise_distros.txt")


def download_category(url_file, category_name):
    """Download ISOs from a specific category URL file."""
    print(f"\n🐧 Downloading {category_name} distributions...")

    # Read URLs from the category file
    try:
        with open(url_file) as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Error: {url_file} not found!")
        return

    if not urls:
        print(f"❌ No URLs found in {url_file}")
        return

    print(f"📋 Found {len(urls)} URLs to download")

    # Create output directory based on category
    output_dir = f"./examples_output/{category_name.lower().replace(' ', '_')}"

    # Create downloader instance
    downloader = ISODownloader(output_dir=output_dir, max_workers=3, retry_attempts=3)

    # Download the files
    successful, failed, results = downloader.download_all(urls)

    print(f"\n✅ Successfully downloaded: {successful} files")
    if failed > 0:
        print(f"❌ Failed downloads: {failed}")
        for result in results:
            print(f"  - {result}")

    print(f"\n📂 Files saved to: {os.path.abspath(output_dir)}")


def main():
    """Main function to demonstrate custom URL file creation and usage."""
    print("🔧 Creating custom URL files for different distribution categories...")

    # Create the examples directory if it doesn't exist
    os.makedirs("examples", exist_ok=True)

    # Create category-specific URL files
    create_lightweight_distros()
    create_enterprise_distros()

    print("\n📋 Available categories:")
    print("  1. Lightweight distributions (Arch-based)")
    print("  2. Enterprise distributions (RHEL-based)")

    # Example: Download lightweight distributions
    print("\n" + "=" * 50)
    download_category("examples/lightweight_distros.txt", "Lightweight")

    print("\n" + "=" * 50)
    print("💡 To download enterprise distributions, run:")
    print("   python examples/create_custom_categories.py --enterprise")


if __name__ == "__main__":
    import sys

    if "--enterprise" in sys.argv:
        download_category("examples/enterprise_distros.txt", "Enterprise")
    elif "--help" in sys.argv or "-h" in sys.argv:
        print("Usage:")
        print("  python examples/create_custom_categories.py")
        print("      # Create files and download lightweight")
        print("  python examples/create_custom_categories.py --enterprise")
        print("      # Download enterprise distributions")
    else:
        main()
