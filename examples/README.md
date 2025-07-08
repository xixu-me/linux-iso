# Examples

This directory contains example scripts demonstrating various ways to use the Linux ISO downloader.

## Available Examples

### 1. `download_specific.py`

Download only specific distributions (Ubuntu and Fedora in this example).

```bash
python examples/download_specific.py
```

**Features:**

- Downloads only Ubuntu and Fedora ISOs
- Uses fewer parallel workers (2) for demonstration
- Saves files to `./examples_output/`

### 2. `create_custom_categories.py`

Demonstrates how to create custom URL files for different categories of Linux distributions.

```bash
# Create category files and download lightweight distributions
python examples/create_custom_categories.py

# Download enterprise distributions
python examples/create_custom_categories.py --enterprise

# Show help
python examples/create_custom_categories.py --help
```

**Features:**

- Creates custom URL files for different distribution categories
- Lightweight distributions (Arch-based): Arch Linux, EndeavourOS, Manjaro
- Enterprise distributions (RHEL-based): AlmaLinux, Rocky Linux, Oracle Linux
- Organizes downloads into category-specific subdirectories

## Output Structure

When running examples, files are organized as follows:

```text
examples_output/
├── lightweight/          # From create_custom_categories.py
│   ├── archlinux-x86_64.iso
│   ├── EndeavourOS-Mercury-Neo-2025.03.19.iso
│   └── manjaro-gnome-25.0.4-250623-linux612.iso
├── enterprise/           # From create_custom_categories.py --enterprise
│   ├── AlmaLinux-10.0-x86_64-dvd.iso
│   ├── Rocky-10.0-x86_64-dvd1.iso
│   └── OracleLinux-R10-U0-x86_64-dvd.iso
└── ubuntu-24.04.2-desktop-amd64.iso  # From download_specific.py
└── Fedora-Workstation-Live-42-1.1.x86_64.iso
```

## Custom URL Files

The `create_custom_categories.py` script generates these URL files:

- `examples/lightweight_distros.txt` - Arch-based distributions
- `examples/enterprise_distros.txt` - Enterprise Linux distributions

You can modify these files or create your own custom URL files to download specific sets of distributions.

## Tips

1. **Start Small**: Begin with the `download_specific.py` example to understand the basic usage
2. **Custom Categories**: Use `create_custom_categories.py` as a template for your own categorization needs
3. **Modify URLs**: Edit the generated URL files in the `examples/` directory to customize which distributions to download
4. **Output Directories**: Each example uses different output directories to keep downloads organized

## Creating Your Own Examples

Use these examples as templates to create your own custom download scripts:

1. Import the `ISODownloader` class from `download_isos`
2. Define your list of URLs
3. Create a downloader instance with your preferred settings
4. Call `download_all()` with your URLs

```python
from download_isos import ISODownloader

# Your custom URLs
urls = ["https://example.com/distro.iso"]

# Create downloader
downloader = ISODownloader(
    output_dir="./my_downloads",
    max_workers=3,
    retry_attempts=5
)

# Download
successful, failed, results = downloader.download_all(urls)
```
