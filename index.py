import json
import requests
import xml.etree.ElementTree as ET

from google.oauth2 import service_account
from google.auth.transport.requests import Request

SITEMAP = "https://converter.thenepal.io/sitemap.xml"

SCOPES = [
    "https://www.googleapis.com/auth/indexing"
]

credentials = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

credentials.refresh(Request())

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {credentials.token}"
}

print("Downloading sitemap...")

response = requests.get(SITEMAP)
response.raise_for_status()

root = ET.fromstring(response.text)

namespace = {
    "ns": "http://www.sitemaps.org/schemas/sitemap/0.9"
}

urls = []

for item in root.findall("ns:url", namespace):
    loc = item.find("ns:loc", namespace).text
    urls.append(loc)

print(f"Found {len(urls)} URLs")

for url in urls:
    payload = {
        "url": url,
        "type": "URL_UPDATED"
    }

    r = requests.post(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        headers=headers,
        data=json.dumps(payload)
    )

    print("--------------------------------")
    print(url)
    print(r.status_code)
    print(r.text)

print("Finished")
