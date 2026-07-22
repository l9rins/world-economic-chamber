import os
import zipfile
import xml.etree.ElementTree as ET
import shutil
import re

DOC_DIR = "document"
OUT_DIR = "."
IMG_DIR = "images"
ARTIFACTS_IMG = r"C:\Users\Mark Lorenz\.gemini\antigravity-ide\brain\a29361e0-155d-41f5-9dc6-7f0cf31e8789"

os.makedirs(IMG_DIR, exist_ok=True)
for f in os.listdir(ARTIFACTS_IMG):
    if f.endswith(".png") and ("diverse_office" in f or "modern_corporate" in f):
        shutil.copy(os.path.join(ARTIFACTS_IMG, f), os.path.join(IMG_DIR, f))
        
hero_img = "diverse_office_interaction_1784753301497.png" # Fallback if not found
bldg_img = "modern_corporate_buildings_1784753313806.png"
for f in os.listdir(IMG_DIR):
    if "diverse_office" in f: hero_img = f
    if "modern_corporate" in f: bldg_img = f

def get_docx_text(path):
    """Extract text from docx without external libraries."""
    paragraphs = []
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            
            # Namespace for Word XML
            WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
            PARA = WORD_NAMESPACE + 'p'
            TEXT = WORD_NAMESPACE + 't'
            
            for paragraph in tree.iter(PARA):
                texts = [node.text for node in paragraph.iter(TEXT) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ["<p>Content could not be loaded.</p>"]
    
    return paragraphs

def docx_to_html(docx_path):
    paragraphs = get_docx_text(docx_path)
    html = []
    for text in paragraphs:
        text = text.strip()
        if not text:
            continue
        
        # Simple heuristics for headings
        if len(text) < 80 and not text.endswith('.') and not text.endswith(','):
            if re.match(r'^[1-9A-Z]\.', text) or text.isupper():
                html.append(f"<h2>{text}</h2>")
                continue
            
        html.append(f"<p>{text}</p>")
    return "\n".join(html)

pages = {
    "1.  About the Chamber.docx": ("about.html", "About the Chamber"),
    "1.0  Charter, Policies and Governance Documents.docx": ("charter-and-governance.html", "Charter, Policies and Governance"),
    "1A.  Charter.docx": ("charter.html", "Charter"),
    "1B.  Governance Documents.docx": ("governance-documents.html", "Governance Documents"),
    "1Ba.  Governance Architecture and Institutional Roles.docx": ("governance-architecture.html", "Governance Architecture"),
    "1Bb.  Decision-Making Procedures and Approval Pathways.docx": ("decision-making.html", "Decision-Making Procedures"),
    "1Bc.  Oversight Responsibilities and Accountability Standards.docx": ("oversight-responsibilities.html", "Oversight Responsibilities"),
    "1Bd.  Leadership Responsibilities and Governance Oversight Standards.docx": ("leadership-responsibilities.html", "Leadership Responsibilities"),
    "1Be.  Executive Secretariat Operational Management Protocols.docx": ("secretariat-management.html", "Secretariat Management")
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | World Economic Chamber</title>
    <meta name="description" content="World Economic Chamber - {title}">
    <link rel="stylesheet" href="css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="main-header">
        <div class="header-container">
            <a href="index.html" class="logo">
                <img src="images/Logo WEC 1 [MAIN].png" alt="World Economic Chamber Logo">
            </a>
            <nav class="main-nav">
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="about.html">About WEC</a></li>
                    <li class="dropdown">
                        <a href="charter-and-governance.html">Governance ▼</a>
                        <ul class="dropdown-menu">
                            <li><a href="charter.html">Charter</a></li>
                            <li><a href="governance-documents.html">Governance Documents</a></li>
                            <li><a href="governance-architecture.html">Governance Architecture</a></li>
                            <li><a href="decision-making.html">Decision-Making</a></li>
                            <li><a href="oversight-responsibilities.html">Oversight</a></li>
                            <li><a href="leadership-responsibilities.html">Leadership</a></li>
                            <li><a href="secretariat-management.html">Secretariat</a></li>
                        </ul>
                    </li>
                </ul>
            </nav>
        </div>
    </header>

    {hero_section}

    <main class="main-content">
        <div class="content-container doc-content">
            {content}
        </div>
    </main>

    <footer class="main-footer">
        <div class="footer-container">
            <div class="footer-col">
                <img src="images/Logo WEC 5 (dark navy blue background).png" alt="WEC Footer Logo" class="footer-logo">
                <p>Leading global economic growth through robust governance and strategic oversight.</p>
            </div>
            <div class="footer-col">
                <h3>Quick Links</h3>
                <ul>
                    <li><a href="about.html">About WEC</a></li>
                    <li><a href="charter.html">Our Charter</a></li>
                    <li><a href="governance-documents.html">Governance</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h3>Contact</h3>
                <p>Email: <a href="mailto:info@worldeconomicchamber.com">info@worldeconomicchamber.com</a></p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 World Economic Chamber. All rights reserved.</p>
        </div>
    </footer>
    <script src="js/main.js"></script>
</body>
</html>
"""

# Generate index.html
index_hero = f"""
    <section class="hero-section" style="background-image: linear-gradient(rgba(0,25,50,0.85), rgba(0,15,30,0.9)), url('images/{hero_img}');">
        <div class="hero-content">
            <h1>Global Economic Leadership</h1>
            <p>Advancing international trade, robust governance, and sustainable economic architecture for the future.</p>
            <div class="hero-buttons">
                <a href="about.html" class="btn-primary">Discover the Chamber</a>
                <a href="charter-and-governance.html" class="btn-secondary">View Governance</a>
            </div>
        </div>
    </section>
"""

index_content = f"""
<div class="home-grid">
    <div class="home-card glass-card">
        <h3>Governance Architecture</h3>
        <p>Explore the structured pathways and institutional roles that define the core of WEC.</p>
        <a href="governance-architecture.html" class="card-link">Read More &rarr;</a>
    </div>
    <div class="home-card glass-card">
        <h3>Our Charter</h3>
        <p>The foundational principles and policies guiding our international operations and standards.</p>
        <a href="charter.html" class="card-link">Read More &rarr;</a>
    </div>
    <div class="home-card glass-card">
        <h3>Decision-Making</h3>
        <p>Transparent, accountable approval pathways for all global economic initiatives.</p>
        <a href="decision-making.html" class="card-link">Read More &rarr;</a>
    </div>
</div>
<div class="home-showcase" style="background-image: linear-gradient(rgba(0,19,45,0.4), rgba(0,19,45,0.7)), url('images/{bldg_img}');">
    <div class="showcase-content">
        <h2>Building the Future of Global Economy</h2>
        <p>Strategic oversight and robust partnerships worldwide.</p>
    </div>
</div>
"""

with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(TEMPLATE.format(title="Home", content=index_content, hero_section=index_hero))
print("Generated index.html")

# Generate other pages
for filename, (html_file, title) in pages.items():
    docx_path = os.path.join(DOC_DIR, filename)
    if os.path.exists(docx_path):
        page_content = docx_to_html(docx_path)
        page_hero = f'''
        <div class="page-header">
            <div class="header-container">
                <h1>{title}</h1>
            </div>
        </div>
        '''
        with open(os.path.join(OUT_DIR, html_file), "w", encoding="utf-8") as f:
            f.write(TEMPLATE.format(title=title, content=page_content, hero_section=page_hero))
        print(f"Generated {html_file}")
    else:
        print(f"Warning: {filename} not found.")

print("Site generation complete!")
