# Tema / Renkler
RENK_ANA = "#2F80ED"        # mavi
RENK_ANA_HOVER = "#2566BE"
RENK_IKINCIL = "#6C757D"    # gri
RENK_IKINCIL_HOVER = "#545B62"
import customtkinter as ctk
from PIL import Image
import os


def logo_ekle(parent, boyut=(80, 80), padding=(15, 10)):

    logo_yol = os.path.join("gorseller", "logo.png")

    if not os.path.exists(logo_yol):
        return

    img = Image.open(logo_yol)
    img = img.resize(boyut)

    logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=boyut)

    lbl = ctk.CTkLabel(parent, image=logo_img, text="")
    lbl.image = logo_img
    lbl.pack(pady=padding)
