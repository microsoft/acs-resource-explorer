import math
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import KeepTogether

PAGE = landscape(A4)
W, H = PAGE

BLUE    = colors.HexColor("#0078D4")
DARK    = colors.HexColor("#201F1E")
WHITE   = colors.white
LGRAY   = colors.HexColor("#F3F2F1")
MGRAY   = colors.HexColor("#E1DFDD")
RED     = colors.HexColor("#C4314B")
ORANGE  = colors.HexColor("#D17300")
DKBLUE  = colors.HexColor("#004578")
LBLUE   = colors.HexColor("#00B4FF")

styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

title_style   = S("TitleStyle",   fontName="Helvetica-Bold",   fontSize=28, textColor=WHITE,  spaceAfter=6,  leading=34)
head_style    = S("HeadStyle",    fontName="Helvetica-Bold",   fontSize=20, textColor=WHITE,  spaceAfter=4,  leading=26)
sub_style     = S("SubStyle",     fontName="Helvetica",        fontSize=13, textColor=colors.HexColor("#AAAAAA"), spaceAfter=4, leading=18)
body_style    = S("BodyStyle",    fontName="Helvetica",        fontSize=11, textColor=DARK,   spaceAfter=4,  leading=16)
bold_body     = S("BoldBody",     fontName="Helvetica-Bold",   fontSize=11, textColor=DARK,   spaceAfter=2,  leading=15)
small_style   = S("SmallStyle",   fontName="Helvetica",        fontSize=9,  textColor=colors.HexColor("#777777"), spaceAfter=2)
link_style    = S("LinkStyle",    fontName="Helvetica",        fontSize=10, textColor=BLUE,   spaceAfter=2)
section_head  = S("SectionHead",  fontName="Helvetica-Bold",   fontSize=15, textColor=DARK,   spaceAfter=6,  leading=20)
white_bold    = S("WhiteBold",    fontName="Helvetica-Bold",   fontSize=11, textColor=WHITE,  spaceAfter=2)
white_small   = S("WhiteSmall",   fontName="Helvetica",        fontSize=9,  textColor=WHITE,  spaceAfter=1)
tag_red       = S("TagRed",       fontName="Helvetica-Bold",   fontSize=9,  textColor=RED)
tag_orange    = S("TagOrange",    fontName="Helvetica-Bold",   fontSize=9,  textColor=ORANGE)

out = "c:/Users/jameelaesa/ACS-Transition-Agent-v0/exports/ACS-Transition-Agent.pdf"
doc = SimpleDocTemplate(out, pagesize=PAGE,
                        leftMargin=0.6*inch, rightMargin=0.6*inch,
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

story = []

# ─── PAGE 1: Title ────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.3*inch))
story.append(Paragraph("ACS Transition Agent", title_style))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Automated Azure Communication Services Deprecation Assessment", sub_style))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("FHL 2026", S("fhl", fontName="Helvetica-Bold", fontSize=16, textColor=BLUE)))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph(
    "Anuj Bhatia  ·  Prabu Dhaksh  ·  Jameela Esa  ·  Farhan Hussain  ·  Kristan Hinnenkamp",
    S("team", fontName="Helvetica", fontSize=13, textColor=colors.HexColor("#AAAAAA"))))
story.append(Spacer(1, 1.8*inch))
story.append(Paragraph("github.com/jameelaesa/ACS-Transition-Agent-v0", S("gh", fontName="Helvetica", fontSize=11, textColor=colors.HexColor("#888888"))))
story.append(PageBreak())

# ─── PAGE 2: Table of Contents ────────────────────────────────────────────────
story.append(Paragraph("Table of Contents", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=16))

toc_entries = [
    ("03", "Product Vision"),
    ("04", "The Audience"),
    ("05", "Business Impact & ROI"),
    ("06", "The Problem: Service Deprecation at Scale"),
    ("07", "Solution: Automated Transition Intelligence"),
    ("08", "The Problem: ACS Channels Overview"),
    ("09", "The Solution: Assessment Workflow"),
    ("10", "How to Use"),
    ("11", "Migration Targets"),
    ("12", "Live Scan Results — Enterprise"),
    ("13", "Live Scan Results — Personal"),
    ("14", "Get Started"),
]

