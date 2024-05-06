import tkinter as tk
from img_watermark import ImageWatermarkWindow
from video_watermark import VideoWatermarkWindow


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


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
