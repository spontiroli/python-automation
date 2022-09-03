#!/usr/bin/env python3

# TODO 
# - Input folder is located at '~/supplier-data/images'
# - Change image resolution from 3000x2000 to 600x400 pixels
# - Change from .TIFF to .JPEG format

# NOTES
# Use convert('RGB')
# Save images to the same path, with JPEG extension

import os
from PIL import Image

def process_images(path, resolution, format, extension):
    files = os.listdir(path)
    for image in files:
        image_path = os.path.join(path, image)
        image_name, image_extension = os.path.splitext(image)

        if os.path.isfile(image_path):

            if image_extension == '.tiff':
                current_image = Image.open(image_path)

                if current_image.mode != 'RGB':
                    current_image = current_image.convert('RGB')

                # let's change the resolution
                current_image = current_image.resize(resolution)

                # let's change the format and save the image as JPEG
                new_filename = ''.join([image_name, extension.lower()])
                output_path = os.path.join(path, new_filename)

                current_image.save(output_path, format)
                print('Saved {} as {}'.format(new_filename, output_path))


if __name__ == '__main__':

    home = os.path.expanduser('~')
    supplier_images = 'supplier-data/images'
    full_path = os.path.join(home, supplier_images)

    resolution = (600, 400)
    format = 'JPEG'
    extension = '.JPEG'

    process_images(full_path, resolution, format, extension)
