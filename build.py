"""
WEC Website Generator — Premium Build Script
"""

import os
import zipfile
import xml.etree.ElementTree as ET

DOC_DIR = "document"
OUT_DIR = "."

WORD_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def get_docx_paragraphs(path):
    paragraphs = []
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            for para in tree.iter(WORD_NS + 'p'):
                texts = []
                is_bold = False
                for run in para.iter(WORD_NS + 'r'):
                    rpr = run.find(WORD_NS + 'rPr')
                    if rpr is not None:
                        if rpr.find(WORD_NS + 'b') is not None:
                            is_bold = True
                    for t in run.iter(WORD_NS + 't'):
                        if t.text:
                            texts.append(t.text)
                text = ''.join(texts).strip()
                if text:
                    ppr = para.find(WORD_NS + 'pPr')
                    style_name = ''
                    if ppr is not None:
                        ps = ppr.find(WORD_NS + 'pStyle')
                        if ps is not None:
                            style_name = ps.get(WORD_NS + 'val', '').lower()
                    if 'heading1' in style_name or 'title' in style_name:
                        paragraphs.append(('h1', text))
                    elif 'heading2' in style_name:
                        paragraphs.append(('h2', text))
                    elif 'heading3' in style_name:
                        paragraphs.append(('h3', text))
                    elif is_bold and len(text) < 100 and not text.endswith('.'):
                        paragraphs.append(('h3', text))
                    elif len(text) < 80 and not text.endswith('.') and not text.endswith(',') and text == text.upper():
                        paragraphs.append(('h2', text))
                    else:
                        paragraphs.append(('p', text))
    except Exception as e:
        print(f"  ERROR reading {path}: {e}")
        return [('p', 'Content could not be loaded.')]
    return paragraphs

def paragraphs_to_html(paragraphs):
    html = []
    toc = []
    used_slugs = {}
    article_num = 0
    for tag, text in paragraphs:
        text = text.replace('&', '&amp;')
        if tag in ('h1', 'h3'):
            slug = text.lower().replace(' ', '-')[:40]
            if slug in used_slugs:
                used_slugs[slug] += 1
                slug = f'{slug}-{used_slugs[slug]}'
            else:
                used_slugs[slug] = 0
            html.append(f'<{tag} id="{slug}" style="scroll-margin-top: calc(var(--nav-height) + var(--space-xl));">{text}</{tag}>')
            toc.append((tag, text, slug))
        elif tag == 'h2':
            slug = text.lower().replace(' ', '-')[:40]
            if slug in used_slugs:
                used_slugs[slug] += 1
                slug = f'{slug}-{used_slugs[slug]}'
            else:
                used_slugs[slug] = 0
            html.append(f'<h2 id="{slug}" style="scroll-margin-top: calc(var(--nav-height) + var(--space-xl));">{text}</h2>')
            toc.append(('h2', text, slug))
        else:
            html.append(f'<p>{text}</p>')
    return '\n            '.join(html), toc

