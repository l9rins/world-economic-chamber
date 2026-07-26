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
    article_num = 0
    for tag, text in paragraphs:
        text = text.replace('&', '&amp;')
        # Detect Article headers for charter pages
        if ('article' in text.lower() or text.strip().startswith('Article')) and text.strip()[:10].lower().startswith('article'):
            article_num += 1
            html.append(f'<div class="article"><span class="article-number">Article {article_num}</span><h2 class="article-title">{text}</h2></div>')
        elif tag in ('h1', 'h3'):
            html.append(f'<{tag}>{text}</{tag}>')
        elif tag == 'h2':
            html.append(f'<h2>{text}</h2>')
        else:
            html.append(f'<p>{text}</p>')
    return '\n            '.join(html)

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

NAV_HTML = """
  <!-- Navigation -->
  <nav class="nav" id="mainNav">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">
        <img src="images/Logo_WEC_White_Text.png" alt="World Economic Chamber">
      </a>

      <ul class="nav-menu" id="navMenu">
        <li class="nav-item">
          <a href="about.html" class="nav-link">About <svg class="nav-arrow" viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px"><polyline points="6 9 12 15 18 9"></polyline></svg></a>
          <div class="nav-dropdown">
            <a href="about.html">About the Chamber</a>
            <a href="charter-and-governance.html">Charter, Policies &amp; Governance</a>
          </div>
        </li>
        <li class="nav-item">
          <a href="charter.html" class="nav-link">Charter <svg class="nav-arrow" viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px"><polyline points="6 9 12 15 18 9"></polyline></svg></a>
          <div class="nav-dropdown">
            <a href="charter.html">The WEC Charter</a>
            <a href="governance-documents.html">Governance Documents</a>
          </div>
        </li>
        <li class="nav-item">
          <a href="governance-architecture.html" class="nav-link">Governance <svg class="nav-arrow" viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px"><polyline points="6 9 12 15 18 9"></polyline></svg></a>
          <div class="nav-dropdown">
            <a href="governance-architecture.html">Governance Architecture</a>
            <a href="decision-making.html">Decision-Making Procedures</a>
            <a href="oversight-responsibilities.html">Oversight &amp; Accountability</a>
            <a href="leadership-responsibilities.html">Leadership Responsibilities</a>
            <a href="secretariat-management.html">Executive Secretariat</a>
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
"""

FOOTER_HTML = """
  <!-- Floating Social Bar -->
  <div class="social-float">
    <a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg></a>
    <a href="#" aria-label="X / Twitter"><svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4l11.733 16h4.267l-11.733 -16z"></path><path d="M4 20l6.768 -6.768m2.46 -2.46l6.772 -6.772"></path></svg></a>
    <div class="social-float-line"></div>
  </div>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="images/Logo_WEC_White_Text.png" alt="WEC Logo">
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
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2026 World Economic Chamber. All rights reserved.</p>
        <div class="footer-social">
          <a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg></a>
          <a href="#" aria-label="X / Twitter"><svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M4 4l11.733 16h4.267l-11.733 -16z"></path><path d="M4 20l6.768 -6.768m2.46 -2.46l6.772 -6.772"></path></svg></a>
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
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="images/Logo WEC 1 [MAIN].png" type="image/png">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
"""

