#!/usr/bin/env python3
from PIL import Image
import os

INPUT_PATH = './images'
OUTPUT_PATH = './output'

# TODO multiprocessing
# TODO sys.argv or argparse
# TODO refactor function definitions
# TODO improve docstring documentation

def batch_process_images(input_path, output_path):
    """Get image files from input_path, rotate each one 90 degrees counter clockwise,
    resize it to (128, 128) JPEG, and save it to output_path """
    for root, dirs, files in os.walk(input_path):
        for f in files:
            if f != '.DS_Store':
                # get the original image or icon
                img_path = os.path.join(root,f)
                img = Image.open(img_path)

                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # new settings
                rotation = 90
                new_size = (128, 128)
                format = 'jpeg'

                #rotate and resize
                new_img = img.rotate(90).resize(new_size)

                # save the file
                output_file = os.path.join(output_path, f)
                print("Saving new file in {} as {}".format(output_file, format))
                new_img.save(output_file, format)

if __name__ == "__main__":

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    batch_process_images(INPUT_PATH, OUTPUT_PATH)
