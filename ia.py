from PIL import Image
import numpy as np

def message_to_bin(message: str) -> str:
    """
    Convert a message to a binary string.
    """
    return ''.join(format(ord(char), '08b') for char in message)

def bin_to_message(binary: str) -> str:
    """
    Convert a binary string to its message.
    """
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def encode_image(img_path: str, message: str, output_path: str) -> str:
    """
    Encode a message into the alpha channel of an image.
    """
    try:
        img = Image.open(img_path)
    except IOError:
        return "Error opening image file."

    binary_message = message_to_bin(message) + '1111111111111110'  # Delimiter

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    datas = np.array(img)
    flat_data = datas.flatten()
    message_len = len(binary_message)

    # Only modify the alpha channel
    for i in range(0, min(message_len, len(flat_data) // 4)):
        flat_data[i4 + 3] = flat_data[i4 + 3] & ~1 | int(binary_message[i])

    datas = flat_data.reshape(datas.shape)
    img = Image.fromarray(datas, 'RGBA')
    img.save(output_path, "PNG")

    return "Message encoded successfully"

def decode_image(img_path: str) -> str:
    """
    Decode a message from the alpha channel of an image.
    """
    try:
        img = Image.open(img_path)
    except IOError:
        return "Error opening image file."

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    datas = np.array(img)
    binary_message = ''.join(str(datas[i // 4][i % 4][3] & 1) for i in range(0, datas.size // 4))
    end_delimiter = binary_message.find('1111111111111110')

    if end_delimiter != -1:
        binary_message = binary_message[:end_delimiter]
        return bin_to_message(binary_message)
    else:
        return "Message not found or incorrect image mode."