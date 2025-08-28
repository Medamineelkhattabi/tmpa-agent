#!/usr/bin/env python3
"""
Generate realistic Oracle EBS R12 interface mockups for the visual guide system.
This script creates authentic-looking Oracle EBS screenshots with proper styling.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.oracle_ebs_mockup_generator import oracle_mockup_generator
from backend.enhanced_visual_guide_generator import enhanced_visual_guide_generator

def main():
    """Generate all Oracle EBS mockups and visual guides"""
    
    print("Starting Oracle EBS R12 Mockup Generation...")
    print("=" * 60)
    
    try:
        # Generate all Oracle EBS mockup screens
        print("Generating Oracle EBS R12 interface mockups...")
        oracle_mockup_generator.generate_all_mockups()
        print("Oracle EBS mockups generated successfully!")
        
        # Generate all enhanced visual guides with annotations
        print("\nGenerating enhanced visual guides with annotations...")
        enhanced_visual_guide_generator.generate_all_visual_guides()
        print("Enhanced visual guides generated successfully!")
        
        print("\n" + "=" * 60)
        print("All Oracle EBS R12 mockups and visual guides generated!")
        print("\nGenerated files:")
        print("Oracle Mockups: /static/images/oracle_mockups/")
        print("Annotated Guides: /static/images/annotated/")
        print("\nFeatures:")
        print("- Realistic Oracle EBS R12 interface styling")
        print("- Proper Oracle color scheme and branding")
        print("- Bilingual support (French/English)")
        print("- Interactive click area annotations")
        print("- Step-by-step visual guidance")
        print("- Authentic form layouts and navigation")
        
    except Exception as e:
        print(f"Error generating mockups: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())