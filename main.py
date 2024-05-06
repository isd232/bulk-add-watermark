import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Label
from PIL import Image, ImageTk

class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main window configurations
        self.title("Bulk Watermark Tool")
        self.geometry("300x150")

        # Create the main menu options
        tk.Label(self, text="Select an option:").pack(pady=(20, 10))
        tk.Button(self, text="Watermark Images", command=self.open_image_watermarking).pack(pady=(10, 5))
        tk.Button(self, text="Watermark Videos", command=self.open_video_watermarking).pack(pady=(10, 5))

    def open_image_watermarking(self):
        ImageWatermarkWindow(self)

    def open_video_watermarking(self):
        VideoWatermarkWindow(self)

class ImageWatermarkWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Watermark Images")
        self.geometry("400x300")

        # Watermark settings
        self.images_folder = tk.StringVar()
        self.watermark_image = tk.StringVar()
        self.rel_x, self.rel_y = 0, 0

        # UI Elements
        tk.Label(self, text="Select Folder Containing Images:").pack(pady=(20, 5))
        tk.Entry(self, textvariable=self.images_folder, width=40).pack()
        tk.Button(self, text="Browse", command=self.select_images_folder).pack()

        tk.Label(self, text="Select Watermark Image:").pack(pady=(20, 5))
        tk.Entry(self, textvariable=self.watermark_image, width=40).pack()
        tk.Button(self, text="Browse", command=self.select_watermark_image).pack()

        tk.Button(self, text="Set Watermark Position", command=self.position_selector).pack(pady=(20, 5))
        tk.Button(self, text="Start Watermarking", command=self.start_watermarking).pack(pady=(20, 5))

    def select_images_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder Containing Images")
        if folder_path:
            self.images_folder.set(folder_path)

    def select_watermark_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Watermark Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.watermark_image.set(file_path)

    def position_selector(self):
        images_folder = self.images_folder.get()
        if not images_folder:
            messagebox.showerror("Error", "Please select an images folder first.")
            return

        selector_win = Toplevel(self)
        selector_win.title("Adjust Watermark Position")

        sample_image_path = next(
            (f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))), None)
        if not sample_image_path:
            messagebox.showerror("Error", "No image files found in the selected folder.")
            selector_win.destroy()
            return

        original_image = Image.open(os.path.join(images_folder, sample_image_path)).convert('RGBA')

        screen_width = self.winfo_screenwidth() * 0.8
        screen_height = self.winfo_screenheight() * 0.8
        scale_width = screen_width / original_image.width
        scale_height = screen_height / original_image.height
        scale = min(scale_width, scale_height)
        display_image = original_image.resize((int(original_image.width * scale), int(original_image.height * scale)),
                                              Image.Resampling.LANCZOS)

        sample_photo = ImageTk.PhotoImage(display_image)
        label_image = Label(selector_win, image=sample_photo)
        label_image.photo = sample_photo
        label_image.pack()

        def on_image_click(event):
            nonlocal self
            self.rel_x = event.x / display_image.width
            self.rel_y = event.y / display_image.height
            selector_win.destroy()

        label_image.bind("<Button-1>", on_image_click)

        selector_win.transient(self)
        selector_win.grab_set()
        self.wait_window(selector_win)

    def start_watermarking(self):
        images_folder = self.images_folder.get()
        watermark_image = self.watermark_image.get()
        if not images_folder or not watermark_image:
            messagebox.showerror("Error", "Please select both images folder and watermark image.")
            return

        output_folder = os.path.join(images_folder, "Watermarked")
        os.makedirs(output_folder, exist_ok=True)

        watermark = Image.open(watermark_image).convert("RGBA")
        wm_width, wm_height = watermark.size

        for filename in os.listdir(images_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(images_folder, filename)
                img = Image.open(img_path).convert("RGBA")
                img_width, img_height = img.size

                x_pos = int(self.rel_x * img_width - wm_width / 2)
                y_pos = int(self.rel_y * img_height - wm_height / 2)
                x_pos = max(0, min(x_pos, img_width - wm_width))
                y_pos = max(0, min(y_pos, img_height - wm_height))

                img.paste(watermark, (x_pos, y_pos), watermark)
                img = img.convert('RGB')
                output_img_path = os.path.join(output_folder, filename)
                img.save(output_img_path, 'JPEG')

        messagebox.showinfo("Success", "Images have been watermarked and saved in {}".format(output_folder))

class VideoWatermarkWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Watermark Videos")
        self.geometry("400x300")
        self.ffmpeg_path = 'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'  # Update this path

        # Watermark settings
        self.input_folder = tk.StringVar()
        self.watermark_image = tk.StringVar()
        self.position_x = tk.StringVar(value="10")
        self.position_y = tk.StringVar(value="10")

        # UI Elements
        tk.Label(self, text="Select Folder Containing Videos:").pack(pady=(20, 5))
        tk.Entry(self, textvariable=self.input_folder, width=40).pack()
        tk.Button(self, text="Browse", command=self.select_input_folder).pack()

        tk.Label(self, text="Select Watermark Image:").pack(pady=(20, 5))
        tk.Entry(self, textvariable=self.watermark_image, width=40).pack()
        tk.Button(self, text="Browse", command=self.select_watermark_image).pack()

        tk.Label(self, text="Watermark Position (x:y)").pack(pady=(20, 5))
        position_frame = tk.Frame(self)
        position_frame.pack()
        tk.Entry(position_frame, textvariable=self.position_x, width=10).pack(side=tk.LEFT, padx=5)
        tk.Entry(position_frame, textvariable=self.position_y, width=10).pack(side=tk.LEFT, padx=5)

        tk.Button(self, text="Start Watermarking", command=self.start_watermarking).pack(pady=(20, 5))

    def select_input_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder Containing Videos")
        if folder_path:
            self.input_folder.set(folder_path)

    def select_watermark_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Watermark Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.watermark_image.set(file_path)

    def start_watermarking(self):
        input_folder = self.input_folder.get()
        watermark_image = self.watermark_image.get()
        position = f"{self.position_x.get()}:{self.position_y.get()}"
        output_folder = os.path.join(input_folder, "watermarked")
        os.makedirs(output_folder, exist_ok=True)

        if not input_folder or not watermark_image:
            messagebox.showerror("Error", "Please select both source folder and watermark image.")
            return

        for filename in os.listdir(input_folder):
            if filename.lower().endswith('.mp4'):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, f"watermarked_{filename}")

                command = [
                    self.ffmpeg_path,
                    '-i', input_path,
                    '-i', watermark_image,
                    '-filter_complex', f'overlay={position}',
                    '-codec:a', 'copy',
                    output_path
                ]

                try:
                    subprocess.run(command, check=True)
                    print(f"Successfully added watermark to {filename}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {filename}: {e}")

        messagebox.showinfo("Success", f"Watermarking complete! Files saved to: {output_folder}")

if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
