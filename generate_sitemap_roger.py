import requests
import xml.etree.ElementTree as ET

# ✅ Roger-specific sitemap source
SITEMAP_URL = "https://docs.roger.myq.cloud/sitemap.xml"

# ✅ Roger-specific output
OUTPUT_FILE = "sitemap-roger.xml"

def fetch_sitemap(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text

def filter_english_sitemaps(xml_text):
    """
    Keep only English sitemaps.
    Roger-specific by source + output file.
    """
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.fromstring(xml_text)
    english_urls = []

    for sitemap in root.findall("sm:sitemap", ns):
        loc = sitemap.find("sm:loc", ns)
        if loc is not None and "/en/" in loc.text:
            english_urls.append(loc.text)

    return english_urls

def generate_sitemap_xml(urls):
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    root = ET.Element("sitemapindex", xmlns=ns)

    for url in urls:
        sitemap = ET.SubElement(root, "sitemap")
        loc = ET.SubElement(sitemap, "loc")
        loc.text = url

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def main():
    xml_text = fetch_sitemap(SITEMAP_URL)
    english_urls = filter_english_sitemaps(xml_text)
    sitemap_xml = generate_sitemap_xml(english_urls)

    with open(OUTPUT_FILE, "wb") as f:
        f.write(sitemap_xml)

    print(f"English sitemap for Roger generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