pages = {
    "1.  About the Chamber.docx": {
        "file": "about.html",
        "title": "About the Chamber",
        "desc": "Learn about the World Economic Chamber's mandate, founding principles, leadership and global engagement model.",
        "breadcrumb": "Home / About",
        "pillar": "cooperation"
    },
    "1.0  Charter, Policies and Governance Documents.docx": {
        "file": "charter-and-governance.html",
        "title": "Charter, Policies & Governance",
        "desc": "The charter, policies and governance documents that define the Chamber's institutional responsibilities.",
        "breadcrumb": "Home / Governance / Charter & Policies",
        "pillar": "governance"
    },
    "1A.  Charter.docx": {
        "file": "charter.html",
        "title": "The WEC Charter",
        "desc": "The foundational charter of the World Economic Chamber, setting out mandate, purpose and authorities.",
        "breadcrumb": "Home / Governance / Charter",
        "pillar": "governance"
    },
    "1B.  Governance Documents.docx": {
        "file": "governance-documents.html",
        "title": "Governance Documents",
        "desc": "Comprehensive governance documentation for the World Economic Chamber.",
        "breadcrumb": "Home / Governance / Documents",
        "pillar": "governance"
    },
    "1Ba.  Governance Architecture and Institutional Roles.docx": {
        "file": "governance-architecture.html",
        "title": "Governance Architecture",
        "desc": "Institutional roles and governance architecture of the World Economic Chamber.",
        "breadcrumb": "Home / Governance / Architecture",
        "pillar": "governance"
    },
    "1Bb.  Decision-Making Procedures and Approval Pathways.docx": {
        "file": "decision-making.html",
        "title": "Decision-Making Procedures",
        "desc": "Decision-making procedures and approval pathways for the World Economic Chamber.",
        "breadcrumb": "Home / Governance / Decision-Making",
        "pillar": "oversight"
    },
    "1Bc.  Oversight Responsibilities and Accountability Standards.docx": {
        "file": "oversight-responsibilities.html",
        "title": "Oversight & Accountability",
        "desc": "Oversight responsibilities and accountability standards of the World Economic Chamber.",
        "breadcrumb": "Home / Governance / Oversight",
        "pillar": "oversight"
    },
    "1Bd.  Leadership Responsibilities and Governance Oversight Standards.docx": {
        "file": "leadership-responsibilities.html",
        "title": "Leadership Responsibilities",
        "desc": "Leadership responsibilities and governance oversight standards of the World Economic Chamber.",
        "breadcrumb": "Home / Governance / Leadership",
        "pillar": "oversight"
    },
    "1Be.  Executive Secretariat Operational Management Protocols.docx": {
        "file": "secretariat-management.html",
        "title": "Executive Secretariat",
        "desc": "Operational management protocols of the WEC Executive Secretariat.",
        "breadcrumb": "Home / Governance / Secretariat",
        "pillar": "governance"
    }
}

def picture_img(src, alt, cls="", style="", lazy=False, eager=False):
    ext = src.rsplit('.', 1)[0]
    webp = ext + '.webp'
    cls_attr = f' class="{cls}"' if cls else ''
    style_attr = f' style="{style}"' if style else ''
    loading = ' loading="eager"' if eager else (' loading="lazy"' if lazy else '')
    return f'<picture><source srcset="{webp}" type="image/webp"><img src="{src}" alt="{alt}"{cls_attr}{style_attr}{loading}></picture>'

NAV_HTML = """
  <div id="readingProgress" class="reading-progress"></div>
  <!-- Navigation -->
  <nav class="nav" id="mainNav">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">
        """ + picture_img("images/Logo_WEC_White_Text.png", "World Economic Chamber", lazy=False, eager=True) + """
      </a>

      <ul class="nav-menu" id="navMenu">
        <!-- The Chamber Mega-Menu -->
        <li class="nav-item has-mega">
          <a href="about.html" class="nav-link">The Chamber <svg class="nav-arrow" viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"></polyline></svg></a>
          <div class="nav-dropdown mega-menu">
            <div class="mega-menu-grid">
              <div class="mega-col">
                <h4>About WEC</h4>
                <a href="about.html">Mission & Vision</a>
                <a href="#">History & Milestones</a>
                <a href="#">Leadership Directory</a>
                <a href="#">Regional Offices</a>
              </div>
              <div class="mega-col">
                <h4>Engagement</h4>
                <a href="#">Member Directory</a>
                <a href="#">Institutional Partners</a>
                <a href="#">NGO Affiliations</a>
                <a href="#">Corporate Sponsors</a>
              </div>
              <div class="mega-col">
                <h4>News & Media</h4>
                <a href="#">Press Releases</a>
                <a href="#">Media Gallery</a>
                <a href="#">Official Statements</a>
                <a href="#">Event Calendar</a>
              </div>
              <div class="mega-col">
                <h4>Contact</h4>
                <a href="#">Global Headquarters</a>
                <a href="#">Media Inquiries</a>
                <a href="#">Career Opportunities</a>
              </div>
            </div>
          </div>
        </li>

        <!-- Governance Mega-Menu -->
        <li class="nav-item has-mega">
          <a href="governance-architecture.html" class="nav-link">Governance <svg class="nav-arrow" viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"></polyline></svg></a>
          <div class="nav-dropdown mega-menu">
            <div class="mega-menu-grid">
              <div class="mega-col">
                <h4>Core Architecture</h4>
                <a href="governance-architecture.html">Governance Architecture</a>
                <a href="charter.html">The WEC Charter</a>
                <a href="governance-documents.html">Governance Documents</a>
              </div>
              <div class="mega-col">
                <h4>Operations</h4>
                <a href="secretariat-management.html">Executive Secretariat</a>
                <a href="leadership-responsibilities.html">Leadership Responsibilities</a>
                <a href="#">Operational Protocols</a>
              </div>
              <div class="mega-col">
                <h4>Accountability</h4>
                <a href="decision-making.html">Decision-Making Procedures</a>
                <a href="oversight-responsibilities.html">Oversight & Accountability</a>
                <a href="#">Compliance Standards</a>
              </div>
              <div class="mega-col">
                <h4>Policies</h4>
                <a href="charter-and-governance.html">Charter & Policies Overview</a>
                <a href="#">Ethics Framework</a>
                <a href="#">Dispute Resolution</a>
              </div>
            </div>
          </div>
        </li>

        <!-- Trade & Economy Mega-Menu -->
        <li class="nav-item has-mega">
          <a href="#" class="nav-link">Trade & Economy <svg class="nav-arrow" viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"></polyline></svg></a>
          <div class="nav-dropdown mega-menu">
            <div class="mega-menu-grid">
              <div class="mega-col">
                <h4>Agreements</h4>
                <a href="#">Active Trade Agreements</a>
                <a href="#">Pending Negotiations</a>
                <a href="#">Regional Integration</a>
              </div>
              <div class="mega-col">
                <h4>Analysis</h4>
                <a href="#">Global Trade Volume</a>
                <a href="#">Economic Forecasts</a>
                <a href="#">Market Access Reports</a>
              </div>
              <div class="mega-col">
                <h4>Policy</h4>
                <a href="#">Commercial Policy Reviews</a>
                <a href="#">Regulatory Convergence</a>
                <a href="#">Investment Frameworks</a>
              </div>
              <div class="mega-col">
                <h4>Resources</h4>
                <a href="#">Trade Statistics Database</a>
                <a href="#">Policy Documents</a>
                <a href="#">Publications Library</a>
              </div>
            </div>
          </div>
        </li>

      </ul>

      <div class="nav-actions">
        <a href="mailto:info@worldeconomicchamber.com" class="btn btn-primary btn-sm">Contact</a>
        <button class="nav-toggle" id="navToggle" aria-label="Toggle navigation">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </div>
  </nav>
  <div class="nav-backdrop" id="navBackdrop">
</div>
"""

