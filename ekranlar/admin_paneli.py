import customtkinter as ctk
from tkinter import messagebox

from ekranlar.ucuslar import UcuslarEkrani
from ekranlar.yolcular import YolcularEkrani
from ekranlar.biletler import BiletlerEkrani
from ayarlar.sabitler import logo_ekle


class AdminPaneli(ctk.CTkToplevel):
    def __init__(self, parent, kullanici_bilgi: dict):
        super().__init__(parent)
        self.kullanici_bilgi = kullanici_bilgi
        self.title("AirportGo - Admin Paneli")
        self.geometry("900x520")
        self.resizable(False, False)
        logo_ekle(self, boyut=(70, 70))


        ust = ctk.CTkFrame(self, corner_radius=12)
        ust.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            ust,
            text="AirportGo",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 0))

        ctk.CTkLabel(
            ust,
            text=f"Admin: {self.kullanici_bilgi.get('kullanici_adi')}  |  Panel: Yönetim",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=(0, 10))


        orta = ctk.CTkFrame(self, corner_radius=12)
        orta.pack(fill="both", expand=True, padx=15, pady=(0, 15))


        sol = ctk.CTkFrame(orta, width=220, corner_radius=12)
        sol.pack(side="left", fill="y", padx=12, pady=12)
        sol.pack_propagate(False)

        ctk.CTkLabel(sol, text="Menü", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))

        ctk.CTkButton(sol, text="Uçuş Yönetimi", command=self.ucuslar_ac).pack(pady=8, padx=15, fill="x")
        ctk.CTkButton(sol, text="Yolcu Yönetimi", command=self.yolcular_ac).pack(pady=8, padx=15, fill="x")
        ctk.CTkButton(sol, text="Bilet Yönetimi", command=self.biletler_ac).pack(pady=8, padx=15, fill="x")

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
            text="Yönetim Paneli",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            sag,
            text="Bu panel üzerinden sistemin tüm yönetim işlemleri gerçekleştirilebilir.\n\n"
        "• Uçuşların eklenmesi, güncellenmesi ve iptal edilmesi\n"
        "• Yolcu kayıtlarının oluşturulması ve görüntülenmesi\n"
        "• Bilet işlemlerinin yönetimi\n\n"
        "Soldaki menüden ilgili modülü seçerek işleme devam edebilirsiniz.",
            justify="left",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=10)



    def ucuslar_ac(self):
        UcuslarEkrani(self, rol="admin")

    def yolcular_ac(self):
        YolcularEkrani(self)

    def biletler_ac(self):
        BiletlerEkrani(self)

    def cikis_yap(self):
        if messagebox.askyesno("Çıkış", "Çıkış yapmak istiyor musunuz?"):
            self.destroy()


from ekranlar.yolcular import YolcularEkrani

def yolcular_ac(self):
    YolcularEkrani(self, rol="admin")
