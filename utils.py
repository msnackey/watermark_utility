import os
import tkinter.filedialog as fd

from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageTk

IMG_SIZE = (500, 500)
WM_COLOR = (255, 255, 255, 128)


class ImageUtility:
    def __init__(self) -> None:
        self.wm_util = WatermarkUtility()
        self.filename = ""
        self.img_og = None
        self.img_og_rs = None
        self.img_wm = None
        self.img_wm_rs = None

    def upload_img(self) -> None:
        fp = fd.askopenfilename(
            title="Select your image...",
            filetypes=[
                ("PNG", ("*.png")),
                ("JPG/JPEG", ("*.jpg", "*.jpeg")),
                ("All files", "*.*"),
            ],
        )
        self.filename = os.path.basename(fp)
        with Image.open(fp).convert("RGBA") as img:
            self.img_og = img
            self.img_og_rs = ImageTk.PhotoImage(self.resize_image(img))

    def make_img_wm(self, mode: str, text: str, fontname: str, fontsize: str) -> None:
        self.wm_util.set_text(text)
        self.wm_util.set_font_options(fontname, fontsize, self.img_og)
        self.img_wm = self.wm_util.make_img_wm(self.img_og, mode)
        self.img_wm_rs = ImageTk.PhotoImage(self.resize_image(self.img_wm))

    def resize_image(self, img: Image.Image) -> Image.Image:
        return ImageOps.contain(img, IMG_SIZE)

    def download_img(self) -> None:
        fp = fd.asksaveasfilename(
            title="Save your image...",
            filetypes=[
                ("PNG", ("*.png")),
                ("JPG/JPEG", ("*.jpg", "*.jpeg")),
                ("All files", "*.*"),
            ],
            initialfile=f"wm_{self.filename}",
        )
        self.img_wm.save(fp)


class WatermarkUtility:
    def __init__(
        self,
        text: str = "Watermark Utility",
        font: str = "Arial",
        size: int = 20,
        mode: str = "bottom",
    ) -> None:
        self.text = text
        self.font = ImageFont.truetype(font_manager.findfont(font), size)
        self.mode = mode

    def make_img_wm(self, img: Image.Image, mode: str) -> Image.Image:
        self.set_mode(mode)
        if self.mode == "middle":
            img = self.create_wm(img, self.middle_wm(img))
        elif self.mode == "bottom":
            img = self.create_wm(img, self.bottom_wm(img))
        elif self.mode == "both":
            img = self.create_wm(img, self.middle_wm(img))
            img = self.create_wm(img, self.bottom_wm(img))
        else:
            pass
        return img

    def create_wm(self, img: Image.Image, txt: Image.Image) -> Image.Image:
        return Image.alpha_composite(img, txt)

    def middle_wm(self, img: Image.Image, **kwargs) -> Image.Image:
        try:
            self.set_font_options(kwargs["fontsize"], kwargs["fontname"], img)
        except:
            pass
        txt = self.wm_text(img)
        d = ImageDraw.Draw(txt)
        d.text(
            xy=(img.width / 2, img.height / 2),
            text=self.text,
            font=self.font,
            fill=WM_COLOR,
            anchor="mm",
        )
        return txt

    def bottom_wm(self, img: Image.Image, **kwargs) -> Image.Image:
        try:
            self.set_font_options(kwargs["fontsize"], kwargs["fontname"], img)
        except:
            pass
        txt = self.wm_text(img)
        d = ImageDraw.Draw(txt)
        d.text(
            xy=(img.width - 10, img.height - 10),
            text=self.text,
            font=self.font,
            fill=WM_COLOR,
            anchor="rb",
        )
        return txt

    def wm_text(self, img: Image.Image) -> Image.Image:
        return Image.new("RGBA", img.size, (255, 255, 255, 0))

    def set_font_options(self, fontname: str, fontsize: str, img: Image.Image) -> None:
        if fontsize == "small":
            fontsize = int(img.height / 20)
        elif fontsize == "medium":
            fontsize = int(img.height / 15)
        elif fontsize == "large":
            fontsize = int(img.height / 10)
        else:
            raise Exception(
                "Invalid fontsize given. Try one of 'small', 'medium' or 'large'."
            )
        self.font = ImageFont.truetype(font_manager.findfont(fontname), fontsize)

    def set_mode(self, mode: str) -> None:
        if mode == "middle" or mode == "bottom" or mode == "both":
            self.mode = mode
        else:
            raise Exception(
                "Sorry, this mode is not available. Try one of 'middle', 'bottom' or 'both'."
            )

    def set_text(self, text: str) -> None:
        self.text = text
