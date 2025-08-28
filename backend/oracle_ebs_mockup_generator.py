from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from typing import Dict, List, Tuple, Optional
import json

class OracleEBSMockupGenerator:
    """Generate realistic Oracle EBS R12 interface mockups that look like actual screenshots"""
    
    def __init__(self):
        self.base_images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "images")
        self.mockup_images_path = os.path.join(self.base_images_path, "oracle_mockups")
        
        # Create mockup directory if it doesn't exist
        os.makedirs(self.mockup_images_path, exist_ok=True)
        
        # Oracle EBS R12 color scheme
        self.colors = {
            'oracle_blue': '#0066CC',
            'oracle_light_blue': '#E6F2FF', 
            'oracle_dark_blue': '#003D7A',
            'header_bg': '#F5F5F5',
            'menu_bg': '#FFFFFF',
            'button_bg': '#0066CC',
            'button_hover': '#0052A3',
            'border_color': '#CCCCCC',
            'text_color': '#333333',
            'link_color': '#0066CC',
            'success_green': '#28A745',
            'warning_orange': '#FFC107',
            'error_red': '#DC3545',
            'table_header': '#F8F9FA',
            'table_border': '#DEE2E6'
        }
        
        # Standard Oracle EBS dimensions
        self.dimensions = {
            'width': 1200,
            'height': 800,
            'header_height': 80,
            'menu_height': 40,
            'sidebar_width': 200,
            'button_height': 32,
            'input_height': 24,
            'table_row_height': 28
        }
    
    def create_oracle_header(self, draw: ImageDraw, width: int) -> int:
        """Create Oracle EBS header with logo and navigation"""
        header_height = self.dimensions['header_height']
        
        # Header background
        draw.rectangle([0, 0, width, header_height], fill=self.colors['header_bg'], outline=self.colors['border_color'])
        
        # Oracle logo area (simplified)
        draw.rectangle([10, 10, 150, header_height-10], fill=self.colors['oracle_blue'])
        
        try:
            font_logo = ImageFont.truetype("arial.ttf", 16)
            font_nav = ImageFont.truetype("arial.ttf", 12)
        except:
            font_logo = ImageFont.load_default()
            font_nav = ImageFont.load_default()
        
        # Oracle text
        draw.text((20, 25), "Oracle", fill='white', font=font_logo)
        draw.text((20, 45), "E-Business Suite", fill='white', font=font_nav)
        
        # Navigation items
        nav_items = ["Home", "Navigator", "Preferences", "Help", "Logout"]
        x_pos = width - 300
        for item in nav_items:
            draw.text((x_pos, 30), item, fill=self.colors['text_color'], font=font_nav)
            x_pos += 60
        
        # User info
        draw.text((width - 150, 10), "User: supplier@tmpa.ma", fill=self.colors['text_color'], font=font_nav)
        
        return header_height
    
    def create_breadcrumb(self, draw: ImageDraw, y_pos: int, width: int, breadcrumbs: List[str]) -> int:
        """Create breadcrumb navigation"""
        try:
            font = ImageFont.truetype("arial.ttf", 11)
        except:
            font = ImageFont.load_default()
        
        # Breadcrumb background
        breadcrumb_height = 25
        draw.rectangle([0, y_pos, width, y_pos + breadcrumb_height], 
                      fill=self.colors['oracle_light_blue'], outline=self.colors['border_color'])
        
        # Breadcrumb text
        x_pos = 10
        for i, crumb in enumerate(breadcrumbs):
            if i > 0:
                draw.text((x_pos, y_pos + 6), " > ", fill=self.colors['text_color'], font=font)
                x_pos += 20
            
            color = self.colors['link_color'] if i < len(breadcrumbs) - 1 else self.colors['text_color']
            draw.text((x_pos, y_pos + 6), crumb, fill=color, font=font)
            
            bbox = draw.textbbox((0, 0), crumb, font=font)
            x_pos += bbox[2] - bbox[0] + 5
        
        return y_pos + breadcrumb_height
    
    def create_form_section(self, draw: ImageDraw, x: int, y: int, width: int, title: str, fields: List[Dict]) -> int:
        """Create a form section with title and fields"""
        try:
            font_title = ImageFont.truetype("arial.ttf", 14)
            font_label = ImageFont.truetype("arial.ttf", 11)
        except:
            font_title = ImageFont.load_default()
            font_label = ImageFont.load_default()
        
        current_y = y
        
        # Section title
        draw.rectangle([x, current_y, x + width, current_y + 30], 
                      fill=self.colors['table_header'], outline=self.colors['border_color'])
        draw.text((x + 10, current_y + 8), title, fill=self.colors['text_color'], font=font_title)
        current_y += 35
        
        # Fields
        for field in fields:
            field_type = field.get('type', 'input')
            label = field.get('label', '')
            value = field.get('value', '')
            required = field.get('required', False)
            
            # Label
            label_text = f"{label}{'*' if required else ''}:"
            draw.text((x + 10, current_y + 5), label_text, fill=self.colors['text_color'], font=font_label)
            
            # Field
            field_x = x + 150
            field_width = width - 160
            
            if field_type == 'input':
                # Input field
                draw.rectangle([field_x, current_y, field_x + field_width, current_y + self.dimensions['input_height']], 
                              fill='white', outline=self.colors['border_color'])
                if value:
                    draw.text((field_x + 5, current_y + 4), value, fill=self.colors['text_color'], font=font_label)
            
            elif field_type == 'dropdown':
                # Dropdown field
                draw.rectangle([field_x, current_y, field_x + field_width, current_y + self.dimensions['input_height']], 
                              fill='white', outline=self.colors['border_color'])
                # Dropdown arrow
                draw.polygon([(field_x + field_width - 15, current_y + 8), 
                             (field_x + field_width - 10, current_y + 16), 
                             (field_x + field_width - 5, current_y + 8)], 
                            fill=self.colors['text_color'])
                if value:
                    draw.text((field_x + 5, current_y + 4), value, fill=self.colors['text_color'], font=font_label)
            
            elif field_type == 'button':
                # Button
                button_width = 80
                draw.rectangle([field_x, current_y, field_x + button_width, current_y + self.dimensions['button_height']], 
                              fill=self.colors['button_bg'], outline=self.colors['oracle_dark_blue'])
                
                bbox = draw.textbbox((0, 0), label, font=font_label)
                text_width = bbox[2] - bbox[0]
                draw.text((field_x + (button_width - text_width) // 2, current_y + 8), 
                         label, fill='white', font=font_label)
            
            current_y += 35
        
        return current_y
    
    def create_table(self, draw: ImageDraw, x: int, y: int, width: int, headers: List[str], rows: List[List[str]]) -> int:
        """Create a data table"""
        try:
            font_header = ImageFont.truetype("arial.ttf", 11)
            font_data = ImageFont.truetype("arial.ttf", 10)
        except:
            font_header = ImageFont.load_default()
            font_data = ImageFont.load_default()
        
        current_y = y
        col_width = width // len(headers)
        
        # Table header
        draw.rectangle([x, current_y, x + width, current_y + self.dimensions['table_row_height']], 
                      fill=self.colors['table_header'], outline=self.colors['table_border'])
        
        for i, header in enumerate(headers):
            col_x = x + i * col_width
            draw.line([col_x, current_y, col_x, current_y + self.dimensions['table_row_height']], 
                     fill=self.colors['table_border'])
            draw.text((col_x + 5, current_y + 6), header, fill=self.colors['text_color'], font=font_header)
        
        current_y += self.dimensions['table_row_height']
        
        # Table rows
        for row_idx, row in enumerate(rows):
            bg_color = 'white' if row_idx % 2 == 0 else '#F8F9FA'
            draw.rectangle([x, current_y, x + width, current_y + self.dimensions['table_row_height']], 
                          fill=bg_color, outline=self.colors['table_border'])
            
            for i, cell in enumerate(row):
                col_x = x + i * col_width
                draw.line([col_x, current_y, col_x, current_y + self.dimensions['table_row_height']], 
                         fill=self.colors['table_border'])
                draw.text((col_x + 5, current_y + 6), str(cell), fill=self.colors['text_color'], font=font_data)
            
            current_y += self.dimensions['table_row_height']
        
        # Bottom border
        draw.line([x, current_y, x + width, current_y], fill=self.colors['table_border'])
        
        return current_y
    
    def create_login_screen(self, language: str = 'fr') -> str:
        """Create Oracle EBS login screen mockup"""
        img = Image.new('RGB', (self.dimensions['width'], self.dimensions['height']), color='white')
        draw = ImageDraw.Draw(img)
        
        # Oracle branding header
        header_y = self.create_oracle_header(draw, self.dimensions['width'])
        
        # Login form
        form_x = (self.dimensions['width'] - 400) // 2
        form_y = header_y + 100
        
        title = "Connexion i-Supplier" if language == 'fr' else "i-Supplier Login"
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 18)
        except:
            font_title = ImageFont.load_default()
        
        # Login box
        draw.rectangle([form_x - 20, form_y - 20, form_x + 420, form_y + 200], 
                      fill=self.colors['oracle_light_blue'], outline=self.colors['border_color'], width=2)
        
        # Title
        bbox = draw.textbbox((0, 0), title, font=font_title)
        title_width = bbox[2] - bbox[0]
        draw.text((form_x + (400 - title_width) // 2, form_y), title, fill=self.colors['oracle_dark_blue'], font=font_title)
        
        # Login fields
        fields = [
            {'label': 'Nom d\'utilisateur' if language == 'fr' else 'Username', 'type': 'input', 'required': True},
            {'label': 'Mot de passe' if language == 'fr' else 'Password', 'type': 'input', 'required': True},
            {'label': 'Connexion' if language == 'fr' else 'Login', 'type': 'button'}
        ]
        
        self.create_form_section(draw, form_x, form_y + 40, 400, "", fields)
        
        # Save image
        filename = f"oracle_login_{language}.png"
        filepath = os.path.join(self.mockup_images_path, filename)
        img.save(filepath, 'PNG')
        
        return f"/static/images/oracle_mockups/{filename}"
    
    def create_work_confirmation_screen(self, step: str, language: str = 'fr') -> str:
        """Create work confirmation screens for different steps"""
        img = Image.new('RGB', (self.dimensions['width'], self.dimensions['height']), color='white')
        draw = ImageDraw.Draw(img)
        
        # Header
        header_y = self.create_oracle_header(draw, self.dimensions['width'])
        
        # Breadcrumbs
        if language == 'fr':
            breadcrumbs = ["Accueil", "Approvisionnement", "Confirmations de Travail"]
        else:
            breadcrumbs = ["Home", "Procurement", "Work Confirmations"]
        
        breadcrumb_y = self.create_breadcrumb(draw, header_y, self.dimensions['width'], breadcrumbs)
        
        content_y = breadcrumb_y + 20
        
        if step == "navigate":
            # Navigation menu
            title = "Confirmations de Travail" if language == 'fr' else "Work Confirmations"
            
            # Create button
            button_label = "Créer une Confirmation" if language == 'fr' else "Create Confirmation"
            fields = [{'label': button_label, 'type': 'button'}]
            self.create_form_section(draw, 50, content_y, 500, title, fields)
            
            # Existing confirmations table
            table_y = content_y + 120
            if language == 'fr':
                headers = ["N° Confirmation", "Commande", "Statut", "Date", "Actions"]
                rows = [
                    ["WC-2024-001", "PO-2024-123", "Brouillon", "15/01/2024", "Modifier"],
                    ["WC-2024-002", "PO-2024-124", "Soumis", "16/01/2024", "Voir"]
                ]
            else:
                headers = ["Confirmation #", "Order", "Status", "Date", "Actions"]
                rows = [
                    ["WC-2024-001", "PO-2024-123", "Draft", "15/01/2024", "Edit"],
                    ["WC-2024-002", "PO-2024-124", "Submitted", "16/01/2024", "View"]
                ]
            
            self.create_table(draw, 50, table_y, 1100, headers, rows)
        
        elif step == "select_po":
            # PO selection screen
            title = "Sélectionner une Commande" if language == 'fr' else "Select Purchase Order"
            
            search_fields = [
                {'label': 'N° Commande' if language == 'fr' else 'PO Number', 'type': 'input', 'value': 'PO-2024-'},
                {'label': 'Rechercher' if language == 'fr' else 'Search', 'type': 'button'}
            ]
            
            form_end_y = self.create_form_section(draw, 50, content_y, 600, title, search_fields)
            
            # Results table
            if language == 'fr':
                headers = ["Sélect.", "N° Commande", "Fournisseur", "Montant", "Statut"]
                rows = [
                    ["☐", "PO-2024-123", "TMPA Supplier", "50,000 MAD", "Approuvé"],
                    ["☐", "PO-2024-124", "TMPA Supplier", "75,000 MAD", "Approuvé"]
                ]
            else:
                headers = ["Select", "PO Number", "Supplier", "Amount", "Status"]
                rows = [
                    ["☐", "PO-2024-123", "TMPA Supplier", "50,000 MAD", "Approved"],
                    ["☐", "PO-2024-124", "TMPA Supplier", "75,000 MAD", "Approved"]
                ]
            
            self.create_table(draw, 50, form_end_y + 20, 1100, headers, rows)
        
        elif step == "details":
            # Confirmation details form
            title = "Détails de la Confirmation" if language == 'fr' else "Confirmation Details"
            
            if language == 'fr':
                detail_fields = [
                    {'label': 'N° Commande', 'type': 'input', 'value': 'PO-2024-123'},
                    {'label': 'Article', 'type': 'dropdown', 'value': 'Équipement Portuaire'},
                    {'label': 'Quantité Commandée', 'type': 'input', 'value': '10'},
                    {'label': 'Quantité Confirmée', 'type': 'input', 'required': True},
                    {'label': 'Date d\'Achèvement', 'type': 'input', 'required': True},
                    {'label': 'Notes', 'type': 'input'}
                ]
            else:
                detail_fields = [
                    {'label': 'PO Number', 'type': 'input', 'value': 'PO-2024-123'},
                    {'label': 'Item', 'type': 'dropdown', 'value': 'Port Equipment'},
                    {'label': 'Ordered Quantity', 'type': 'input', 'value': '10'},
                    {'label': 'Confirmed Quantity', 'type': 'input', 'required': True},
                    {'label': 'Completion Date', 'type': 'input', 'required': True},
                    {'label': 'Notes', 'type': 'input'}
                ]
            
            form_end_y = self.create_form_section(draw, 50, content_y, 800, title, detail_fields)
            
            # Action buttons
            button_y = form_end_y + 20
            if language == 'fr':
                draw.rectangle([50, button_y, 130, button_y + 32], fill=self.colors['button_bg'])
                draw.text((70, button_y + 8), "Soumettre", fill='white')
                draw.rectangle([150, button_y, 220, button_y + 32], fill=self.colors['border_color'])
                draw.text((170, button_y + 8), "Annuler", fill=self.colors['text_color'])
            else:
                draw.rectangle([50, button_y, 120, button_y + 32], fill=self.colors['button_bg'])
                draw.text((75, button_y + 8), "Submit", fill='white')
                draw.rectangle([140, button_y, 200, button_y + 32], fill=self.colors['border_color'])
                draw.text((155, button_y + 8), "Cancel", fill=self.colors['text_color'])
        
        # Save image
        filename = f"oracle_work_confirmation_{step}_{language}.png"
        filepath = os.path.join(self.mockup_images_path, filename)
        img.save(filepath, 'PNG')
        
        return f"/static/images/oracle_mockups/{filename}"
    
    def create_rfq_response_screen(self, step: str, language: str = 'fr') -> str:
        """Create RFQ response screens"""
        img = Image.new('RGB', (self.dimensions['width'], self.dimensions['height']), color='white')
        draw = ImageDraw.Draw(img)
        
        # Header
        header_y = self.create_oracle_header(draw, self.dimensions['width'])
        
        # Breadcrumbs
        if language == 'fr':
            breadcrumbs = ["Accueil", "Approvisionnement", "Réponses aux Appels d'Offres"]
        else:
            breadcrumbs = ["Home", "Procurement", "RFQ Responses"]
        
        breadcrumb_y = self.create_breadcrumb(draw, header_y, self.dimensions['width'], breadcrumbs)
        content_y = breadcrumb_y + 20
        
        if step == "review":
            # RFQ details review
            title = "Détails de l'Appel d'Offres" if language == 'fr' else "RFQ Details"
            
            if language == 'fr':
                rfq_fields = [
                    {'label': 'N° RFQ', 'type': 'input', 'value': 'RFQ-TMPA-2024-001'},
                    {'label': 'Description', 'type': 'input', 'value': 'Équipements de manutention portuaire'},
                    {'label': 'Date Limite', 'type': 'input', 'value': '30/01/2024'},
                    {'label': 'Statut', 'type': 'input', 'value': 'Ouvert'}
                ]
            else:
                rfq_fields = [
                    {'label': 'RFQ Number', 'type': 'input', 'value': 'RFQ-TMPA-2024-001'},
                    {'label': 'Description', 'type': 'input', 'value': 'Port handling equipment'},
                    {'label': 'Due Date', 'type': 'input', 'value': '30/01/2024'},
                    {'label': 'Status', 'type': 'input', 'value': 'Open'}
                ]
            
            self.create_form_section(draw, 50, content_y, 800, title, rfq_fields)
        
        elif step == "quotation":
            # Quotation preparation
            title = "Préparer la Cotation" if language == 'fr' else "Prepare Quotation"
            
            if language == 'fr':
                quote_fields = [
                    {'label': 'Article', 'type': 'input', 'value': 'Grue Portuaire - Modèle XYZ'},
                    {'label': 'Quantité', 'type': 'input', 'value': '2'},
                    {'label': 'Prix Unitaire (MAD)', 'type': 'input', 'required': True},
                    {'label': 'Montant Total (MAD)', 'type': 'input'},
                    {'label': 'Délai de Livraison', 'type': 'input', 'required': True},
                    {'label': 'Conformité Technique', 'type': 'dropdown', 'value': 'Conforme'}
                ]
            else:
                quote_fields = [
                    {'label': 'Item', 'type': 'input', 'value': 'Port Crane - Model XYZ'},
                    {'label': 'Quantity', 'type': 'input', 'value': '2'},
                    {'label': 'Unit Price (MAD)', 'type': 'input', 'required': True},
                    {'label': 'Total Amount (MAD)', 'type': 'input'},
                    {'label': 'Delivery Time', 'type': 'input', 'required': True},
                    {'label': 'Technical Compliance', 'type': 'dropdown', 'value': 'Compliant'}
                ]
            
            form_end_y = self.create_form_section(draw, 50, content_y, 800, title, quote_fields)
            
            # Submit button
            button_y = form_end_y + 20
            button_label = "Soumettre la Cotation" if language == 'fr' else "Submit Quotation"
            draw.rectangle([50, button_y, 200, button_y + 32], fill=self.colors['success_green'])
            draw.text((70, button_y + 8), button_label, fill='white')
        
        # Save image
        filename = f"oracle_rfq_{step}_{language}.png"
        filepath = os.path.join(self.mockup_images_path, filename)
        img.save(filepath, 'PNG')
        
        return f"/static/images/oracle_mockups/{filename}"
    
    def generate_all_mockups(self):
        """Generate all Oracle EBS mockup screens"""
        print("Generating Oracle EBS R12 mockup screens...")
        
        # Generate for both languages
        for lang in ['fr', 'en']:
            # Login screen
            self.create_login_screen(lang)
            
            # Work confirmation screens
            for step in ['navigate', 'select_po', 'details']:
                self.create_work_confirmation_screen(step, lang)
            
            # RFQ response screens
            for step in ['review', 'quotation']:
                self.create_rfq_response_screen(step, lang)
        
        print("All Oracle EBS mockup screens generated successfully!")

# Initialize the mockup generator
oracle_mockup_generator = OracleEBSMockupGenerator()