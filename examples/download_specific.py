#!/usr/bin/env python3
"""
Example script demonstrating how to use the ISO downloader for specific distributions.
This script shows how to download only Ubuntu and Fedora ISOs.
"""

import os

from download_isos import ISODownloader


def main():
    # Define specific URLs for Ubuntu and Fedora
    ubuntu_fedora_urls = [
        "https://releases.ubuntu.com/noble/ubuntu-24.04.2-desktop-amd64.iso",
        "https://download.fedoraproject.org/pub/fedora/linux/releases/42/Workstation/x86_64/iso/Fedora-Workstation-Live-42-1.1.x86_64.iso",
    ]

    print("🐧 Downloading Ubuntu and Fedora ISOs...")
    print("📁 Output directory: ./examples_output")

    # Create downloader instance
    downloader = ISODownloader(
        output_dir="./examples_output",
        max_workers=2,  # Use fewer workers for this example
        retry_attempts=3,
    )

    # Download the files
    successful, failed, results = downloader.download_all(ubuntu_fedora_urls)

    print(f"\n✅ Successfully downloaded: {successful} files")
    if failed > 0:
        print(f"❌ Failed downloads: {failed}")
        for result in results:
            print(f"  - {result}")

    print(f"\n📂 Files saved to: {os.path.abspath('./examples_output')}")


if __name__ == "__main__":
    main()
