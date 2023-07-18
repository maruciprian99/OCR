import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract

# Define the colors
BG_COLOR = "#333333"  # Dark gray
FG_COLOR = "#FFFFFF"  # White
BUTTON_COLOR = "#666666"  # Light gray

# Define the fonts
FONT_TITLE = ("Arial", 16, "bold")
FONT_BUTTON = ("Arial", 12)

def tesseract(image_path):
    pytesseract.pytesseract.tesseract_cmd = r"./tesseract/tesseract.exe"
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config='--psm 3')
    return text.strip()  # Return the extracted text without leading/trailing whitespace

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image_path.set(file_path)
        image = Image.open(file_path)
        resized_image = image.resize((125, 125))  # Resize the image for display
        photo = ImageTk.PhotoImage(resized_image)
        image_label.configure(image=photo)
        image_label.image = photo

def process_image():
    file_path = image_path.get()
    if file_path:
        extracted_text = tesseract(file_path)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, extracted_text)

def copy_text():
    text = text_box.get("1.0", tk.END)
    if text:
        window.clipboard_clear()
        window.clipboard_append(text)
        messagebox.showinfo("Copy Text", "Text copied to clipboard!")

# Create the Tkinter window
window = tk.Tk()
window.title("Image OCR")
window.geometry("500x500")
window.configure(bg=BG_COLOR)  # Set the background color
window.resizable(False, False)

# Create the widgets
upload_button = tk.Button(window, text="Upload Image", command=open_file, bg=BUTTON_COLOR, fg=FG_COLOR,
                          font=FONT_BUTTON)
upload_button.pack(pady=10)

image_path = tk.StringVar()
image_label = tk.Label(window, bg=BG_COLOR)
image_label.pack(pady=10)

process_button = tk.Button(window, text="Process Image", command=process_image, bg=BUTTON_COLOR, fg=FG_COLOR,
                           font=FONT_BUTTON)
process_button.pack(pady=10)

text_frame = tk.Frame(window, bg=BG_COLOR)
text_frame.pack(pady=10)

text_box = tk.Text(text_frame, wrap="none", height=11, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR,
                   font=FONT_BUTTON)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

text_scrollbar = tk.Scrollbar(text_frame, command=text_box.yview)
text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.config(yscrollcommand=text_scrollbar.set)

copy_button = tk.Button(window, text="Copy Text", command=copy_text, bg=BUTTON_COLOR, fg=FG_COLOR,
                        font=FONT_BUTTON)
copy_button.pack(pady=(0, 10))  # Adjust the padding of the copy button

# Start the Tkinter event loop
window.mainloop()