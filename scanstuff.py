#! /usr/bin/env python3
#
# For usage type
# python3 scanstuff.py --help
# example:
# python3 scanstuff.py -f filename -t 20 -b 20 -m 20 -w 2400 -i
#
# Giuseppe A. Marzo
# 30 October 2024
#
# v 20241030
# First working version
#

# Importing the libraries
import cv2
import sys
import os
import glob
import argparse
import numpy as np
from PIL import Image
# import matplotlib.pyplot as plt
from pdf2image import convert_from_path


# Define parser
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-f', '--file', help='Name of the PDF file to be processed')
parser.add_argument('-d', '--double', default=False, action='store_true', help='Double page for scanned image')
parser.add_argument('-t', '--top', default=20, help='Pixels to be cropped on top margin')
parser.add_argument('-b', '--bottom', default=20, help='Pixels to be cropped on bottom margin')
parser.add_argument('-m', '--margin', default=30, help='Pixels to be cropped on inner margin (if double) or right margin (if single)')
parser.add_argument('-w', '--width', default=0, help='Page width in pixel')
parser.add_argument('-i', '--improve', default=False, action='store_true', help='Makes some magic')

# More parser stuff
args = vars(parser.parse_args())
pdf_path = str(args['file'])
double = args['double']
top = int(args['top'])
bottom = int(args['bottom'])
margin = int(args['margin'])
width = int(args['width'])
improve = args['improve']


print('Reading '+pdf_path+'.pdf')

# Convert each page to PIL image
pages = convert_from_path(pdf_path+'.pdf', dpi=300)

# Save each page into temporary PNG
for i, page in enumerate(pages):
    page.save(f'page_{i+1}_original.png', 'PNG')

print('Working on pages')
for i in range(len(glob.glob('*_original.png'))):
    original_image = cv2.imread(f'page_{i+1}_original.png')  # Load RGB page in PNG format
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)   # Convert to grayscale
    gray_size = int(gray_image.shape[1])
    if (width == 0):
        width = gray_size    # In case width is not specified use the full page width

    # Split page if double is true based on finding the middle darkness minimum
    if double == True:
        darkness = np.empty(gray_size)
        for ic in range(gray_size):
            darkness[ic] = np.sum(np.abs(gray_image[:, ic]))
            min_middle_val = np.min(darkness[int(gray_size*0.33):int(gray_size*0.66)])
        middle_index = np.where(darkness == min_middle_val)
        # print(i+1, min_middle_val, middle_index)
        if len(middle_index) == 1:
            middle_index = int(middle_index[0][0])
        else:
            middle_index = int(width / 2.)
        # Plot the sum of the column pixel values against rows
        # plt.plot(darkness)
        # plt.show()

        odd_page  = original_image[:, :middle_index]
        even_page = original_image[:, middle_index+1:]

        odd_page = odd_page[top:-(bottom+1), -(width+margin+1):-(margin+1)]
        even_page = even_page[top:-(bottom+1), margin:(margin+width)]
        # print(odd_page.shape, even_page.shape)

        # Save images
        even_img_path = f'page_{int((i+1)*2.)}_untouched.png'
        cv2.imwrite(even_img_path, even_page)
        odd_img_path = f'page_{int((i+1)*2.-1.)}_untouched.png'
        cv2.imwrite(odd_img_path, odd_page)

    if double == False:
        single_page = original_image[top:-(bottom+1), margin:(margin+width)]

        # Save image
        single_img_path = f'page_{int(i+1)}_untouched.png'
        cv2.imwrite(single_img_path, single_page)

    # Remove unneeded file
    os.remove(f'page_{i+1}_original.png')

# Some cleaning
# for f in glob.glob('*_original.png'):
#     os.remove(f)

for i in range(len(glob.glob('*_untouched.png'))):
    image = cv2.imread(f'page_{i+1}_untouched.png')  # Load RGB page in PNG format

    if improve == True:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)  # Gaussian blur to reduce noise
        _, mask = cv2.threshold(blur_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   # Otsu threshold
        image = cv2.addWeighted(gray_image, 0.6, mask, 0.4, 0)
        # In case a RGB output is wanted
        # mask3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # Otsu threshold for RGB image
        # image = cv2.addWeighted(image, 0.6, mask3, 0.4, 0)

    # Save image
    img_path = f'page_{int(i+1)}_final.png'
    cv2.imwrite(img_path, image)

    # Remove unneeded file
    os.remove(f'page_{i+1}_untouched.png')

# Some cleaning
# for f in glob.glob('*_untouched.png'):
#     os.remove(f)

img_list = []
for i in range(len(glob.glob('*_final.png'))):
    page = Image.open(f'page_{i+1}_final.png')
    img_list.append(page.convert('RGB'))

# Save final PDF
img_list[0].save(pdf_path + '_output.pdf', save_all=True, append_images=img_list[1:])

# Final cleaning
for f in glob.glob('page*.png'):
    os.remove(f)

print(pdf_path+'_output.pdf has been created')