CONSTELLATION_SVG = """
  <svg viewBox="0 0 800 340" fill="none" xmlns="http://www.w3.org/2000/svg" class="constellation-draw-in">
    <!-- Connecting lines -->
    <path class="const-line" d="M110 250 L200 80 L310 190 L450 60 L530 170 L650 90 L720 220 L620 280 L530 170 L450 60 L310 190 L200 80" stroke="rgba(201,168,76,0.35)" stroke-width="1.2" fill="none"/>
    <path class="const-line" d="M310 190 L400 280 L530 170 L620 280" stroke="rgba(201,168,76,0.2)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M110 250 L220 300 L400 280 L530 170" stroke="rgba(10,88,166,0.25)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M450 60 L530 170 L650 90 L720 220" stroke="rgba(17,129,67,0.25)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M200 80 L310 190 L400 280" stroke="rgba(210,38,39,0.2)" stroke-width="0.7" fill="none"/>
    <path class="const-line" d="M110 250 L200 80" stroke="rgba(239,125,0,0.2)" stroke-width="0.7" fill="none"/>
    <!-- Dots -->
    <circle class="const-dot" cx="110" cy="250" r="4" fill="var(--pillar-cooperation)" opacity="0"/>
    <circle class="const-dot" cx="200" cy="80" r="4" fill="var(--pillar-cooperation)" opacity="0"/>
    <circle class="const-dot" cx="310" cy="190" r="4" fill="var(--pillar-oversight)" opacity="0"/>
    <circle class="const-dot" cx="450" cy="60" r="4" fill="var(--pillar-trade)" opacity="0"/>
    <circle class="const-dot" cx="530" cy="170" r="4" fill="var(--pillar-trade)" opacity="0"/>
    <circle class="const-dot" cx="650" cy="90" r="4" fill="var(--pillar-trade)" opacity="0"/>
    <circle class="const-dot" cx="720" cy="220" r="4" fill="var(--pillar-trade)" opacity="0"/>
    <circle class="const-dot" cx="620" cy="280" r="4" fill="var(--pillar-oversight)" opacity="0"/>
    <circle class="const-dot" cx="400" cy="280" r="4" fill="var(--pillar-governance)" opacity="0"/>
    <circle class="const-dot" cx="220" cy="300" r="4" fill="var(--pillar-governance)" opacity="0"/>
    <!-- Gold central node -->
    <circle class="const-dot" cx="380" cy="170" r="6" fill="var(--gold-500)" opacity="0"/>
  </svg>
"""