def toc_entry_row(num, title):
    num_cell = Table(
        [[Paragraph(num, S(f"tn{num}", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE, alignment=TA_CENTER))]],
        colWidths=[0.42*inch], rowHeights=[0.40*inch],
        style=TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),("VALIGN",(0,0),(-1,-1),"MIDDLE")])
    )
    title_cell = Paragraph(title, S(f"tt{num}", fontName="Helvetica", fontSize=12, textColor=DARK, leading=16))
    return Table(
        [[num_cell, title_cell]],
        colWidths=[0.52*inch, 4.3*inch],
        style=TableStyle([
            ("VALIGN",        (0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",   (0,0),(-1,-1),0),
            ("RIGHTPADDING",  (0,0),(-1,-1),0),
            ("TOPPADDING",    (0,0),(-1,-1),6),
            ("BOTTOMPADDING", (0,0),(-1,-1),6),
        ])
    )

left_entries  = toc_entries[:6]
right_entries = toc_entries[6:]

left_rows  = [[toc_entry_row(n, t)] for n, t in left_entries]
right_rows = [[toc_entry_row(n, t)] for n, t in right_entries]

toc_left_tbl = Table(left_rows, colWidths=[5.0*inch],
                     style=TableStyle([
                         ("ROWBACKGROUNDS", (0,0),(-1,-1),[LGRAY, WHITE]),
                         ("TOPPADDING",     (0,0),(-1,-1),0),
                         ("BOTTOMPADDING",  (0,0),(-1,-1),0),
                     ]))
toc_right_tbl = Table(right_rows, colWidths=[5.0*inch],
                      style=TableStyle([
                          ("ROWBACKGROUNDS", (0,0),(-1,-1),[LGRAY, WHITE]),
                          ("TOPPADDING",     (0,0),(-1,-1),0),
                          ("BOTTOMPADDING",  (0,0),(-1,-1),0),
                      ]))

toc_grid = Table([[toc_left_tbl, toc_right_tbl]], colWidths=[5.2*inch, 5.2*inch],
                 style=TableStyle([
                     ("VALIGN",       (0,0),(-1,-1),"TOP"),
                     ("LEFTPADDING",  (0,0),(-1,-1),0),
                     ("RIGHTPADDING", (0,0),(0,-1), 20),
                 ]))
story.append(toc_grid)
story.append(PageBreak())

# ─── PAGE 3: Product Vision ──────────────────────────────────────────────────
story.append(Paragraph("Product Vision", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
story.append(Paragraph(
    "The ACS Transition Agent is an AI-powered assessment tool that connects directly to customer "
    "Azure subscriptions to automatically discover, analyze, and report on retiring Azure Communication "
    "Services resources — empowering customers and partners to migrate seamlessly before the "
    "<b>March 31, 2029</b> retirement deadline.",
    body_style))
story.append(Spacer(1, 0.2*inch))

vision_items = [
    ("Discover",  "Automatically find all ACS resources across one or more Azure subscriptions"),
    ("Analyze",   "Measure actual channel usage via Azure Monitor metrics over a 90-day lookback"),
    ("Match",     "Map detected usage to retiring features and applicable migration paths"),
    ("Guide",     "Generate actionable reports (CSV, Markdown, JSON) with per-channel migration links"),
    ("Scale",     "Designed as a model for future Azure retirement scenarios — reusable and extensible"),
]
for icon, desc in vision_items:
    story.append(Table([[
        Table([[Paragraph(icon, S(f"vi{icon}", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE, alignment=TA_CENTER))]],
              colWidths=[0.85*inch], rowHeights=[0.38*inch],
              style=TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),("VALIGN",(0,0),(-1,-1),"MIDDLE")])),
        Paragraph(desc, body_style),
    ]], colWidths=[0.95*inch, 8.5*inch],
       style=TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),0),
                         ("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)])))
story.append(PageBreak())

# ─── PAGE 4: The Audience ────────────────────────────────────────────────────
story.append(Paragraph("The Audience", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
story.append(Paragraph("Who is this tool designed for?", section_head))
story.append(Spacer(1, 0.1*inch))

audience_data = [
    [
        Paragraph("Technical Lead / Developer", S("ah", fontName="Helvetica-Bold", fontSize=14, textColor=WHITE)),
        Paragraph("Business Decision Maker (BDM)", S("ah2", fontName="Helvetica-Bold", fontSize=14, textColor=WHITE)),
    ],
    [
        Table([
            [Paragraph(p, body_style)] for p in [
                "Runs the scan directly using Claude Code or GitHub Copilot",
                "Reviews which ACS resources and channels are in use",
                "Uses exported reports to plan and execute migration",
                "Integrates skill-based workflow into existing DevOps processes",
                "Can run assessments across multiple subscriptions",
            ]
        ], colWidths=[4.3*inch],
           style=TableStyle([("ROWBACKGROUNDS",(0,0),(-1,-1),[LGRAY,WHITE]),
                             ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
                             ("LEFTPADDING",(0,0),(-1,-1),10)])),
        Table([
            [Paragraph(p, body_style)] for p in [
                "Reviews the Markdown and CSV impact reports",
                "Understands migration urgency and business risk",
                "Uses findings to allocate migration resources and timelines",
                "Gets a clear picture of which services are affected",
                "Informed without needing to run the technical scan",
            ]
        ], colWidths=[4.3*inch],
           style=TableStyle([("ROWBACKGROUNDS",(0,0),(-1,-1),[LGRAY,WHITE]),
                             ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
                             ("LEFTPADDING",(0,0),(-1,-1),10)])),
    ],
]
aud_tbl = Table(audience_data, colWidths=[4.6*inch, 4.6*inch],
                style=TableStyle([
                    ("BACKGROUND",   (0,0), (-1,0), BLUE),
                    ("TOPPADDING",   (0,0), (-1,0), 10),
                    ("BOTTOMPADDING",(0,0), (-1,0), 10),
                    ("LEFTPADDING",  (0,0), (-1,-1), 10),
                    ("VALIGN",       (0,0), (-1,-1), "TOP"),
                    ("LINEAFTER",    (0,0), (0,-1), 1, WHITE),
                ]))
story.append(aud_tbl)
story.append(PageBreak())

# ─── PAGE 5: Business Impact & ROI ───────────────────────────────────────────
story.append(Paragraph("Business Impact & ROI", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
story.append(Paragraph(
    "The goal is to have a product that can be a <b>model for other Azure retirements</b>. "
    "It provides customers with information on what is changing and how it impacts them, and "
    "empowers the developer customer to migrate seamlessly by providing the BDM/TDM with actionable intelligence.",
    body_style))
story.append(Spacer(1, 0.2*inch))

roi_items = [
    ("Reducing Support Burden",
     "Proactive, automated assessment reduces inbound support tickets from customers who are "
     "unaware of how the retirement affects them. Customers arrive informed rather than reactive."),
    ("Solution for Customer Migration",
     "Provides a structured, repeatable path for customers to migrate their ACS services — with "
     "per-channel migration guides, usage data, and exportable reports ready to share with engineering teams."),
    ("Integration with Existing Services",
     "Built on open Agent Skills standard (Linux Foundation / AAIF). Compatible with GitHub Copilot, "
     "Claude Code, Cursor, and Windsurf — integrates into existing developer workflows with zero new tooling."),
    ("Reusable Model for Future Retirements",
     "The skill-based architecture is generic. The same pattern can be applied to any future Azure "
     "service retirement — reducing time-to-delivery for the next deprecation assessment tool."),
]
for i, (title, desc) in enumerate(roi_items):
    bg = LGRAY if i % 2 == 0 else WHITE
    story.append(Table([[
        Table([[Paragraph(str(i+1), S(f"rn{i}", fontName="Helvetica-Bold", fontSize=16, textColor=WHITE, alignment=TA_CENTER))]],
              colWidths=[0.4*inch], rowHeights=[0.4*inch],
              style=TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),("VALIGN",(0,0),(-1,-1),"MIDDLE")])),
        Table([[Paragraph(title, bold_body)],[Paragraph(desc, body_style)]],
              colWidths=[8.8*inch],
              style=TableStyle([("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2),
                                ("LEFTPADDING",(0,0),(-1,-1),10),("BACKGROUND",(0,0),(-1,-1),bg)])),
    ]], colWidths=[0.55*inch, 9.0*inch],
       style=TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),0),
                         ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)])))
