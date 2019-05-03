from __future__ import print_function
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import os.path  
import PIL
import PIL.ImageDraw
import PIL.ImageOps
import math

# All necessary libraries should be imported past here

current_directory = os.path.abspath(os.path.dirname(__file__))
image_directory = current_directory + os.sep + "Project_Images"
brand_image = PIL.Image.open(image_directory + os.sep + "Editing_Assets" + \
os.sep + "modified-generic-company-logo.png")

def draw_border_gradient(img, center_color=(0, 0, 0, 255), \
outer_color=(255, 255, 255, 255), excluding_region=None):
    """Draws a circular gradient onto an image.
    img: The image which is being edited
    center_color: the color from the center of the image
    outer_color: The color which the background is transitioned to
    excluding_region: The area which is not drawn"""
    center = (img.size[0] / 2, img.size[1] / 2)
    # Used to calculate scalar
    max_distance = math.sqrt(center[0] ** 2 + center[1] ** 2)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if excluding_region != None:
                if not (x < excluding_region[0] or x >= excluding_region[1] or \
                y < excluding_region[2] or y >= excluding_region[3]):
                    continue
            
            # This gets the delta between the current point and the center
            distance = math.sqrt((center[0] - x) ** 2 + (center[1] - y) ** 2)
            # We turn this into a scale from 0 to 1, with 1 meaning being on the
            # very outside, and 0 being on the center
            distance_scalar = float(distance) / max_distance
            
            r = (1 - distance_scalar) * center_color[0] + distance_scalar * \
            outer_color[0]
            g = (1 - distance_scalar) * center_color[1] + distance_scalar * \
            outer_color[1]
            b = (1 - distance_scalar) * center_color[2] + distance_scalar * \
            outer_color[2]
            
            img.putpixel((x, y), (int(r), int(g), int(b), 255))
            

def brandify_img(img, img_name, border_width_percentage=0.10, \
border_width_cap=150, inner_border_width=7, \
inner_border_color=(50, 255, 50, 0), outer_border_color=(50, 50, 50, 0)):
    """This adds a border on the image. It will change the size of the image
    (enlargen it) to accomodate the border.
    img: The center image, which the border will be added on
    img_name: The name of the image(used when saving the image)
    border_width_percentage: The percent(min 0, usually to 1) which will
    determine the size of the border
    border_width_cap: The maximum size of the border in pixels on each side
    inner_border_width: The size of the inner part of the border in pixels on
    each side
    inner_border_color: The color of the center of the image(used for the
    gradient), expressed as an RGBA 4-value tuple
    outer_border_color: The color of the outer edges of the image(used for the
    gradient), expressed as an RGBA 4-value tuple"""
    if img_name.startswith("Modified-"):
        return
    width = img.size[0]
    height = img.size[1]
    # A new image that will be embiggened to fit the border
    border_width = int(float(width + height) / 2 * border_width_percentage)
    if border_width > border_width_cap:
        border_width = border_width_cap
    total_width = width + border_width * 2
    total_height = height + border_width * 2
    img.convert(mode="RGBA")
    bordered_img = PIL.Image.new("RGBA", img.size)
    bordered_img = PIL.ImageOps.expand(img, border=border_width)
    draw = PIL.ImageDraw.Draw(bordered_img)
    
    # Fill in the border for the image
    # The inner part of the border will be later covered up by the image itself
    draw_border_gradient(bordered_img, center_color=inner_border_color, \
    outer_color=outer_border_color, excluding_region=(border_width, \
    width + border_width, border_width, height + border_width))
    
    # Inner border
    # "bb" stands for border for border
    bb_color = (255 - 50, 255 - 50, 255 - 50, 255)
    draw.rectangle((border_width - inner_border_width, border_width - \
    inner_border_width, width + border_width + inner_border_width, height + \
    border_width + inner_border_width), fill=bb_color)
    
    # Add the original image
    bordered_img.paste(img, (border_width, border_width, width + border_width, \
    height + border_width))
    
    # Add some basic design to the border
    # Add lines on each corner
    # Order is top left, top right, bottom left, bottom right
    draw.line((0, 0, border_width, border_width), fill=bb_color, width=3)
    draw.line((total_width, 0, total_width - border_width, border_width), \
    fill=bb_color, width=3)
    draw.line((0, total_height, border_width, total_height - border_width), \
    fill=bb_color, width=3)
    draw.line((total_width, total_height, total_width - border_width, \
    total_height - border_width), fill=bb_color, width=3)
    
    # Apply the brand image
    new_width = int((float(brand_image.size[0]) / brand_image.size[1]) * \
    border_width)
    new_height = border_width - inner_border_width
    resized_img = brand_image.resize((new_width, new_height))
    bordered_img.paste(resized_img, box=((width - resized_img.size[0] / 2) \
    / 2, 0), mask=resized_img)
    
    bordered_img.save(image_directory + os.sep + "Modified-" + img_name)
    

# Loads all the images which are in the Project_Images directory

for child_file in os.listdir(image_directory):
    abs_filename = os.path.abspath(image_directory + os.sep + child_file)
    try:
        child_img = PIL.Image.open(abs_filename)
        # This is where the options are set
        brandify_img(child_img, child_file, border_width_percentage=0.10, \
        border_width_cap=150, inner_border_width=7, \
        inner_border_color=(50, 255, 50, 0), outer_border_color=(50, 50, 50, 0))
    except IOError:
        # Ignore broken files
        pass