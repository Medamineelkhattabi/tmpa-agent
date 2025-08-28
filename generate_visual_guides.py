#!/usr/bin/env python3
"""
Script to generate all visual guides with annotated screenshots
Run this script to create annotated images with red circles for all procedures
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.visual_guide_generator import visual_guide_generator

def main():
    print("Generating visual guides for Oracle EBS procedures...")
    print("Creating annotated screenshots with red circles and instructions...")
    
    try:
        # Generate all visual guides
        visual_guide_generator.generate_all_visual_guides()
        
        print("Visual guides generated successfully!")
        print(f"Images saved in: {visual_guide_generator.annotated_images_path}")
        print("\nGenerated guides include:")
        print("   - Work Confirmation procedure")
        print("   - RFQ Response procedure") 
        print("   - Invoice Submission procedure")
        print("   - All other Oracle EBS procedures")
        print("\nAvailable in both French and English")
        print("Each image includes red circles showing where to click")
        print("Step-by-step instructions overlay")
        
    except Exception as e:
        print(f"Error generating visual guides: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())