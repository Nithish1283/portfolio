import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
            self._startPage()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def build_pdf(filename="Nithish_Gadde.pdf"):
    # Target 1-page layout with compact margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=32,
        rightMargin=32,
        topMargin=26,
        bottomMargin=26
    )

    story = []
    styles = getSampleStyleSheet()

    # Color definitions
    primary_color = colors.HexColor("#1A2530")
    dark_gray = colors.HexColor("#333333")
    light_line = colors.HexColor("#CCCCCC")

    # Custom styles
    title_style = ParagraphStyle(
        'NameTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=21,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=2
    )

    contact_style = ParagraphStyle(
        'ContactInfo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=11.5,
        textColor=dark_gray,
        alignment=1, # Center
        spaceAfter=5
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        textColor=primary_color,
        spaceBefore=4,
        spaceAfter=1
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=10.5,
        textColor=dark_gray
    )

    bold_body_style = ParagraphStyle(
        'BoldBodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=dark_gray
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=10,
        leftIndent=10,
        firstLineIndent=-6,
        textColor=dark_gray,
        spaceAfter=1
    )

    # 1. Header
    story.append(Paragraph("GADDE NITHISH", title_style))
    contact_text = (
        "Kesavaram, Nellore District, AP | +91 9032281283 | <a href='mailto:gaddenithishyadav@gmail.com' color='#1A2530'><u>gaddenithishyadav@gmail.com</u></a><br/>"
        "LinkedIn: <a href='https://linkedin.com/in/gadde-nithish-8094783a3' color='#1A2530'><u>linkedin.com/in/gadde-nithish-8094783a3</u></a> | "
        "GitHub: <a href='https://github.com/Nithish1283' color='#1A2530'><u>github.com/Nithish1283</u></a>"
    )
    story.append(Paragraph(contact_text, contact_style))

    def add_section(title):
        story.append(Paragraph(title, section_heading))
        story.append(HRFlowable(width="100%", thickness=0.7, color=light_line, spaceBefore=1, spaceAfter=3))

    # 2. Professional Summary
    add_section("Professional Summary")
    summary_text = (
        "Computer Science & Engineering (Data Science) graduate with hands-on experience in Java Full-Stack, MERN Stack, "
        "and Data Science technologies. Skilled in Java, JSP, Servlets, React.js, Python, SQL, and MySQL. Experienced in building "
        "scalable web applications, dynamic database solutions, and machine learning models."
    )
    story.append(Paragraph(summary_text, body_style))

    # 3. Technical Skills
    add_section("Technical Skills")
    skills_data = [
        [Paragraph("<b>Languages & Web:</b>", body_style), Paragraph("Java, SQL, JavaScript, Python, HTML5, CSS3, JSP, Servlets, React.js, Node.js, Express, Django", body_style)],
        [Paragraph("<b>Databases & APIs:</b>", body_style), Paragraph("MySQL, MongoDB, JDBC, RESTful APIs, PreparedStatements", body_style)],
        [Paragraph("<b>Core Concepts:</b>", body_style), Paragraph("OOP, MVC Architecture, CRUD Operations, Session Management, Machine Learning Basics", body_style)],
        [Paragraph("<b>Tools & Platforms:</b>", body_style), Paragraph("Eclipse IDE, VS Code, Git, GitHub, Apache Tomcat, MySQL Workbench", body_style)],
    ]
    skills_table = Table(skills_data, colWidths=[115, 433])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(skills_table)

    # 4. Experience & Internships
    add_section("Experience & Internships")

    exp1_header = [
        Paragraph("<b>MERN Stack Developer Intern — Codec Technologies Pvt. Ltd. (Google Partner & AICTE)</b>", bold_body_style),
        Paragraph("<font size=8><b>Dec 2025 – Mar 2026</b></font>", ParagraphStyle('R', parent=body_style, alignment=2))
    ]
    t_exp1 = Table([exp1_header], colWidths=[420, 128])
    t_exp1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(t_exp1)
    story.append(Paragraph("• Completed a 3-Month AICTE approved internship focused on MERN stack development and modern UI frameworks.", bullet_style))
    story.append(Paragraph("• Built full-stack features with Node.js, Express, React, and MongoDB for dynamic data handling.", bullet_style))

    story.append(Spacer(1, 2))

    exp2_header = [
        Paragraph("<b>Web Development Intern — ExcelR Edtech Pvt. Ltd. & APSCHE</b>", bold_body_style),
        Paragraph("<font size=8><b>July 2024</b></font>", ParagraphStyle('R', parent=body_style, alignment=2))
    ]
    t_exp2 = Table([exp2_header], colWidths=[420, 128])
    t_exp2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(t_exp2)
    story.append(Paragraph("• Developed responsive web pages using HTML, CSS, and JavaScript, enhancing layout responsiveness.", bullet_style))

    # 5. Key Projects
    add_section("Projects")

    # Project 1: Restaurant Management System
    proj1_header = [
        Paragraph("<b>Restaurant Management System</b> | <a href='https://github.com/Nithish1283/RestaurantManagementSystem' color='#0044CC'><u>GitHub: RestaurantManagementSystem</u></a>", bold_body_style),
        Paragraph("<font size=8><b>Java, JSP, Servlets, JDBC, MySQL</b></font>", ParagraphStyle('R', parent=body_style, alignment=2))
    ]
    t1 = Table([proj1_header], colWidths=[360, 188])
    t1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(t1)
    story.append(Paragraph("• Built a web-based restaurant operations platform for menu management, ordering, and automated bill calculation.", bullet_style))
    story.append(Paragraph("• Designed relational database schema using MySQL with PreparedStatements for SQL injection prevention.", bullet_style))

    story.append(Spacer(1, 2))

    # Project 2: Student Performance Prediction
    proj2_header = [
        Paragraph("<b>Student Performance Prediction</b> | <a href='https://github.com/Nithish1283/Students_Performance_Prediction' color='#0044CC'><u>GitHub: Students_Performance_Prediction</u></a>", bold_body_style),
        Paragraph("<font size=8><b>Python, Django, ML, MySQL</b></font>", ParagraphStyle('R', parent=body_style, alignment=2))
    ]
    t2 = Table([proj2_header], colWidths=[370, 178])
    t2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(t2)
    story.append(Paragraph("• Developed a Data Science web application predicting student academic performance based on historical indicators.", bullet_style))

    story.append(Spacer(1, 2))

    # Project 3: Student Management System
    proj3_header = [
        Paragraph("<b>Student Management System</b> | <a href='https://github.com/Nithish1283/StudentManagementSystem' color='#0044CC'><u>GitHub: StudentManagementSystem</u></a>", bold_body_style),
        Paragraph("<font size=8><b>Java, JSP, Servlets, JDBC, MySQL</b></font>", ParagraphStyle('R', parent=body_style, alignment=2))
    ]
    t3 = Table([proj3_header], colWidths=[360, 188])
    t3.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(t3)
    story.append(Paragraph("• Implemented Admin login, session tracking, and complete Student CRUD operations using MVC architecture.", bullet_style))

    # 6. Certifications
    add_section("Certifications & Training")
    cert_data = [
        [Paragraph("• <b>MERN Stack Developer Internship</b> – Codec Technologies & AICTE (Google Partner)", bullet_style), Paragraph("<font size=8>2026</font>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("• <b>Full Stack Java Development</b> – Tap Academy", bullet_style), Paragraph("<font size=8>2026</font>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("• <b>Web Full Stack Developer (120 Hours)</b> – EduSkills & APSCHE", bullet_style), Paragraph("<font size=8>2024</font>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("• <b>Data Science Master Virtual Internship</b> – EduSkills & ALTAIR (Grade: E - Excellent)", bullet_style), Paragraph("<font size=8>2024</font>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("• <b>Google AI-ML TECH CAMP</b> – Google for Developers & EduSkills", bullet_style), Paragraph("<font size=8>2024</font>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("• <b>Web Development & JavaScript Internship</b> – ExcelR Edtech & APSCHE", bullet_style), Paragraph("<font size=8>2024</font>", ParagraphStyle('R', parent=body_style, alignment=2))],
    ]
    cert_table = Table(cert_data, colWidths=[460, 88])
    cert_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(cert_table)

    # 7. Education
    add_section("Education")
    edu_data = [
        [Paragraph("<b>B.Tech – CSE (Data Science)</b> | Rise Krishna Sai Prakasam Group of Institutions, JNTU Kakinada", body_style), Paragraph("2022–2026 | CGPA: 6.5/10%", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Intermediate (MPC)</b> : Narayana Junior College (2020–2022)", body_style), Paragraph("Percentage: 61%", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>SSC</b> : Rathnam E.M High School (2019–2020)", body_style), Paragraph("Percentage: 77%", ParagraphStyle('R', parent=body_style, alignment=2))],
    ]
    edu_table = Table(edu_data, colWidths=[410, 138])
    edu_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(edu_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf()
