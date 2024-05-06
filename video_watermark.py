import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel


class VideoWatermarkWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.ffmpeg_path = 'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'

        self.title("Watermark Videos")
        # Set initial size of the window
        self.geometry("400x300")

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position x and y coordinates
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        # Set the position of the window
        self.geometry(f'+{x}+{y}')

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
        self.destroy()
