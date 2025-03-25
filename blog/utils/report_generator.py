from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from django.utils import timezone
import os

class ShareAnalyticsReport:
    def __init__(self, post):
        self.post = post
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#007bff')
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#2c3e50')
        )
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )

    def create_header(self):
        """Create report header with post information"""
        elements = []
        elements.append(Paragraph(f"Share Analytics Report", self.title_style))
        elements.append(Paragraph(f"Post: {self.post.title}", self.heading_style))
        elements.append(Paragraph(f"Author: {self.post.author.username}", self.body_style))
        elements.append(Paragraph(f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", self.body_style))
        elements.append(Spacer(1, 20))
        return elements

    def create_summary_section(self):
        """Create summary section with key metrics"""
        elements = []
        elements.append(Paragraph("Summary", self.heading_style))
        
        data = [
            ["Total Shares", str(self.post.total_shares)],
            ["Social Reach", f"{self.post.social_reach:,} people"],
            ["Shares Today", str(self.post.shares_today)],
        ]
        
        table = Table(data, colWidths=[2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        return elements

    def create_platform_distribution(self):
        """Create platform distribution section with pie chart"""
        elements = []
        elements.append(Paragraph("Platform Distribution", self.heading_style))
        
        # Create pie chart
        drawing = Drawing(400, 200)
        pie = Pie()
        pie.x = 100
        pie.y = 0
        pie.width = 200
        pie.height = 200
        
        # Get platform data
        platforms = {
            'Facebook': self.post.facebook_shares,
            'Twitter': self.post.twitter_shares,
            'LinkedIn': self.post.linkedin_shares,
            'WhatsApp': self.post.whatsapp_shares,
            'Pinterest': self.post.pinterest_shares,
            'Reddit': self.post.reddit_shares,
            'Email': self.post.email_shares
        }
        
        # Filter out platforms with 0 shares
        platforms = {k: v for k, v in platforms.items() if v > 0}
        
        pie.data = list(platforms.values())
        pie.labels = list(platforms.keys())
        
        # Add some colors
        pie.slices.strokeWidth = 0.5
        pie.slices[0].fillColor = colors.HexColor('#3b5998')  # Facebook
        pie.slices[1].fillColor = colors.HexColor('#1da1f2')  # Twitter
        pie.slices[2].fillColor = colors.HexColor('#0077b5')  # LinkedIn
        pie.slices[3].fillColor = colors.HexColor('#25d366')  # WhatsApp
        pie.slices[4].fillColor = colors.HexColor('#e60023')  # Pinterest
        pie.slices[5].fillColor = colors.HexColor('#ff4500')  # Reddit
        pie.slices[6].fillColor = colors.HexColor('#d44638')  # Email
        
        drawing.add(pie)
        elements.append(drawing)
        elements.append(Spacer(1, 20))
        return elements

    def create_share_history(self):
        """Create share history section with line chart"""
        elements = []
        elements.append(Paragraph("Share History (Last 30 Days)", self.heading_style))
        
        # Create line chart
        drawing = Drawing(400, 200)
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        
        # Get share history data
        history = self.post.share_history
        dates = [entry['date'] for entry in history]
        counts = [entry['count'] for entry in history]
        
        chart.data = [counts]
        chart.categoryAxis.categoryNames = dates
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.angle = 30
        chart.categoryAxis.labels.dx = 8
        chart.categoryAxis.labels.dy = -2
        
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(counts) + 5
        chart.valueAxis.valueStep = 5
        
        chart.lines[0].strokeWidth = 2
        chart.lines[0].strokeColor = colors.HexColor('#007bff')
        
        drawing.add(chart)
        elements.append(drawing)
        elements.append(Spacer(1, 20))
        return elements

    def create_milestone_section(self):
        """Create milestone section"""
        elements = []
        elements.append(Paragraph("Share Milestones", self.heading_style))
        
        milestones = [
            (10, "First 10 Shares"),
            (50, "Going Viral"),
            (100, "Centurion"),
            (500, "Super Viral"),
            (1000, "Mega Viral")
        ]
        
        data = []
        for count, name in milestones:
            status = "✓" if self.post.total_shares >= count else "Pending"
            data.append([name, str(count), status])
        
        table = Table(data, colWidths=[2*inch, inch, inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        return elements

    def generate_pdf(self, output_path):
        """Generate the complete PDF report"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        elements = []
        elements.extend(self.create_header())
        elements.extend(self.create_summary_section())
        elements.extend(self.create_platform_distribution())
        elements.extend(self.create_share_history())
        elements.extend(self.create_milestone_section())
        
        doc.build(elements)
        return output_path 