FOOTER_HTML = """
  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
          <div class="footer-brand">
            """ + picture_img("images/Logo_WEC_White_Text.png", "WEC Logo", lazy=True) + """
          <p>The World Economic Chamber — strengthening cross-border commerce, investment and economic cooperation through principled governance and institutional discipline.</p>
        </div>

        <div>
          <h4 class="footer-heading">The Chamber</h4>
          <ul class="footer-links">
            <li><a href="about.html">About WEC</a></li>
            <li><a href="charter.html">Our Charter</a></li>
            <li><a href="charter-and-governance.html">Policies &amp; Governance</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-heading">Governance</h4>
          <ul class="footer-links">
            <li><a href="governance-architecture.html">Architecture</a></li>
            <li><a href="decision-making.html">Decision-Making</a></li>
            <li><a href="oversight-responsibilities.html">Oversight</a></li>
            <li><a href="leadership-responsibilities.html">Leadership</a></li>
            <li><a href="secretariat-management.html">Secretariat</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-heading">Contact</h4>
          <ul class="footer-links">
            <li><a href="mailto:info@worldeconomicchamber.com">info@worldeconomicchamber.com</a></li>
            <li><span style="color: var(--text-muted); font-size: var(--font-size-sm);">7th Floor, Tower 42<br>25 Old Broad Street<br>London EC2N 1HN<br>United Kingdom</span></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2026 World Economic Chamber. All rights reserved.</p>
        <div class="footer-social">
          <a href="https://linkedin.com/company/world-economic-chamber" aria-label="LinkedIn"><svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" aria-hidden="true"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg></a>
          <a href="https://x.com/WEC_Chamber" aria-label="X / Twitter"><svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" aria-hidden="true"><path d="M4 4l11.733 16h4.267l-11.733 -16z"></path><path d="M4 20l6.768 -6.768m2.46 -2.46l6.772 -6.772"></path></svg></a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Scroll to Top -->
  <button class="scroll-top" aria-label="Scroll to top">
    <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"></polyline></svg>
  </button>

  <!-- Cookie Consent Pill -->
  <div class="cookie-consent" id="cookieConsent">
    <div class="cookie-icon"><svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5"></path><path d="M8.5 8.5v.01"></path><path d="M16 12.5v.01"></path><path d="M12 16v.01"></path><path d="M11 12.5v.01"></path></svg></div>
    <div class="cookie-text">
      <strong>Privacy & Cookies</strong>
      <p>We use cookies to improve your experience.</p>
    </div>
    <div class="cookie-consent-actions">
      <button class="btn btn-primary btn-sm" data-cookie-accept>Accept</button>
    </div>
  </div>

  <script src="js/main.js"></script>
"""

