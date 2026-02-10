import urllib.request
import os
import time

TARGET_DIR = "assets/img"
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

images = [
    ("course_ba.jpg", "business,laptop,office"),
    ("course_pm.jpg", "meeting,team,planning"),
    ("course_sa.jpg", "technology,server,code"),
    ("course_crm.jpg", "marketing,analytics,graph"),
    ("course_accountant.jpg", "calculator,finance,paperwork"),
    ("course_integrator.jpg", "network,cables,server")
]

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
urllib.request.install_opener(opener)

print("Downloading images...")
for filename, keywords in images:
    url = f"https://loremflickr.com/800/600/{keywords}/all"
    filepath = os.path.join(TARGET_DIR, filename)
    try:
        print(f"Downloading {filename} from {url}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"Saved {filename}")
        time.sleep(1) # Be nice to the server
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

print("Done.")
