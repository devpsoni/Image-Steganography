# Importing necessary libraries
from PIL import Image
import numpy as np

# Function to convert a message to binary
def message_to_bin(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

# Function to convert binary to message
def bin_to_message(binary):
    message = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return message

# Function to encode a message into an image
def encode_image(img_path, message, output_path):
    img = Image.open(img_path)
    binary_message = message_to_bin(message) + '1111111111111110' # Adding a delimiter to signify end of the message
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        newData = []
        digit = 0
        for item in datas:
            if (digit < len(binary_message)):
                newpix = item[:3] + (item[3] & ~1 | int(binary_message[digit]),) # change the LSB of the alpha channel
                digit += 1
            else:
                newpix = item
            newData.append(newpix)

        img.putdata(newData)
        img.save(output_path, "PNG")
        return "Message encoded successfully"
    else:
        return "Incorrect image mode, couldn't encode"

# Function to decode the message from an image
def decode_image(img_path):
    img = Image.open(img_path)
    binary_message = ""
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:
            digit = item[3] & 1 # extracting the LSB of the alpha channel
            binary_message += str(digit)
            if binary_message[-16:] == '1111111111111110': # check if we've reached the delimiter
                break

        binary_message = binary_message[:-16] # remove the delimiter
        message = bin_to_message(binary_message)
        return message
    else:
        return "Incorrect image mode, couldn't decode"


#print(encode_image('./panda.png', 'This is Dev & Atharva', './enimage.png'))
print(decode_image('./enimage.png'))