story.append(PageBreak())

# ─── PAGE 6: The Problem (Detailed) ──────────────────────────────────────────
story.append(Paragraph("The Problem: Navigating Service Deprecation at Scale", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=8))
story.append(Paragraph(
    "Azure Communication Services (ACS) is evolving from standalone SDKs and APIs toward integrated "
    "scenarios with Microsoft Teams. While this unlocks powerful new capabilities, it creates a complex "
    "migration challenge for customers, partners, and Microsoft teams alike.",
    body_style))
story.append(Spacer(1, 0.15*inch))

challenge_items = [
    "Customers using ACS standalone features need to understand if and how the deprecation affects them",
    "Many customers don't know which specific features they're using or how heavily they rely on them",
    "Migration guidance exists but customers must manually assess their eligibility and relevance",
    "Partners supporting customers need a systematic way to evaluate migration scope across portfolios",
    "Microsoft support and engineering teams need visibility into customer impact for prioritization",
]
opp_items = [
    "An intelligent, automated eligibility checker transforms the deprecation experience from reactive and uncertain to proactive and clear",
    "Benefits every stakeholder in the ecosystem — customers, partners, and Microsoft teams",
    "Reduces time-to-clarity from weeks of manual assessment to minutes of automated scanning",
]

def make_icon_row(icon_text, item_text, icon_color, text_style_name, pw):
    return [Table([[
        Table([[Paragraph(icon_text, S(f"ic_{text_style_name}", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE, alignment=TA_CENTER))]],
               colWidths=[0.25*inch], rowHeights=[0.25*inch],
               style=TableStyle([("BACKGROUND",(0,0),(-1,-1),icon_color),("VALIGN",(0,0),(-1,-1),"MIDDLE")])),
        Paragraph(item_text, S(f"it_{text_style_name}", fontName="Helvetica", fontSize=10, textColor=DARK)),
    ]], colWidths=[0.32*inch, pw],
       style=TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),3),("LEFTPADDING",(0,0),(-1,-1),0)]))]

prob_left = [[Paragraph("The Challenge", S("chl", fontName="Helvetica-Bold", fontSize=13, textColor=WHITE))]]
for item in challenge_items:
    prob_left.append(make_icon_row("!", item, RED, f"ch{len(prob_left)}", 4.0*inch))

prob_right = [[Paragraph("The Opportunity", S("opp", fontName="Helvetica-Bold", fontSize=13, textColor=WHITE))]]
for item in opp_items:
    prob_right.append(make_icon_row("*", item, BLUE, f"op{len(prob_right)}", 3.8*inch))

left_tbl  = Table(prob_left,  colWidths=[4.5*inch],
                  style=TableStyle([("BACKGROUND",(0,0),(-1,0),RED),("TOPPADDING",(0,0),(-1,0),8),
                                    ("BOTTOMPADDING",(0,0),(-1,0),8),("LEFTPADDING",(0,0),(-1,-1),8),
                                    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY,WHITE]),
                                    ("TOPPADDING",(0,1),(-1,-1),4),("BOTTOMPADDING",(0,1),(-1,-1),4)]))
right_tbl = Table(prob_right, colWidths=[4.5*inch],
                  style=TableStyle([("BACKGROUND",(0,0),(-1,0),BLUE),("TOPPADDING",(0,0),(-1,0),8),
                                    ("BOTTOMPADDING",(0,0),(-1,0),8),("LEFTPADDING",(0,0),(-1,-1),8),
                                    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY,WHITE]),
                                    ("TOPPADDING",(0,1),(-1,-1),4),("BOTTOMPADDING",(0,1),(-1,-1),4)]))
story.append(Table([[left_tbl, right_tbl]], colWidths=[4.7*inch, 4.7*inch],
                   style=TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),8)])))
