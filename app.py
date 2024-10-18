# Let the user decide on a watermark design, give several options
# Either automatically apply the watermark after an option has been selected, or create a button to apply the watermark

# Show the watermarked image in the Tkinter window, on the right (with instructions to right-click and save)
# And/or give the ability to download the image

import tkinter as tk
from tkinter import StringVar, ttk

from PIL import ImageTk

from utils import ImageUtility

FONT_OPTIONS = [
    "Arial",
    "Baskerville",
    "Courier New",
    "Geneva",
    "Helvetica",
    "PT Sans",
    "PT Serif",
    "Tahoma",
    "Times New Roman",
    "Verdana",
]
WM_BUTTON_WIDTH = 12


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Watermark Utility")
        self.minsize(600, 300)
        self.main_frame = MainFrame(parent=self)

    def adjust_window_size(self, img: ImageTk.PhotoImage):
        self.minsize(
            width=int((2.1 * img.width() + 40)), height=int((1.1 * img.height() + 140))
        )


class MainFrame(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, master=parent, padding=10)
        self.grid()

        self.img_util = ImageUtility()

        # Row 0
        self.spacer_left = ttk.Label(self, text="")
        self.spacer_left.grid(column=0, row=0, padx=(10, 0))
        self.upload_btn = ttk.Button(
            self,
            text="Upload image",
            command=lambda: [
                self.img_util.upload_img(),
                self.update_img_og(),
                self.master.adjust_window_size(self.img_util.img_og_rs),
            ],
        )
        self.upload_btn.grid(column=1, row=0, pady=(0, 10), sticky="NW")
        self.quit_btn = ttk.Button(self, text="Quit", command=parent.destroy)
        self.quit_btn.grid(column=5, row=0, sticky="NE")
        self.spacer_right = ttk.Label(self, text="")
        self.spacer_right.grid(column=6, row=0, padx=(0, 10))

        # Row 1
        self.wm_frame = WatermarkFrame(parent=self)
        self.wm_frame.grid(column=1, row=1, sticky="NW", pady=(0, 20))

        # Row 2
        self.img_og = ttk.Label(self, image=self.img_util.img_og_rs)
        self.img_og.grid(column=1, columnspan=3, row=2, sticky="W", padx=(0, 20))
        self.img_wm = ttk.Label(self, image=self.img_util.img_wm_rs)
        self.img_wm.grid(column=4, columnspan=2, row=2)

    def update_img_og(self) -> None:
        self.img_og.config(image=self.img_util.img_og_rs)

    def update_img_wk(self) -> None:
        self.img_wm.config(image=self.img_util.img_wm_rs)


class WatermarkFrame(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, master=parent)
        self.grid()

        # Row 0
        self.watermark_label = ttk.Label(self, text="Watermark settings")
        self.watermark_label.grid(column=0, row=0)

        # Row 1
        self.fontname = StringVar()
        self.fontname_drop = ttk.Combobox(
            self,
            width=WM_BUTTON_WIDTH,
            textvariable=self.fontname,
            values=FONT_OPTIONS,
        )
        self.fontname_drop.grid(column=0, row=1)
        self.fontname_drop.current(1)
        self.watermark1_btn = ttk.Button(
            self,
            text="Middle",
            width=WM_BUTTON_WIDTH,
            command=lambda: [
                self.master.img_util.make_img_wm(),
                self.master.update_img_wk(),
            ],
        )
        self.watermark1_btn.grid(column=1, row=1)
        self.watermark2_btn = ttk.Button(
            self,
            text="Both",
            width=WM_BUTTON_WIDTH,
            command=lambda: [
                self.master.img_util.make_img_wm(),
                self.master.update_img_wk(),
            ],
        )
        self.watermark2_btn.grid(column=2, row=1, padx=(6, 0))

        # Row 2
        self.fontsize = StringVar()
        fontsize_options = ["Small", "Medium", "Large"]
        self.wm_font_drop = ttk.Combobox(
            self,
            width=WM_BUTTON_WIDTH,
            textvariable=self.fontsize,
            values=fontsize_options,
        )
        self.wm_font_drop.grid(column=0, row=2)
        self.wm_font_drop.current(1)
        self.watermark3_btn = ttk.Button(
            self,
            text="Bottom",
            width=WM_BUTTON_WIDTH,
            command=lambda: [
                self.master.img_util.make_img_wm(),
                self.master.update_img_wk(),
            ],
        )
        self.watermark3_btn.grid(column=1, row=2)

    def get_font_options(self) -> dict:
        return dict([("fontname", self.fontname), ("fontsize", self.fontsize)])


MainWindow().mainloop()
