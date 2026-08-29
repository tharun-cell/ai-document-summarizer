import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Header (Top decorative line and text)
        self.setStrokeColor(colors.HexColor('#1E3A8A'))
        self.setLineWidth(1)
        self.line(54, 738, 612 - 54, 738)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#1E3A8A'))
        self.drawString(54, 744, "IBM SKILLSBUILD INTERNSHIP PROJECT DOCUMENTATION")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawRightString(612 - 54, 744, "TEAM HYDRA")

        # Footer
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.line(54, 50, 612 - 54, 50)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(54, 38, "AI Document Summarizer | https://ai-document-summarizer-58v8.onrender.com/")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 38, page_str)
        
        self.restoreState()


def generate_pdf(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor('#1E3A8A')
    secondary_color = colors.HexColor('#2563EB')
    dark_neutral = colors.HexColor('#0F172A')
    text_color = colors.HexColor('#334155')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=secondary_color,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F8FAFC'),
        borderColor=colors.HexColor('#CBD5E1'),
        borderWidth=0.5,
        borderPadding=4,
        spaceBefore=3,
        spaceAfter=4
    )

    story = []

    # Title Banner
    story.append(Paragraph("AI DOCUMENT & YOUTUBE VIDEO SUMMARIZER", title_style))
    story.append(Paragraph("IBM SkillsBuild Internship Final Project Documentation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=0, spaceAfter=12))

    # Meta Table: Team Details & Web App Info
    team_data = [
        [Paragraph("<b>Project Title:</b>", body_style), Paragraph("AI Document & YouTube Video Summarizer", body_style)],
        [Paragraph("<b>Live Project URL:</b>", body_style), Paragraph("<font color='#2563EB'><u>https://ai-document-summarizer-58v8.onrender.com/</u></font>", body_style)],
        [Paragraph("<b>Internship Program:</b>", body_style), Paragraph("IBM SkillsBuild Internship Program", body_style)],
        [Paragraph("<b>Team Name:</b>", body_style), Paragraph("HYDRA", body_style)],
        [Paragraph("<b>Team Leader:</b>", body_style), Paragraph("S Praneeth Reddy", body_style)],
        [Paragraph("<b>Team Members:</b>", body_style), Paragraph("1. Sangireddy Sritharun Reddy<br/>2. Pilla Rajesh<br/>3. Paila Eshwar", body_style)],
        [Paragraph("<b>Core Stack:</b>", body_style), Paragraph("Python (Flask), Groq Llama 3.3 AI, PyPDF, Supadata API, HTML5/CSS3 Glassmorphic UI", body_style)],
    ]
    t_meta = Table(team_data, colWidths=[120, 384])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    exec_summary_text = (
        "In today's fast-paced digital world, users spend considerable time scanning through long articles, "
        "dense multi-page PDF documents, and extended YouTube video lectures. "
        "The <b>AI Document & YouTube Video Summarizer</b> was developed by <b>Team HYDRA</b> under the "
        "<b>IBM SkillsBuild Internship Program</b> to solve this challenge. It provides an efficient, web-based tool "
        "that instantly distills long content into clear, concise, structured, bulleted summaries using state-of-the-art AI models."
    )
    story.append(Paragraph(exec_summary_text, body_style))

    # 2. Key Features & Capabilities
    story.append(Paragraph("2. Key Features & Capabilities", h1_style))
    features = [
        "<b>Multi-Format Input Support:</b> Process plain text (`.txt`) files, multi-page `.pdf` files, and direct YouTube video URLs.",
        "<b>YouTube Transcript Extraction Pipeline:</b> High-reliability dual-tier retrieval using the Supadata API with direct cloud fallbacks.",
        "<b>Ultra-Fast AI Engine:</b> Powered by Meta's Llama 3.3 70B model via Groq LPUs for near-instantaneous summary generation.",
        "<b>Modern Responsive UI:</b> Engineered with dynamic glassmorphism UI, tabbed navigation, live loading indicators, drag-and-drop targets, and one-click copy functions.",
        "<b>Markdown Rendering:</b> Renders structured headings, bold phrases, and bullet lists using client-side `marked.js`.",
        "<b>Production Deployment:</b> Hosted live on Render cloud platform with full CORS support and HTTPS security."
    ]
    for feat in features:
        story.append(Paragraph(f"• {feat}", bullet_style))

    story.append(Spacer(1, 8))

    # 3. System Architecture & Tech Stack
    story.append(Paragraph("3. System Architecture & Tech Stack", h1_style))
    
    tech_stack_data = [
        [Paragraph("<b>Component</b>", h2_style), Paragraph("<b>Technology / Library</b>", h2_style), Paragraph("<b>Role & Purpose</b>", h2_style)],
        [Paragraph("Backend Framework", body_style), Paragraph("Python Flask 3.x", body_style), Paragraph("REST API routing, static file serving, backend handling.", body_style)],
        [Paragraph("AI Inference Engine", body_style), Paragraph("Groq SDK (Llama 3.3 70B)", body_style), Paragraph("High-speed natural language summarization engine.", body_style)],
        [Paragraph("PDF Parsing", body_style), Paragraph("PyPDF (`pypdf`)", body_style), Paragraph("Extracting raw readable text from uploaded PDF files.", body_style)],
        [Paragraph("Transcript API", body_style), Paragraph("Supadata API / YouTube Transcript", body_style), Paragraph("Automated YouTube transcript fetching engine.", body_style)],
        [Paragraph("Frontend Interface", body_style), Paragraph("HTML5, CSS3, JavaScript (ES6+)", body_style), Paragraph("Single Page Application (SPA), glassmorphic styling.", body_style)],
        [Paragraph("Cloud Hosting", body_style), Paragraph("Render Web Service", body_style), Paragraph("Production hosting using Gunicorn and automated builds.", body_style)],
    ]
    t_stack = Table(tech_stack_data, colWidths=[110, 140, 254])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_stack)

    # 4. API Endpoints Specification
    story.append(Paragraph("4. Backend API Endpoints Specification", h1_style))
    endpoints = [
        ("POST /summarize/text", "Multipart Form-data ('file')", "Ingests text file, decodes text data, and queries Groq AI."),
        ("POST /summarize/pdf", "Multipart Form-data ('file')", "Parses PDF document content with PyPDF and generates summary."),
        ("POST /summarize/youtube", "JSON `{ \"url\": \"<youtube_link>\" }`", "Extracts Video ID, fetches transcript via Supadata API, and summarizes.")
    ]
    for ep_name, payload, ep_desc in endpoints:
        story.append(Paragraph(f"<b>{ep_name}</b>", h2_style))
        story.append(Paragraph(f"• <b>Payload:</b> {payload}", bullet_style))
        story.append(Paragraph(f"• <b>Details:</b> {ep_desc}", bullet_style))

    story.append(Spacer(1, 8))

    # 5. Team Members & Roles
    story.append(Paragraph("5. Team HYDRA - Members & Project Responsibilities", h1_style))
    team_members = [
        ("S Praneeth Reddy", "Team Leader", "Overall System Architecture, Groq Llama AI Integration, Flask Backend Development, Render Cloud Deployment."),
        ("Sangireddy Sritharun Reddy", "Full Stack Developer", "Frontend UI Design (Glassmorphism), CSS animations, marked.js Integration, Single-Page UX."),
        ("Pilla Rajesh", "Backend Specialist", "PyPDF Text Extraction Engine, File Upload Handling, Data Validation Rules."),
        ("Paila Eshwar", "QA & Integration Engineer", "YouTube Transcript Pipeline (Supadata API Integration), Testing, Documentation.")
    ]

    t_team_data = [
        [Paragraph("<b>Name</b>", h2_style), Paragraph("<b>Role</b>", h2_style), Paragraph("<b>Key Responsibilities</b>", h2_style)]
    ]
    for name, role, resp in team_members:
        t_team_data.append([
            Paragraph(f"<b>{name}</b>", body_style),
            Paragraph(role, body_style),
            Paragraph(resp, body_style)
        ])
    t_team = Table(t_team_data, colWidths=[130, 110, 264])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_team)

    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Conclusion & IBM SkillsBuild Internship Acknowledgment", h1_style))
    conclusion_text = (
        "The completion of this project marks a successful milestone for <b>Team HYDRA</b>. "
        "Under the opportunity and mentorship provided by the <b>IBM SkillsBuild Internship Program</b>, "
        "the team successfully conceptualized, built, and deployed a production-grade AI solution live at "
        "<u>https://ai-document-summarizer-58v8.onrender.com/</u>."
    )
    story.append(Paragraph(conclusion_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF documentation at: {pdf_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\madhu\OneDrive\Desktop\project sum\summarizer"
    pdf_filename = os.path.join(out_dir, "IBM_SkillsBuild_Internship_Project_Documentation_Team_HYDRA.pdf")
    generate_pdf(pdf_filename)
