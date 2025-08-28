from PIL import Image, ImageDraw, ImageFont
import os
from typing import Dict, List, Tuple, Optional
import json
from .oracle_ebs_mockup_generator import oracle_mockup_generator

class VisualGuideGenerator:
    """Generate annotated screenshots with red circles and arrows for Oracle EBS procedures"""
    
    def __init__(self):
        self.base_images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "images")
        self.annotated_images_path = os.path.join(self.base_images_path, "annotated")
        
        # Create annotated directory if it doesn't exist
        os.makedirs(self.annotated_images_path, exist_ok=True)
        
        # Define click coordinates for each procedure step
        self.click_coordinates = {
            "login_screen.png": [
                {"x": 400, "y": 200, "label": "Username", "type": "input"},
                {"x": 400, "y": 250, "label": "Password", "type": "input"},
                {"x": 400, "y": 300, "label": "Login", "type": "button"}
            ],
            "navigate_confirmations.png": [
                {"x": 150, "y": 100, "label": "Procurement", "type": "menu"},
                {"x": 250, "y": 150, "label": "Work Confirmations", "type": "submenu"}
            ],
            "create_confirmation.png": [
                {"x": 100, "y": 80, "label": "Create", "type": "button"}
            ],
            "select_po.png": [
                {"x": 300, "y": 150, "label": "Search PO", "type": "input"},
                {"x": 450, "y": 150, "label": "Search", "type": "button"},
                {"x": 200, "y": 200, "label": "Select PO", "type": "checkbox"}
            ],
            "confirmation_details.png": [
                {"x": 200, "y": 180, "label": "Quantity", "type": "input"},
                {"x": 200, "y": 220, "label": "Completion Date", "type": "date"},
                {"x": 200, "y": 260, "label": "Notes", "type": "textarea"}
            ],
            "review_submit.png": [
                {"x": 350, "y": 400, "label": "Submit", "type": "button"}
            ],
            # RFQ Response coordinates
            "rfq_review.png": [
                {"x": 300, "y": 120, "label": "RFQ Details", "type": "section"},
                {"x": 300, "y": 200, "label": "Technical Specs", "type": "section"},
                {"x": 300, "y": 280, "label": "Evaluation Criteria", "type": "section"}
            ],
            "quotation_prep.png": [
                {"x": 200, "y": 150, "label": "Unit Price", "type": "input"},
                {"x": 200, "y": 190, "label": "Total Amount", "type": "input"},
                {"x": 200, "y": 230, "label": "Delivery Date", "type": "date"},
                {"x": 200, "y": 270, "label": "Technical Compliance", "type": "checkbox"}
            ],
            "quotation_submit.png": [
                {"x": 350, "y": 350, "label": "Submit Quotation", "type": "button"}
            ],
            # Add more coordinates for other procedures...
        }
        
        # Define step-by-step instructions with visual cues
        self.visual_instructions = {
            "work_confirmation": {
                "login": {
                    "image": "login_screen.png",
                    "instructions_fr": "1. Saisissez votre nom d'utilisateur\n2. Saisissez votre mot de passe\n3. Cliquez sur 'Connexion'",
                    "instructions_en": "1. Enter your username\n2. Enter your password\n3. Click 'Login'"
                },
                "navigate_to_confirmations": {
                    "image": "navigate_confirmations.png", 
                    "instructions_fr": "1. Cliquez sur 'Approvisionnement' dans le menu\n2. Sélectionnez 'Confirmations de Travail'",
                    "instructions_en": "1. Click 'Procurement' in the menu\n2. Select 'Work Confirmations'"
                },
                "create_new_confirmation": {
                    "image": "create_confirmation.png",
                    "instructions_fr": "Cliquez sur le bouton 'Créer' pour commencer",
                    "instructions_en": "Click the 'Create' button to start"
                },
                "select_purchase_order": {
                    "image": "select_po.png",
                    "instructions_fr": "1. Recherchez votre commande d'achat\n2. Cliquez sur 'Rechercher'\n3. Sélectionnez la commande appropriée",
                    "instructions_en": "1. Search for your purchase order\n2. Click 'Search'\n3. Select the appropriate order"
                },
                "enter_confirmation_details": {
                    "image": "confirmation_details.png",
                    "instructions_fr": "1. Saisissez la quantité confirmée\n2. Sélectionnez la date d'achèvement\n3. Ajoutez des notes si nécessaire",
                    "instructions_en": "1. Enter confirmed quantity\n2. Select completion date\n3. Add notes if needed"
                },
                "review_and_submit": {
                    "image": "review_submit.png",
                    "instructions_fr": "Vérifiez tous les détails et cliquez sur 'Soumettre'",
                    "instructions_en": "Review all details and click 'Submit'"
                }
            },
            "rfq_response": {
                "rfq_review": {
                    "image": "rfq_review.png",
                    "instructions_fr": "1. Examinez les détails de l'appel d'offres\n2. Lisez les spécifications techniques\n3. Comprenez les critères d'évaluation",
                    "instructions_en": "1. Review RFQ details\n2. Read technical specifications\n3. Understand evaluation criteria"
                },
                "prepare_quotation": {
                    "image": "quotation_prep.png",
                    "instructions_fr": "1. Saisissez le prix unitaire\n2. Calculez le montant total\n3. Indiquez la date de livraison\n4. Confirmez la conformité technique",
                    "instructions_en": "1. Enter unit price\n2. Calculate total amount\n3. Specify delivery date\n4. Confirm technical compliance"
                },
                "submit_quotation": {
                    "image": "quotation_submit.png",
                    "instructions_fr": "Vérifiez votre cotation et cliquez sur 'Soumettre la Cotation'",
                    "instructions_en": "Review your quotation and click 'Submit Quotation'"
                }
            }
        }
    
    def create_annotated_image(self, base_image_name: str, language: str = 'fr') -> str:
        """Create an annotated version of the base image with red circles and instructions"""
        
        base_image_path = os.path.join(self.base_images_path, base_image_name)
        annotated_image_name = f"annotated_{language}_{base_image_name}"
        annotated_image_path = os.path.join(self.annotated_images_path, annotated_image_name)
        
        # If annotated image already exists, return its path
        if os.path.exists(annotated_image_path):
            return f"/static/images/annotated/{annotated_image_name}"
        
        # Create a placeholder image if base image doesn't exist
        if not os.path.exists(base_image_path):
            return self.create_placeholder_image(base_image_name, language)
        
        try:
            # Open the base image
            with Image.open(base_image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create a copy for annotation
                annotated_img = img.copy()
                draw = ImageDraw.Draw(annotated_img)
                
                # Get coordinates for this image
                coordinates = self.click_coordinates.get(base_image_name, [])
                
                # Draw red circles and labels
                for i, coord in enumerate(coordinates):
                    x, y = coord['x'], coord['y']
                    label = coord['label']
                    
                    # Draw red circle
                    circle_radius = 25
                    draw.ellipse([x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius], 
                               outline='red', width=3)
                    
                    # Draw step number in circle
                    try:
                        font = ImageFont.truetype("arial.ttf", 16)
                    except:
                        font = ImageFont.load_default()
                    
                    step_num = str(i + 1)
                    bbox = draw.textbbox((0, 0), step_num, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    draw.text((x - text_width//2, y - text_height//2), step_num, 
                             fill='red', font=font)
                    
                    # Draw label with background
                    label_y = y + circle_radius + 10
                    label_bbox = draw.textbbox((0, 0), label, font=font)
                    label_width = label_bbox[2] - label_bbox[0]
                    
                    # Background rectangle for label
                    draw.rectangle([x - label_width//2 - 5, label_y - 5, 
                                  x + label_width//2 + 5, label_y + 20], 
                                 fill='white', outline='red')
                    
                    # Label text
                    draw.text((x - label_width//2, label_y), label, fill='red', font=font)
                
                # Save annotated image
                annotated_img.save(annotated_image_path, 'PNG')
                
                return f"/static/images/annotated/{annotated_image_name}"
                
        except Exception as e:
            print(f"Error creating annotated image: {e}")
            return self.create_placeholder_image(base_image_name, language)
    
    def create_placeholder_image(self, base_image_name: str, language: str = 'fr') -> str:
        """Create a placeholder image with instructions when base image is not available"""
        
        placeholder_name = f"placeholder_{language}_{base_image_name}"
        placeholder_path = os.path.join(self.annotated_images_path, placeholder_name)
        
        # Create a simple placeholder image
        img = Image.new('RGB', (800, 600), color='lightgray')
        draw = ImageDraw.Draw(img)
        
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Title
        title = "Guide Visuel Oracle EBS" if language == 'fr' else "Oracle EBS Visual Guide"
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text((400 - title_width//2, 50), title, fill='black', font=font_large)
        
        # Instructions
        instructions = [
            "Étapes à suivre :" if language == 'fr' else "Steps to follow:",
            "1. Connectez-vous au portail i-Supplier" if language == 'fr' else "1. Login to i-Supplier portal",
            "2. Naviguez vers la section appropriée" if language == 'fr' else "2. Navigate to appropriate section", 
            "3. Suivez les instructions à l'écran" if language == 'fr' else "3. Follow on-screen instructions",
            "4. Complétez et soumettez" if language == 'fr' else "4. Complete and submit"
        ]
        
        y_pos = 150
        for instruction in instructions:
            draw.text((50, y_pos), instruction, fill='black', font=font_small)
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
        
        # Get base image name
        base_image = step_visual.get('image', 'placeholder.png')
        
        # Create annotated image
        annotated_image_url = self.create_annotated_image(base_image, language)
        
        # Get instructions in appropriate language
        instructions_key = f'instructions_{language}'
        instructions = step_visual.get(instructions_key, step_visual.get('instructions_en', ''))
        
        return {
            "has_visual": True,
            "image_url": annotated_image_url,
            "instructions": instructions,
            "base_image": base_image
        }
    
    def generate_all_visual_guides(self):
        """Pre-generate all visual guides for better performance"""
        
        for procedure_id, steps in self.visual_instructions.items():
            for step_id, step_data in steps.items():
                base_image = step_data.get('image', 'placeholder.png')
                
                # Generate for both languages
                self.create_annotated_image(base_image, 'fr')
                self.create_annotated_image(base_image, 'en')
        
        print("All visual guides generated successfully!")

# Initialize the visual guide generator
visual_guide_generator = VisualGuideGenerator()