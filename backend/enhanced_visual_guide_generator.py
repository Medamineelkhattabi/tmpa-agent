from PIL import Image, ImageDraw, ImageFont
import os
from typing import Dict, List, Tuple, Optional
import json
from .oracle_ebs_mockup_generator import oracle_mockup_generator

class EnhancedVisualGuideGenerator:
    """Generate realistic Oracle EBS R12 visual guides with authentic interface mockups"""
    
    def __init__(self):
        self.base_images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "images")
        self.annotated_images_path = os.path.join(self.base_images_path, "annotated")
        
        # Create annotated directory if it doesn't exist
        os.makedirs(self.annotated_images_path, exist_ok=True)
        
        # Define Oracle EBS procedure steps with realistic mockup configurations
        self.visual_instructions = {
            "work_confirmation": {
                "login": {
                    "mockup_type": "login",
                    "instructions_fr": "1. Saisissez votre nom d'utilisateur\n2. Saisissez votre mot de passe\n3. Cliquez sur 'Connexion'",
                    "instructions_en": "1. Enter your username\n2. Enter your password\n3. Click 'Login'",
                    "click_areas": [
                        {"x": 400, "y": 200, "label": "Username"},
                        {"x": 400, "y": 240, "label": "Password"}, 
                        {"x": 400, "y": 280, "label": "Login"}
                    ]
                },
                "navigate_to_confirmations": {
                    "mockup_type": "work_confirmation",
                    "mockup_step": "navigate",
                    "instructions_fr": "1. Cliquez sur 'Créer une Confirmation' pour commencer\n2. Consultez les confirmations existantes si nécessaire",
                    "instructions_en": "1. Click 'Create Confirmation' to start\n2. Review existing confirmations if needed",
                    "click_areas": [
                        {"x": 200, "y": 180, "label": "Create Confirmation"}
                    ]
                },
                "select_purchase_order": {
                    "mockup_type": "work_confirmation",
                    "mockup_step": "select_po",
                    "instructions_fr": "1. Saisissez le numéro de commande\n2. Cliquez sur 'Rechercher'\n3. Sélectionnez la commande dans les résultats",
                    "instructions_en": "1. Enter purchase order number\n2. Click 'Search'\n3. Select the order from results",
                    "click_areas": [
                        {"x": 300, "y": 150, "label": "PO Search"},
                        {"x": 450, "y": 150, "label": "Search"},
                        {"x": 100, "y": 250, "label": "Select"}
                    ]
                },
                "enter_confirmation_details": {
                    "mockup_type": "work_confirmation", 
                    "mockup_step": "details",
                    "instructions_fr": "1. Saisissez la quantité confirmée\n2. Sélectionnez la date d'achèvement\n3. Ajoutez des notes\n4. Cliquez sur 'Soumettre'",
                    "instructions_en": "1. Enter confirmed quantity\n2. Select completion date\n3. Add notes\n4. Click 'Submit'",
                    "click_areas": [
                        {"x": 350, "y": 220, "label": "Quantity"},
                        {"x": 350, "y": 260, "label": "Date"},
                        {"x": 350, "y": 300, "label": "Notes"},
                        {"x": 90, "y": 400, "label": "Submit"}
                    ]
                }
            },
            "rfq_response": {
                "rfq_review": {
                    "mockup_type": "rfq_response",
                    "mockup_step": "review",
                    "instructions_fr": "1. Examinez le numéro RFQ\n2. Lisez la description détaillée\n3. Notez la date limite\n4. Vérifiez le statut",
                    "instructions_en": "1. Review RFQ number\n2. Read detailed description\n3. Note the due date\n4. Check status",
                    "click_areas": [
                        {"x": 350, "y": 150, "label": "RFQ Details"},
                        {"x": 350, "y": 190, "label": "Description"},
                        {"x": 350, "y": 230, "label": "Due Date"}
                    ]
                },
                "prepare_quotation": {
                    "mockup_type": "rfq_response",
                    "mockup_step": "quotation", 
                    "instructions_fr": "1. Saisissez le prix unitaire\n2. Le montant total se calcule automatiquement\n3. Indiquez le délai de livraison\n4. Confirmez la conformité technique\n5. Soumettez la cotation",
                    "instructions_en": "1. Enter unit price\n2. Total amount calculates automatically\n3. Specify delivery time\n4. Confirm technical compliance\n5. Submit quotation",
                    "click_areas": [
                        {"x": 350, "y": 220, "label": "Unit Price"},
                        {"x": 350, "y": 300, "label": "Delivery"},
                        {"x": 350, "y": 340, "label": "Compliance"},
                        {"x": 125, "y": 420, "label": "Submit"}
                    ]
                }
            }
        }
    
    def create_annotated_oracle_mockup(self, mockup_type: str, mockup_step: str, click_areas: List[Dict], language: str = 'fr') -> str:
        """Create an annotated Oracle EBS mockup with red circles and instructions"""
        
        annotated_image_name = f"oracle_{mockup_type}_{mockup_step}_{language}_annotated.png"
        annotated_image_path = os.path.join(self.annotated_images_path, annotated_image_name)
        
        # If annotated image already exists, return its path
        if os.path.exists(annotated_image_path):
            return f"/static/images/annotated/{annotated_image_name}"
        
        try:
            # Generate the base Oracle mockup
            if mockup_type == "login":
                base_image_url = oracle_mockup_generator.create_login_screen(language)
            elif mockup_type == "work_confirmation":
                base_image_url = oracle_mockup_generator.create_work_confirmation_screen(mockup_step, language)
            elif mockup_type == "rfq_response":
                base_image_url = oracle_mockup_generator.create_rfq_response_screen(mockup_step, language)
            else:
                return self.create_placeholder_image(f"{mockup_type}_{mockup_step}.png", language)
            
            # Get the actual file path from URL
            base_image_path = base_image_url.replace("/static/images/oracle_mockups/", "")
            base_image_path = os.path.join(oracle_mockup_generator.mockup_images_path, base_image_path)
            
            # Open and annotate the mockup
            with Image.open(base_image_path) as img:
                annotated_img = img.copy()
                draw = ImageDraw.Draw(annotated_img)
                
                # Draw red circles and labels for click areas
                for i, area in enumerate(click_areas):
                    x, y = area['x'], area['y']
                    label = area['label']
                    
                    # Draw red circle with semi-transparent fill
                    circle_radius = 20
                    draw.ellipse([x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius], 
                               outline='#FF0000', width=3)
                    
                    # Draw step number in circle
                    try:
                        font = ImageFont.truetype("arial.ttf", 14)
                        font_small = ImageFont.truetype("arial.ttf", 10)
                    except:
                        font = ImageFont.load_default()
                        font_small = ImageFont.load_default()
                    
                    step_num = str(i + 1)
                    bbox = draw.textbbox((0, 0), step_num, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    # White background for number
                    draw.ellipse([x-12, y-12, x+12, y+12], fill='white')
                    draw.text((x - text_width//2, y - text_height//2), step_num, 
                             fill='#FF0000', font=font)
                    
                    # Draw label with background (positioned to avoid overlap)
                    label_y = y + circle_radius + 15
                    if label_y > img.height - 30:  # If too close to bottom, put above
                        label_y = y - circle_radius - 25
                    
                    label_bbox = draw.textbbox((0, 0), label, font=font_small)
                    label_width = label_bbox[2] - label_bbox[0]
                    
                    # Background rectangle for label
                    draw.rectangle([x - label_width//2 - 3, label_y - 2, 
                                  x + label_width//2 + 3, label_y + 15], 
                                 fill='white', outline='#FF0000')
                    
                    # Label text
                    draw.text((x - label_width//2, label_y), label, fill='#FF0000', font=font_small)
                
                # Save annotated image
                annotated_img.save(annotated_image_path, 'PNG')
                
                return f"/static/images/annotated/{annotated_image_name}"
                
        except Exception as e:
            print(f"Error creating annotated Oracle mockup: {e}")
            return self.create_placeholder_image(f"{mockup_type}_{mockup_step}.png", language)
    
    def create_placeholder_image(self, base_image_name: str, language: str = 'fr') -> str:
        """Create a placeholder image with Oracle EBS styling"""
        
        placeholder_name = f"oracle_placeholder_{language}_{base_image_name}"
        placeholder_path = os.path.join(self.annotated_images_path, placeholder_name)
        
        # Create Oracle-styled placeholder
        img = Image.new('RGB', (1200, 800), color='white')
        draw = ImageDraw.Draw(img)
        
        # Oracle header
        draw.rectangle([0, 0, 1200, 80], fill='#F5F5F5', outline='#CCCCCC')
        draw.rectangle([10, 10, 150, 70], fill='#0066CC')
        
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_medium = ImageFont.truetype("arial.ttf", 16)
            font_small = ImageFont.truetype("arial.ttf", 12)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Oracle branding
        draw.text((20, 25), "Oracle", fill='white', font=font_medium)
        draw.text((20, 45), "E-Business Suite", fill='white', font=font_small)
        
        # Title
        title = "Guide Visuel Oracle EBS R12" if language == 'fr' else "Oracle EBS R12 Visual Guide"
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text((600 - title_width//2, 150), title, fill='#0066CC', font=font_large)
        
        # Instructions
        if language == 'fr':
            instructions = [
                "Étapes à suivre dans Oracle EBS R12 i-Supplier :",
                "1. Connectez-vous avec vos identifiants",
                "2. Naviguez vers le module approprié", 
                "3. Suivez les instructions détaillées",
                "4. Complétez et soumettez votre demande"
            ]
        else:
            instructions = [
                "Steps to follow in Oracle EBS R12 i-Supplier:",
                "1. Login with your credentials",
                "2. Navigate to appropriate module",
                "3. Follow detailed instructions", 
                "4. Complete and submit your request"
            ]
        
        y_pos = 250
        for instruction in instructions:
            draw.text((100, y_pos), instruction, fill='#333333', font=font_medium)
            y_pos += 40
        
        # Save placeholder
        img.save(placeholder_path, 'PNG')
        
        return f"/static/images/annotated/{placeholder_name}"
    
    def get_visual_guide(self, procedure_id: str, step_id: str, language: str = 'fr') -> Dict:
        """Get visual guide information for a specific procedure step"""
        
        # Get visual instructions for this procedure and step
        procedure_visuals = self.visual_instructions.get(procedure_id, {})
        step_visual = procedure_visuals.get(step_id, {})
        
        if not step_visual:
            return {
                "has_visual": False,
                "image_url": None,
                "instructions": "Guide visuel non disponible" if language == 'fr' else "Visual guide not available"
            }
        
        # Get mockup information
        mockup_type = step_visual.get('mockup_type')
        mockup_step = step_visual.get('mockup_step', '')
        click_areas = step_visual.get('click_areas', [])
        
        # Create annotated Oracle mockup
        if mockup_type:
            annotated_image_url = self.create_annotated_oracle_mockup(mockup_type, mockup_step, click_areas, language)
        else:
            # Fallback to placeholder
            annotated_image_url = self.create_placeholder_image(f"{procedure_id}_{step_id}.png", language)
        
        # Get instructions in appropriate language
        instructions_key = f'instructions_{language}'
        instructions = step_visual.get(instructions_key, step_visual.get('instructions_en', ''))
        
        return {
            "has_visual": True,
            "image_url": annotated_image_url,
            "instructions": instructions,
            "mockup_type": mockup_type,
            "mockup_step": mockup_step
        }
    
    def generate_all_visual_guides(self):
        """Pre-generate all Oracle EBS visual guides"""
        
        print("Generating Oracle EBS R12 visual guides...")
        
        # First generate all Oracle EBS mockups
        oracle_mockup_generator.generate_all_mockups()
        
        # Then generate annotated versions
        for procedure_id, steps in self.visual_instructions.items():
            for step_id, step_data in steps.items():
                mockup_type = step_data.get('mockup_type')
                mockup_step = step_data.get('mockup_step', '')
                click_areas = step_data.get('click_areas', [])
                
                if mockup_type:
                    # Generate annotated Oracle mockups for both languages
                    self.create_annotated_oracle_mockup(mockup_type, mockup_step, click_areas, 'fr')
                    self.create_annotated_oracle_mockup(mockup_type, mockup_step, click_areas, 'en')
                else:
                    # Fallback for missing mockup types
                    self.create_placeholder_image(f"{procedure_id}_{step_id}.png", 'fr')
                    self.create_placeholder_image(f"{procedure_id}_{step_id}.png", 'en')
        
        print("All Oracle EBS R12 visual guides generated successfully!")

# Initialize the enhanced visual guide generator
enhanced_visual_guide_generator = EnhancedVisualGuideGenerator()