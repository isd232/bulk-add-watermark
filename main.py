import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Toplevel, Label, Radiobutton, StringVar, Button
from PIL import Image
import os

def apply_watermark(images_folder, watermark_path, output_folder, position):
    watermark = Image.open(watermark_path).convert("RGBA")
    wm_width, wm_height = watermark.size

    for filename in os.listdir(images_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(images_folder, filename)
            img = Image.open(img_path).convert("RGBA")
            img_width, img_height = img.size

            # Calculate position based on user selection
            if position == 'top-left':
                pos = (0, 0)
            elif position == 'top-right':
                pos = (img_width - wm_width, 0)
            elif position == 'bottom-left':
                pos = (0, img_height - wm_height)
            elif position == 'bottom-right':
                pos = (img_width - wm_width, img_height - wm_height)
            elif position == 'center':
                pos = ((img_width - wm_width) // 2, (img_height - wm_height) // 2)

            img.paste(watermark, pos, watermark)
            img = img.convert('RGB')
            output_img_path = os.path.join(output_folder, filename)
            img.save(output_img_path, 'JPEG')

    return output_folder

def open_folder():
    images_folder = filedialog.askdirectory(title="Select Folder Containing Images")
    if not images_folder:
        return

    watermark_path = filedialog.askopenfilename(title="Select Watermark Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not watermark_path:
        return

    # Create a small dialog to select the position
    position = select_position()
    if not position:
        return

    output_folder = os.path.join(images_folder, "Watermarked")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_folder = apply_watermark(images_folder, watermark_path, output_folder, position)
    messagebox.showinfo("Success", f"Images have been watermarked and saved in {output_folder}")

def select_position():
    position_win = Toplevel(root)
    position_win.title("Select Watermark Position")

    pos_var = StringVar(value='bottom-right')

    positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']
    for pos in positions:
        Radiobutton(position_win, text=pos.replace('-', ' ').title(), variable=pos_var, value=pos).pack(anchor=tk.W)

    Button(position_win, text="OK", command=lambda: position_win.destroy()).pack(pady=10)

    position_win.transient(root)  # Make the position window modal
    position_win.grab_set()       # Focus on the new window
    root.wait_window(position_win)  # Wait for the window to close

    return pos_var.get()


root = tk.Tk()
root.title("Bulk Image Watermarking Tool")
open_button = tk.Button(root, text="Select Images and Apply Watermark", command=open_folder)
open_button.pack(pady=20, padx=20)
root.mainloop()
