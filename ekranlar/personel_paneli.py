import customtkinter as ctk
from tkinter import messagebox

from ekranlar.ucuslar import UcuslarEkrani
from ekranlar.biletler import BiletlerEkrani
from ekranlar.yolcular import YolcularEkrani
from ayarlar.sabitler import logo_ekle


class PersonelPaneli(ctk.CTkToplevel):
    def __init__(self, parent, kullanici_bilgi: dict):
        super().__init__(parent)
        self.kullanici_bilgi = kullanici_bilgi

        self.title("AirportGo - Personel Paneli")
        self.geometry("900x520")
        self.resizable(False, False)
        logo_ekle(self, boyut=(70, 70))


        self.lift()
        self.focus_force()
        self.grab_set()

        ust = ctk.CTkFrame(self, corner_radius=12)
        ust.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            ust,
            text="AirportGo",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 0))

        ctk.CTkLabel(
            ust,
            text=f"Personel: {self.kullanici_bilgi.get('kullanici_adi')}  |  Panel: İşlemler",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=(0, 10))

        orta = ctk.CTkFrame(self, corner_radius=12)
        orta.pack(fill="both", expand=True, padx=15, pady=(0, 15))


        sol = ctk.CTkFrame(orta, width=220, corner_radius=12)
        sol.pack(side="left", fill="y", padx=12, pady=12)
        sol.pack_propagate(False)

        ctk.CTkLabel(sol, text="Menü", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))

        ctk.CTkButton(sol, text="Uçuşlar", command=self.ucuslar_ac).pack(pady=8, padx=15, fill="x")
        ctk.CTkButton(sol, text="Yolcular", command=self.yolcular_ac).pack(pady=8, padx=15, fill="x")
        ctk.CTkButton(sol, text="Bilet Oluştur ", command=self.bilet_kes_ac).pack(pady=8, padx=15, fill="x")

        ctk.CTkButton(
            sol,
            text="Çıkış Yap",
            fg_color="gray",
            hover_color="#555555",
            command=self.cikis_yap
        ).pack(pady=(25, 10), padx=15, fill="x")


        sag = ctk.CTkFrame(orta, corner_radius=12)
        sag.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=12)

        ctk.CTkLabel(
            sag,
            text="Hızlı İşlemler",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            sag,
            text="Bu panel, personelin operasyonel işlemlerini\n"
        "yürütebilmesi için tasarlanmıştır.\n\n"
        "• Mevcut uçuşları görüntüleme\n"
        "• Yolcular adına bilet oluşturma\n\n"
        "İlgili işlemi soldaki menüden seçebilirsiniz.",
            justify="left",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=10)

    def ucuslar_ac(self):
        UcuslarEkrani(self, rol="personel")

    def yolcular_ac(self):
        YolcularEkrani(self, rol="personel")

    def bilet_kes_ac(self):
        BiletlerEkrani(self)

    def cikis_yap(self):
        if messagebox.askyesno("Çıkış", "Çıkış yapmak istiyor musunuz?"):
            self.destroy()