story.append(PageBreak())

# ─── PAGE 7: Solution ────────────────────────────────────────────────────────
story.append(Paragraph("Solution: Automated Transition Intelligence", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=8))
story.append(Paragraph(
    "The ACS AI Transition Agent is a web-based tool that connects directly to customer Azure "
    "subscriptions to automatically assess deprecation impact and guide migration.",
    body_style))
story.append(Spacer(1, 0.15*inch))

sol_steps = [
    ("1", "Discover",  "Find all Azure Communication Services resources across subscriptions"),
    ("2", "Analyze",   "Analyze actual usage patterns through Azure Monitor metrics and SDK telemetry"),
    ("3", "Match",     "Match detected usage against the catalog of retiring features"),
    ("4", "Guide",     "Guide customers to appropriate migration paths and integrated scenarios"),
]
sol_rows = []
for num, title, desc in sol_steps:
    sol_rows.append([
        Table([[Paragraph(num, S(f"sn{num}", fontName="Helvetica-Bold", fontSize=20, textColor=WHITE, alignment=TA_CENTER))]],
              colWidths=[0.5*inch], rowHeights=[0.5*inch],
              style=TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),("VALIGN",(0,0),(-1,-1),"MIDDLE")])),
        Paragraph(title, bold_body),
        Paragraph(desc, body_style),
    ])
sol_tbl = Table(sol_rows, colWidths=[0.65*inch, 1.5*inch, 7.2*inch],
                style=TableStyle([
                    ("ROWBACKGROUNDS",(0,0),(-1,-1),[LGRAY,WHITE]),
                    ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
                    ("TOPPADDING",   (0,0),(-1,-1),10),
                    ("BOTTOMPADDING",(0,0),(-1,-1),10),
                    ("LEFTPADDING",  (0,0),(-1,-1),8),
                    ("LINEBELOW",    (0,0),(-1,-1),0.5,MGRAY),
                ]))
story.append(sol_tbl)
story.append(Spacer(1, 0.2*inch))

# Output formats
story.append(Paragraph("Output Formats", section_head))
fmt_data = [[
    Paragraph(f, S(f"fmt{i}", fontName="Helvetica-Bold", fontSize=12, textColor=WHITE, alignment=TA_CENTER))
    for i, f in enumerate(["CSV", "Markdown", "JSON"])
],[
    Paragraph("Excel-compatible, 17-column impact report. One row per ACS resource.", body_style),
    Paragraph("Human-readable report with migration guide links per channel.", body_style),
    Paragraph("Machine-readable output for integration with existing tooling.", body_style),
]]
fmt_tbl = Table(fmt_data, colWidths=[3.0*inch, 3.0*inch, 3.0*inch],
                style=TableStyle([
                    ("BACKGROUND",   (0,0),(-1,0), DKBLUE),
                    ("BACKGROUND",   (1,0),(1,0),  BLUE),
                    ("BACKGROUND",   (2,0),(2,0),  colors.HexColor("#005A9E")),
                    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY]),
                    ("TOPPADDING",   (0,0),(-1,-1), 8),
                    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
                    ("LEFTPADDING",  (0,0),(-1,-1), 10),
                    ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
                    ("LINEAFTER",    (0,0),(1,-1),  0.5, WHITE),
                ]))
story.append(fmt_tbl)
story.append(PageBreak())

# ─── PAGE 8: The Problem (ACS channels overview) ─────────────────────────────
story.append(Paragraph("The Problem", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=12))

problem_text = [
    [
        Paragraph("Microsoft is retiring Azure Communication Services", section_head),
        Paragraph("5 channels are being retired or changed effective <b>March 31, 2029</b>.<br/><br/>"
                  "Organizations using ACS must identify which services they use and migrate "
                  "before the deadline — or face service disruption.", body_style),
    ],
    [
        Paragraph("Channels Affected", section_head),
        Table([
            [Paragraph("Email Service",     bold_body), Paragraph("Retirement",      tag_red)],
            [Paragraph("SMS API",           bold_body), Paragraph("Retirement",      tag_red)],
            [Paragraph("Chat SDK",          bold_body), Paragraph("Retirement",      tag_red)],
            [Paragraph("Calling SDK",       bold_body), Paragraph("Breaking Change", tag_orange)],
            [Paragraph("Phone Numbers SDK", bold_body), Paragraph("Retirement",      tag_red)],
        ], colWidths=[2.8*inch, 1.5*inch],
           style=TableStyle([
               ("ROWBACKGROUNDS", (0,0), (-1,-1), [LGRAY, WHITE]),
               ("TOPPADDING",     (0,0), (-1,-1), 6),
               ("BOTTOMPADDING",  (0,0), (-1,-1), 6),
               ("LEFTPADDING",    (0,0), (-1,-1), 8),
               ("LINEBELOW",      (0,-1), (-1,-1), 0.5, MGRAY),
           ])),
    ],
]

tbl = Table([[problem_text[0][0]], [problem_text[0][1]],
             [Spacer(1, 0.2*inch)],
             [problem_text[1][0]], [problem_text[1][1]]],
            colWidths=[9.5*inch])
story.append(tbl)
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("Retirement date: March 31, 2029  |  Source: aka.ms/acs-retirement-and-breaking-changes-guide", small_style))
story.append(PageBreak())

