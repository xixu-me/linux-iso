# Linux ISO Downloader

A Python utility for downloading Linux distribution ISO files in parallel with resume capability, progress tracking, and robust error handling.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/xixu-me/linux-iso.git
cd linux-iso

# Run the setup script (recommended for first-time users)
python setup.py

# Or install dependencies manually
pip install -r requirements.txt

# Start downloading all Linux ISOs
python download_isos.py
```

## ⭐ Features

- **⚡ Parallel Downloads**: Download multiple ISO files simultaneously with configurable worker threads
- **🔄 Resume Support**: Automatically resume interrupted downloads
- **📊 Progress Tracking**: Real-time progress bars for each download
- **🔁 Retry Logic**: Configurable retry attempts with exponential backoff
- **🛡️ Error Handling**: Robust error handling with detailed failure reporting
- **⚙️ Flexible Configuration**: Command-line options for all parameters

## 🐧 Supported Distributions

The included `urls.txt` contains direct links to the latest stable releases of popular Linux distributions:

| Distribution | Architecture | Version |
|--------------|-------------|---------|
| AlmaLinux | x86_64 | 10.0 |
| Arch Linux | x86_64 | Latest |
| CachyOS | x86_64 | Latest |
| CentOS | x86_64 | 7.9/8.5 |
| Debian | amd64 | 12.11.0 |
| EndeavourOS | x86_64 | Latest |
| Fedora | x86_64 | 42 |
| Kali Linux | amd64 | 2025.2 |
| Linux Mint | x86_64 | 22.1 |
| Manjaro | x86_64 | 25.0.4 |
| openEuler | x86_64 | 24.03-LTS-SP2 |
| Pop!_OS | amd64 | 22.04 |
| openSUSE | x86_64 | Tumbleweed |
| Oracle Linux | x86_64 | 10.0 |
| Rocky Linux | x86_64 | 10.0 |
| Ubuntu | amd64 | 24.04.2 |

## 📦 Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Download all ISOs from the default `urls.txt` file:

```bash
python download_isos.py
```

### Advanced Usage

```bash
python download_isos.py --urls-file custom_urls.txt --output-dir /path/to/isos --max-workers 10 --retries 3
```

### Command Line Options

- `--urls-file`: File containing URLs to download (default: `urls.txt`)
- `--output-dir`: Directory to save downloaded files (default: `./isos`)
- `--max-workers`: Maximum number of parallel downloads (default: 5)
- `--retries`: Number of retry attempts per file (default: 5)
- `--chunk-size`: Chunk size for downloading in bytes (default: 8192)

### Help

```bash
python download_isos.py --help
```

## URL File Format

The URL file should contain one URL per line. Empty lines are ignored. Example:

```text
https://releases.ubuntu.com/24.04/ubuntu-24.04.2-desktop-amd64.iso
https://download.fedoraproject.org/pub/fedora/linux/releases/42/Workstation/x86_64/iso/Fedora-Workstation-Live-42-1.1.x86_64.iso
```

## Examples

### Download with Custom Settings

```bash
# Use 8 parallel workers and save to custom directory
python download_isos.py --max-workers 8 --output-dir ~/Downloads/linux-isos

# Use custom URL file with different retry settings
python download_isos.py --urls-file my_distros.txt --retries 10
```

### Download Single Distribution

Create a custom URL file with just one distribution:

```bash
echo "https://releases.ubuntu.com/24.04/ubuntu-24.04.2-desktop-amd64.iso" > ubuntu.txt
python download_isos.py --urls-file ubuntu.txt
```

## 📚 Examples

The `examples/` directory contains sample scripts demonstrating various usage patterns:

- **`download_specific.py`** - Download only specific distributions (Ubuntu + Fedora)
- **`create_custom_categories.py`** - Create and use custom distribution categories

See the [examples README](examples/README.md) for detailed usage instructions.

## Output

The script provides real-time progress information:

- Individual progress bars for each file
- Download speed and ETA
- Success/failure summary
- Detailed error reporting for failed downloads

## Error Handling

- **Network Issues**: Automatic retry with exponential backoff
- **Interrupted Downloads**: Resume from where it left off
- **Invalid URLs**: Detailed error messages
- **Disk Space**: Handles low disk space gracefully
- **Permissions**: Clear error messages for permission issues

## Performance Tips

1. **Optimal Worker Count**: Start with 5 workers and adjust based on your network and system performance
2. **Chunk Size**: Default 8KB works well for most cases; increase for faster networks
3. **Retry Attempts**: Increase for unreliable connections
4. **Resume Downloads**: The script automatically resumes interrupted downloads

## Troubleshooting

### Common Issues

**Downloads are slow:**

- Reduce `--max-workers` if you have limited bandwidth
- Check your internet connection
- Some mirrors may be slower than others

**Downloads fail repeatedly:**

- Increase `--retries` for unreliable connections
- Check if the URLs are still valid
- Verify you have write permissions to the output directory

**Out of disk space:**

- Check available disk space before starting large downloads
- Use `--output-dir` to specify a location with more space

## 🏆 Acknowledgments

- Thanks to all the Linux distribution maintainers for providing direct download links
- Built with Python's `requests` library for HTTP handling
- Uses `tqdm` for beautiful progress bars
- Implements concurrent downloads with `concurrent.futures`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool downloads files from third-party servers. Please respect the bandwidth and terms of service of the mirror providers. Consider using official torrents or mirrors when available.