def head_html(title, description):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | World Economic Chamber</title>
  <meta name="description" content="{description}">
  <meta property="og:title" content="{title} | World Economic Chamber">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.worldeconomicchamber.com">
  <meta property="og:image" content="https://www.worldeconomicchamber.com/images/Logo_WEC_White_Text.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="images/Logo WEC 1 [MAIN].png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
"""

CONSTELLATION_SVG = """
  <svg viewBox="0 0 900 440" fill="none" xmlns="http://www.w3.org/2000/svg" class="constellation-draw-in" aria-hidden="true">
    <defs>
      <clipPath id="globeClip"><circle cx="450" cy="225" r="165"/></clipPath>
      <radialGradient id="globeGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#c9a84c" stop-opacity="0.15"/>
        <stop offset="60%" stop-color="#c9a84c" stop-opacity="0.04"/>
        <stop offset="100%" stop-color="#c9a84c" stop-opacity="0"/>
      </radialGradient>
    </defs>
    <!-- Globe glow -->
    <circle cx="450" cy="225" r="200" fill="url(#globeGlow)"/>
    <!-- Globe wireframe -->
    <circle cx="450" cy="225" r="165" fill="none" stroke="rgba(201,168,76,0.12)" stroke-width="1"/>
    <g clip-path="url(#globeClip)">
      <ellipse cx="450" cy="225" rx="40" ry="165" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
      <ellipse cx="450" cy="225" rx="82" ry="165" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
      <ellipse cx="450" cy="225" rx="124" ry="165" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
      <line x1="285" y1="107" x2="615" y2="107" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
      <line x1="285" y1="167" x2="615" y2="167" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
      <line x1="285" y1="225" x2="615" y2="225" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
      <line x1="285" y1="283" x2="615" y2="283" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
      <line x1="285" y1="343" x2="615" y2="343" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
    </g>
    <!-- Hub-and-spoke connection lines -->
    <path class="const-line" d="M450.0 225.0 Q336.7 154.5 205.0 133.0" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <path class="const-line" d="M450.0 225.0 Q393.8 256.0 330.0 263.0" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <path class="const-line" d="M450.0 225.0 Q519.8 245.2 592.0 237.0" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <path class="const-line" d="M450.0 225.0 Q484.2 297.2 488.0 377.0" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <path class="const-line" d="M450.0 225.0 Q357.2 278.2 292.0 363.0" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <!-- Perimeter route lines -->
    <path class="const-line" d="M140.0 315.0 Q188.9 229.8 205.0 133.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M205.0 133.0 Q233.8 175.9 242.0 227.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M242.0 227.0 Q281.3 256.4 330.0 263.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M330.0 263.0 Q320.0 316.4 292.0 363.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M292.0 363.0 Q221.3 322.3 140.0 315.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M470.0 87.0 Q550.5 146.1 592.0 237.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M592.0 237.0 Q662.3 190.8 712.0 123.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M712.0 123.0 Q761.5 190.7 778.0 273.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M778.0 273.0 Q702.1 298.1 648.0 357.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M648.0 357.0 Q569.8 381.4 488.0 377.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M330.0 263.0 Q463.9 278.8 592.0 237.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M488.0 377.0 Q305.9 391.2 140.0 315.0" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <!-- Pillar dots -->
    <circle class="const-dot" cx="140" cy="315" r="4" fill="var(--pillar-cooperation)" opacity="0"><title>Cooperation — Constructive international dialogue and multilateral engagement</title></circle>
    <circle class="const-dot" cx="205" cy="133" r="4" fill="var(--pillar-cooperation)" opacity="0"><title>Cooperation — Cross-border economic cooperation framework</title></circle>
    <circle class="const-dot" cx="330" cy="263" r="4" fill="var(--pillar-oversight)" opacity="0"><title>Oversight — Accountability and compliance monitoring</title></circle>
    <circle class="const-dot" cx="470" cy="87" r="4" fill="var(--pillar-trade)" opacity="0"><title>Trade &amp; Economy — Global market access and trade facilitation</title></circle>
    <circle class="const-dot" cx="592" cy="237" r="4" fill="var(--pillar-trade)" opacity="0"><title>Trade &amp; Economy — Investment and economic cooperation</title></circle>
    <circle class="const-dot" cx="712" cy="123" r="4" fill="var(--pillar-trade)" opacity="0"><title>Trade &amp; Economy — Regional economic integration</title></circle>
    <circle class="const-dot" cx="778" cy="273" r="4" fill="var(--pillar-trade)" opacity="0"><title>Trade &amp; Economy — Cross-border commercial policy</title></circle>
    <circle class="const-dot" cx="648" cy="357" r="4" fill="var(--pillar-oversight)" opacity="0"><title>Oversight — Institutional integrity and ethical standards</title></circle>
    <circle class="const-dot" cx="488" cy="377" r="4" fill="var(--pillar-governance)" opacity="0"><title>Governance — Institutional framework and decision-making</title></circle>
    <circle class="const-dot" cx="292" cy="363" r="4" fill="var(--pillar-governance)" opacity="0"><title>Governance — Principled leadership and stewardship</title></circle>
    <circle class="const-dot" cx="242" cy="227" r="4" fill="var(--pillar-governance)" opacity="0"><title>Governance — Charter and mandate implementation</title></circle>
    <!-- Central hub node -->
    <circle class="const-dot const-dot-hub" cx="450" cy="225" r="7" fill="var(--gold-500)" opacity="0"><title>World Economic Chamber — Central hub of international cooperation</title></circle>
  </svg>