# ─── PAGE 9: The Solution (workflow) ─────────────────────────────────────────
story.append(Paragraph("The Solution", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=8))
story.append(Paragraph(
    "ACS Transition Agent automates the entire assessment workflow using AI agent skills and Azure CLI. No PowerShell required.",
    body_style))
story.append(Spacer(1, 0.15*inch))

steps = [
    ("1", "Authenticate",        "az login — verify Azure session"),
    ("2", "Select Subscription", "Choose one or all subscriptions to scan"),
    ("3", "Discover Resources",  "Find all ACS CommunicationServices resources"),
    ("4", "Detect Channels",     "Fast (Email/Phone) or Full (all 5 via Azure Monitor)"),
    ("5", "Analyze Impact",      "Map channels to migration guides and retirement dates"),
    ("6", "Generate Reports",    "CSV + Markdown + JSON exported to ./exports/"),
]

step_rows = []
for num, title, desc in steps:
    num_cell = Table([[Paragraph(num, S("N", fontName="Helvetica-Bold", fontSize=16, textColor=WHITE, alignment=TA_CENTER))]],
                     colWidths=[0.45*inch], rowHeights=[0.45*inch],
                     style=TableStyle([("BACKGROUND", (0,0), (-1,-1), BLUE),
                                       ("VALIGN", (0,0), (-1,-1), "MIDDLE")]))
    content_cell = [Paragraph(title, bold_body), Paragraph(desc, body_style)]
    step_rows.append([num_cell, content_cell])

left_steps  = step_rows[:3]
right_steps = step_rows[3:]

def step_table(rows):
    data = [[r[0], r[1]] for r in rows]
    return Table(data, colWidths=[0.55*inch, 4.0*inch],
                 style=TableStyle([
                     ("VALIGN",         (0,0), (-1,-1), "TOP"),
                     ("TOPPADDING",     (0,0), (-1,-1), 8),
                     ("BOTTOMPADDING",  (0,0), (-1,-1), 8),
                     ("ROWBACKGROUNDS", (0,0), (-1,-1), [LGRAY, WHITE]),
                 ]))

grid = Table([[step_table(left_steps), step_table(right_steps)]],
             colWidths=[4.8*inch, 4.8*inch],
             style=TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"),
                                ("LEFTPADDING", (0,0), (-1,-1), 0),
                                ("RIGHTPADDING", (0,0), (-1,-1), 10)]))
story.append(grid)
story.append(PageBreak())

# ─── PAGE 10: How to Use ───────────────────────────────────────────────────────
story.append(Paragraph("How to Use", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=12))

prereqs = [
    "Git",
    "Azure CLI  (learn.microsoft.com/cli/azure)",
    "GitHub Copilot or Claude Code",
    "Reader + Monitoring Reader on target subscription(s)",
]
prereq_rows = [[Paragraph('<font color="#0078D4">&#9632;</font>', body_style),
                Paragraph(p, body_style)] for p in prereqs]

run_steps = [
    "Clone the repository",
    "Open in VS Code with GitHub Copilot or Claude Code",
    'Type in chat:  <b>"Run an ACS deprecation scan"</b>',
    "Follow the interactive prompts",
    "Reports saved to  ./exports/",
]
run_rows = [[Paragraph(f'<font color="#0078D4"><b>{i+1}.</b></font>', body_style),
             Paragraph(r, body_style)] for i, r in enumerate(run_steps)]

prereq_tbl = Table(prereq_rows, colWidths=[0.25*inch, 4.2*inch],
                   style=TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"),
                                     ("TOPPADDING", (0,0), (-1,-1), 5),
                                     ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                                     ("ROWBACKGROUNDS", (0,0), (-1,-1), [LGRAY, WHITE])]))

run_tbl = Table(run_rows, colWidths=[0.3*inch, 4.2*inch],
                style=TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"),
                                  ("TOPPADDING", (0,0), (-1,-1), 5),
                                  ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                                  ("ROWBACKGROUNDS", (0,0), (-1,-1), [LGRAY, WHITE])]))

left_col = [[Paragraph("Prerequisites", section_head)], [prereq_tbl]]
right_col = [[Paragraph("Run the Scan", section_head)], [run_tbl]]

cols = Table([[left_col, right_col]],
             colWidths=[5.0*inch, 4.8*inch],
             style=TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"),
                                ("LEFTPADDING", (0,0), (-1,-1), 0),
                                ("RIGHTPADDING", (0,0), (-1,-1), 10)]))
story.append(cols)
story.append(PageBreak())

# ─── PAGE 11: Migration Targets ───────────────────────────────────────────────
story.append(Paragraph("Migration Targets", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=12))

header = [Paragraph(h, white_bold) for h in ["Channel", "Recommended Migration Path", "Guide"]]
mig_rows = [
    ("Email Service",      "Microsoft 365 High-Volume Email (HVE)",                               "aka.ms/acs-email-migration"),
    ("SMS API",            "Port numbers to a third-party SMS provider",                           "aka.ms/acs-sms-migration"),
    ("Chat SDK",           "Microsoft Teams Chat via Microsoft Graph APIs",                        "aka.ms/acs-chat-migration"),
    ("Calling SDK",        "Microsoft Teams (Phone Extensibility, Meeting Interop, Click-2-Call)", "aka.ms/acs-calling-migration"),
    ("Phone Numbers SDK",  "Port to Teams Phone Extensibility or third-party provider",            "aka.ms/acs-phone-migration"),
]
data = [header]
for ch, path, guide in mig_rows:
    data.append([Paragraph(ch, bold_body), Paragraph(path, body_style), Paragraph(guide, link_style)])

