import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepInFrame, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
import datetime
from models.database import Database
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH_NORMAL = os.path.join(BASE_DIR, '..', 'fonts', 'DejaVuSans.ttf')
FONT_PATH_NORMAL_BOLD = os.path.join(BASE_DIR, '..', 'fonts', 'DejaVuSans-Bold.ttf')
FONT_PATH_ITALIC = os.path.join(BASE_DIR, '..', 'fonts', 'DejaVuSerif-Italic.ttf')
BARCODE_PATH = os.path.join(BASE_DIR, '..','images', 'barcode.png')


pdfmetrics.registerFont(TTFont('TurkishFont', FONT_PATH_NORMAL))
pdfmetrics.registerFont(TTFont('TurkishFontBold', FONT_PATH_NORMAL_BOLD))
pdfmetrics.registerFont(TTFont('TurkishFontItalic', FONT_PATH_ITALIC))





class ExpensePdfGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.font_name = 'TurkishFont'
        self.db = Database()
        self.barcode_path = os.path.join(os.path.dirname(__file__), BARCODE_PATH)
            
        self.title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Heading1'],
            fontName='TurkishFontBold',
            alignment=1,  
            fontSize=20
        )
        
        self.normal_style = ParagraphStyle(
            'NormalStyle',
            parent=self.styles['Normal'],
            fontName=self.font_name,
            fontSize=10
        )
        
        self.header_style = ParagraphStyle(
            'HeaderStyle',
            parent=self.styles['Heading2'],
            fontName=self.font_name,
            fontSize=12
        )

        self.date_style = ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            fontName='TurkishFontItalic',
            fontSize=8,
            alignment=2  
        )

        self.footer_style = ParagraphStyle(
            'FooterStyle',
            parent=self.styles['Normal'],
            fontName='TurkishFontItalic',
            fontSize=7,
      )
    
    def getEmployeeDepartmentName(self,department_id):
        query = "SELECT birimIsmi FROM birim WHERE birimId = ?"
        self.db.cursor.execute(query, (department_id,))
        result = self.db.cursor.fetchone()
        return result[0] if result else "Bilinmeyen Departman"

    def generate_expense_pdf(self, expense_data, employee_data, save_path=None):

        if not expense_data or not employee_data:
            return None
            
        if not save_path:
            employee_name = f"{employee_data['isim']}_{employee_data['soyisim']}"
            expense_id = expense_data['harcamaId']            
            employee_department_name = self.getEmployeeDepartmentName(employee_data['birimId'])
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            file_name = f"{employee_name}_{expense_id}.pdf"
            save_path = os.path.join(desktop_path, file_name)
        
        doc = SimpleDocTemplate(
            save_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        title = Paragraph("Harcama Tazmin Belgesi", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")

        date_text = Paragraph(f"Belge Tarihi: {current_date.replace('/', '.')}", self.date_style)        
        if os.path.exists(self.barcode_path):
            barcode_img = Image(self.barcode_path, width=100, height=25,hAlign='RIGHT')
            story.append(barcode_img)
            story.append(Spacer(1, 10))
        
        
        story.append(date_text)
        story.append(Spacer(1, 20))
        
        employee_name = f"{employee_data['isim']} {employee_data['soyisim']}"
        emp_info = Paragraph(f"Çalışan: {employee_name}", self.normal_style)
        department_info = Paragraph(f"Bağlı Bulunan Departman: {employee_department_name}", self.normal_style)
        story.append(emp_info)
        story.append(department_info)
        story.append(Spacer(1, 15))
        horizontal_line = Table([[''], ], colWidths=[doc.width])
        horizontal_line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
        ]))
        story.append(horizontal_line)
        story.append(Spacer(1, 20))
        
        expense_details = [
            ["Talep No", str(expense_data['harcamaId'])],
            ["Harcama Kalemi", expense_data['kalemAd']],
            ["Talep Edilen Tutar", f"{expense_data['tutar']:.2f} TL"],
            ["Talep Tarihi", expense_data['tarih']],
            ["Onay Durumu", expense_data['onayDurumu']],
            ["Tazmin Miktarı", f"{expense_data['tazminTutari']:.2f} TL"]
        ]
        
        table = Table(expense_details, colWidths=[200, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Add spacer to push content toward the bottom
        story.append(Spacer(1, 250))

        # Add more space to push footer lower
        story.append(Spacer(1, 50))
        
        # Create a horizontal line spanning the full width
        horizontal_line = Table([[''], ], colWidths=[doc.width])
        horizontal_line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
        ]))
        story.append(horizontal_line)
        story.append(Spacer(1, 15))        # Add the confirmation text
        confirmation = Paragraph("Lütfen bu belgeyi muhasebe biriminize onaylatınız. Muhasebe biriminin imza ve kaşesi olmayan belgeler geçersiz sayılır.", self.footer_style)
        story.append(confirmation)

        
        doc.build(story)
        
        return save_path