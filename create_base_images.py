#!/usr/bin/env python3
"""
Create base images for Oracle EBS procedures
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_base_images():
    """Create simple base images for Oracle EBS procedures"""
    
    images_path = os.path.join("static", "images")
    os.makedirs(images_path, exist_ok=True)
    
    # Define images to create
    images_to_create = {
        "rfq_review.png": {
            "title": "RFQ Review Screen",
            "elements": [
                {"text": "RFQ Details", "pos": (100, 120), "type": "section"},
                {"text": "Technical Specifications", "pos": (100, 200), "type": "section"},
                {"text": "Evaluation Criteria", "pos": (100, 280), "type": "section"}
            ]
        },
        "quotation_prep.png": {
            "title": "Quotation Preparation",
            "elements": [
                {"text": "Unit Price: [____]", "pos": (100, 150), "type": "input"},
                {"text": "Total Amount: [____]", "pos": (100, 190), "type": "input"},
                {"text": "Delivery Date: [____]", "pos": (100, 230), "type": "input"},
                {"text": "☐ Technical Compliance", "pos": (100, 270), "type": "checkbox"}
            ]
        },
        "quotation_submit.png": {
            "title": "Submit Quotation",
            "elements": [
                {"text": "Review your quotation details", "pos": (100, 150), "type": "text"},
                {"text": "[Submit Quotation]", "pos": (300, 350), "type": "button"}
            ]
        },
        "login_screen.png": {
            "title": "i-Supplier Login",
            "elements": [
                {"text": "Username: [____]", "pos": (200, 200), "type": "input"},
                {"text": "Password: [____]", "pos": (200, 250), "type": "input"},
                {"text": "[Login]", "pos": (250, 300), "type": "button"}
            ]
        },
        "navigate_confirmations.png": {
            "title": "Navigation Menu",
            "elements": [
                {"text": "[Procurement]", "pos": (100, 100), "type": "button"},
                {"text": "Work Confirmations", "pos": (200, 150), "type": "menu"}
            ]
        },
        "create_confirmation.png": {
            "title": "Work Confirmations",
            "elements": [
                {"text": "[Create]", "pos": (100, 80), "type": "button"}
            ]
        },
        "select_po.png": {
            "title": "Select Purchase Order",
            "elements": [
                {"text": "PO Number: [____]", "pos": (200, 150), "type": "input"},
                {"text": "[Search]", "pos": (350, 150), "type": "button"},
                {"text": "☐ PO-2024-001", "pos": (200, 200), "type": "checkbox"}
            ]
        },
        "confirmation_details.png": {
            "title": "Confirmation Details",
            "elements": [
                {"text": "Quantity: [____]", "pos": (200, 180), "type": "input"},
                {"text": "Date: [____]", "pos": (200, 220), "type": "input"},
                {"text": "Notes: [____]", "pos": (200, 260), "type": "textarea"}
            ]
        },
        "review_submit.png": {
            "title": "Review and Submit",
            "elements": [
                {"text": "Review all details above", "pos": (200, 300), "type": "text"},
                {"text": "[Submit]", "pos": (350, 400), "type": "button"}
            ]
        }
    }
    
    for filename, config in images_to_create.items():
        create_single_image(os.path.join(images_path, filename), config)
    
    print(f"Created {len(images_to_create)} base images in {images_path}")

def create_single_image(filepath, config):
    """Create a single base image"""
    
    # Create image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_text = ImageFont.truetype("arial.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
    
    # Draw title
    title = config["title"]
    draw.text((50, 30), title, fill='black', font=font_title)
    
    # Draw border
    draw.rectangle([20, 20, 780, 580], outline='gray', width=2)
    
    # Draw elements
    for element in config["elements"]:
        text = element["text"]
        pos = element["pos"]
        elem_type = element["type"]
        
        if elem_type == "button":
            # Draw button
            bbox = draw.textbbox((0, 0), text, font=font_text)
            width = bbox[2] - bbox[0] + 20
            height = bbox[3] - bbox[1] + 10
            draw.rectangle([pos[0]-10, pos[1]-5, pos[0]+width, pos[1]+height], 
                         outline='blue', fill='lightblue', width=2)
            draw.text(pos, text, fill='black', font=font_text)
        elif elem_type == "input":
            # Draw input field
            draw.rectangle([pos[0]+100, pos[1]-2, pos[0]+250, pos[1]+18], 
                         outline='gray', fill='white', width=1)
            draw.text(pos, text, fill='black', font=font_text)
        elif elem_type == "section":
            # Draw section header
            draw.rectangle([pos[0]-5, pos[1]-5, pos[0]+300, pos[1]+25], 
                         outline='green', fill='lightgreen', width=1)
            draw.text(pos, text, fill='black', font=font_text)
        else:
            # Regular text
            draw.text(pos, text, fill='black', font=font_text)
    
    # Save image
    img.save(filepath, 'PNG')

if __name__ == "__main__":
    create_base_images()