tbl = Table(data, colWidths=[1.8*inch, 4.8*inch, 2.8*inch],
            style=TableStyle([
                ("BACKGROUND",    (0,0), (-1,0),  BLUE),
                ("ROWBACKGROUNDS",(0,1), (-1,-1), [LGRAY, WHITE]),
                ("TOPPADDING",    (0,0), (-1,-1), 8),
                ("BOTTOMPADDING", (0,0), (-1,-1), 8),
                ("LEFTPADDING",   (0,0), (-1,-1), 8),
                ("LINEBELOW",     (0,0), (-1,-1), 0.5, MGRAY),
                ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ]))
story.append(tbl)
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Full guide: aka.ms/acs-retirement-and-breaking-changes-guide", small_style))
story.append(PageBreak())

# ─── PAGE 12: Scan Results — Enterprise ──────────────────────────────────────
story.append(Paragraph("Live Scan Results", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=8))
story.append(Paragraph(
    "Subscription: <b>Azure Communication Services</b>  (50ad1522-5c2c-4d9a-a6c8-67c11ecb75b8)<br/>"
    "Scan Date: <b>2026-03-04</b>  |  Detection Mode: <b>Fast (Email + Phone Numbers via child resources)</b>",
    body_style))
story.append(Spacer(1, 0.2*inch))

summary_data = [
    ["836",    "183",           "0",              "Not scanned"],
    ["ACS Resources\nFound", "Resources with\nEmail Detected", "Resources with\nPhone Numbers", "SMS / Chat / Calling\n(fast mode)"],
]
summary_colors = [BLUE, RED, MGRAY, MGRAY]
stat_cells = []
label_cells = []
for i, (val, lbl, col) in enumerate(zip(summary_data[0], summary_data[1], summary_colors)):
    stat_cells.append(
        Table([[Paragraph(val, S(f"sv{i}", fontName="Helvetica-Bold", fontSize=28, textColor=WHITE, alignment=TA_CENTER))]],
              colWidths=[2.1*inch], rowHeights=[0.6*inch],
              style=TableStyle([("BACKGROUND", (0,0), (-1,-1), col),
                                ("VALIGN", (0,0), (-1,-1), "MIDDLE")])))
    label_cells.append(
        Paragraph(lbl, S(f"sl{i}", fontName="Helvetica", fontSize=10, textColor=DARK, alignment=TA_CENTER)))

stat_row   = Table([stat_cells],  colWidths=[2.3*inch]*4, style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)]))
label_row  = Table([label_cells], colWidths=[2.3*inch]*4, style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),4)]))
story.append(stat_row)
story.append(label_row)
story.append(Spacer(1, 0.25*inch))

story.append(Paragraph("Channel Detection Summary", section_head))
ch_header = [Paragraph(h, white_bold) for h in ["Channel", "Status", "Resources Impacted", "Retirement Date", "Action Required"]]
ch_rows = [
    ("Email Service",      "Detected",     "183",          "2029-03-31", "Migrate to M365 HVE"),
    ("Phone Numbers SDK",  "Not detected", "0",            "2029-03-31", "No action required"),
    ("SMS API",            "Not scanned",  "—",            "2029-03-31", "Re-run with Full scan"),
    ("Chat SDK",           "Not scanned",  "—",            "2029-03-31", "Re-run with Full scan"),
    ("Calling SDK",        "Not scanned",  "—",            "2029-03-31", "Re-run with Full scan"),
]
ch_data = [ch_header]
for ch, status, count, date, action in ch_rows:
    status_color = RED if status == "Detected" else (colors.HexColor("#777777") if status == "Not detected" else ORANGE)
    ch_data.append([
        Paragraph(ch, bold_body),
        Paragraph(status, S(f"cs", fontName="Helvetica-Bold", fontSize=11, textColor=status_color)),
        Paragraph(count, S("cc", fontName="Helvetica-Bold", fontSize=11, textColor=DARK, alignment=TA_CENTER)),
        Paragraph(date, body_style),
        Paragraph(action, body_style),
    ])
ch_tbl = Table(ch_data, colWidths=[1.7*inch, 1.1*inch, 1.4*inch, 1.2*inch, 2.4*inch],
               style=TableStyle([
                   ("BACKGROUND",    (0,0), (-1,0),  BLUE),
                   ("ROWBACKGROUNDS",(0,1), (-1,-1), [LGRAY, WHITE]),
                   ("TOPPADDING",    (0,0), (-1,-1), 7),
                   ("BOTTOMPADDING", (0,0), (-1,-1), 7),
                   ("LEFTPADDING",   (0,0), (-1,-1), 8),
                   ("LINEBELOW",     (0,0), (-1,-1), 0.5, MGRAY),
                   ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
                   ("ALIGN",         (2,0), (2,-1),  "CENTER"),
               ]))
story.append(ch_tbl)
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph(
    "Reports exported to ./exports/  |  acs-impact-20260304-164754.csv  |  .json  |  .md",
    small_style))
story.append(Paragraph(
    "Next step: Re-run with Full scan (mode 2) to detect SMS, Chat, and Calling usage via Azure Monitor.",
    S("ns", fontName="Helvetica-Oblique", fontSize=10, textColor=BLUE)))
story.append(PageBreak())

