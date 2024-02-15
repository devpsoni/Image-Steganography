import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import os

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

# Initialize the main window
root = tk.Tk()
root.title("Image Encoder/Decoder")

frame_image_preview = tk.LabelFrame(root, text="Image Preview", padx=5, pady=5)
frame_image_preview.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

label_image_preview = tk.Label(frame_image_preview, text="No Image Selected", bg="black", fg="white", width=64, height=32)
label_image_preview.pack(padx=5, pady=5)

# Set up the user interaction frame
frame_user_interaction = tk.LabelFrame(root, text="", padx=5, pady=5)
frame_user_interaction.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

# Choose Image Button

def choose_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Open the image and calculate the aspect ratio
        img = Image.open(file_path)
        aspect_ratio = img.width / img.height
        base_width = 250  # You can adjust the base width to fit the preview area

        # Calculate the new height based on the aspect ratio
        new_height = int(base_width / aspect_ratio)

        # Resize the image to fit the preview while maintaining aspect ratio
        img.thumbnail((base_width, new_height))
        img = ImageTk.PhotoImage(img)

        # Set the image to the label and store a reference
        label_image_preview.configure(image=img, width=base_width, height=new_height)
        label_image_preview.image = img  # Keep a reference to avoid garbage collection
        entry_encode.delete(0, tk.END)
        entry_encode.insert(0, file_path)

btn_choose_image = tk.Button(frame_user_interaction, text="Choose Image", command=choose_image)
btn_choose_image.pack(fill="x")

# Encode/Decode Entry fields
label_encode = tk.Label(frame_user_interaction, text="Image Path")
label_encode.pack(fill="x")
entry_encode = tk.Entry(frame_user_interaction)
entry_encode.pack(fill="x")

label_decode = tk.Label(frame_user_interaction, text="Encode/Decode Text")
label_decode.pack(fill="x")
entry_decode = tk.Entry(frame_user_interaction)
entry_decode.pack(fill="x")

# Encode/Decode Buttons
def encode():
    img_path = entry_encode.get()
    message = entry_decode.get()
    if img_path and message:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            result = encode_image(img_path, message, output_path)
            messagebox.showinfo("Result", result)
    else:
        messagebox.showwarning("Warning", "Please select an image and enter a message to encode.")

def decode():
    img_path = entry_encode.get()
    if img_path:
        message = decode_image(img_path)
        entry_decode.delete(0, tk.END)
        entry_decode.insert(0, message)
    else:
        messagebox.showwarning("Warning", "Please select an image to decode.")

btn_encode = tk.Button(frame_user_interaction, text="Encode", command=encode)
btn_encode.pack(side="left", expand=True, fill="x")

btn_decode = tk.Button(frame_user_interaction, text="Decode", command=decode)
btn_decode.pack(side="right", expand=True, fill="x")

root.mainloop()
