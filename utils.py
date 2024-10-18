import tkinter.filedialog as fd

from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageTk

IMG_SIZE = (500, 500)
WM_COLOR = (255, 255, 255, 128)


class ImageUtility:
    def __init__(self) -> None:
        self.wm_util = WatermarkUtility()
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
        with Image.open(fp).convert("RGBA") as img:
            self.img_og = img
            self.img_og_rs = ImageTk.PhotoImage(self.resize_image(img))

    def make_img_wm(self) -> None:
        self.img_wm = self.wm_util.make_img_wm(self.img_og)
        self.img_wm_rs = ImageTk.PhotoImage(self.resize_image(self.img_wm))

    def resize_image(self, img) -> Image.Image:
        return ImageOps.contain(img, IMG_SIZE)


class WatermarkUtility:
    def __init__(
        self,
        text: str = "Watermark Utility",
        font: str = "Arial",
        size: int = 200,
        mode: str = "bottom",
    ) -> None:
        self.text = text
        self.fontname = font
        self.fontsize = size
        self.font = ImageFont.truetype(
            font_manager.findfont(self.fontname), self.fontsize
        )
        self.mode = mode
        # print(self.master.master.wm_frame.get_font_options())

    def make_img_wm(self, img) -> None:
        if self.mode == "middle":
            img = self.create_wm(img, self.middle_wm(img))
        elif self.mode == "bottom":
            img = self.create_wm(img, self.bottom_wm(img))
        elif self.mode == "both":
            img = self.create_wm(img, self.middle_wm(img))
            img = self.create_wm(img, self.bottom_wm(img))
        else:
            raise Exception(
                "Sorry, this mode is not available. Try one of 'middle', 'bottom' or 'both'."
            )
        return img

    def create_wm(self, img, txt):
        return Image.alpha_composite(img, txt)

    def middle_wm(self, img, **kwargs) -> Image.Image:
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

    def bottom_wm(self, img, **kwargs) -> Image.Image:
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

    def wm_text(self, img) -> Image.Image:
        return Image.new("RGBA", img.size, (255, 255, 255, 0))

    def set_font_options(self, fontsize: str, fontname: str, img: Image.Image):
        if fontsize.lower() == "Small":
            fontsize = int(img.height / 10)
        elif fontsize.lower() == "Medium":
            fontsize = int(img.height / 5)
        elif fontsize.lower() == "Large":
            fontsize = int(img.height / 3)
        else:
            raise Exception(
                "Invalid fontsize given. Try one of 'small', 'medium' or 'large'."
            )
        self.fontsize = fontsize
        self.fontname = fontname

    def set_mode(self, mode):
        if mode == "middle" or mode == "bottom" or mode == "both":
            self.mode = mode
        else:
            raise Exception(
                "Sorry, this mode is not available. Try one of 'middle', 'bottom' or 'both'."
            )