# ─── PAGE 13: Scan Results — Personal ────────────────────────────────────────
story.append(Paragraph("Live Scan Results", head_style))
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=8))
story.append(Paragraph(
    "Account: <b>jameelahr2002@gmail.com</b><br/>"
    "Scan Date: <b>2026-03-09</b>  |  Detection Mode: <b>Full (all 5 channels via Azure Monitor, 90-day lookback)</b>",
    body_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("Subscriptions Scanned: 2", section_head))
sub_rows = [
    ("Visual Studio Enterprise Subscription", "a024334f-849a-4470-9d81-d28e2c5a8386", "0 ACS resources", "No action required"),
    ("JameelaPayAsYouGo",                     "a89e7234-d3e0-4956-aee2-934220095a4e", "2 ACS resources", "Provisioned, zero usage — retirement planning required"),
]
sub_data = [[Paragraph(h, white_bold) for h in ["Subscription", "ID", "Resources", "Status"]]]
for name, sid, resources, status in sub_rows:
    sub_data.append([
        Paragraph(name, bold_body),
        Paragraph(sid,  S("sid", fontName="Helvetica", fontSize=9, textColor=DARK)),
        Paragraph(resources, body_style),
        Paragraph(status, body_style),
    ])
sub_tbl = Table(sub_data, colWidths=[2.2*inch, 2.5*inch, 1.3*inch, 3.3*inch],
                style=TableStyle([
                    ("BACKGROUND",    (0,0), (-1,0),  BLUE),
                    ("ROWBACKGROUNDS",(0,1), (-1,-1), [LGRAY, WHITE]),
                    ("TOPPADDING",    (0,0), (-1,-1), 7),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
                    ("LEFTPADDING",   (0,0), (-1,-1), 8),
                    ("LINEBELOW",     (0,0), (-1,-1), 0.5, MGRAY),
                    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
                ]))
story.append(sub_tbl)
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("Channel Detection — JameelaPayAsYouGo", section_head))
res_header = [Paragraph(h, white_bold) for h in ["Resource", "Email", "SMS", "Chat", "Calling", "Phone Numbers", "Channels Active"]]
res_rows = [
    ("ACSProd",       "0 requests", "0 requests", "0 requests", "0 requests", "0 requests", "0 / 5"),
    ("ACSDevAndTest", "0 requests", "0 requests", "0 requests", "0 requests", "0 requests", "0 / 5"),
]
res_data = [res_header]
for row in res_rows:
    res_data.append([Paragraph(c, body_style if i > 0 else bold_body) for i, c in enumerate(row)])
res_tbl = Table(res_data, colWidths=[1.5*inch, 1.1*inch, 1.0*inch, 1.0*inch, 1.1*inch, 1.4*inch, 1.2*inch],
                style=TableStyle([
                    ("BACKGROUND",    (0,0), (-1,0),  BLUE),
                    ("ROWBACKGROUNDS",(0,1), (-1,-1), [LGRAY, WHITE]),
                    ("TOPPADDING",    (0,0), (-1,-1), 7),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
                    ("LEFTPADDING",   (0,0), (-1,-1), 8),
                    ("LINEBELOW",     (0,0), (-1,-1), 0.5, MGRAY),
                    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
                ]))
story.append(res_tbl)
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph(
    "Both resources are provisioned but have had zero API activity in the past 90 days.",
    S("note", fontName="Helvetica-Oblique", fontSize=10, textColor=colors.HexColor("#777777"))))
story.append(Paragraph(
    "Recommendation: Decommission unused resources, or plan migration before 2029-03-31.",
    S("rec", fontName="Helvetica-Oblique", fontSize=10, textColor=BLUE)))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph(
    "Reports: acs-impact-20260309-115909.csv  |  .json  |  .md",
    small_style))
story.append(PageBreak())

# ─── PAGE 14: Get Started ─────────────────────────────────────────────────────
story.append(Spacer(1, 1.4*inch))
story.append(Paragraph("Get Started", title_style))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("github.com/jameelaesa/ACS-Transition-Agent-v0",
                        S("GH", fontName="Helvetica", fontSize=16, textColor=LBLUE)))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(
    'Type &nbsp; <b>"Run an ACS deprecation scan"</b> &nbsp; in any supported AI agent to begin.',
    S("GS", fontName="Helvetica", fontSize=14, textColor=colors.HexColor("#CCCCCC"))))
story.append(Spacer(1, 1.8*inch))
story.append(Paragraph("Retirement deadline: March 31, 2029",
                        S("DD", fontName="Helvetica", fontSize=12, textColor=colors.HexColor("#888888"))))