def build_index():
    html = head_html("Global Economic Leadership", "The World Economic Chamber — strengthening cross-border commerce, investment and economic cooperation through principled governance.")
    html += NAV_HTML

    html += """
  <!-- News Ticker -->
  <div class="news-ticker">
    <div class="container">
      <div class="news-ticker-inner">
        <span class="news-ticker-item"><span class="news-ticker-dot"></span> <strong>Announcement:</strong> World Economic Chamber formally establishes institutional charter and governance framework</span>
        <span class="news-ticker-item"><span class="news-ticker-dot"></span> <strong>Governance:</strong> Executive Secretariat operational management protocols now published</span>
        <span class="news-ticker-item"><span class="news-ticker-dot"></span> <strong>Update:</strong> Decision-making procedures and approval pathways adopted by the Chamber</span>
        <span class="news-ticker-item"><span class="news-ticker-dot"></span> <strong>New:</strong> Oversight responsibilities and accountability standards framework released</span>
        <span class="news-ticker-item"><span class="news-ticker-dot"></span> <strong>Announcement:</strong> World Economic Chamber formally establishes institutional charter and governance framework</span>
        <span class="news-ticker-item"><span class="news-ticker-dot"></span> <strong>Governance:</strong> Executive Secretariat operational management protocols now published</span>
        <span class="news-ticker-item"><span class="news-ticker-dot"></span> <strong>Update:</strong> Decision-making procedures and approval pathways adopted by the Chamber</span>
        <span class="news-ticker-item"><span class="news-ticker-dot"></span> <strong>New:</strong> Oversight responsibilities and accountability standards framework released</span>
      </div>
    </div>
  </div>

  <!-- Hero Section -->
  <section class="hero" id="hero">
    <div class="hero-bg">
      <img src="images/hero-summit.png" alt="Global Economic Summit" loading="eager">
    </div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <span class="section-label">World Economic Chamber</span>
      <h1 class="hero-title">Strengthening <span class="accent shimmer-gold">Global Economic</span> Cooperation</h1>
      <p class="hero-subtitle">An institutional anchor for organisations engaged in cross-border commerce, investment and economic cooperation — operating under principled governance and disciplined international engagement.</p>
      <div class="hero-actions">
        <a href="about.html" class="btn btn-primary btn-lg">Discover the Chamber</a>
        <a href="charter.html" class="btn btn-secondary btn-lg">Read Our Charter</a>
      </div>
    </div>
  </section>

  <!-- Quick Links Bar -->
  <div class="quick-links-bar">
    <div class="container">
      <div class="quick-links-inner">
        <a href="charter.html" class="quick-link-item">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
          Charter
        </a>
        <a href="governance-architecture.html" class="quick-link-item">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M3 21h18M4 17h16M4 7h16M2 21h20M12 2L2 7v2h20V7L12 2z"></path></svg>
          Governance
        </a>
        <a href="decision-making.html" class="quick-link-item">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg>
          Decision-Making
        </a>
        <a href="oversight-responsibilities.html" class="quick-link-item">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
          Oversight
        </a>
        <a href="secretariat-management.html" class="quick-link-item">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          Secretariat
        </a>
        <a href="about.html" class="quick-link-item">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
          About
        </a>
      </div>
    </div>
  </div>

  <!-- Mission Statement -->
  <section class="section" id="mission">
    <div class="container">
      <div class="text-center fade-in">
        <span class="section-label">Our Mandate</span>
        <h2 class="section-title">Principled Governance for International Business</h2>
        <div class="divider divider-center divider-thick"></div>
        <p class="section-subtitle" style="margin: var(--space-xl) auto 0;">The WEC provides a structured, principled setting in which multinational institutions, corporations, businesses, NGOs and government bodies can engage with one another under a common framework of professionalism, integrity and long-term economic stewardship.</p>
      </div>
    </div>
  </section>

  <!-- Features Highlights -->
  <section class="section-sm section-alt">
    <div class="container">
      <div class="feature-grid">
        <div class="feature-item">
          <div class="feature-icon" style="background: rgba(10,88,166,0.12); color: var(--pillar-governance);"><svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg></div>
          <h4>Principled Governance</h4>
          <p>Institutional integrity as a core operating principle</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon" style="background: rgba(17,129,67,0.12); color: var(--pillar-trade);"><svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></div>
          <h4>Global Reach</h4>
          <p>Operating across jurisdictions with neutrality</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon" style="background: rgba(210,38,39,0.12); color: var(--pillar-oversight);"><svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg></div>
          <h4>Institutional Leadership</h4>
          <p>Structured, accountable governance architecture</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon" style="background: rgba(239,125,0,0.12); color: var(--pillar-cooperation);"><svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg></div>
          <h4>Constructive Dialogue</h4>
          <p>Cross-border cooperation through disciplined engagement</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Constellation Map — replaces stat counters -->
  <section class="section constellation-section">
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

  <!-- Core Sections Grid -->
  <section class="section" id="sections">
    <div class="container">
      <div class="text-center fade-in">
        <span class="section-label">What We Do</span>
        <h2 class="section-title">Core Institutional Functions</h2>
        <div class="divider divider-center divider-thick"></div>
      </div>

      <div class="grid grid-3" style="margin-top: var(--space-3xl);">
        <a href="charter.html" class="card" style="text-decoration:none;">
          <div class="card-icon pillar-governance"><svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg></div>
          <h3 class="card-title">Charter &amp; Mandate</h3>
          <p class="card-text">The foundational document that establishes the Chamber's institutional purpose, authorities and the principles guiding cross-border economic engagement.</p>
          <span class="card-link">Read the Charter <svg class="link-arrow" viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px; margin-bottom:-2px"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></span>
        </a>

        <a href="governance-architecture.html" class="card" style="text-decoration:none;">
          <div class="card-icon pillar-governance"><svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none"><path d="M3 21h18M4 17h16M4 7h16M2 21h20M12 2L2 7v2h20V7L12 2z"></path><path d="M6 9v8M10 9v8M14 9v8M18 9v8"></path></svg></div>
          <h3 class="card-title">Governance Architecture</h3>
          <p class="card-text">Structured pathways, institutional roles and decision-making frameworks that define how the Chamber operates across jurisdictions.</p>
          <span class="card-link">Explore Architecture <svg class="link-arrow" viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px; margin-bottom:-2px"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></span>
        </a>

        <a href="oversight-responsibilities.html" class="card" style="text-decoration:none;">
          <div class="card-icon pillar-oversight"><svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></div>
          <h3 class="card-title">Oversight &amp; Accountability</h3>
          <p class="card-text">Oversight responsibilities, accountability standards and the safeguards that protect the Chamber's independence and institutional integrity.</p>
          <span class="card-link">View Standards <svg class="link-arrow" viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px; margin-bottom:-2px"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></span>
        </a>

        <a href="decision-making.html" class="card" style="text-decoration:none;">
          <div class="card-icon pillar-oversight"><svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg></div>
          <h3 class="card-title">Decision-Making</h3>
          <p class="card-text">Transparent, accountable decision-making procedures and approval pathways for all Chamber initiatives and cross-border programs.</p>
          <span class="card-link">View Procedures <svg class="link-arrow" viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px; margin-bottom:-2px"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></span>
        </a>

        <a href="leadership-responsibilities.html" class="card" style="text-decoration:none;">
          <div class="card-icon pillar-oversight"><svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg></div>
          <h3 class="card-title">Leadership &amp; Secretariat</h3>
          <p class="card-text">Leadership responsibilities, governance oversight and the operational management protocols of the Executive Secretariat.</p>
          <span class="card-link">Learn More <svg class="link-arrow" viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px; margin-bottom:-2px"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></span>
        </a>

        <a href="about.html" class="card" style="text-decoration:none;">
          <div class="card-icon pillar-cooperation"><svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg></div>
          <h3 class="card-title">Global Engagement</h3>
          <p class="card-text">The Chamber's engagement model — supporting institutions that work across borders through constructive international dialogue and institutional neutrality.</p>
          <span class="card-link">Discover Our Model <svg class="link-arrow" viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px; margin-bottom:-2px"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></span>
        </a>
      </div>
    </div>
  </section>

  <!-- Featured Section - Split -->
  <section class="section section-alt">
    <div class="container">
      <div class="content-split">
        <div class="fade-in">
          <span class="section-label">Founding Principles</span>
          <h2 class="section-title">Integrity, Independence &amp; Constructive Internationalism</h2>
          <div class="divider divider-thick"></div>
          <p>The Chamber is built on a set of principles that reflect the responsibilities associated with international economic engagement. Members are expected to conduct themselves in a manner that respects regulatory frameworks, honours contractual obligations and recognises the broader implications of international activity.</p>
          <p>A governance structure that protects the institution from commercial, political or sector-specific influence allows the Chamber to operate with clarity of purpose and maintain credibility across jurisdictions.</p>
          <a href="charter.html" class="btn btn-outline-gold btn-lg" style="margin-top: var(--space-md);">Read the Charter</a>
        </div>
        <div class="img-duotone">
          <img src="images/hero-partnership.png" alt="Global Partnership">
        </div>
      </div>
    </div>
  </section>

  <!-- Section Divider -->
  <div class="section-divider">
    <svg viewBox="0 0 1440 60" preserveAspectRatio="none" fill="rgba(10, 22, 40, 1)"><path d="M0,30 C360,60 1080,0 1440,30 L1440,60 L0,60 Z"></path></svg>
  </div>

  <!-- Testimonials / Institutional Recognition -->
  <section class="section section-dark">
    <div class="container">
      <div class="text-center fade-in">
        <span class="section-label">Institutional Recognition</span>
        <h2 class="section-title">Trusted by the Global Community</h2>
        <div class="divider divider-center divider-thick"></div>
      </div>

      <div class="testimonials" style="margin-top: var(--space-3xl);">
        <div class="testimonial-card">
          <p class="testimonial-text">The WEC's governance framework brings much-needed rigour and consistency to international commercial engagement. This is a serious institution for serious practitioners of global commerce.</p>
          <div class="testimonial-author">
            <div class="testimonial-avatar">HM</div>
            <div>
              <div class="testimonial-name">Helena Morais</div>
              <div class="testimonial-role">Director of International Trade — European Business Council</div>
            </div>
          </div>
        </div>

        <div class="testimonial-card">
          <p class="testimonial-text">What distinguishes the WEC is its insistence on institutional neutrality and ethical discipline as core competencies. The global economy needs exactly this kind of institutional leadership.</p>
          <div class="testimonial-author">
            <div class="testimonial-avatar">RK</div>
            <div>
              <div class="testimonial-name">Rajesh Kumar</div>
              <div class="testimonial-role">Senior Advisor, Economic Cooperation — ASEAN Secretariat</div>
            </div>
          </div>
        </div>

        <div class="testimonial-card">
          <p class="testimonial-text">The Chamber's commitment to principled governance and long-term economic stewardship provides a credible and reliable counterpart for governments engaging in cross-border economic dialogue.</p>
          <div class="testimonial-author">
            <div class="testimonial-avatar">AP</div>
            <div>
              <div class="testimonial-name">Amira Patel</div>
              <div class="testimonial-role">Chief Economist — African Development Bank</div>
            </div>
          </div>
        </div>

        <div class="testimonial-card">
          <p class="testimonial-text">As an institution, the WEC understands that cross-border business requires cooperation, not just facilitation. Their structured approach to international dialogue is precisely what the profession needs.</p>
          <div class="testimonial-author">
            <div class="testimonial-avatar">JW</div>
            <div>
              <div class="testimonial-name">James Whitfield</div>
              <div class="testimonial-role">Managing Partner, Global Markets — Deloitte</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Section Divider -->
  <div class="section-divider" style="transform: rotate(180deg);">
    <svg viewBox="0 0 1440 60" preserveAspectRatio="none" fill="var(--navy-800)"><path d="M0,30 C360,60 1080,0 1440,30 L1440,60 L0,60 Z"></path></svg>
  </div>

  <!-- Featured Image Showcase -->
  <section class="section section-gradient">
    <div class="container">
      <div class="content-split">
        <div class="img-duotone">
          <img src="images/hero-governance.png" alt="Governance Meeting" style="border-radius: var(--border-radius-lg);">
        </div>
        <div class="fade-in">
          <span class="section-label">Governance Framework</span>
          <h2 class="section-title">Structured, Accountable &amp; Transparent</h2>
          <div class="divider divider-thick"></div>
          <p>The Chamber operates through defined authorities, documented policies and clear decision-making processes. Governance responsibilities are allocated to support oversight, maintain ethical standards and ensure activities remain aligned with the institutional mandate.</p>
          <p>This framework is the mechanism through which the Chamber safeguards its credibility and ensures that its work contributes to a more stable and responsible global economic system.</p>
          <a href="governance-architecture.html" class="btn btn-outline-gold btn-lg" style="margin-top: var(--space-md);">Explore Governance</a>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="section section-alt">
    <div class="container">
      <div class="text-center fade-in">
        <span class="section-label">Engage With the Chamber</span>
        <h2 class="section-title">International Cooperation Through Principled Governance</h2>
        <div class="divider divider-center divider-thick"></div>
        <p class="section-subtitle" style="margin: 0 auto var(--space-2xl);">The World Economic Chamber welcomes institutions committed to professional conduct, ethical integrity and the long-term stability of global markets.</p>
        <div class="hero-actions" style="justify-content: center;">
          <a href="about.html" class="btn btn-primary btn-lg">About the Chamber</a>
          <a href="charter.html" class="btn btn-secondary btn-lg">Read Our Charter</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Newsletter -->
  <section class="section-sm section-dark">
    <div class="container">
      <div class="newsletter-box fade-in">
        <span class="section-label">Stay Informed</span>
        <h3 style="font-family: var(--font-heading); font-size: var(--font-size-2xl); color: var(--white);">Subscribe to the WEC Briefing</h3>
        <p style="font-size: var(--font-size-sm); color: var(--text-secondary); max-width: 500px; margin: var(--space-md) auto 0;">Policy updates, governance announcements and institutional developments delivered to your inbox.</p>
        <form class="newsletter-form" onsubmit="event.preventDefault();alert('Thank you for subscribing to the WEC Briefing.');">
          <input type="email" class="form-input" placeholder="your@email.com" required>
          <button type="submit" class="btn btn-primary">Subscribe</button>
        </form>
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
    content_html = paragraphs_to_html(paragraphs)

    html = head_html(page_info['title'], page_info['desc'])
    html += NAV_HTML

    pillar = page_info.get('pillar', 'governance')
    badge_color = {
        'governance': '#0A58A6',
        'trade': '#118143',
        'oversight': '#D22627',
        'cooperation': '#EF7D00'
    }.get(pillar, '#c9a84c')

    html += f"""
  <!-- Page Header -->
  <div class="page-header">
    <div class="container">
      <span class="page-badge">
        <span style="width:8px;height:8px;border-radius:50%;display:inline-block;background:{badge_color};"></span>
        {pillar.title()}
      </span>
      <h1>{page_info['title']}</h1>
      <div class="breadcrumb">{page_info['breadcrumb']}</div>
    </div>
  </div>

  <!-- Document Content -->
  <main>
    <div class="doc-content">
            {content_html}
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
    print(f"  Generated {1 + len(pages)} pages total.")
