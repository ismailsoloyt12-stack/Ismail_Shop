"""
Create default placeholder images for the app store
This script creates basic placeholder images for testing
"""

import os
from pathlib import Path

def create_placeholder_images():
    """Create placeholder images using PIL if available, otherwise create empty files"""
    
    # Define directories
    STATIC_DIR = Path("static")
    IMAGES_DIR = STATIC_DIR / "images"
    APP_ICONS_DIR = IMAGES_DIR / "app_icons"
    APP_BANNERS_DIR = IMAGES_DIR / "app_banners"
    SCREENSHOTS_DIR = IMAGES_DIR / "screenshots"
    
    # Create directories
    for directory in [APP_ICONS_DIR, APP_BANNERS_DIR, SCREENSHOTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create default icon (512x512)
        icon = Image.new('RGB', (512, 512), color='#4285F4')
        draw = ImageDraw.Draw(icon)
        
        # Draw a simple app icon placeholder
        draw.rectangle([100, 100, 412, 412], fill='white')
        draw.text((256, 256), "APP", fill='#4285F4', anchor="mm")
        
        icon_path = APP_ICONS_DIR / "default_icon.png"
        icon.save(icon_path)
        print(f"✅ Created: {icon_path}")
        
        # Create default banner (1024x500)
        banner = Image.new('RGB', (1024, 500), color='#34A853')
        draw = ImageDraw.Draw(banner)
        draw.rectangle([50, 50, 974, 450], fill='white')
        draw.text((512, 250), "APP BANNER", fill='#34A853', anchor="mm")
        
        banner_path = APP_BANNERS_DIR / "default_banner.jpg"
        banner.save(banner_path, 'JPEG')
        print(f"✅ Created: {banner_path}")
        
        # Create sample screenshots (720x1280 - typical phone size)
        for i in range(1, 4):
            screenshot = Image.new('RGB', (720, 1280), color='#EA4335')
            draw = ImageDraw.Draw(screenshot)
            draw.rectangle([20, 20, 700, 1260], fill='white')
            draw.text((360, 640), f"SCREENSHOT {i}", fill='#EA4335', anchor="mm")
            
            screenshot_path = SCREENSHOTS_DIR / f"screenshot{i}.png"
            screenshot.save(screenshot_path)
            print(f"✅ Created: {screenshot_path}")
        
        # Create preview photos
        for i in range(1, 4):
            preview = Image.new('RGB', (1080, 1920), color='#FBBC04')
            draw = ImageDraw.Draw(preview)
            draw.rectangle([40, 40, 1040, 1880], fill='white')
            draw.text((540, 960), f"PREVIEW {i}", fill='#FBBC04', anchor="mm")
            
            preview_path = SCREENSHOTS_DIR / f"preview{i}.png"
            preview.save(preview_path)
            print(f"✅ Created: {preview_path}")
        
        print("\n✅ All placeholder images created successfully!")
        print("\nYou can now:")
        print("1. Replace these with your actual app images")
        print("2. Use them as templates for your app icons and screenshots")
        
    except ImportError:
        print("PIL/Pillow not installed. Installing...")
        import subprocess
        import sys
        
        # Try to install Pillow
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            print("\n✅ Pillow installed successfully!")
            print("Please run this script again to create the images.")
        except:
            print("\n⚠️ Could not install Pillow automatically.")
            print("\nTo create placeholder images, please:")
            print("1. Install Pillow: pip install Pillow")
            print("2. Run this script again")
            print("\nAlternatively, manually add images to these folders:")
            print(f"  - App Icons: {APP_ICONS_DIR}")
            print(f"  - Banners: {APP_BANNERS_DIR}")
            print(f"  - Screenshots: {SCREENSHOTS_DIR}")
            
            # Create empty placeholder files as fallback
            print("\nCreating empty placeholder files...")
            
            # Create directories
            for directory in [APP_ICONS_DIR, APP_BANNERS_DIR, SCREENSHOTS_DIR]:
                directory.mkdir(parents=True, exist_ok=True)
            
            # Create empty files
            (APP_ICONS_DIR / "default_icon.png").touch()
            (APP_BANNERS_DIR / "default_banner.jpg").touch()
            
            for i in range(1, 4):
                (SCREENSHOTS_DIR / f"screenshot{i}.png").touch()
                (SCREENSHOTS_DIR / f"preview{i}.png").touch()
            
            print("✅ Empty placeholder files created.")
            print("Note: These are empty files. Replace them with actual images!")

if __name__ == "__main__":
    print("="*60)
    print("   DEFAULT IMAGE CREATOR FOR APP STORE")
    print("="*60)
    print()
    create_placeholder_images()
    print()
    input("Press Enter to exit...")
