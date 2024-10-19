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

    def adjust_window_size(self, img: ImageTk.PhotoImage) -> None:
        self.minsize(
            width=int((2.1 * img.width() + 40)), height=int((1.1 * img.height() + 140))
        )


class MainFrame(ttk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
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
        self.download_btn = ttk.Button(
            self,
            text="Download image",
            command=lambda: [
                self.img_util.download_img(),
            ],
        )
        self.download_btn.grid(column=2, row=0, padx=(0, 10), sticky="N")
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

    def make_img_wm(self, mode: str) -> None:
        wm_text = self.wm_frame.get_wm_text()
        font_options = self.wm_frame.get_font_options()
        self.img_util.make_img_wm(
            mode, wm_text, font_options["fontname"], font_options["fontsize"]
        )
        self.update_img_wk()

    def update_img_og(self) -> None:
        self.img_og.config(image=self.img_util.img_og_rs)

    def update_img_wk(self) -> None:
        self.img_wm.config(image=self.img_util.img_wm_rs)


class WatermarkFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        ttk.Frame.__init__(self, master=parent)
        self.grid()

        # Row
        self.watermark_label = ttk.Label(self, text="Watermark settings")
        self.watermark_label.grid(column=0, row=0)

        # Row
        self.wm_text_label = ttk.Label(self, text="Watermark text:")
        self.wm_text_label.grid(column=0, row=1)
        self.wm_text = StringVar()
        self.wm_text_entry = ttk.Entry(
            self, width=WM_BUTTON_WIDTH, textvariable=self.wm_text
        )
        self.wm_text_entry.grid(column=1, row=1, pady=(0, 10))

        # Row
        self.fontname = StringVar()
        self.fontname_drop = ttk.Combobox(
            self,
            width=WM_BUTTON_WIDTH,
            textvariable=self.fontname,
            values=FONT_OPTIONS,
        )
        self.fontname_drop.grid(column=0, row=2)
        self.fontname_drop.current(1)
        self.watermark1_btn = ttk.Button(
            self,
            text="Middle",
            width=WM_BUTTON_WIDTH,
            command=lambda: self.master.make_img_wm("middle"),
        )
        self.watermark1_btn.grid(column=1, row=2)
        self.watermark2_btn = ttk.Button(
            self,
            text="Both",
            width=WM_BUTTON_WIDTH,
            command=lambda: self.master.make_img_wm("both"),
        )
        self.watermark2_btn.grid(column=2, row=2, padx=(6, 0))

        # Row
        self.fontsize = StringVar()
        fontsize_options = ["Small", "Medium", "Large"]
        self.wm_font_drop = ttk.Combobox(
            self,
            width=WM_BUTTON_WIDTH,
            textvariable=self.fontsize,
            values=fontsize_options,
        )
        self.wm_font_drop.grid(column=0, row=3)
        self.wm_font_drop.current(1)
        self.watermark3_btn = ttk.Button(
            self,
            text="Bottom",
            width=WM_BUTTON_WIDTH,
            command=lambda: self.master.make_img_wm("bottom"),
        )
        self.watermark3_btn.grid(column=1, row=3)

    def get_font_options(self) -> dict:
        return dict(
            [
                ("fontname", self.fontname.get()),
                ("fontsize", self.fontsize.get().lower()),
            ]
        )

    def get_wm_text(self) -> str:
        return self.wm_text.get()


MainWindow().mainloop()