# ─── Tech icon cluster for title slide (drawn on canvas via on_page) ──────────
def draw_tech_icons(c):
    """Draw Azure + Claude + Agent Skills connected node diagram on the title slide."""
    # Node centers (canvas coords: 0,0 = bottom-left, y goes up)
    az_x, az_y = 9.6 * inch, 5.1 * inch    # Azure — top
    cl_x, cl_y = 7.7 * inch, 2.8 * inch    # Claude — bottom-left
    sk_x, sk_y = 11.3 * inch, 2.8 * inch   # Agent Skills — bottom-right
    r_big = 0.82 * inch
    r_med = 0.67 * inch

    c.saveState()

    # Glow halos (soft colored circles behind each node)
    c.setStrokeColor(colors.transparent)
    c.setFillColor(colors.HexColor("#002952"))
    c.circle(az_x, az_y, r_big * 1.55, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#2C1600"))
    c.circle(cl_x, cl_y, r_med * 1.55, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#00282A"))
    c.circle(sk_x, sk_y, r_med * 1.55, fill=1, stroke=0)

    # Connecting lines
    c.setStrokeColor(colors.HexColor("#1A4B7A"))
    c.setLineWidth(1.5)
    c.line(az_x, az_y, cl_x, cl_y)
    c.line(az_x, az_y, sk_x, sk_y)
    c.line(cl_x, cl_y, sk_x, sk_y)

    # Arrow heads on connecting lines
    def arrow_head(x1, y1, x2, y2, col):
        dx, dy = x2 - x1, y2 - y1
        L = math.sqrt(dx * dx + dy * dy)
        if L == 0:
            return
        ux, uy = dx / L, dy / L
        mx, my = x1 + dx * 0.58, y1 + dy * 0.58
        s = 7
        px, py = -uy * s * 0.5, ux * s * 0.5
        c.setFillColor(col)
        c.setStrokeColor(col)
        p = c.beginPath()
        p.moveTo(mx + ux * s,       my + uy * s)
        p.lineTo(mx + px - ux * 2,  my + py - uy * 2)
        p.lineTo(mx - px - ux * 2,  my - py - uy * 2)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    ac = colors.HexColor("#1E5FA8")
    arrow_head(az_x, az_y, cl_x, cl_y, ac)
    arrow_head(az_x, az_y, sk_x, sk_y, ac)
    arrow_head(cl_x, cl_y, sk_x, sk_y, ac)

    # ── Azure node (blue) ──────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor("#0078D4"))
    c.setStrokeColor(colors.HexColor("#50AAFF"))
    c.setLineWidth(2.5)
    c.circle(az_x, az_y, r_big, fill=1, stroke=1)
    # Inner accent circle
    c.setStrokeColor(colors.transparent)
    c.setFillColor(colors.HexColor("#3BA8F5"))
    c.circle(az_x, az_y + r_big * 0.18, r_big * 0.30, fill=1, stroke=0)
    # Labels
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(az_x, az_y + 13, "Azure")
    c.setFont("Helvetica", 8)
    c.drawCentredString(az_x, az_y + 1, "Communication")
    c.drawCentredString(az_x, az_y - 11, "Services")

    # ── Claude node (orange) ───────────────────────────────────────────────────
    c.setFillColor(colors.HexColor("#C24A00"))
    c.setStrokeColor(colors.HexColor("#FF8C42"))
    c.setLineWidth(2.5)
    c.circle(cl_x, cl_y, r_med, fill=1, stroke=1)
    c.setStrokeColor(colors.transparent)
    c.setFillColor(colors.HexColor("#FF9A5C"))
    c.circle(cl_x, cl_y + r_med * 0.20, r_med * 0.30, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(cl_x, cl_y + 10, "Claude")
    c.setFont("Helvetica", 8)
    c.drawCentredString(cl_x, cl_y - 4, "AI Agent")

    # ── Agent Skills node (teal) ───────────────────────────────────────────────
    c.setFillColor(colors.HexColor("#006B6E"))
    c.setStrokeColor(colors.HexColor("#00C8D0"))
    c.setLineWidth(2.5)
    c.circle(sk_x, sk_y, r_med, fill=1, stroke=1)
    c.setStrokeColor(colors.transparent)
    c.setFillColor(colors.HexColor("#00B7C3"))
    c.circle(sk_x, sk_y + r_med * 0.20, r_med * 0.30, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(sk_x, sk_y + 10, "Agent")
    c.setFont("Helvetica", 8)
    c.drawCentredString(sk_x, sk_y - 4, "Skills")

    # ── Decorative scatter dots ────────────────────────────────────────────────
    c.setStrokeColor(colors.transparent)
    for fx, fy, fr, fc in [
        (8.2,  6.4, 4, "#1A3B5C"),
        (10.8, 6.2, 4, "#1A3B5C"),
        (7.1,  4.2, 3, "#1A3B5C"),
        (12.1, 4.5, 3, "#1A3B5C"),
        (8.6,  1.6, 4, "#1A3B5C"),
        (10.7, 1.5, 3, "#1A3B5C"),
        (9.6,  7.0, 5, "#0D2540"),
        (12.5, 3.0, 4, "#0D2540"),
        (7.0,  2.0, 3, "#0D2540"),
    ]:
        c.setFillColor(colors.HexColor(fc))
        c.circle(fx * inch, fy * inch, fr, fill=1, stroke=0)

    c.restoreState()

# ─── Build with per-page backgrounds ─────────────────────────────────────────
page_bgs = {
    1: DARK, 2: WHITE, 3: WHITE, 4: WHITE, 5: WHITE, 6: WHITE, 7: WHITE,
    8: WHITE, 9: WHITE, 10: WHITE, 11: WHITE, 12: WHITE, 13: WHITE, 14: DARK,
}

def on_page(canvas, doc):
    pn = doc.page
    bg_color = page_bgs.get(pn, WHITE)
    canvas.saveState()
    canvas.setFillColor(bg_color)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    if bg_color == DARK:
        canvas.setFillColor(BLUE)
        canvas.rect(0, 0, 0.35 * inch, H, fill=1, stroke=0)
    else:
        canvas.setFillColor(BLUE)
        canvas.rect(0, H - 0.65 * inch, W, 0.65 * inch, fill=1, stroke=0)
    canvas.restoreState()
    # Draw tech icon cluster on title slide
    if pn == 1:
        draw_tech_icons(canvas)

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Saved: {out}")
