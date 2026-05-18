import customtkinter as ctk
from tkinter import messagebox

from veritabani.sorgular import giris_kontrol
from ekranlar.admin_paneli import AdminPaneli
from ekranlar.personel_paneli import PersonelPaneli
from kayit_ekrani import KayitEkrani
from ayarlar.sabitler import logo_ekle


class GirisEkrani(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AirportGo - Giriş")
        self.geometry("400x450")
        self.resizable(False, False)
        logo_ekle(self, boyut=(90, 90))

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(
            self,
            text="AirportGo",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Havalimanı Yönetim Sistemi",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 20))

        self.kullanici_entry = ctk.CTkEntry(self, placeholder_text="Kullanıcı Adı")
        self.kullanici_entry.pack(pady=10)

        self.sifre_entry = ctk.CTkEntry(self, placeholder_text="Şifre", show="*")
        self.sifre_entry.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Giriş Yap",
            command=self.giris_yap
        ).pack(pady=15)

        ctk.CTkButton(
            self,
            text="Kayıt Ol",
            fg_color="gray",
            hover_color="#555555",
            command=self.kayit_ekranini_ac
        ).pack()

    def giris_yap(self):
        kullanici = self.kullanici_entry.get()
        sifre = self.sifre_entry.get()

        basarili, mesaj, user = giris_kontrol(kullanici, sifre)

        if not basarili:
            messagebox.showerror("Hata", mesaj)
            return

        messagebox.showinfo("Başarılı", mesaj)

        self.withdraw()

        if user["rol"] == "admin":
            panel = AdminPaneli(self, user)
        else:
            panel = PersonelPaneli(self, user)

        panel.protocol("WM_DELETE_WINDOW", lambda: self._paneleden_don(panel))

    def _paneleden_don(self, panel):
        try:
            panel.destroy()
        except Exception:
            pass
        self.deiconify()

    def kayit_ekranini_ac(self):
        kayit = KayitEkrani(self, kayit_basarili_callback=self.kayit_basarili_oldu)
        kayit.protocol("WM_DELETE_WINDOW", lambda: self._kayittan_don(kayit))

    def _kayittan_don(self, kayit):
        try:
            kayit.destroy()
        except Exception:
            pass
        self._login_one_getir()

    def kayit_basarili_oldu(self, kullanici_adi: str):
        self.kullanici_entry.delete(0, "end")
        self.kullanici_entry.insert(0, kullanici_adi)
        self.sifre_entry.delete(0, "end")
        self._login_one_getir()

    def _login_one_getir(self):
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(150, lambda: self.attributes("-topmost", False))
