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
    },
    "1Bf.  Coordination and Reporting Procedures Between Leadership and Secretariat.docx": {
        "file": "coordination-reporting.html",
        "title": "Coordination & Reporting Procedures",
        "desc": "Coordination and reporting procedures between leadership and the Executive Secretariat.",
        "breadcrumb": "Home / Governance / Coordination & Reporting",
        "pillar": "governance"
    },
    "1Bg.  Secretariat Documentation, Record-Keeping and Complilance Requirements.docx": {
        "file": "secretariat-documentation.html",
        "title": "Secretariat Documentation & Record-Keeping",
        "desc": "Documentation, record-keeping and compliance requirements for the Executive Secretariat.",
        "breadcrumb": "Home / Governance / Secretariat Documentation",
        "pillar": "governance"
    },
    "1Bh.  Institutional Accountability and Performance-Monitoring Guidelines.docx": {
        "file": "institutional-accountability.html",
        "title": "Institutional Accountability & Performance Monitoring",
        "desc": "Institutional accountability and performance-monitoring guidelines.",
        "breadcrumb": "Home / Governance / Accountability",
        "pillar": "oversight"
    },
    "1Bi.  Institutional Independence and Neutrality Policy.docx": {
        "file": "institutional-independence.html",
        "title": "Institutional Independence & Neutrality",
        "desc": "Policy on institutional independence and neutrality.",
        "breadcrumb": "Home / Governance / Independence",
        "pillar": "governance"
    },
    "1Bj.  Regulatory Engagement Standards.docx": {
        "file": "regulatory-engagement.html",
        "title": "Regulatory Engagement Standards",
        "desc": "Standards for regulatory engagement and interaction.",
        "breadcrumb": "Home / Governance / Regulatory Engagement",
        "pillar": "governance"
    },
    "1Bk.  Cross-Jurisdictional Consultation and Coordination Procedures.docx": {
        "file": "cross-jurisdictional-consultation.html",
        "title": "Cross-Jurisdictional Consultation & Coordination",
        "desc": "Procedures for cross-jurisdictional consultation and coordination.",
        "breadcrumb": "Home / Governance / Cross-Jurisdictional",
        "pillar": "cooperation"
    },
    "1Bl.  Regulatory Correspondence and Information-Handling Guidelines.docx": {
        "file": "regulatory-correspondence.html",
        "title": "Regulatory Correspondence & Information Handling",
        "desc": "Guidelines for regulatory correspondence and information handling.",
        "breadcrumb": "Home / Governance / Regulatory Correspondence",
        "pillar": "governance"
    },
    "1Bm.  Regulatory Meeting and Submission Protocols.docx": {
        "file": "regulatory-meeting-protocols.html",
        "title": "Regulatory Meeting & Submission Protocols",
        "desc": "Protocols for regulatory meetings and submissions.",
        "breadcrumb": "Home / Governance / Meeting Protocols",
        "pillar": "governance"
    },
    "1Bn.  Cross-Border Engagement Standards.docx": {
        "file": "cross-border-engagement.html",
        "title": "Cross-Border Engagement Standards",
        "desc": "Standards for cross-border engagement and interaction.",
        "breadcrumb": "Home / Governance / Cross-Border Engagement",
        "pillar": "cooperation"
    },
    "1Bo.  International Coordination and Liaison Procedures.docx": {
        "file": "international-coordination.html",
        "title": "International Coordination & Liaison",
        "desc": "Procedures for international coordination and liaison.",
        "breadcrumb": "Home / Governance / International Coordination",
        "pillar": "cooperation"
    },
    "1Bp.  Cross-Jurisdictional Communication and Information-Handling Guidelines.docx": {
        "file": "cross-jurisdictional-communication.html",
        "title": "Cross-Jurisdictional Communication & Information Handling",
        "desc": "Guidelines for cross-jurisdictional communication and information handling.",
        "breadcrumb": "Home / Governance / Communication Guidelines",
        "pillar": "cooperation"
    },
    "1Bq.  Cross-Border Meeting, Consultation and Participation Protocols.docx": {
        "file": "cross-border-meeting-protocols.html",
        "title": "Cross-Border Meeting & Consultation Protocols",
        "desc": "Protocols for cross-border meetings, consultation and participation.",
        "breadcrumb": "Home / Governance / Cross-Border Meetings",
        "pillar": "cooperation"
    },
    "1Br.  Core Record-Keeping Requirements.docx": {
        "file": "core-record-keeping.html",
        "title": "Core Record-Keeping Requirements",
        "desc": "Core requirements for institutional record-keeping.",
        "breadcrumb": "Home / Governance / Record-Keeping",
        "pillar": "governance"
    },
    "1Bs.  Documentation Standards for Governance and Decision-Making.docx": {
        "file": "documentation-standards.html",
        "title": "Documentation Standards for Governance",
        "desc": "Documentation standards for governance and decision-making processes.",
        "breadcrumb": "Home / Governance / Documentation Standards",
        "pillar": "governance"
    },
    "1Bt.  Operational Documentation and Archival Procedures.docx": {
        "file": "operational-documentation.html",
        "title": "Operational Documentation & Archival",
        "desc": "Procedures for operational documentation and archival.",
        "breadcrumb": "Home / Governance / Documentation & Archival",
        "pillar": "governance"
    },
    "1Bu.  Cross‑Border Engagement Record‑Keeping Protocols.docx": {
        "file": "cross-border-record-keeping.html",
        "title": "Cross-Border Engagement Record-Keeping",
        "desc": "Protocols for cross-border engagement record-keeping.",
        "breadcrumb": "Home / Governance / Cross-Border Records",
        "pillar": "cooperation"
    },
    "1Bv.  Compliance, Audit and Retrieval Guidelines.docx": {
        "file": "compliance-audit.html",
        "title": "Compliance, Audit & Retrieval Guidelines",
        "desc": "Guidelines for compliance, audit and retrieval.",
        "breadcrumb": "Home / Governance / Compliance & Audit",
        "pillar": "oversight"
    },
    "1C.  Ethical and Conduct Policies.docx": {
        "file": "ethical-conduct-policies.html",
        "title": "Ethical & Conduct Policies",
        "desc": "Ethical and conduct policies of the World Economic Chamber.",
        "breadcrumb": "Home / Governance / Ethics & Conduct",
        "pillar": "oversight"
    },
    "1Ca.  Member Conduct and Professional Standards Policy.docx": {
        "file": "member-conduct.html",
        "title": "Member Conduct & Professional Standards",
        "desc": "Policy on member conduct and professional standards.",
        "breadcrumb": "Home / Governance / Member Conduct",
        "pillar": "oversight"
    },
    "1Cb.  Conflict of Interest Management Policy.docx": {
        "file": "conflict-of-interest.html",
        "title": "Conflict of Interest Management",
        "desc": "Policy on conflict of interest management.",
        "breadcrumb": "Home / Governance / Conflict of Interest",
        "pillar": "oversight"
    },
    "1Cc.  Ethical Business Practices and Compliance Policy.docx": {
        "file": "ethical-business-practices.html",
        "title": "Ethical Business Practices & Compliance",
        "desc": "Policy on ethical business practices and compliance.",
        "breadcrumb": "Home / Governance / Ethical Practices",
        "pillar": "oversight"
    },
    "1Cd.  Jurisdictional Respect and Regulatory Adherence Policy.docx": {
        "file": "jurisdictional-respect.html",
        "title": "Jurisdictional Respect & Regulatory Adherence",
        "desc": "Policy on jurisdictional respect and regulatory adherence.",
        "breadcrumb": "Home / Governance / Jurisdictional Respect",
        "pillar": "governance"
    },
    "1D.  Operational Policies.docx": {
        "file": "operational-policies.html",
        "title": "Operational Policies",
        "desc": "Operational policies of the World Economic Chamber.",
        "breadcrumb": "Home / Governance / Operational Policies",
        "pillar": "governance"
    },
    "1Da.  Program Design and Approval Protocols.docx": {
        "file": "program-design-approval.html",
        "title": "Program Design & Approval Protocols",
        "desc": "Protocols for program design and approval.",
        "breadcrumb": "Home / Governance / Program Design",
        "pillar": "governance"
    },
    "1Db. Cross-Border Initiative Implementation Procedures.docx": {
        "file": "cross-border-initiative.html",
        "title": "Cross-Border Initiative Implementation",
        "desc": "Procedures for cross-border initiative implementation.",
        "breadcrumb": "Home / Governance / Cross-Border Initiatives",
        "pillar": "cooperation"
    },
    "1Dc. Stakeholder Coordination and Engagement Standards.docx": {
        "file": "stakeholder-coordination.html",
        "title": "Stakeholder Coordination & Engagement",
        "desc": "Standards for stakeholder coordination and engagement.",
        "breadcrumb": "Home / Governance / Stakeholder Coordination",
        "pillar": "cooperation"
    },
    "1Dd. Program Documentation & Record‑Keeping Requirements.docx": {
        "file": "program-documentation.html",
        "title": "Program Documentation & Record-Keeping",
        "desc": "Requirements for program documentation and record-keeping.",
        "breadcrumb": "Home / Governance / Program Documentation",
        "pillar": "governance"
    },
    "1De. Monitoring, Reporting & Evaluation Framework.docx": {
        "file": "monitoring-reporting.html",
        "title": "Monitoring, Reporting & Evaluation",
        "desc": "Framework for monitoring, reporting and evaluation.",
        "breadcrumb": "Home / Governance / Monitoring & Reporting",
        "pillar": "oversight"
    },
    "1Df. Risk Management & Issue Escalation Procedures.docx": {
        "file": "risk-management.html",
        "title": "Risk Management & Issue Escalation",
        "desc": "Procedures for risk management and issue escalation.",
        "breadcrumb": "Home / Governance / Risk Management",
        "pillar": "oversight"
    },
    "1Dg. Public‑Institution Engagement Protocols.docx": {
        "file": "public-institution-engagement.html",
        "title": "Public-Institution Engagement Protocols",
        "desc": "Protocols for public-institution engagement.",
        "breadcrumb": "Home / Governance / Public-Institution Engagement",
        "pillar": "governance"
    },
    "1Dh. Operational Compliance & Quality Assurance Standards.docx": {
        "file": "operational-compliance.html",
        "title": "Operational Compliance & Quality Assurance",
        "desc": "Standards for operational compliance and quality assurance.",
        "breadcrumb": "Home / Governance / Operational Compliance",
        "pillar": "oversight"
    },
    "1Di. Program Communications & Information Handling Policy.docx": {
        "file": "program-communications.html",
        "title": "Program Communications & Information Handling",
        "desc": "Policy on program communications and information handling.",
        "breadcrumb": "Home / Governance / Program Communications",
        "pillar": "governance"
    },
    "1Dj. Public‑Institution Engagement Protocol.docx": {
        "file": "public-institution-protocol.html",
        "title": "Public-Institution Engagement Protocol",
        "desc": "Protocol for engagement with public institutions.",
        "breadcrumb": "Home / Governance / Public-Institution Protocol",
        "pillar": "governance"
    },
    "1Dk. Government & Regulatory Liaison Standards.docx": {
        "file": "government-liaison.html",
        "title": "Government & Regulatory Liaison Standards",
        "desc": "Standards for government and regulatory liaison.",
        "breadcrumb": "Home / Governance / Government Liaison",
        "pillar": "governance"
    },
    "1Dl. Cross‑Border Regulatory Coordination Procedures.docx": {
        "file": "cross-border-regulatory.html",
        "title": "Cross-Border Regulatory Coordination",
        "desc": "Procedures for cross-border regulatory coordination.",
        "breadcrumb": "Home / Governance / Cross-Border Regulatory",
        "pillar": "cooperation"
    },
    "1Dm. Official Communications & Correspondence Guidelines.docx": {
        "file": "official-communications.html",
        "title": "Official Communications & Correspondence",
        "desc": "Guidelines for official communications and correspondence.",
        "breadcrumb": "Home / Governance / Official Communications",
        "pillar": "governance"
    },
    "1Dn. Public‑Sector Meeting & Consultation Procedures.docx": {
        "file": "public-sector-meeting.html",
        "title": "Public-Sector Meeting & Consultation",
        "desc": "Procedures for public-sector meetings and consultations.",
        "breadcrumb": "Home / Governance / Public-Sector Meetings",
        "pillar": "governance"
    },
    "1Do. Documentation, Reporting & Record‑Keeping Requirements.docx": {
        "file": "documentation-reporting.html",
        "title": "Documentation, Reporting & Record-Keeping",
        "desc": "Requirements for documentation, reporting and record-keeping.",
        "breadcrumb": "Home / Governance / Documentation & Reporting",
        "pillar": "governance"
    },
    "1Dp. Institutional Neutrality & Influence‑Safeguard Policy.docx": {
        "file": "institutional-neutrality.html",
        "title": "Institutional Neutrality & Influence Safeguard",
        "desc": "Policy on institutional neutrality and influence safeguards.",
        "breadcrumb": "Home / Governance / Neutrality & Safeguards",
        "pillar": "governance"
    },
    "1Dq. International Cooperation Framework.docx": {
        "file": "international-cooperation-framework.html",
        "title": "International Cooperation Framework",
        "desc": "Framework for international cooperation.",
        "breadcrumb": "Home / Governance / Cooperation Framework",
        "pillar": "cooperation"
    },
    "1Dr. Cross‑Border Liaison & Coordination Standards.docx": {
        "file": "cross-border-liaison.html",
        "title": "Cross-Border Liaison & Coordination",
        "desc": "Standards for cross-border liaison and coordination.",
        "breadcrumb": "Home / Governance / Cross-Border Liaison",
        "pillar": "cooperation"
    },
    "1Ds. Multilateral Engagement Procedures.docx": {
        "file": "multilateral-engagement.html",
        "title": "Multilateral Engagement Procedures",
        "desc": "Procedures for multilateral engagement.",
        "breadcrumb": "Home / Governance / Multilateral Engagement",
        "pillar": "cooperation"
    },
    "1Dt. International Partnership Development Guidelines.docx": {
        "file": "international-partnership.html",
        "title": "International Partnership Development",
        "desc": "Guidelines for international partnership development.",
        "breadcrumb": "Home / Governance / Partnership Development",
        "pillar": "cooperation"
    },
    "1Du. Cross‑Jurisdictional Information‑Sharing Protocols.docx": {
        "file": "information-sharing.html",
        "title": "Cross-Jurisdictional Information Sharing",
        "desc": "Protocols for cross-jurisdictional information sharing.",
        "breadcrumb": "Home / Governance / Information Sharing",
        "pillar": "cooperation"
    },
    "1Dv. Cooperation Program Documentation & Record‑Keeping Requirements.docx": {
        "file": "cooperation-documentation.html",
        "title": "Cooperation Program Documentation & Record-Keeping",
        "desc": "Requirements for cooperation program documentation and record-keeping.",
        "breadcrumb": "Home / Governance / Cooperation Documentation",
        "pillar": "cooperation"
    },
    "1Dw. Institutional Neutrality & Safeguard Measures for International Engagement.docx": {
        "file": "neutrality-safeguard-international.html",
        "title": "Neutrality & Safeguard Measures for International Engagement",
        "desc": "Institutional neutrality and safeguard measures for international engagement.",
        "breadcrumb": "Home / Governance / International Safeguards",
        "pillar": "governance"
    },
    "1Dx. Participation Eligibility & Institutional Conduct Requirements.docx": {
        "file": "participation-eligibility.html",
        "title": "Participation Eligibility & Institutional Conduct",
        "desc": "Requirements for participation eligibility and institutional conduct.",
        "breadcrumb": "Home / Governance / Participation Eligibility",
        "pillar": "governance"
    },
    "1Dy. Forum & Initiative Engagement Protocols.docx": {
        "file": "forum-engagement.html",
        "title": "Forum & Initiative Engagement Protocols",
        "desc": "Protocols for forum and initiative engagement.",
        "breadcrumb": "Home / Governance / Forum Engagement",
        "pillar": "cooperation"
    },
    "1Dz. Cross‑Border Discussion & Collaboration Standards.docx": {
        "file": "cross-border-discussion.html",
        "title": "Cross-Border Discussion & Collaboration",
        "desc": "Standards for cross-border discussion and collaboration.",
        "breadcrumb": "Home / Governance / Cross-Border Collaboration",
        "pillar": "cooperation"
    },
    "1Dz2. Professional Conduct & Behavioural Expectations.docx": {
        "file": "professional-conduct.html",
        "title": "Professional Conduct & Behavioural Expectations",
        "desc": "Professional conduct and behavioural expectations.",
        "breadcrumb": "Home / Governance / Professional Conduct",
        "pillar": "oversight"
    },
    "1Dz3. Confidentiality, Information‑Handling & Disclosure Guidelines.docx": {
        "file": "confidentiality-guidelines.html",
        "title": "Confidentiality, Information Handling & Disclosure",
        "desc": "Guidelines for confidentiality, information handling and disclosure.",
        "breadcrumb": "Home / Governance / Confidentiality",
        "pillar": "governance"
    },
    "1Dz4. Participation Documentation & Record‑Keeping Procedures.docx": {
        "file": "participation-documentation.html",
        "title": "Participation Documentation & Record-Keeping",
        "desc": "Procedures for participation documentation and record-keeping.",
        "breadcrumb": "Home / Governance / Participation Documentation",
        "pillar": "governance"
    },
    "1Dz5. Institutional Neutrality & Influence‑Safeguard Measures.docx": {
        "file": "influence-safeguard.html",
        "title": "Institutional Neutrality & Influence Safeguard Measures",
        "desc": "Institutional neutrality and influence safeguard measures.",
        "breadcrumb": "Home / Governance / Influence Safeguards",
        "pillar": "governance"
    },
    "1Dz6. Communications and Institutional Correspondence Policy.docx": {
        "file": "institutional-correspondence.html",
        "title": "Communications & Institutional Correspondence",
        "desc": "Policy on communications and institutional correspondence.",
        "breadcrumb": "Home / Governance / Institutional Correspondence",
        "pillar": "governance"
    },
    "1E.  Safeguard and Integrity Rules.docx": {
        "file": "safeguard-integrity.html",
        "title": "Safeguard & Integrity Rules",
        "desc": "Safeguard and integrity rules of the World Economic Chamber.",
        "breadcrumb": "Home / Governance / Safeguard & Integrity",
        "pillar": "oversight"
    },
    "1Ea.  Independence Safeguards and Influence-Protection Policy.docx": {
        "file": "independence-safeguards.html",
        "title": "Independence Safeguards & Influence Protection",
        "desc": "Policy on independence safeguards and influence protection.",
        "breadcrumb": "Home / Governance / Independence Safeguards",
        "pillar": "oversight"
    },
    "1Eb.  Transparency and Disclosure Expectations.docx": {
        "file": "transparency-disclosure.html",
        "title": "Transparency & Disclosure Expectations",
        "desc": "Expectations for transparency and disclosure.",
        "breadcrumb": "Home / Governance / Transparency & Disclosure",
        "pillar": "oversight"
    },
    "1Ec.  Institutional Risk Management Guidelines.docx": {
        "file": "institutional-risk-management.html",
        "title": "Institutional Risk Management",
        "desc": "Guidelines for institutional risk management.",
        "breadcrumb": "Home / Governance / Risk Management",
        "pillar": "oversight"
    },
    "2.  Membership.docx": {
        "file": "membership.html",
        "title": "Membership",
        "desc": "Membership information for the World Economic Chamber.",
        "breadcrumb": "Home / Membership",
        "pillar": "cooperation"
    },
    "3.  Global Relations and Regional Engagement.docx": {
        "file": "global-relations.html",
        "title": "Global Relations & Regional Engagement",
        "desc": "Global relations and regional engagement of the World Economic Chamber.",
        "breadcrumb": "Home / Global Relations",
        "pillar": "cooperation"
    },
    "4.  Programs and Initiatives.docx": {
        "file": "programs-initiatives.html",
        "title": "Programs & Initiatives",
        "desc": "Programs and initiatives of the World Economic Chamber.",
        "breadcrumb": "Home / Programs & Initiatives",
        "pillar": "trade"
    },
    "5.  Policy and Advocacy.docx": {
        "file": "policy-advocacy.html",
        "title": "Policy & Advocacy",
        "desc": "Policy and advocacy efforts of the World Economic Chamber.",
        "breadcrumb": "Home / Policy & Advocacy",
        "pillar": "governance"
    },
    "6.  Research and Intelligence.docx": {
        "file": "research-intelligence.html",
        "title": "Research & Intelligence",
        "desc": "Research and intelligence publications of the World Economic Chamber.",
        "breadcrumb": "Home / Research & Intelligence",
        "pillar": "governance"
    },
    "7.  Events and Diplomatic Forums.docx": {
        "file": "events-forums.html",
        "title": "Events & Diplomatic Forums",
        "desc": "Events and diplomatic forums of the World Economic Chamber.",
        "breadcrumb": "Home / Events & Forums",
        "pillar": "cooperation"
    },
    "8.  Partnerships and Affiliations.docx": {
        "file": "partnerships-affiliations.html",
        "title": "Partnerships & Affiliations",
        "desc": "Partnerships and affiliations of the World Economic Chamber.",
        "breadcrumb": "Home / Partnerships",
        "pillar": "trade"
    },
    "9.  Professional Development.docx": {
        "file": "professional-development.html",
        "title": "Professional Development",
        "desc": "Professional development programs of the World Economic Chamber.",
        "breadcrumb": "Home / Professional Development",
        "pillar": "cooperation"
    },
    "10.  Media and Communications.docx": {
        "file": "media-communications.html",
        "title": "Media & Communications",
        "desc": "Media and communications of the World Economic Chamber.",
        "breadcrumb": "Home / Media & Communications",
        "pillar": "cooperation"
    },
    "11.  Join Us.docx": {
        "file": "join-us.html",
        "title": "Join Us",
        "desc": "Join the World Economic Chamber — become part of global economic cooperation.",
        "breadcrumb": "Home / Join Us",
        "pillar": "cooperation"
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
                <a href="global-relations.html">Global Relations & Regional Engagement</a>
                <a href="join-us.html">Join Us</a>
              </div>
              <div class="mega-col">
                <h4>Engagement</h4>
                <a href="personnel-directory.html">Personnel Directory</a>
                <a href="membership.html">Membership</a>
                <a href="partnerships-affiliations.html">Partnerships & Affiliations</a>
                <a href="programs-initiatives.html">Programs & Initiatives</a>
              </div>
              <div class="mega-col">
                <h4>News & Media</h4>
                <a href="media-communications.html">Media & Communications</a>
                <a href="events-forums.html">Events & Diplomatic Forums</a>
                <a href="official-communications.html">Official Communications</a>
              </div>
              <div class="mega-col">
                <h4>Contact & Careers</h4>
                <a href="professional-development.html">Professional Development</a>
                <a href="contact.html">Global Headquarters</a>
                <a href="mailto:info@worldeconomicchamber.org?subject=Media%20Inquiry">Media Inquiries</a>
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
                <a href="operational-policies.html">Operational Policies</a>
              </div>
              <div class="mega-col">
                <h4>Accountability</h4>
                <a href="decision-making.html">Decision-Making Procedures</a>
                <a href="oversight-responsibilities.html">Oversight & Accountability</a>
                <a href="compliance-audit.html">Compliance, Audit & Retrieval</a>
              </div>
              <div class="mega-col">
                <h4>Policies</h4>
                <a href="charter-and-governance.html">Charter & Policies Overview</a>
                <a href="ethical-conduct-policies.html">Ethical & Conduct Policies</a>
                <a href="safeguard-integrity.html">Safeguard & Integrity Rules</a>
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
                <h4>Cooperation</h4>
                <a href="international-cooperation-framework.html">International Cooperation Framework</a>
                <a href="cross-border-initiative.html">Cross-Border Initiative Implementation</a>
                <a href="multilateral-engagement.html">Multilateral Engagement Procedures</a>
              </div>
              <div class="mega-col">
                <h4>Analysis</h4>
                <a href="research-intelligence.html">Research & Intelligence</a>
                <a href="institutional-risk-management.html">Institutional Risk Management</a>
                <a href="monitoring-reporting.html">Monitoring, Reporting & Evaluation</a>
              </div>
              <div class="mega-col">
                <h4>Policy</h4>
                <a href="policy-advocacy.html">Policy & Advocacy</a>
                <a href="regulatory-engagement.html">Regulatory Engagement Standards</a>
                <a href="government-liaison.html">Government & Regulatory Liaison</a>
              </div>
              <div class="mega-col">
                <h4>Resources</h4>
                <a href="core-record-keeping.html">Core Record-Keeping</a>
                <a href="documentation-standards.html">Documentation Standards</a>
                <a href="program-documentation.html">Program Documentation</a>
              </div>
            </div>
          </div>
        </li>

      </ul>

      <div class="nav-actions">
        <a href="mailto:info@worldeconomicchamber.org" class="btn btn-primary btn-sm">Contact</a>
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
          <p>The World Economic Chamber &mdash; strengthening cross-border commerce, investment and economic cooperation through principled governance and institutional discipline.</p>
        </div>

                <div>
          <h4 class="footer-heading">The Chamber</h4>
          <ul class="footer-links">
            <li><a href="about.html">Mission &amp; Vision</a></li>
            <li><a href="global-relations.html">Global Relations</a></li>
            <li><a href="membership.html">Membership</a></li>
            <li><a href="join-us.html">Join Us</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-heading">Governance</h4>
          <ul class="footer-links">
            <li><a href="governance-architecture.html">Governance Architecture</a></li>
            <li><a href="charter.html">The WEC Charter</a></li>
            <li><a href="governance-documents.html">Governance Documents</a></li>
            <li><a href="decision-making.html">Decision-Making</a></li>
            <li><a href="oversight-responsibilities.html">Oversight</a></li>
            <li><a href="leadership-responsibilities.html">Leadership</a></li>
            <li><a href="secretariat-management.html">Secretariat</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-heading">Resources</h4>
          <ul class="footer-links">
            <li><a href="charter-and-governance.html">Charter &amp; Policies Overview</a></li>
            <li><a href="ethical-conduct-policies.html">Ethical Policies</a></li>
            <li><a href="safeguard-integrity.html">Safeguard &amp; Integrity</a></li>
            <li><a href="personnel-directory.html">Personnel Directory</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-heading">Contact</h4>
          <ul class="footer-links">
            <li><a href="mailto:info@worldeconomicchamber.org">info@worldeconomicchamber.org</a></li>
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
      <strong>Privacy &amp; Cookies</strong>
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
  <meta property="og:url" content="https://www.worldeconomicchamber.org">
  <meta property="og:image" content="https://www.worldeconomicchamber.org/images/Logo%20WEC%201%20[MAIN].png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="images/Logo WEC 1 [MAIN].png" type="image/png">
  <link rel="apple-touch-icon" href="images/Logo WEC 1 [MAIN].png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "World Economic Chamber",
    "url": "https://www.worldeconomicchamber.org",
    "logo": "https://www.worldeconomicchamber.org/images/Logo%20WEC%201%20[MAIN].png",
    "sameAs": [
      "https://twitter.com/WorldEconChamber",
      "https://www.linkedin.com/company/world-economic-chamber"
    ]
  }}
  </script>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
