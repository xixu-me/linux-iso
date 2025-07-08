#!/usr/bin/env python3

import argparse
import concurrent.futures
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from tqdm import tqdm


class ISODownloader:
    def __init__(self, output_dir, max_workers=5, retry_attempts=3, chunk_size=8192):
        self.output_dir = Path(output_dir)
        self.max_workers = max_workers
        self.retry_attempts = retry_attempts
        self.chunk_size = chunk_size
        self.session = requests.Session()
        # Configure session with longer timeouts
        self.session.mount(
            "https://",
            requests.adapters.HTTPAdapter(
                max_retries=3, pool_connections=max_workers, pool_maxsize=max_workers
            ),
        )
        self.session.mount(
            "http://",
            requests.adapters.HTTPAdapter(
                max_retries=3, pool_connections=max_workers, pool_maxsize=max_workers
            ),
        )

    def download_file(self, url):
        """Download a single file with retry capability and progress tracking"""
        file_name = os.path.basename(urlparse(url).path)
        file_path = self.output_dir / file_name

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Check if file already exists and get its size
        file_size = file_path.stat().st_size if file_path.exists() else 0

        for attempt in range(1, self.retry_attempts + 1):
            try:
                # Setup the request with resume capability if file exists
                headers = {}
                if file_size > 0:
                    headers["Range"] = f"bytes={file_size}-"

                # Make the request with a timeout
                response = self.session.get(
                    url, headers=headers, stream=True, timeout=30, allow_redirects=True
                )

                if (
                    response.status_code == 416
                ):  # Range not satisfiable, file may be complete
                    print(f"File {file_name} appears to be complete, skipping.")
                    return True

                # Handle non-successful status codes
                response.raise_for_status()

                # Get total file size
                total_size = int(response.headers.get("content-length", 0))
                if file_size > 0 and response.status_code == 206:  # Partial content
                    total_size += file_size
                else:
                    # If not a resume, start from scratch
                    file_size = 0

                # Setup progress bar
                desc = f"[Attempt {attempt}] {file_name}"
                with tqdm(
                    total=total_size,
                    initial=file_size,
                    unit="B",
                    unit_scale=True,
                    desc=desc,
                    ncols=100,
                ) as pbar:
                    # Write to file
                    mode = "ab" if file_size > 0 else "wb"
                    with open(file_path, mode) as f:
                        for chunk in response.iter_content(chunk_size=self.chunk_size):
                            if chunk:  # filter out keep-alive chunks
                                f.write(chunk)
                                pbar.update(len(chunk))

                return True

            except (OSError, requests.exceptions.RequestException) as e:
                if attempt < self.retry_attempts:
                    wait_time = 2**attempt  # Exponential backoff
                    print(f"Error downloading {file_name}: {e}")
                    print(
                        f"Retrying in {wait_time} seconds... (Attempt {attempt}/{self.retry_attempts})"
                    )
                    time.sleep(wait_time)
                else:
                    print(
                        f"Failed to download {file_name} after {self.retry_attempts} attempts: {e}"
                    )
                    return False

    def download_all(self, urls):
        """Download all files in parallel"""
        results = []
        successful = 0
        failed = 0

        print(f"Starting downloads with {self.max_workers} parallel workers")

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            # Submit all download tasks
            future_to_url = {
                executor.submit(self.download_file, url): url for url in urls
            }

            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                file_name = os.path.basename(urlparse(url).path)

                try:
                    if future.result():
                        successful += 1
                    else:
                        failed += 1
                        results.append(f"Failed: {file_name}")
                except Exception as e:
                    failed += 1
                    results.append(f"Error with {file_name}: {str(e)}")

        print("\nDownload Summary:")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")

        if failed > 0:
            print("\nFailed Downloads:")
            for result in results:
                print(f"  - {result}")

        return successful, failed, results


def main():
    parser = argparse.ArgumentParser(description="Download ISO files in parallel.")
    parser.add_argument(
        "--urls-file",
        default="urls.txt",
        help="File containing URLs to download (default: urls.txt)",
    )
    parser.add_argument(
        "--output-dir",
        default="./isos",
        help="Directory to save downloaded files (default: ./isos)",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=5,
        help="Maximum number of parallel downloads (default: 5)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=5,
        help="Number of retry attempts per file (default: 5)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=8192,
        help="Chunk size for downloading in bytes (default: 8192)",
    )

    args = parser.parse_args()

    # Read URLs from file
    try:
        with open(args.urls_file) as f:
            urls = [line.strip() for line in f if line.strip()]
    except OSError as e:
        print(f"Error reading URLs file: {e}")
        sys.exit(1)

    if not urls:
        print("No URLs found in the file.")
        sys.exit(1)

    print(f"Found {len(urls)} URLs to download.")

    # Initialize downloader
    downloader = ISODownloader(
        args.output_dir,
        max_workers=args.max_workers,
        retry_attempts=args.retries,
        chunk_size=args.chunk_size,
    )

    # Start the download
    start_time = time.time()
    successful, failed, results = downloader.download_all(urls)
    elapsed_time = time.time() - start_time

    # Print summary
    print(f"\nDownload process completed in {elapsed_time:.2f} seconds.")
    print(f"Files saved to: {os.path.abspath(args.output_dir)}")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
