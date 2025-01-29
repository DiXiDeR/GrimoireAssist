import requests

# Uživatelský vstup
url = input("Zadejte URL adresu: ")

# Konfigurace
BASE_URL = "http://192.168.31.62:5173"
AUTH_COOKIE = "auth_session=36khlndtmtz2unshdclq5fifg73ol5fwepl76j7r"

# 1. Krok - Získání metadat
fetch_response = requests.post(
    f"{BASE_URL}/api/fetch-metadata",
    headers={
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Cookie": AUTH_COOKIE,
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    },
    json={"url": url},
)

fetch_response.raise_for_status()
metadata = fetch_response.json()["metadata"]

# 2. Krok - Vytvoření záložky
form_data = {
    "domain": metadata["domain"],
    "content_html": metadata["contentHtml"],
    "content_published_date": metadata.get("contentPublishedDate", ""),
    "url": metadata["url"],
    "category": '{"value":"1","label":"Uncategorized"}',
    "tags": "",
    "importance": "",
    "title": metadata["title"],
    "icon_url": metadata["iconUrl"],
    "description": metadata["description"],
    "main_image_url": metadata["mainImageUrl"],
    "content_text": metadata["contentText"],
    "author": metadata["author"],
    "note": "",
}

add_response = requests.post(
    f"{BASE_URL}/?/addNewBookmark",
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "x-sveltekit-action": "true",
        "Cookie": AUTH_COOKIE,
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json",
    },
    data=form_data,
)

print(f"Status: {add_response.status_code}")
print("Odpověď serveru:", add_response.text)
