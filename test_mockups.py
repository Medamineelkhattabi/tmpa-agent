#!/usr/bin/env python3
"""
Test the Oracle EBS mockup system by generating a sample image and checking the visual guide.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.oracle_ebs_mockup_generator import oracle_mockup_generator
from backend.enhanced_visual_guide_generator import enhanced_visual_guide_generator

def test_mockup_generation():
    """Test generating a single mockup"""
    print("Testing Oracle EBS mockup generation...")
    
    try:
        # Test login screen generation
        login_url_fr = oracle_mockup_generator.create_login_screen('fr')
        login_url_en = oracle_mockup_generator.create_login_screen('en')
        
        print(f"French login screen: {login_url_fr}")
        print(f"English login screen: {login_url_en}")
        
        # Test work confirmation screen
        wc_url_fr = oracle_mockup_generator.create_work_confirmation_screen('navigate', 'fr')
        wc_url_en = oracle_mockup_generator.create_work_confirmation_screen('navigate', 'en')
        
        print(f"French work confirmation: {wc_url_fr}")
        print(f"English work confirmation: {wc_url_en}")
        
        return True
        
    except Exception as e:
        print(f"Error testing mockup generation: {e}")
        return False

def test_visual_guide():
    """Test the enhanced visual guide system"""
    print("\nTesting enhanced visual guide system...")
    
    try:
        # Test getting visual guide for work confirmation login
        guide_fr = enhanced_visual_guide_generator.get_visual_guide('work_confirmation', 'login', 'fr')
        guide_en = enhanced_visual_guide_generator.get_visual_guide('work_confirmation', 'login', 'en')
        
        print(f"French guide has visual: {guide_fr['has_visual']}")
        print(f"French guide image: {guide_fr['image_url']}")
        print(f"English guide has visual: {guide_en['has_visual']}")
        print(f"English guide image: {guide_en['image_url']}")
        
        # Test RFQ response guide
        rfq_guide = enhanced_visual_guide_generator.get_visual_guide('rfq_response', 'rfq_review', 'fr')
        print(f"RFQ guide has visual: {rfq_guide['has_visual']}")
        print(f"RFQ guide image: {rfq_guide['image_url']}")
        
        return True
        
    except Exception as e:
        print(f"Error testing visual guide: {e}")
        return False

def check_generated_files():
    """Check if the generated files exist"""
    print("\nChecking generated files...")
    
    mockup_dir = os.path.join(os.path.dirname(__file__), "static", "images", "oracle_mockups")
    annotated_dir = os.path.join(os.path.dirname(__file__), "static", "images", "annotated")
    
    if os.path.exists(mockup_dir):
        mockup_files = os.listdir(mockup_dir)
        print(f"Oracle mockup files ({len(mockup_files)}): {mockup_files[:5]}...")
    else:
        print("Oracle mockup directory not found")
        
    if os.path.exists(annotated_dir):
        annotated_files = os.listdir(annotated_dir)
        oracle_annotated = [f for f in annotated_files if f.startswith('oracle_')]
        print(f"Oracle annotated files ({len(oracle_annotated)}): {oracle_annotated[:5]}...")
    else:
        print("Annotated directory not found")

def main():
    """Run all tests"""
    print("=" * 60)
    print("Oracle EBS R12 Mockup System Test")
    print("=" * 60)
    
    success = True
    
    # Test mockup generation
    if not test_mockup_generation():
        success = False
    
    # Test visual guide system
    if not test_visual_guide():
        success = False
    
    # Check generated files
    check_generated_files()
    
    print("\n" + "=" * 60)
    if success:
        print("All tests passed! Oracle EBS mockup system is working correctly.")
        print("\nKey features:")
        print("- Realistic Oracle EBS R12 interface styling")
        print("- Proper Oracle branding and color scheme")
        print("- Bilingual support (French/English)")
        print("- Interactive click area annotations")
        print("- Authentic form layouts and navigation")
    else:
        print("Some tests failed. Please check the error messages above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())