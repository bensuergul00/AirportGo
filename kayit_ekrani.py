import customtkinter as ctk
from tkinter import messagebox
from veritabani.sorgular import kullanici_ekle
from ayarlar.sabitler import logo_ekle


class KayitEkrani(ctk.CTkToplevel):
    def __init__(self, parent, kayit_basarili_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.kayit_basarili_callback = kayit_basarili_callback

        self.title("AirportGo - Kayıt Ol")
        self.geometry("420x580")
        self.resizable(False, False)
        logo_ekle(self, boyut=(80, 80))

        self.lift()
        self.focus_force()
        self.grab_set()

        ust = ctk.CTkFrame(self, corner_radius=14)
        ust.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(
            ust, text="Kayıt Ol",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=16, pady=(14, 2))

        ctk.CTkLabel(
            ust,
            text="Yeni kullanıcı oluşturun ve sisteme giriş yapın.",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(anchor="w", padx=16, pady=(0, 14))

        kart = ctk.CTkFrame(self, corner_radius=14)
        kart.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        ic = ctk.CTkFrame(kart, fg_color="transparent")
        ic.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(ic, text="Kullanıcı Adı", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 6))
        self.ent_kullanici = ctk.CTkEntry(ic, placeholder_text="örn: bensu")
        self.ent_kullanici.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(ic, text="Şifre", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 6))
        self.ent_sifre = ctk.CTkEntry(ic, placeholder_text="••••••••", show="*")
        self.ent_sifre.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(ic, text="Şifre (Tekrar)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 6))
        self.ent_sifre2 = ctk.CTkEntry(ic, placeholder_text="••••••••", show="*")
        self.ent_sifre2.pack(fill="x", pady=(0, 18))

        alt = ctk.CTkFrame(ic, fg_color="transparent")
        alt.pack(fill="x")

        ctk.CTkButton(alt, text="Kayıt Oluştur", height=40, command=self.kayit_ol).pack(side="left")
        ctk.CTkButton(alt, text="Kapat", height=40, fg_color="gray", hover_color="#555555", command=self.destroy).pack(side="left", padx=12)

    def kayit_ol(self):
        kullanici_adi = self.ent_kullanici.get().strip()
        sifre = self.ent_sifre.get().strip()
        sifre2 = self.ent_sifre2.get().strip()

        if not kullanici_adi or not sifre or not sifre2:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return

        if sifre != sifre2:
            messagebox.showwarning("Uyarı", "Şifreler eşleşmiyor.")
            return


        ok, msg = kullanici_ekle(kullanici_adi, sifre)

        if ok:
            messagebox.showinfo("Başarılı", "Kayıt oluşturuldu. Şimdi giriş yapabilirsiniz.")

            if callable(self.kayit_basarili_callback):
                try:
                    self.kayit_basarili_callback(kullanici_adi)
                except Exception:
                    pass

            self.destroy()


            try:
                self.parent.lift()
                self.parent.focus_force()
                self.parent.attributes("-topmost", True)
                self.parent.after(150, lambda: self.parent.attributes("-topmost", False))
            except Exception:
                pass
        else:
            messagebox.showerror("Hata", msg)
