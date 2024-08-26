import os
from PIL import Image, ImageEnhance, ImageStat

def auto_adjustments(image):
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    brightness = stat.mean[0]
    contrast = stat.stddev[0]
    
    # Dynamic exposure adjustment
    if brightness < 100:
        exposure_factor = 1.1
    elif 100 <= brightness < 150:
        exposure_factor = 1.05
    else:
        exposure_factor = 0.9
    
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(exposure_factor)
    
    if contrast < 40:
        contrast_factor = 1.1
    elif 40 <= contrast < 70:
        contrast_factor = 1.05
    else:
        contrast_factor = 1.0
    
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)
    
    # Adjust highlights and shadows
    grayscale = image.convert("L")
    highlights_mask = grayscale.point(lambda p: p > 200 and 255)
    shadows_mask = grayscale.point(lambda p: p < 50 and 255)
    
    highlights = ImageEnhance.Brightness(image).enhance(0.95)
    shadows = ImageEnhance.Brightness(image).enhance(1.05)
    
    image = Image.composite(highlights, image, highlights_mask)
    image = Image.composite(shadows, image, shadows_mask)
    
    # Increase overall shadows by 20%
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2)
    
    # Dynamic vibrance adjustment
    stat = ImageStat.Stat(image)
    vibrance = sum(stat.stddev) / len(stat.stddev)
    
    if vibrance < 30:
        vibrancy = 1.2
    elif 30 <= vibrance < 50:
        vibrancy = 1.1
    else:
        vibrancy = 1.0
    
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(vibrancy)
    
    return image

def edit_photos(folder):
    edited_folder = os.path.join(folder, 'edited')
    os.makedirs(edited_folder, exist_ok=True)
    for file in os.listdir(folder):
        if file.endswith('.JPG'):
            image = Image.open(os.path.join(folder, file))
            image = auto_adjustments(image)
            image.save(os.path.join(edited_folder, file))
    

photos = input("Enter the folder path containing the photos: ")
edit_photos(photos)
print("All photos have been edited and saved in the 'edited' folder.")
