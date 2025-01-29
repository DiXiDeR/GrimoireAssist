import os
import csv
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()


class BookmarkManager:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.auth_cookie = os.getenv("AUTH_COOKIE")
        self.default_image = os.getenv(
            "DEFAULT_IMAGE", "http://192.168.31.62:5173/files/1/default.png"
        )
        self.processed_urls = set()

        # Validate required environment variables
        if not all([self.base_url, self.auth_cookie]):
            raise ValueError("Missing required environment variables")

    def extract_urls_from_csv(self, file_path):
        """Extract unique URLs from CSV file"""
        urls = set()

        try:
            with open(file_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                if "domains" not in reader.fieldnames:
                    raise ValueError("CSV must contain 'domains' column header")

                for row in reader:
                    url = row["domains"].strip()
                    if self._is_valid_url(url):
                        urls.add(url)
                    else:
                        print(f"Skipping invalid URL: {url}")

            return list(urls)

        except FileNotFoundError:
            print(f"Error: CSV file not found at {file_path}")
            return []

    def _is_valid_url(self, url):
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def fetch_metadata(self, url):
        """Fetch metadata for a URL"""
        try:
            response = requests.post(
                f"{self.base_url}/api/fetch-metadata",
                headers=self._get_headers("fetch"),
                json={"url": url},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()["metadata"]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching metadata for {url}: {str(e)}")
            return None

    def add_bookmark(self, metadata):
        """Add new bookmark using metadata"""
        try:
            response = requests.post(
                f"{self.base_url}/?/addNewBookmark",
                headers=self._get_headers("bookmark"),
                data=self._prepare_form_data(metadata),
                timeout=10,
            )
            response.raise_for_status()
            return response.status_code == 200

        except requests.exceptions.RequestException as e:
            print(f"Error adding bookmark: {str(e)}")
            return False

    def _get_headers(self, request_type):
        """Get headers for different request types"""
        base_headers = {
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "Cookie": self.auth_cookie,
        }

        if request_type == "fetch":
            base_headers.update({"Accept": "*/*", "Content-Type": "application/json"})
        elif request_type == "bookmark":
            base_headers.update(
                {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "x-sveltekit-action": "true",
                    "Accept": "application/json",
                }
            )

        return base_headers

    def _prepare_form_data(self, metadata):
        """Prepare form data with fallback values"""
        return {
            "domain": metadata.get("domain", ""),
            "content_html": metadata.get("contentHtml", ""),
            "content_published_date": metadata.get("contentPublishedDate", ""),
            "url": metadata.get("url", ""),
            "category": '{"value":"1","label":"Uncategorized"}',
            "tags": "",
            "importance": "",
            "title": metadata.get("title", ""),
            "icon_url": metadata.get("iconUrl", ""),
            "description": metadata.get("description", ""),
            "main_image_url": metadata.get("mainImageUrl", self.default_image),
            "content_text": metadata.get("contentText", ""),
            "author": metadata.get("author", ""),
            "note": "",
        }

    def process_csv(self, file_path):
        """Main processing method for CSV file"""
        urls = self.extract_urls_from_csv(file_path)

        for url in urls:
            if url in self.processed_urls:
                print(f"Skipping duplicate URL: {url}")
                continue

            print(f"Processing URL: {url}")
            metadata = self.fetch_metadata(url)

            if metadata and self.add_bookmark(metadata):
                self.processed_urls.add(url)
                print(f"Successfully added: {url}")
            else:
                print(f"Failed to process: {url}")


if __name__ == "__main__":
    try:
        manager = BookmarkManager()
        manager.process_csv("input.csv")
        print(f"Processing complete. Total URLs added: {len(manager.processed_urls)}")

    except Exception as e:
        print(f"Fatal error: {str(e)}")
