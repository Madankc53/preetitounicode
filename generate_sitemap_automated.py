import os
from datetime import datetime

# Configuration
BASE_URL = "https://converter.thenepal.io"
REPO_PATH = "."  # Root of your GitHub repo
SITEMAP_PATH = "sitemap.xml"
EXCLUDE_DIRS = [".git", ".github", "node_modules"]
EXCLUDE_FILES = ["404.html", "google_verify.html"]

def get_html_files(directory):
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file.endswith(".html") and file not in EXCLUDE_FILES:
                full_path = os.path.join(root, file)
                # Convert file path to URL path
                rel_path = os.path.relpath(full_path, directory)
                
                # Clean up URL (index.html -> /, remove .html)
                if rel_path == "index.html":
                    url_path = "/"
                elif rel_path.endswith("index.html"):
                    url_path = "/" + rel_path.replace("index.html", "")
                else:
                    url_path = "/" + rel_path.replace(".html", "")
                
                html_files.append(url_path)
    return sorted(list(set(html_files)))

def generate_sitemap(urls):
    today = datetime.now().strftime("%Y-%m-%d")
    sitemap_content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    for url in urls:
        priority = "1.0" if url == "/" else "0.8"
        sitemap_content.append(f"  <url>")
        sitemap_content.append(f"    <loc>{BASE_URL}{url}</loc>")
        sitemap_content.append(f"    <lastmod>{today}</lastmod>")
        sitemap_content.append(f"    <priority>{priority}</priority>")
        sitemap_content.append(f"  </url>")
    
    sitemap_content.append("</urlset>")
    
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_content))
    
    print(f"Sitemap generated with {len(urls)} URLs.")

if __name__ == "__main__":
    urls = get_html_files(REPO_PATH)
    # Add your custom paths that might not be static HTML files if needed
    # urls.append("/custom-path")
    generate_sitemap(urls)
