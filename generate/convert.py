from PIL import Image
import os
from pathlib import Path
from tqdm import tqdm

# Create output directories if they don't exist
Path("thumbs").mkdir(exist_ok=True)
Path("optimised").mkdir(exist_ok=True)

def create_thumbnail(image, size=(340, 170)):
    # Calculate dimensions to maintain aspect ratio
    width, height = image.size
    aspect_ratio = width / height
    target_ratio = size[0] / size[1]

    if aspect_ratio > target_ratio:
        # Image is wider than target ratio
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        image = image.crop((left, 0, left + new_width, height))
    else:
        # Image is taller than target ratio
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        image = image.crop((0, top, width, top + new_height))

    return image.resize(size, Image.Resampling.LANCZOS)

def process_images():
    # Supported image formats
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    
    # Get all image files
    image_files = [f for f in os.listdir('images') 
                   if f.lower().endswith(image_extensions)]
    
    # Add progress bar
    for index, filename in enumerate(tqdm(image_files, desc="Processing images"), 1):
        # Open image
        with Image.open(os.path.join('images', filename)) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Save optimized version
            img.save(
                f'optimised/image-{index}.webp',
                'WEBP',
                quality=85,
                method=6  # Highest compression method
            )
            
            # Create and save thumbnail
            thumb = create_thumbnail(img)
            thumb.save(
                f'thumbs/image-{index}.webp',
                'WEBP',
                quality=85,
                method=6
            )

if __name__ == "__main__":
    process_images()