"""

def build_index():
    html = head_html("Global Economic Leadership", "The World Economic Chamber — strengthening cross-border commerce, investment and economic cooperation through principled governance.")
    html += NAV_HTML

    html += """
<!-- Bento Hero Hub -->
  <section class="hero-hub" id="hero">
    <div class="container">
      <div class="bento-hero fade-up">
        <div class="bento-main">
          """ + picture_img("images/boardroom_interaction.png", "Global Economic Summit", lazy=False, eager=True) + """
          <div class="bento-overlay">
            <span class="bento-tag">World Economic Chamber</span>
            <h2>Strengthening Global Economic Cooperation</h2>
            <p>An institutional anchor for organisations engaged in cross-border commerce, investment and economic cooperation — operating under principled governance and disciplined international engagement.</p>
            <div class="hero-actions">
              <a href="about.html" class="btn btn-primary btn-sm">Discover the Chamber</a>
              <a href="charter.html" class="btn btn-secondary btn-sm">Read Our Charter</a>
            </div>
          </div>
        </div>
        <div class="bento-sidebar">
          <div class="bento-sub">
            """ + picture_img("images/imposing_skyscraper.png", "WEC Headquarters", lazy=False, eager=True) + """
            <div class="bento-overlay">
              <span class="bento-tag" style="background: var(--pillar-governance); color: #fff;">Governance</span>
              <h3>Institutional Leadership</h3>
            </div>
          </div>
          <div class="bento-sub">
            """ + picture_img("images/office_collaboration.png", "Global Collaboration", lazy=False, eager=True) + """
            <div class="bento-overlay">
              <span class="bento-tag" style="background: var(--pillar-trade); color: #fff;">Trade</span>
              <h3>Cross-Border Dialogue</h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Top Economic Indicators Ticker -->
  <div class="indicators-ticker">
    <div class="ticker-inner">
      <span class="ticker-item"><span class="ticker-label">Global Trade Vol. Index:</span><span class="ticker-val up">+2.4% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Cross-Border Investment:</span><span class="ticker-val up">+1.8% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Policy Stability Index:</span><span class="ticker-val down">-0.5% &#9660;</span></span>
      <span class="ticker-item"><span class="ticker-label">Market Access Score:</span><span class="ticker-val up">+3.1% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Regulatory Convergence:</span><span class="ticker-val up">+1.2% &#9650;</span></span>
      <!-- Duplicate for infinite scroll -->
      <span class="ticker-item"><span class="ticker-label">Global Trade Vol. Index:</span><span class="ticker-val up">+2.4% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Cross-Border Investment:</span><span class="ticker-val up">+1.8% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Policy Stability Index:</span><span class="ticker-val down">-0.5% &#9660;</span></span>
      <span class="ticker-item"><span class="ticker-label">Market Access Score:</span><span class="ticker-val up">+3.1% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Regulatory Convergence:</span><span class="ticker-val up">+1.2% &#9650;</span></span>
    </div>
  </div>

  <!-- Information Dense Data Section -->
  <section class="section-dense">
    <div class="container">
      <div class="complex-grid fade-up fade-delay-1">
        <!-- Main News Column -->
        <div class="main-news">
          <div class="section-header-compact">
            <h3>Latest Announcements</h3>
            <a href="#" class="view-all">View All News &rarr;</a>
          </div>
          <div class="news-list">
            <a href="charter-and-governance.html" class="news-item">
              <span class="news-date">Today</span>
              <h4>World Economic Chamber formally establishes institutional charter and governance framework</h4>
              <p>The core foundational document defining the Chamber's institutional responsibilities has been formally ratified, marking a new era of global economic cooperation.</p>
            </a>
            <a href="secretariat-management.html" class="news-item">
              <span class="news-date">Yesterday</span>
              <h4>Executive Secretariat operational management protocols now published</h4>
              <p>In a move for transparency, the complete operational and management protocols of the Executive Secretariat are now available for review by member nations and institutional partners.</p>
            </a>
            <a href="decision-making.html" class="news-item">
              <span class="news-date">August 12, 2026</span>
              <h4>Decision-making procedures and approval pathways adopted by the Chamber</h4>
              <p>A new robust framework has been implemented to ensure all resolutions and cross-border commercial policies undergo rigorous, accountable review processes.</p>
            </a>
            <a href="oversight-responsibilities.html" class="news-item">
              <span class="news-date">August 05, 2026</span>
              <h4>Oversight responsibilities and accountability standards framework released</h4>
              <p>Detailed oversight mechanisms have been structured to ensure activities remain aligned with the institutional mandate and ethical standards.</p>
            </a>
          </div>
        </div>

        <!-- Upcoming Events / Calendar -->
        <div class="events-column">
          <div class="section-header-compact">
            <h3>Chamber Calendar</h3>
            <a href="#" class="view-all">All Events &rarr;</a>
          </div>
          <ul class="event-list">
            <li>
              <div class="event-date">
                <span class="day">18</span>
                <span class="month">Aug</span>
              </div>
              <div class="event-details">
                <h5>Global Market Access Summit</h5>
                <span class="event-location">Geneva, Switzerland</span>
              </div>
            </li>
            <li>
              <div class="event-date">
                <span class="day">24</span>
                <span class="month">Aug</span>
              </div>
              <div class="event-details">
                <h5>Secretariat Policy Review</h5>
                <span class="event-location">London, UK (HQ)</span>
              </div>
            </li>
            <li>
              <div class="event-date">
                <span class="day">03</span>
                <span class="month">Sep</span>
              </div>
              <div class="event-details">
                <h5>Trade &amp; Economy Working Group</h5>
                <span class="event-location">Virtual / Secure Link</span>
              </div>
            </li>
            <li>
              <div class="event-date">
                <span class="day">15</span>
                <span class="month">Sep</span>
              </div>
              <div class="event-details">
                <h5>Annual Governance Conference</h5>
                <span class="event-location">New York, USA</span>
              </div>
            </li>
          </ul>
          
          <div style="margin-top: var(--space-xl);">
            """ + picture_img("images/global_trade_hub.png", "Global Trade Hub", lazy=True, style="border-radius: var(--border-radius-md); width: 100%; object-fit: cover; height: 180px;") + """
          </div>
        </div>

        <!-- Data Vis / Stats -->
        <div class="data-column">
          <div class="section-header-compact">
            <h3>Key Metrics</h3>
          </div>
          <div class="data-stat">
            <span class="data-label">Active Trade Agreements</span>
            <div>
              <span class="data-value">1,402</span>
              <span class="data-trend up">+12 YoY</span>
            </div>
          </div>
          <div class="data-stat">
            <span class="data-label">Participating Nations</span>
            <div>
              <span class="data-value">164</span>
              <span class="data-trend up">+2</span>
            </div>
          </div>
          <div class="data-stat">
            <span class="data-label">Dispute Resolutions</span>
            <div>
              <span class="data-value">38</span>
              <span class="data-trend down">-5% &#9660;</span>
            </div>
          </div>
          <div class="data-stat">
            <span class="data-label">Policy Consultations</span>
            <div>
              <span class="data-value">840</span>
              <span class="data-trend up">+18%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Constellation Map -->
  <section class="section constellation-section section-dark fade-up fade-delay-2">
    <div class="container">
      <div class="text-center fade-in">
        <span class="section-label">Global Constellation</span>
        <h2 class="section-title">A Network of <span class="shimmer-gold">International Cooperation</span></h2>
        <div class="divider divider-center divider-thick"></div>
      </div>
      <div class="constellation-wrap" style="margin-top: var(--space-3xl);">
