import customtkinter as ctk
from tkinter import messagebox

from veritabani.sorgular import (
    yolculari_getir, yolcu_ekle, yolcu_getir_by_id, yolcu_guncelle, yolcu_pasif_et
)
from ayarlar.sabitler import logo_ekle


class YolcularEkrani(ctk.CTkToplevel):
    def __init__(self, parent, rol="personel"):
        super().__init__(parent)
        self.rol = rol

        self.title("AirportGo - Yolcular")
        self.geometry("1000x580")
        self.resizable(False, False)
        logo_ekle(self, boyut=(70, 70))

        self.lift()
        self.focus_force()
        self.grab_set()

        self.secili_yolcu_id = None
        self.satirlar = {}

        ctk.CTkLabel(self, text="Yolcular", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=12)

        ust = ctk.CTkFrame(self, corner_radius=12)
        ust.pack(fill="x", padx=15, pady=10)

        ctk.CTkButton(ust, text="Yenile", command=self.yenile).pack(side="left", padx=10, pady=10)

        self.btn_ekle = ctk.CTkButton(ust, text="Yolcu Ekle", command=self.yolcu_ekle_penceresi)
        self.btn_ekle.pack(side="left", padx=10, pady=10)

        self.btn_guncelle = ctk.CTkButton(ust, text="Yolcu Güncelle", command=self.yolcu_guncelle_penceresi)
        self.btn_guncelle.pack(side="left", padx=10, pady=10)

        self.btn_pasif = ctk.CTkButton(
            ust, text="Seçili Yolcuyu Pasif Et",
            fg_color="#B00020", hover_color="#8a0019",
            command=self.secili_yolcuyu_pasif_et
        )
        self.btn_pasif.pack(side="left", padx=10, pady=10)

        self.secim_yazi = ctk.CTkLabel(ust, text="Seçili Yolcu: Yok", font=ctk.CTkFont(size=13))
        self.secim_yazi.pack(side="right", padx=12)

        self.liste_frame = ctk.CTkScrollableFrame(self, corner_radius=12, height=420)
        self.liste_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.yenile()

    def yenile(self):
        for w in self.liste_frame.winfo_children():
            w.destroy()

        self.satirlar.clear()
        self.secili_yolcu_id = None
        self.secim_yazi.configure(text="Seçili Yolcu: Yok")

        header = ctk.CTkFrame(self.liste_frame, corner_radius=8)
        header.pack(fill="x", padx=8, pady=(8, 4))

        basliklar = ["ID", "Ad", "Soyad", "TC No", "Telefon", "Durum"]
        genislikler = [60, 160, 160, 160, 160, 80]

        for i, (b, g) in enumerate(zip(basliklar, genislikler)):
            ctk.CTkLabel(header, text=b, width=g, anchor="w", font=ctk.CTkFont(weight="bold")).grid(
                row=0, column=i, padx=6, pady=8
            )

        yolcular = yolculari_getir(sadece_aktif=True)

        if not yolcular:
            ctk.CTkLabel(self.liste_frame, text="Aktif yolcu bulunamadı.", font=ctk.CTkFont(size=14)).pack(pady=30)
            return

        for y in yolcular:
            satir = ctk.CTkFrame(self.liste_frame, corner_radius=10, border_width=1)
            satir.pack(fill="x", padx=8, pady=4)

            self.satirlar[y["id"]] = satir

            degerler = [
                y["id"], y["ad"], y["soyad"],
                y.get("tc_no") if y.get("tc_no") is not None else "",
                y.get("telefon") if y.get("telefon") is not None else "",
                y.get("durum", "")
            ]
            for i, (val, g) in enumerate(zip(degerler, genislikler)):
                ctk.CTkLabel(satir, text=str(val), width=g, anchor="w").grid(row=0, column=i, padx=6, pady=8)

            def sec(yid=y["id"]):
                self.secili_yolcu_id = yid
                self.secim_yazi.configure(text=f"Seçili Yolcu: ID {yid}")

                for sid, fr in self.satirlar.items():
                    fr.configure(border_width=1)
                self.satirlar[yid].configure(border_width=3)

            satir.bind("<Button-1>", lambda e, f=sec: f())
            for child in satir.winfo_children():
                child.bind("<Button-1>", lambda e, f=sec: f())

    def yolcu_ekle_penceresi(self):
        pencere = ctk.CTkToplevel(self)
        pencere.title("AirportGo - Yolcu Ekle")
        pencere.geometry("420x420")
        pencere.resizable(False, False)

        pencere.lift()
        pencere.focus_force()
        pencere.grab_set()

        ctk.CTkLabel(pencere, text="Yolcu Ekle", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        e_ad = ctk.CTkEntry(pencere, placeholder_text="Ad")
        e_ad.pack(pady=8)

        e_soyad = ctk.CTkEntry(pencere, placeholder_text="Soyad")
        e_soyad.pack(pady=8)

        e_tc = ctk.CTkEntry(pencere, placeholder_text="TC No (opsiyonel)")
        e_tc.pack(pady=8)

        e_tel = ctk.CTkEntry(pencere, placeholder_text="Telefon (opsiyonel)")
        e_tel.pack(pady=8)

        def kaydet():
            ok, msg = yolcu_ekle(
                e_ad.get().strip(),
                e_soyad.get().strip(),
                e_tc.get().strip(),
                e_tel.get().strip()
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

    def yolcu_guncelle_penceresi(self):
        if not self.secili_yolcu_id:
            messagebox.showwarning("Uyarı", "Önce listeden bir yolcu seçmelisiniz.")
            return

        veri = yolcu_getir_by_id(self.secili_yolcu_id)
        if not veri:
            messagebox.showerror("Hata", "Seçili yolcu bulunamadı.")
            return

        pencere = ctk.CTkToplevel(self)
        pencere.title("AirportGo - Yolcu Güncelle")
        pencere.geometry("420x420")
        pencere.resizable(False, False)

        pencere.lift()
        pencere.focus_force()
        pencere.grab_set()

        ctk.CTkLabel(pencere, text="Yolcu Güncelle", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        e_ad = ctk.CTkEntry(pencere); e_ad.pack(pady=8); e_ad.insert(0, str(veri["ad"]))
        e_soyad = ctk.CTkEntry(pencere); e_soyad.pack(pady=8); e_soyad.insert(0, str(veri["soyad"]))
        e_tc = ctk.CTkEntry(pencere); e_tc.pack(pady=8); e_tc.insert(0, "" if veri.get("tc_no") is None else str(veri["tc_no"]))
        e_tel = ctk.CTkEntry(pencere); e_tel.pack(pady=8); e_tel.insert(0, "" if veri.get("telefon") is None else str(veri["telefon"]))

        def kaydet():
            ok, msg = yolcu_guncelle(
                self.secili_yolcu_id,
                e_ad.get().strip(),
                e_soyad.get().strip(),
                e_tc.get().strip(),
                e_tel.get().strip()
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

    def secili_yolcuyu_pasif_et(self):
        if not self.secili_yolcu_id:
            messagebox.showwarning("Uyarı", "Önce listeden bir yolcu seçmelisiniz.")
            return

        if not messagebox.askyesno("Onay", "Seçili yolcuyu pasif etmek istiyor musunuz?"):
            return

        ok, msg = yolcu_pasif_et(self.secili_yolcu_id)
        if ok:
            messagebox.showinfo("Başarılı", msg)
            self.secili_yolcu_id = None
            self.yenile()

            self.lift()
            self.focus_force()
            self.attributes("-topmost", True)
            self.after(150, lambda: self.attributes("-topmost", False))
        else:
            messagebox.showerror("Hata", msg)