"""

CONSTELLATION_SVG = """  <svg viewBox="0 0 900 440" fill="none" xmlns="http://www.w3.org/2000/svg" class="constellation-draw-in" aria-hidden="true">
    <defs>
      <radialGradient id="globeGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#c9a84c" stop-opacity="0.15"/>
        <stop offset="60%" stop-color="#c9a84c" stop-opacity="0.04"/>
        <stop offset="100%" stop-color="#c9a84c" stop-opacity="0"/>
      </radialGradient>
    </defs>
    <!-- Background glow for central hub -->
    <circle cx="450" cy="220" r="220" fill="url(#globeGlow)"/>
    
    <!-- World Map Silhouette -->
    <path d="M165 65 c-15 15 -25 40 -10 60 c15 20 40 30 65 20 c20 -10 30 -30 20 -50 c-10 -20 -35 -40 -60 -35 z M200 150 c-20 20 -15 60 10 80 c25 20 50 15 60 -10 c10 -25 -10 -60 -40 -70 z M420 80 c-10 10 -15 40 5 60 c20 20 50 10 60 -10 c10 -20 -10 -40 -40 -50 z M450 180 c-30 20 -20 70 10 90 c30 20 60 10 70 -15 c10 -25 -20 -70 -50 -80 z M650 90 c-30 15 -20 60 15 80 c35 20 80 15 90 -10 c10 -25 -20 -60 -60 -75 z M750 250 c-20 15 -10 50 15 60 c25 10 50 5 60 -15 c10 -20 -20 -50 -50 -55 z" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>

    <!-- Hub-and-spoke connection lines -->
    <!-- NY / DC -->
    <path class="const-line" d="M450 220 Q330 150 220 120" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <!-- Sao Paulo -->
    <path class="const-line" d="M450 220 Q350 250 240 220" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <!-- London / Paris -->
    <path class="const-line" d="M450 220 Q440 150 450 110" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <!-- Johannesburg -->
    <path class="const-line" d="M450 220 Q480 260 490 250" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <!-- Dubai -->
    <path class="const-line" d="M450 220 Q520 180 540 180" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <!-- Singapore -->
    <path class="const-line" d="M450 220 Q600 240 680 230" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <!-- Tokyo -->
    <path class="const-line" d="M450 220 Q600 150 720 140" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    <!-- Sydney -->
    <path class="const-line" d="M450 220 Q650 300 770 280" stroke="rgba(201,168,76,0.35)" stroke-width="1.1" fill="none"/>
    
    <!-- Perimeter route lines -->
    <path class="const-line" d="M220 120 Q200 180 240 220" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M240 220 Q350 300 490 250" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M490 250 Q600 280 680 230" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M680 230 Q750 280 770 280" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M680 230 Q700 180 720 140" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M720 140 Q650 150 540 180" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M540 180 Q480 150 450 110" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    <path class="const-line" d="M450 110 Q300 100 220 120" stroke="rgba(255,255,255,0.12)" stroke-width="0.8" fill="none"/>
    
    <!-- Pillar dots (Regional Hubs) -->
    <circle class="const-dot" cx="220" cy="120" r="4" fill="var(--pillar-cooperation)" opacity="0"><title>North America Hub</title></circle>
    <circle class="const-dot" cx="240" cy="220" r="4" fill="var(--pillar-trade)" opacity="0"><title>South America Hub</title></circle>
    <circle class="const-dot" cx="450" cy="110" r="4" fill="var(--pillar-governance)" opacity="0"><title>Europe Hub</title></circle>
    <circle class="const-dot" cx="490" cy="250" r="4" fill="var(--pillar-oversight)" opacity="0"><title>Africa Hub</title></circle>
    <circle class="const-dot" cx="540" cy="180" r="4" fill="var(--pillar-trade)" opacity="0"><title>Middle East Hub</title></circle>
    <circle class="const-dot" cx="680" cy="230" r="4" fill="var(--pillar-cooperation)" opacity="0"><title>Southeast Asia Hub</title></circle>
    <circle class="const-dot" cx="720" cy="140" r="4" fill="var(--pillar-governance)" opacity="0"><title>East Asia Hub</title></circle>
    <circle class="const-dot" cx="770" cy="280" r="4" fill="var(--pillar-oversight)" opacity="0"><title>Oceania Hub</title></circle>
    
    <!-- Central hub node -->
    <circle class="const-dot const-dot-hub" cx="450" cy="220" r="7" fill="var(--gold-500)" opacity="0"><title>World Economic Chamber — Central hub of international cooperation</title></circle>
  </svg>"""

def build_index():
    html = head_html("Global Economic Leadership", "The World Economic Chamber — strengthening cross-border commerce, investment and economic cooperation through principled governance.")
    html += NAV_HTML

    html += """
