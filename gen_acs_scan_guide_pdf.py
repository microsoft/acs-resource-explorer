"""
Generate: ACS Deprecation Scan — Account Manager Guide (PDF)
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, ListFlowable, ListItem
)
from datetime import datetime
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "ACS_Scan_AccountManager_Guide.pdf")

MSFT_BLUE    = colors.HexColor("#0078D4")
LIGHT_BLUE   = colors.HexColor("#E6F3FB")
DARK_GREY    = colors.HexColor("#323130")
MID_GREY     = colors.HexColor("#605E5C")
LIGHT_GREY   = colors.HexColor("#F3F2F1")
BORDER_GREY  = colors.HexColor("#C8C6C4")
WARN_BG      = colors.HexColor("#FFF4CE")
WARN_BORDER  = colors.HexColor("#C7A208")
GREEN_BG     = colors.HexColor("#DFF6DD")
GREEN_BORDER = colors.HexColor("#107C10")

def s(name, **kw):
    return ParagraphStyle(name, **kw)

H1   = s("H1",   fontSize=22, textColor=colors.white, fontName="Helvetica-Bold", spaceAfter=4, leading=26)
H2   = s("H2",   fontSize=14, textColor=MSFT_BLUE,    fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=4, leading=18)
H3   = s("H3",   fontSize=11, textColor=DARK_GREY,    fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=3, leading=14)
BODY = s("Body", fontSize=10, textColor=DARK_GREY,    fontName="Helvetica", leading=15, spaceAfter=4)
SMALL= s("Sm",   fontSize=9,  textColor=MID_GREY,     fontName="Helvetica", leading=12, spaceAfter=2)
CODE = s("Code", fontSize=9,  textColor=DARK_GREY,    fontName="Courier", backColor=LIGHT_GREY, leading=13, leftIndent=10, spaceAfter=2)

def p(text, style=BODY): return Paragraph(text, style)
def sp(h=6): return Spacer(1, h)
def rule(): return HRFlowable(width="100%", thickness=1, color=BORDER_GREY, spaceAfter=8, spaceBefore=4)

def box(text, bg, border, label):
    t = Table([[p(f"<b>{label}:</b> {text}")]], colWidths=[6.5*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg), ("BOX",(0,0),(-1,-1),1,border),
        ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),10), ("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    return t

def code_block(lines):
    t = Table([[p(l, CODE)] for l in lines], colWidths=[6.5*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),LIGHT_GREY), ("BOX",(0,0),(-1,-1),0.5,BORDER_GREY),
        ("TOPPADDING",(0,0),(-1,-1),3), ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),10), ("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    return t

def bullets(items):
    return ListFlowable(
        [ListItem(p(i), leftIndent=16, bulletIndent=6) for i in items],
        bulletType="bullet", bulletFontSize=8, bulletColor=MSFT_BLUE, spaceAfter=4
    )

def numbered(items):
    return ListFlowable(
        [ListItem(p(i), leftIndent=20, bulletIndent=4) for i in items],
        bulletType="1", bulletFontSize=10, bulletColor=MSFT_BLUE, spaceAfter=4
    )

def banner(title, subtitle):
    sub_st = s("sub", fontSize=11, textColor=colors.white, fontName="Helvetica", leading=15)
    t = Table([[p(title, H1)], [p(subtitle, sub_st)]], colWidths=[7*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),MSFT_BLUE),
        ("TOPPADDING",(0,0),(-1,-1),16), ("BOTTOMPADDING",(0,0),(-1,-1),14),
        ("LEFTPADDING",(0,0),(-1,-1),18), ("RIGHTPADDING",(0,0),(-1,-1),18),
    ]))
    return t

def grid(headers, rows, col_widths):
    data = [[p(f"<b>{h}</b>") for h in headers]] + [[p(c) for c in r] for r in rows]
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),MSFT_BLUE), ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, LIGHT_GREY]),
        ("BOX",(0,0),(-1,-1),0.5,BORDER_GREY), ("INNERGRID",(0,0),(-1,-1),0.5,BORDER_GREY),
        ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),8),
        ("VALIGN",(0,0),(-1,-1),"TOP"), ("FONTSIZE",(0,0),(-1,-1),9),
    ]))
    return t

# ── Story ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter,
    rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.6*inch, bottomMargin=0.6*inch)

now = datetime.now().strftime("%B %d, %Y")
story = [
    banner("ACS Deprecation Scan",
           "Account Manager Guide — Running the scan on behalf of a customer"),
    sp(4),
    p(f"Azure Communication Services (ACS)  ·  Retirement: 31 July 2028  ·  Generated {now}", SMALL),
    sp(10),

    p("Overview", H2), rule(),
    p("This guide is for <b>Microsoft account managers, CSAMs, and TAMs</b> who need to identify "
      "which ACS capabilities a customer is actively using — without being the tenant owner or "
      "having administrative rights on the customer's subscription."),
    sp(4),
    p("The ACS Deprecation Scan discovers all <b>Microsoft.Communication/CommunicationServices</b> "
      "resources across one or more Azure subscriptions and maps each to the five retiring channels: "
      "Email, SMS, Chat, Calling SDK, and Phone Numbers."),
    sp(8),

    p("Minimum Access Requirements", H2), rule(),
    p("You do <b>not</b> need Owner or Contributor rights. The scan is entirely read-only."),
    sp(6),
    grid(
        ["Option", "Access Needed", "Notes"],
        [
            ("Fast scan (Email + Phone Numbers)", "Reader on subscription",
             "Discovers child resources. ~30 sec per subscription."),
            ("Full scan (all 5 channels)", "Reader + Monitoring Reader on subscription",
             "Adds Azure Monitor metrics. ~3–5 min per subscription."),
        ],
        [1.8*inch, 2.0*inch, 2.7*inch]
    ),
    sp(8),

    p("Two Ways to Run the Scan", H2), rule(),

    # Option 1
    p("Option 1 — Customer runs it themselves (recommended)", H3),
    p("The fastest path with zero access friction. Share the tool with the customer and walk "
      "them through the 5-minute quickstart."),
    sp(4),
    p("<b>What to send the customer:</b>"),
    bullets([
        "Link to the ACS Transition Agent repo (contains the scan tool and all migration guides)",
        "Ask them to run: <font name='Courier' size='9'>Run an ACS deprecation scan</font> in "
        "GitHub Copilot or Claude Code, or use the standalone PowerShell script below",
        "Request they share the exported CSV or Markdown report with you for joint review",
    ]),
    sp(6),
    p("<b>Standalone PowerShell (no AI agent required):</b>"),
    code_block([
        "# Fast scan — Email + Phone Numbers only",
        ".\\scripts\\powershell\\acs-impact-assessment-tool.ps1",
        "",
        "# Full scan — all 5 channels",
        ".\\scripts\\powershell\\acs-impact-assessment-tool.ps1 -IncludeMetrics",
        "",
        "# Target a specific subscription",
        ".\\scripts\\powershell\\acs-impact-assessment-tool.ps1 -SubscriptionId '<id>' -IncludeMetrics",
    ]),
    sp(8),

    # Option 2
    p("Option 2 — Customer delegates temporary Reader access to you", H3),
    p("The customer grants your Microsoft account <b>Reader</b> (and optionally "
      "<b>Monitoring Reader</b>) on their subscription via Azure RBAC. You run the scan "
      "yourself and share results."),
    sp(4),
    p("<b>Steps:</b>"),
    numbered([
        "Ask the customer to go to: Azure Portal → Subscription → Access control (IAM) → Add role assignment",
        "Role: <b>Reader</b> (required) + <b>Monitoring Reader</b> (optional, for full scan)",
        "Assign to: your @microsoft.com account or a shared service account",
        "On your machine, authenticate: <font name='Courier' size='9'>az login</font>",
        "Run the scan using the PowerShell commands above, or via the AI agent skills",
        "Export the report and share findings — the customer revokes access when done",
    ]),
    sp(4),
    box("Role assignments typically propagate within 1–2 minutes. If no subscriptions appear, "
        "wait briefly and re-run <font name='Courier' size='9'>az login</font>.",
        LIGHT_BLUE, MSFT_BLUE, "Tip"),
    sp(8),

    p("After the Scan — What You Get", H2), rule(),
    p("The tool exports three files to the <b>./exports/</b> folder:"),
    sp(4),
    bullets([
        "<b>CSV</b> — 17-column spreadsheet, Excel-compatible; easy to paste into account plans",
        "<b>Markdown</b> — human-readable summary with migration guide links per channel",
        "<b>JSON</b> — machine-readable; useful for automation or ticketing systems",
    ]),
    sp(6),
    p("<b>Key fields in the report:</b>"),
    bullets([
        "Resource name, Resource Group, Subscription",
        "Channels detected: Email, SMS, Chat, Calling, Phone Numbers",
        "Retirement date and recommended migration path per channel",
        "30/60/90-day active usage metrics (full scan only)",
    ]),
    sp(8),

    p("AI Agent — Conversation Starters", H2), rule(),
    p("If the customer (or you) is using the AI agent interface (GitHub Copilot or Claude Code), "
      "any of these phrases will trigger the full scan workflow:"),
    sp(4),
    code_block([
        "Run an ACS deprecation scan",
        "Do a full ACS impact assessment",
        "Check my subscriptions for retiring ACS services",
        "Generate an ACS deprecation impact report",
    ]),
    sp(8),

    p("Reference — Five Retiring ACS Channels", H2), rule(),
    grid(
        ["Channel", "Retirement Date", "Type", "Migration Path"],
        [
            ("Email Service",     "31 Jul 2028", "Retirement",      "Migrate to Exchange Online / M365"),
            ("SMS API",           "31 Jul 2028", "Retirement",      "Migrate to Teams SMS / partner SMS"),
            ("Chat SDK",          "31 Jul 2028", "Retirement",      "Migrate to Teams Chat API"),
            ("Calling SDK",       "31 Jul 2028", "Breaking change", "Integrate with Teams Calling"),
            ("Phone Numbers SDK", "31 Jul 2028", "Retirement",      "Migrate to Teams Phone Numbers"),
        ],
        [1.5*inch, 1.3*inch, 1.3*inch, 2.4*inch]
    ),
    sp(8),

    rule(),
    box("This guide covers read-only discovery only. No changes are made to customer resources "
        "during the scan. Any access granted can be safely revoked immediately after the report "
        "is exported.", GREEN_BG, GREEN_BORDER, "Security"),
    sp(6),
    p(f"ACS Transition Agent  ·  Internal use  ·  Generated {now}", SMALL),
]

doc.build(story)
print(f"PDF saved to: {OUTPUT_PATH}")