#--------------------------------------------------------------------------------
# MODULE: image_cropper.py
# BY: Benjamin Pieczynski
# 2024-04-08
#
# PURPOSE:
#   Crops images to have even dimensions
#--------------------------------------------------------------------------------

# imports
from PIL import Image
import os
import argparse
from PIL import Image

def adjust_dimensions(image_path, method='crop'):
    """Adjust the image dimensions to be even."""
    with Image.open(image_path) as img:
        width, height = img.size
        
        new_width = width if width % 2 == 0 else width - 1
        new_height = height if height % 2 == 0 else height - 1
        
        if method == 'crop':
            cropped_image = img.crop((0, 0, new_width, new_height))
            cropped_image.save(image_path)
        elif method == 'resize':
            resized_image = img.resize((new_width, new_height))
            resized_image.save(image_path)

def process_images(images, method):
    """Process a list of images."""
    for image_path in images:
        adjust_dimensions(image_path, method)

def find_images_in_directory(directory: str) -> list:
    """Find valid image files in a directory."""
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(valid_extensions)]

def create_image_list(directory: str, files: list) -> list:
    """
    Builds image list for the case that the files and directory are provided

    Args:
        directory (str): search directory
        files (list): user provided files

    Returns:
        images (list): list of files to crop
    """
    images = []
    for file in files:
        images.append(os.path.join(directory,file))
    return images

def main():
    description = """Program to crop or resize image dimmensions for the purpose of working with the ips animator program."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-d", "--directory", help="Directory containing images.")
    parser.add_argument("-f", "--files", nargs='+', help="File names. (use -d to specify directory)")
    parser.add_argument("-m", "--method", choices=['crop', 'resize'], default='crop', help="Method to adjust dimensions: crop or resize.")
    
    args = parser.parse_args()

    if args.directory and args.files:
        create_image_list(args.directory, args.files)
    elif args.directory:
        images = find_images_in_directory(args.directory)
    else:
        images = args.files

    process_images(images, args.method)

if __name__ == "__main__":
    main()