<!-- Bento Hero Hub -->
  <section class="hero-hub" id="hero">
    <div class="container">
      <div class="bento-hero fade-up">
        <div class="bento-main">
          """ + picture_img("images/hero_global_economic.jpg", "Global Economic Summit", lazy=False, eager=True) + """
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
      <span class="ticker-item"><span class="ticker-label">Global Trade Vol. Index:</span><span class="ticker-val">0% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Cross-Border Investment:</span><span class="ticker-val">0% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Policy Stability Index:</span><span class="ticker-val">0% &#9660;</span></span>
      <span class="ticker-item"><span class="ticker-label">Market Access Score:</span><span class="ticker-val">0% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Regulatory Convergence:</span><span class="ticker-val">0% &#9650;</span></span>
      <!-- Duplicate for infinite scroll -->
      <span class="ticker-item"><span class="ticker-label">Global Trade Vol. Index:</span><span class="ticker-val">0% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Cross-Border Investment:</span><span class="ticker-val">0% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Policy Stability Index:</span><span class="ticker-val">0% &#9660;</span></span>
      <span class="ticker-item"><span class="ticker-label">Market Access Score:</span><span class="ticker-val">0% &#9650;</span></span>
      <span class="ticker-item"><span class="ticker-label">Regulatory Convergence:</span><span class="ticker-val">0% &#9650;</span></span>
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
              
            </a>
            <a href="secretariat-management.html" class="news-item">
              <span class="news-date">Yesterday</span>
              <h4>Executive Secretariat operational management protocols now published</h4>
              
            </a>
            <a href="decision-making.html" class="news-item">
              <span class="news-date">August 12, 2026</span>
              <h4>Decision-making procedures and approval pathways adopted by the Chamber</h4>
              
            </a>
            <a href="oversight-responsibilities.html" class="news-item">
              <span class="news-date">August 05, 2026</span>
              <h4>Oversight responsibilities and accountability standards framework released</h4>
              
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
          
        </div>

        <!-- Data Vis / Stats -->
        <div class="data-column">
          <div class="section-header-compact">
            <h3>Key Metrics</h3>
          </div>
          <div class="data-list">
            <div class="data-stat">
              <span class="data-label">Active Trade Agreements</span>
              <div>
                <span class="data-value">3</span>
                
              </div>
            </div>
            <div class="data-stat">
              <span class="data-label">Participating Nations</span>
              <div>
                <span class="data-value">0</span>
                
              </div>
            </div>
            <div class="data-stat">
              <span class="data-label">Dispute Resolutions</span>
              <div>
                <span class="data-value">23</span>
                
              </div>
            </div>
            <div class="data-stat">
              <span class="data-label">Policy Consultations</span>
              <div>
                <span class="data-value">7</span>
                
              </div>
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
          <span class="constellation-stat-number" data-target="0">0</span>
          <span class="constellation-stat-label">Member Nations</span>
        </div>
        <div class="constellation-stat">
          <span class="constellation-stat-number" data-target="3">0</span>
          <span class="constellation-stat-label">Institutional Partners</span>
        </div>
        <div class="constellation-stat">
          <span class="constellation-stat-number" data-target="5">0</span>
          <span class="constellation-stat-label">Regional Offices</span>
        </div>
        <div class="constellation-stat">
          <span class="constellation-stat-number" data-target="11">0</span>
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
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write('  <url>\n    <loc>https://www.worldeconomicchamber.org/index.html</loc>\n  </url>\n')
        for docx_file, page_info in pages.items():
            f.write(f'  <url>\n    <loc>https://www.worldeconomicchamber.org/{page_info["file"]}</loc>\n  </url>\n')
        f.write('</urlset>')
    print("  [OK] Generated sitemap.xml")


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
      <ul class="breadcrumb">
        <li class="breadcrumb-item"><a href="index.html" class="breadcrumb-link">Home</a></li>
        <li class="breadcrumb-item"><span class="breadcrumb-link">{pillar.title()}</span></li>
        <li class="breadcrumb-item active">{page_info['title']}</li>
      </ul>
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
