import requests
import xml.etree.ElementTree as ET

SITEMAP_URL = "https://docs.myq-solution.com/sitemap.xml"
OUTPUT_FILE = "sitemap-x.xml"

def fetch_sitemap(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text

def filter_sitemaps_for_x(xml_text):
    """
    Currently this script passes through all English sitemaps.
    It is labeled as X-specific purely by output naming.
    """
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.fromstring(xml_text)
    urls = []

    for sitemap in root.findall("sm:sitemap", ns):
        loc = sitemap.find("sm:loc", ns)
        if loc is not None:
            urls.append(loc.text)

    return urls

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
    urls = filter_sitemaps_for_x(xml_text)
    sitemap_xml = generate_sitemap_xml(urls)

    with open(OUTPUT_FILE, "wb") as f:
        f.write(sitemap_xml)

    print(f"X sitemap generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
