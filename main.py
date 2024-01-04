from PIL import Image, ImageDraw, ImageFont
import time

def rounded_rectangle(draw, xy, radius, fill=None, outline=None):
    x1, y1, x2, y2 = xy
    draw.rectangle([(x1, y1 + radius), (x2, y2 - radius)], fill=fill)
    draw.rectangle([(x1 + radius, y1), (x2 - radius, y2)], fill=fill)
    draw.pieslice([(x1, y1), (x1 + radius * 2, y1 + radius * 2)], 180, 270, fill=fill)
    draw.pieslice([(x2 - radius * 2, y1), (x2, y1 + radius * 2)], 270, 360, fill=fill)
    draw.pieslice([(x1, y2 - radius * 2), (x1 + radius * 2, y2)], 90, 180, fill=fill)
    draw.pieslice([(x2 - radius * 2, y2 - radius * 2), (x2, y2)], 0, 90, fill=fill)
    if outline:
        draw.arc([(x1, y1), (x1 + radius * 2, y1 + radius * 2)], 180, 270, fill=outline)
        draw.arc([(x2 - radius * 2, y1), (x2, y1 + radius * 2)], 270, 360, fill=outline)
        draw.arc([(x1, y2 - radius * 2), (x1 + radius * 2, y2)], 90, 180, fill=outline)
        draw.arc([(x2 - radius * 2, y2 - radius * 2), (x2, y2)], 0, 90, fill=outline)

# CTRL + C & CTRL + V from stackoverflow
def parse_string(string: str) -> str:
    new_string = ""

    for letter_index in range(len(string)):

        if letter_index % 35 == 0 and letter_index != 0:
            new_string += f"{string[letter_index]}\n"
        else:
            new_string += string[letter_index]

    return new_string

color_sel = input('do u want to change text and bg colors?\n\n1 to yes, 0 to no: ')
if int(color_sel) == 1:
    quote_bg = input('enter quote bg color (hex): ').lstrip('#')
    quote_bg = tuple(int(quote_bg[i:i+2], 16) for i in (0, 2, 4))
    text_color = input('enter text color (hex): ').lstrip('#')
    text_color = tuple(int(text_color[i:i+2], 16) for i in (0, 2, 4))
    isdefault = 0
elif int(color_sel) == 0:
    print('using default colors.\n')
    isdefault = 1
else:
    eblan = 0
    while eblan <= 100:
        print('еблан')
        eblan += 1
    time.sleep(5)
    exit()

font_sel = input('\ndo u want to change text font?\n\n1 to yes, 0 to no: ')
if int(font_sel) == 1:
    selected_font = input('enter font name.\nlike "lobster.ttf": ')
    font = ImageFont.truetype(selected_font, 25) 
    font2 = ImageFont.truetype(selected_font, 15) 
elif int(font_sel) == 0:
    print('using default font (Arial).')
    font = ImageFont.truetype('arial.ttf', 25) 
    font2 = ImageFont.truetype('arial.ttf', 15) 
else:
    eblan = 0
    while eblan <= 100:
        print('еблан')
        eblan += 1
    time.sleep(5)
    exit()

# Create a new image
img = Image.new('RGBA', (500, 500), (0, 0, 0, 0))

file_path = input('avatar pic: ')

# Open avatar
avatar = Image.open(file_path)

# Ellipse mask for avatar
mask = Image.new('L', avatar.size, 0)
draw = ImageDraw.Draw(mask) 
draw.ellipse((0, 0) + avatar.size, fill=255)
avatar.putalpha(mask)
avatar = avatar.resize((45, 45))

# Draw the text
text = input('quote text: ')
text2 = input('quote author: ')

new_text = parse_string(text)

text_width, text_height = draw.textbbox((0, 0), new_text, font=font)[2:]
author_name_width, author_name_height = draw.textbbox((0, 0), text2, font=font2)[2:]

# Calculate the height of the rectangle based on the number of lines in the text
num_lines = new_text.count('\n') + 1
rect_height = num_lines + text_height

if author_name_width > text_width:
    xsize = 10 + author_name_width + 55
    ysize = 25 + rect_height + 20
    print('xsize = '+ str(xsize))
    print('ysize = '+ str(ysize))
    img = img.resize((45 + xsize, 45 + ysize))
else:
    xsize = 10 + text_width + 55
    ysize = 25 + rect_height + 20
    print('xsize = '+ str(xsize))
    print('ysize = '+ str(ysize))
    img = img.resize((45 + xsize, 45 + ysize))

# Create an object for drawing
draw = ImageDraw.Draw(img)

if isdefault == 0:
    draw.rounded_rectangle([(50, 10), (xsize, ysize)], radius=15, fill=(quote_bg))
    draw.text((57, 35), new_text, font=font, fill=(text_color))
    draw.text((58, 15), text2, font=font2, fill=(text_color))
else: 
    draw.rounded_rectangle([(50, 10), (xsize, ysize)], radius=15, fill=(255, 255, 255))
    draw.text((57, 35), new_text, font=font, fill=(0, 0, 0))
    draw.text((58, 15), text2, font=font2, fill=(0, 0, 0))

img.paste(avatar, (0, 0))
# Save the image
img.show()
outputname = input(enter output file name: )
img.save(outputname+'.png')
