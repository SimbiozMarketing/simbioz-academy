import urllib.request
import urllib.parse
import os
import re

BASE_URL = "https://simbioz.academy/"
TARGET_DIR = "assets/img"
LOG_FILE = "image_map.txt"

if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

# Headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def download_images():
    print(f"Fetching {BASE_URL}...")
    try:
        req = urllib.request.Request(BASE_URL, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch page: {e}")
        return

    # Find all image sources (img src="..." and style="background-image: url(...)")
    img_urls = set()
    
    # 1. Regex for <img src="...">
    img_tags = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    for url in img_tags:
        img_urls.add(url)

    # 2. Regex for background-image: url(...)
    bg_images = re.findall(r'url\([\"\']?([^"\')]+)[\"\']?\)', html)
    for url in bg_images:
        img_urls.add(url)

    print(f"Found {len(img_urls)} potential images.")

    downloaded_map = {}

    for i, img_url in enumerate(img_urls):
        # Resolve relative URLs
        full_url = urllib.parse.urljoin(BASE_URL, img_url)
        
        # Get filename
        filename = os.path.basename(urllib.parse.urlparse(full_url).path)
        if not filename or '.' not in filename:
            filename = f"image_{i}.jpg" # Fallback
        
        # Clean filename
        filename = re.sub(r'[^\w\-.]', '_', filename)
        local_path = os.path.join(TARGET_DIR, filename)

        try:
            print(f"Downloading {full_url} -> {local_path}")
            img_req = urllib.request.Request(full_url, headers=headers)
            with urllib.request.urlopen(img_req) as img_response:
                with open(local_path, 'wb') as f:
                    f.write(img_response.read())
            
            downloaded_map[full_url] = f"assets/img/{filename}"

        except Exception as e:
            print(f"Failed to download {full_url}: {e}")

    # Write map to file for the agent to read
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        for remote, local in downloaded_map.items():
            f.write(f"{remote} | {local}\n")

if __name__ == "__main__":
    download_images()
