#!/usr/bin/env python3
"""
Test image access and create a simple test image
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    """Create a simple test image"""
    
    # Create test image
    img = Image.new('RGB', (600, 400), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Draw test content
    draw.text((50, 50), "Oracle EBS Visual Guide", fill='black', font=font)
    draw.text((50, 100), "Step 1: Login to i-Supplier", fill='black', font=font)
    
    # Draw red circle
    draw.ellipse([200, 150, 250, 200], outline='red', width=3)
    draw.text((210, 165), "1", fill='red', font=font)
    
    # Save test image
    test_path = os.path.join("static", "images", "annotated", "test_image.png")
    os.makedirs(os.path.dirname(test_path), exist_ok=True)
    img.save(test_path, 'PNG')
    
    print(f"Test image created: {test_path}")
    return test_path

if __name__ == "__main__":
    create_test_image()