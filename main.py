import tkinter as tk
from tkinter import filedialog, messagebox, Label, Toplevel
from PIL import Image, ImageTk
import os


def apply_watermark(images_folder, watermark_path, output_folder, rel_x, rel_y):
    watermark = Image.open(watermark_path).convert("RGBA")
    wm_width, wm_height = watermark.size

    for filename in os.listdir(images_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(images_folder, filename)
            img = Image.open(img_path).convert("RGBA")
            img_width, img_height = img.size

            # Calculate the absolute position based on the relative position and image size
            x_pos = int(rel_x * img_width - wm_width / 2)
            y_pos = int(rel_y * img_height - wm_height / 2)
            x_pos = max(0, min(x_pos, img_width - wm_width))
            y_pos = max(0, min(y_pos, img_height - wm_height))

            img.paste(watermark, (x_pos, y_pos), watermark)
            img = img.convert('RGB')
            output_img_path = os.path.join(output_folder, filename)
            img.save(output_img_path, 'JPEG')

    return output_folder


def open_folder():
    images_folder = filedialog.askdirectory(title="Select Folder Containing Images")
    if not images_folder:
        return

    watermark_path = filedialog.askopenfilename(title="Select Watermark Image",
                                                filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not watermark_path:
        return

    rel_x, rel_y = position_selector(images_folder)
    if rel_x is None or rel_y is None:
        return

    output_folder = os.path.join(images_folder, "Watermarked")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    apply_watermark(images_folder, watermark_path, output_folder, rel_x, rel_y)
    messagebox.showinfo("Success", "Images have been watermarked and saved in {}".format(output_folder))


def position_selector(images_folder):
    selector_win = Toplevel(root)
    selector_win.title("Adjust Watermark Position")

    sample_image_path = os.listdir(images_folder)[0]
    original_image = Image.open(os.path.join(images_folder, sample_image_path)).convert('RGBA')

    # Ensure the image fits within the screen size
    screen_width = root.winfo_screenwidth() * 0.8
    screen_height = root.winfo_screenheight() * 0.8
    scale_width = screen_width / original_image.width
    scale_height = screen_height / original_image.height
    scale = min(scale_width, scale_height)
    display_image = original_image.resize((int(original_image.width * scale), int(original_image.height * scale)),
                                          Image.Resampling.LANCZOS)

    sample_photo = ImageTk.PhotoImage(display_image)
    label_image = Label(selector_win, image=sample_photo)
    label_image.photo = sample_photo
    label_image.pack()

    # Define rel_x and rel_y as nonlocal variables to retain their values outside the nested function
    rel_x, rel_y = 0, 0  # Initialize with default values

    def on_image_click(event):
        nonlocal rel_x, rel_y  # Declare nonlocal to modify the outer scope variables
        rel_x = event.x / display_image.width
        rel_y = event.y / display_image.height
        selector_win.destroy()

    label_image.bind("<Button-1>", on_image_click)

    selector_win.transient(root)
    selector_win.grab_set()
    root.wait_window(selector_win)

    return rel_x, rel_y


root = tk.Tk()
root.title("Bulk Image Watermarking Tool")
open_button = tk.Button(root, text="Select Images and Apply Watermark", command=open_folder)
open_button.pack(pady=20, padx=20)
root.mainloop()
