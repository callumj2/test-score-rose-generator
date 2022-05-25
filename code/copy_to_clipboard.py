""" copy_to_clipboard.py

Created by 
    name: Callum Johnson
    mail: callum.johnson.aafc@gmail.com

Helper tool for use with the file gui.py.

Code largely (Entirely) taken from the following StackOverflow post:

https://stackoverflow.com/questions/34322132/copy-image-to-clipboard

"""
from io import BytesIO
import win32clipboard
from PIL import Image

def send_to_clipboard(filepath):
    # Open the image and convert to Bitmap
    image = Image.open(filepath)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    # Add to clipboard
    clip_type = win32clipboard.CF_DIB
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()



