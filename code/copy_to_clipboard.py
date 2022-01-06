from io import BytesIO
#import win32clipboard
from PIL import Image
import subprocess
# Code taken from
# https://stackoverflow.com/questions/34322132/copy-image-to-clipboard
def send_to_clipboard(filepath):
    subprocess.run(["osascript", "-e", 'set the clipboard to (read (POSIX file "results.jpg") as JPEG picture)'])




