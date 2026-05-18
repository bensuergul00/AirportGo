import customtkinter as ctk
from tkinter import messagebox

from veritabani.sorgular import (
    ucuslari_getir,
    ucus_ekle,
    ucus_iptal_et,
    ucus_getir_by_id,
    ucus_guncelle
)


class UcuslarEkrani(ctk.CTkToplevel):
    def __init__(self, parent: object, rol: object = "personel") -> None:
        super().__init__(parent)
        self.rol = rol

        self.title("AirportGo - Uçuşlar")
        self.geometry("1000x580")
        self.resizable(False, False)

        self.lift()
        self.focus_force()
        self.grab_set()

        self.secili_ucus_id = None
        self.sadece_aktif = True  # varsayılan: iptal olanları gizle
        self.satirlar = {}        # {ucus_id: frame} seçimi göstermek için

        ctk.CTkLabel(self, text="Uçuşlar", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=12)

        ust = ctk.CTkFrame(self, corner_radius=12)
        ust.pack(fill="x", padx=15, pady=10)

        ctk.CTkButton(ust, text="Yenile", command=self.yenile).pack(side="left", padx=10, pady=10)

        self.btn_ekle = ctk.CTkButton(ust, text="Uçuş Ekle", command=self.ucus_ekle_penceresi)
        self.btn_ekle.pack(side="left", padx=10, pady=10)

        self.btn_guncelle = ctk.CTkButton(ust, text="Uçuş Güncelle", command=self.ucus_guncelle_penceresi)
        self.btn_guncelle.pack(side="left", padx=10, pady=10)

        self.btn_iptal = ctk.CTkButton(ust, text="Seçili Uçuşu İptal Et", command=self.secili_ucusu_iptal_et)
        self.btn_iptal.pack(side="left", padx=10, pady=10)

        self.secim_yazi = ctk.CTkLabel(ust, text="Seçili Uçuş: Yok", font=ctk.CTkFont(size=13))
        self.secim_yazi.pack(side="right", padx=12)


        self.var_iptal_goster = ctk.BooleanVar(value=False)
        self.sw_iptal = ctk.CTkSwitch(
            ust,
            text="İptal Edilenleri Göster",
            variable=self.var_iptal_goster,
            command=self.iptal_goster_degisti
        )
        self.sw_iptal.pack(side="right", padx=12, pady=10)

        self.liste_frame = ctk.CTkScrollableFrame(self, corner_radius=12, height=420)
        self.liste_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.yenile()


        if self.rol != "admin":
            self.btn_ekle.configure(state="disabled")
            self.btn_guncelle.configure(state="disabled")
            self.btn_iptal.configure(state="disabled")

    def iptal_goster_degisti(self):

        self.sadece_aktif = not self.var_iptal_goster.get()
        self.secili_ucus_id = None
        self.yenile()

    def yenile(self):
        for w in self.liste_frame.winfo_children():
            w.destroy()

        self.satirlar.clear()
        self.secili_ucus_id = None
        self.secim_yazi.configure(text="Seçili Uçuş: Yok")


        header = ctk.CTkFrame(self.liste_frame, corner_radius=8)
        header.pack(fill="x", padx=8, pady=(8, 4))

        basliklar = ["ID", "Uçuş Kodu", "Kalkış", "Varış", "Kalkış Saati", "Varış Saati", "Kapasite", "Durum"]
        genislikler = [50, 110, 140, 140, 160, 160, 90, 80]

        for i, (b, g) in enumerate(zip(basliklar, genislikler)):
            ctk.CTkLabel(
                header, text=b, width=g, anchor="w",
                font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=i, padx=6, pady=8)

        ucuslar = ucuslari_getir(sadece_aktif=self.sadece_aktif)

        if not ucuslar:
            bilgi = "Aktif uçuş bulunamadı." if self.sadece_aktif else "Uçuş bulunamadı."
            ctk.CTkLabel(self.liste_frame, text=bilgi, font=ctk.CTkFont(size=14)).pack(pady=30)
            return

        for u in ucuslar:
            satir = ctk.CTkFrame(self.liste_frame, corner_radius=10, border_width=1)


            if u.get("durum") == "iptal":
                satir.configure(border_width=2)

            satir.pack(fill="x", padx=8, pady=4)

            self.satirlar[u["id"]] = satir

            degerler = [
                u["id"],
                u["ucus_kodu"],
                u["kalkis_havalimani"],
                u["varis_havalimani"],
                str(u["kalkis_saati"]),
                str(u["varis_saati"]),
                u["kapasite"],
                u.get("durum", "aktif")
            ]

            for i, (val, g) in enumerate(zip(degerler, genislikler)):
                ctk.CTkLabel(satir, text=str(val), width=g, anchor="w").grid(
                    row=0, column=i, padx=6, pady=8
                )


            satir.bind("<Button-1>", lambda e, ucus_id=u["id"]: self.sec(ucus_id))
            for child in satir.winfo_children():
                child.bind("<Button-1>", lambda e, ucus_id=u["id"]: self.sec(ucus_id))

    def _clear_highlights(self):
        for frame in self.satirlar.values():
            frame.configure(border_width=1)

    def _highlight(self, ucus_id: int):
        self._clear_highlights()
        frame = self.satirlar.get(ucus_id)
        if frame:
            frame.configure(border_width=3)

    def sec(self, ucus_id: int):
        self.secili_ucus_id = ucus_id
        self._highlight(ucus_id)
        self.secim_yazi.configure(text=f"Seçili Uçuş: ID {ucus_id}")

    def ucus_ekle_penceresi(self):
        pencere = ctk.CTkToplevel(self)
        pencere.title("AirportGo - Uçuş Ekle")
        pencere.geometry("420x420")
        pencere.resizable(False, False)

        pencere.lift()
        pencere.focus_force()
        pencere.grab_set()

        ctk.CTkLabel(pencere, text="Uçuş Ekle", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        e_kod = ctk.CTkEntry(pencere, placeholder_text="Uçuş Kodu (ör: TK123)")
        e_kod.pack(pady=8)

        e_kalkis = ctk.CTkEntry(pencere, placeholder_text="Kalkış Havalimanı (ör: İzmir)")
        e_kalkis.pack(pady=8)

        e_varis = ctk.CTkEntry(pencere, placeholder_text="Varış Havalimanı (ör: İstanbul)")
        e_varis.pack(pady=8)

        e_ks = ctk.CTkEntry(pencere, placeholder_text="Kalkış Saati (YYYY-AA-GG SS:DD:SS)")
        e_ks.pack(pady=8)

        e_vs = ctk.CTkEntry(pencere, placeholder_text="Varış Saati (YYYY-AA-GG SS:DD:SS)")
        e_vs.pack(pady=8)

        e_kap = ctk.CTkEntry(pencere, placeholder_text="Kapasite (ör: 180)")
        e_kap.pack(pady=8)

        def kaydet():
            try:
                kapasite = int(e_kap.get().strip())
            except Exception:
                messagebox.showerror("Hata", "Kapasite sayı olmalı.")
                return

            ok, msg = ucus_ekle(
                e_kod.get().strip(),
                e_kalkis.get().strip(),
                e_varis.get().strip(),
                e_ks.get().strip(),
                e_vs.get().strip(),
                kapasite
            )

            if ok:
                messagebox.showinfo("Başarılı", msg)
                pencere.destroy()
                self.yenile()

                self.lift()
                self.focus_force()
                self.attributes("-topmost", True)
                self.after(150, lambda: self.attributes("-topmost", False))
            else:
                messagebox.showerror("Hata", msg)

        ctk.CTkButton(pencere, text="Kaydet", command=kaydet).pack(pady=16)

    def secili_ucusu_iptal_et(self):
        if not self.secili_ucus_id:
            messagebox.showwarning("Uyarı", "Önce listeden bir uçuş seçmelisiniz.")
            return

        if not messagebox.askyesno("Onay", f"Uçuş (ID: {self.secili_ucus_id}) iptal edilsin mi?"):
            return

        ok, msg = ucus_iptal_et(self.secili_ucus_id)
        if ok:
            messagebox.showinfo("Başarılı", msg)
            self.secili_ucus_id = None
            self.yenile()

            self.lift()
            self.focus_force()
            self.attributes("-topmost", True)
            self.after(150, lambda: self.attributes("-topmost", False))
        else:
            messagebox.showerror("Hata", msg)

    def ucus_guncelle_penceresi(self):
        if not self.secili_ucus_id:
            messagebox.showwarning("Uyarı", "Önce listeden bir uçuş seçmelisiniz.")
            return

        veri = ucus_getir_by_id(self.secili_ucus_id)
        if not veri:
            messagebox.showerror("Hata", "Seçili uçuş bulunamadı.")
            return

        pencere = ctk.CTkToplevel(self)
        pencere.title("AirportGo - Uçuş Güncelle")
        pencere.geometry("420x440")
        pencere.resizable(False, False)

        pencere.lift()
        pencere.focus_force()
        pencere.grab_set()

        ctk.CTkLabel(pencere, text="Uçuş Güncelle", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        e_kod = ctk.CTkEntry(pencere); e_kod.pack(pady=8); e_kod.insert(0, str(veri["ucus_kodu"]))
        e_kalkis = ctk.CTkEntry(pencere); e_kalkis.pack(pady=8); e_kalkis.insert(0, str(veri["kalkis_havalimani"]))
        e_varis = ctk.CTkEntry(pencere); e_varis.pack(pady=8); e_varis.insert(0, str(veri["varis_havalimani"]))
        e_ks = ctk.CTkEntry(pencere); e_ks.pack(pady=8); e_ks.insert(0, str(veri["kalkis_saati"]))
        e_vs = ctk.CTkEntry(pencere); e_vs.pack(pady=8); e_vs.insert(0, str(veri["varis_saati"]))
        e_kap = ctk.CTkEntry(pencere); e_kap.pack(pady=8); e_kap.insert(0, str(veri["kapasite"]))

        def kaydet():
            try:
                kapasite = int(e_kap.get().strip())
            except Exception:
                messagebox.showerror("Hata", "Kapasite sayı olmalı.")
                return

            ok, msg = ucus_guncelle(
                self.secili_ucus_id,
                e_kod.get().strip(),
                e_kalkis.get().strip(),
                e_varis.get().strip(),
                e_ks.get().strip(),
                e_vs.get().strip(),
                kapasite
            )

            if ok:
                messagebox.showinfo("Başarılı", msg)
                pencere.destroy()
                self.yenile()

                self.lift()
                self.focus_force()
                self.attributes("-topmost", True)
                self.after(150, lambda: self.attributes("-topmost", False))
            else:
                messagebox.showerror("Hata", msg)

        ctk.CTkButton(pencere, text="Güncelle", command=kaydet).pack(pady=16)