""" + CONSTELLATION_SVG + """
      </div>
      <div class="constellation-legend">
        <div class="constellation-legend-item">
          <div class="constellation-legend-dot" style="background: var(--pillar-governance);"></div>
          Governance
        </div>
        <div class="constellation-legend-item">
          <div class="constellation-legend-dot" style="background: var(--pillar-trade);"></div>
          Trade &amp; Economy
        </div>
        <div class="constellation-legend-item">
          <div class="constellation-legend-dot" style="background: var(--pillar-oversight);"></div>
          Oversight
        </div>
        <div class="constellation-legend-item">
          <div class="constellation-legend-dot" style="background: var(--pillar-cooperation);"></div>
          Cooperation
        </div>
      </div>
      <div class="constellation-stats">
        <div class="constellation-stat">
          <span class="constellation-stat-number" data-target="195" data-suffix="+">0</span>
          <span class="constellation-stat-label">Member Nations</span>
        </div>
        <div class="constellation-stat">
          <span class="constellation-stat-number" data-target="500" data-suffix="+">0</span>
          <span class="constellation-stat-label">Institutional Partners</span>
        </div>
        <div class="constellation-stat">
          <span class="constellation-stat-number" data-target="30">0</span>
          <span class="constellation-stat-label">Regional Offices</span>
        </div>
        <div class="constellation-stat">
          <span class="constellation-stat-number" data-target="50" data-suffix="+">0</span>
          <span class="constellation-stat-label">Trade Agreements</span>
        </div>
      </div>
    </div>
  </section>

