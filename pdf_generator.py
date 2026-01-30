from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import datetime

class BiopsyReportGenerator:
    def __init__(self, audit_data):
        self.data = audit_data
        self.filename = f"SREV_Biopsy_{audit_data['hospital_info']['name'].replace(' ', '_')}.pdf"
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(name='MedicalTitle', parent=self.styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, textColor=colors.HexColor('#004A99'), spaceAfter=20))
        self.styles.add(ParagraphStyle(name='MedicalSubHeader', parent=self.styles['Heading2'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#2D3748'), spaceAfter=12))
        self.styles.add(ParagraphStyle(name='NormalMedical', parent=self.styles['Normal'], fontName='Helvetica', fontSize=12, leading=16))
        self.styles.add(ParagraphStyle(name='CriticalSymptom', parent=self.styles['Normal'], fontName='Helvetica-Oblique', fontSize=11, textColor=colors.red))
        self.styles.add(ParagraphStyle(name='ScoreHighlight', parent=self.styles['Normal'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#004A99')))

    def generate(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        story = []

        # --- Page 1: Executive Summary ---
        story.append(Paragraph("SREV DIGITAL HEALTH BIOPSY", self.styles['MedicalTitle']))
        story.append(Spacer(1, 20))
        
        info = self.data['hospital_info']
        story.append(Paragraph(f"<b>Patient (Practice):</b> {info['name']}", self.styles['NormalMedical']))
        story.append(Paragraph(f"<b>Date of Diagnosis:</b> {datetime.datetime.now().strftime('%d %B %Y')}", self.styles['NormalMedical']))
        story.append(Spacer(1, 30))

        score = self.data['health_score']
        condition = "STABLE" if score > 80 else "CRITICAL" if score > 50 else "EMERGENCY"
        color = colors.green if score > 80 else colors.orange if score > 50 else colors.red
        
        story.append(Paragraph(f"Overall Health Score: <font color='{color}'>{score}%</font>", self.styles['MedicalSubHeader']))
        story.append(Paragraph(f"Condition Status: <b>{condition}</b>", self.styles['NormalMedical']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Executive Life Support Summary:", self.styles['MedicalSubHeader']))
        story.append(Paragraph("This automated biopsy has scanned your digital infrastructure. Below is a high-level summary of failing organs:", self.styles['NormalMedical']))
        story.append(Spacer(1, 10))
        
        biopsy = self.data['digital_biopsy']
        summary_data = [
            ["Vital Sign", "Score", "Status"],
            ["Structural Integrity (Web)", f"{biopsy['structural_integrity']['score']}/100", "Critical" if biopsy['structural_integrity']['score'] < 50 else "Stable"],
            ["Public Pulse (Social/GMB)", f"{biopsy['public_pulse']['score']}/100", "Critical" if biopsy['public_pulse']['score'] < 50 else "Stable"],
            ["Conversion Circulation", f"{biopsy['conversion_circulation']['score']}/100", "Review"],
            ["Meta Profile", f"{biopsy['meta_profile']['score']}/100", "Review"]
        ]
        
        t = Table(summary_data, colWidths=[200, 100, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#004A99')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ]))
        story.append(t)
        story.append(PageBreak())

        # --- Page 2: Website Biopsy ---
        self._add_section_page(story, "Website Biopsy (Structure)", biopsy['structural_integrity'])

        # --- Page 3: Social Vital Signs ---
        self._add_section_page(story, "Social Vital Signs (Pulse)", biopsy['public_pulse'])

        # --- Page 4: Trust Metrics (GMB Details) ---
        # Note: In our Logic, GMB is inside Public Pulse. We can extract it for clarity if consistent.
        # Or just simulate a separate page from the Combined pulse data if we want.
        # Let's write a generic page 4 with Conversion + Trust details logic.
        story.append(Paragraph("Trust & Conversion Metrics", self.styles['MedicalTitle']))
        story.append(Paragraph("Detailed analysis of reputation and lead capture efficiency.", self.styles['NormalMedical']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Conversion Circulation:", self.styles['MedicalSubHeader']))
        for s in biopsy['conversion_circulation']['symptoms']:
             story.append(Paragraph(f"• {s}", self.styles['CriticalSymptom']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Meta Profile Check:", self.styles['MedicalSubHeader']))
        for k, v in biopsy['meta_profile']['metrics'].items():
            story.append(Paragraph(f"• {k.replace('_', ' ').title()}: {'DETECTED' if v else 'MISSING'}", self.styles['NormalMedical']))
        
        story.append(PageBreak())

        # --- Page 5: The Prescription ---
        story.append(Paragraph("The Prescription", self.styles['MedicalTitle']))
        story.append(Paragraph("<b>CONFIDENTIAL: TREATMENT PLAN LOCKED</b>", self.styles['MedicalSubHeader']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("To access the complete recovery roadmap including code fixes, content calendars, and reputation management scripts, you must unlock the full report.", self.styles['NormalMedical']))
        story.append(Spacer(1, 40))
        
        # Simulated Large CTA Button
        story.append(Table([["CALL +91-8860800507 TO UNLOCK"]], colWidths=[400], style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#004A99')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ])))
        
        story.append(Spacer(1, 40))
        disclaimer_text = """<b>DISCLAIMER & CLINICAL NOTE:</b> This Digital Health Biopsy is an indicative diagnostic report based on current algorithmic signals and publicly available data at the time of the scan. While these findings highlight critical "Digital Leaks" and growth gaps, they do not constitute a complete performance strategy. Digital health is dynamic; for a Full Prescription & Implementation Plan tailored to your clinic's specific revenue goals, a specialist consultation is required. Don't leave your growth to chance. Consult the Digital Doctors now. 📞 Call/WhatsApp: +91-8860800507"""
        story.append(Paragraph(disclaimer_text, self.styles['NormalMedical']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _add_section_page(self, story, title, data):
        story.append(Paragraph(title, self.styles['MedicalTitle']))
        story.append(Paragraph(f"Section Health Score: {data['score']}/100", self.styles['ScoreHighlight']))
        story.append(Spacer(1, 15))
        
        # Authenticity / Source
        if 'page_title' in data['metrics']:
             src = data['metrics']['page_title']
             story.append(Paragraph(f"<b>Source Verified:</b> {src}", self.styles['NormalMedical']))
             story.append(Spacer(1, 10))
        
        story.append(Paragraph("Observed Metrics:", self.styles['MedicalSubHeader']))
        for k, v in data['metrics'].items():
            if isinstance(v, bool):
                val = "Yes" if v else "No"
            else:
                val = str(v)
            story.append(Paragraph(f"• <b>{k.replace('_', ' ').title()}</b>: {val}", self.styles['NormalMedical']))
        
        story.append(Spacer(1, 15))
        
        if "Social" in title:
             story.append(Paragraph("<b>⚠️ Profile not optimized to Meta Algorithms - Consult immediately for Content Analysis.</b>", self.styles['CriticalSymptom']))
             story.append(Spacer(1, 10))

        story.append(Paragraph("Diagnosed Symptoms:", self.styles['MedicalSubHeader']))
        if data['symptoms']:
            for s in data['symptoms']:
                story.append(Paragraph(f"• {s}", self.styles['CriticalSymptom']))
        else:
            story.append(Paragraph("No critical symptoms detected.", self.styles['NormalMedical']))
            
        story.append(PageBreak())

def generate_pdf_report(audit_results):
    generator = BiopsyReportGenerator(audit_results)
    return generator.generate()