"""

    html += FOOTER_HTML
    html += "\n</body>\n</html>"

    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("  [OK] Generated index.html")

def build_subpage(docx_file, page_info):
    docx_path = os.path.join(DOC_DIR, docx_file)
    if not os.path.exists(docx_path):
        print(f"  [!] Warning: {docx_file} not found.")
        return

    paragraphs = get_docx_paragraphs(docx_path)
    content_html, toc = paragraphs_to_html(paragraphs)

    html = head_html(page_info['title'], page_info['desc'])
    html += NAV_HTML

    pillar = page_info.get('pillar', 'governance')

    # Build sidebar TOC
    sidebar_items = ''
    for tag, text, slug in toc:
        indent = '  ' if tag == 'h3' else ''
        sidebar_items += f'            <li><a href="#{slug}">{indent}{text}</a></li>\n'

    html += f"""
  <!-- Page Header -->
  <div class="page-header" data-pillar="{pillar}">
    <div class="container">
      <span class="page-badge page-badge--{pillar}">{pillar.title()}</span>
      <h1>{page_info['title']}</h1>
      <div class="breadcrumb">{page_info['breadcrumb']}</div>
    </div>
  </div>

  <!-- Document Content -->
  <main>
    <div class="doc-layout">
      <aside class="doc-sidebar">
        <div class="doc-sidebar-inner">
          <h4 class="doc-sidebar-title">On this page</h4>
          <ul>
{sidebar_items}          </ul>
        </div>
      </aside>
      <div class="doc-content" data-pillar="{pillar}">
            {content_html}
      </div>
    </div>
  </main>
"""

    html += FOOTER_HTML
    html += "\n</body>\n</html>"

    with open(os.path.join(OUT_DIR, page_info['file']), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK] Generated {page_info['file']}")

if __name__ == '__main__':
    print("=" * 50)
    print("   WEC Website Generator — Premium Build")
    print("=" * 50)
    print()
    print("Building pages...")
    build_index()
    for docx_file, page_info in pages.items():
        build_subpage(docx_file, page_info)
    print()
    print("Site generation complete!")
