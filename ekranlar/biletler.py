import customtkinter as ctk
from tkinter import messagebox

from ayarlar.sabitler import RENK_ANA, RENK_ANA_HOVER
from veritabani.sorgular import ucuslari_getir, yolculari_getir, bilet_kes
from ayarlar.sabitler import logo_ekle


class BiletlerEkrani(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("AirportGo - Bilet Oluştur")
        self.geometry("560x560")
        self.resizable(False, False)
        logo_ekle(self, boyut=(70, 70))

        self.lift()
        self.focus_force()
        self.grab_set()


        ust = ctk.CTkFrame(self, corner_radius=14)
        ust.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(
            ust,
            text="Bilet Oluştur",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=16, pady=(14, 2))

        ctk.CTkLabel(
            ust,
            text="Uçuş ve yolcu seçin, koltuk numarası girin ve bileti kaydedin.",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(anchor="w", padx=16, pady=(0, 14))


        kart = ctk.CTkFrame(self, corner_radius=14)
        kart.pack(fill="both", expand=True, padx=16, pady=(0, 16))


        ic = ctk.CTkFrame(kart, corner_radius=0, fg_color="transparent")
        ic.pack(fill="both", expand=True, padx=18, pady=18)


        ctk.CTkLabel(ic, text="Uçuş", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 6))

        self.ucuslar = ucuslari_getir(sadece_aktif=False)  # şimdilik filtresiz
        self.ucus_map = {
            f"{u['ucus_kodu']} | {u['kalkis_havalimani']} → {u['varis_havalimani']}": u["id"]
            for u in self.ucuslar
        }

        self.cmb_ucus = ctk.CTkComboBox(ic, values=list(self.ucus_map.keys()), width=480)
        self.cmb_ucus.pack(pady=(0, 16))


        ctk.CTkLabel(ic, text="Yolcu", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 6))

        self.yolcular = yolculari_getir(sadece_aktif=False)  # şimdilik filtresiz
        self.yolcu_map = {
            f"{y['ad']} {y['soyad']} (ID {y['id']})": y["id"]
            for y in self.yolcular
        }

        self.cmb_yolcu = ctk.CTkComboBox(ic, values=list(self.yolcu_map.keys()), width=480)
        self.cmb_yolcu.pack(pady=(0, 16))


        ctk.CTkLabel(ic, text="Koltuk Numarası", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 6))

        self.ent_koltuk = ctk.CTkEntry(ic, placeholder_text="Örn: 12A", width=220)
        self.ent_koltuk.pack(anchor="w", pady=(0, 18))


        alt = ctk.CTkFrame(ic, corner_radius=0, fg_color="transparent")
        alt.pack(fill="x", pady=(6, 0))

        self.btn_kaydet = ctk.CTkButton(
            alt,
            text="Bileti Kaydet",
            command=self.bilet_kes_tikla,
            fg_color=RENK_ANA,
            hover_color=RENK_ANA_HOVER,
            height=40,
            width=220
        )
        self.btn_kaydet.pack(side="left")

        ctk.CTkButton(
            alt,
            text="Kapat",
            command=self.destroy,
            fg_color="gray",
            hover_color="#555555",
            height=40,
            width=140
        ).pack(side="left", padx=12)


        self.after(10, self._ilk_degerleri_ayarla)

    def _ilk_degerleri_ayarla(self):
        if not self.winfo_exists():
            return

        eksikler = []

        if len(self.ucus_map) == 0:
            eksikler.append("Uçuş bulunamadı. Önce uçuş ekleyin.")
        else:
            self.cmb_ucus.set(list(self.ucus_map.keys())[0])

        if len(self.yolcu_map) == 0:
            eksikler.append("Yolcu bulunamadı. Önce yolcu ekleyin.")
        else:
            self.cmb_yolcu.set(list(self.yolcu_map.keys())[0])

        if eksikler:
            try:
                if self.btn_kaydet.winfo_exists():
                    self.btn_kaydet.configure(state="disabled")
            except Exception:
                pass

            self.after(10, lambda: messagebox.showwarning("Uyarı", "\n".join(eksikler)))

    def bilet_kes_tikla(self):
        ucus_etiket = self.cmb_ucus.get()
        yolcu_etiket = self.cmb_yolcu.get()
        koltuk_no = self.ent_koltuk.get().strip()

        if not ucus_etiket or ucus_etiket not in self.ucus_map:
            messagebox.showwarning("Uyarı", "Lütfen bir uçuş seçin.")
            return

        if not yolcu_etiket or yolcu_etiket not in self.yolcu_map:
            messagebox.showwarning("Uyarı", "Lütfen bir yolcu seçin.")
            return

        if not koltuk_no:
            messagebox.showwarning("Uyarı", "Koltuk numarası girin (örn: 12A).")
            return

        ucus_id = self.ucus_map[ucus_etiket]
        yolcu_id = self.yolcu_map[yolcu_etiket]

        ok, msg = bilet_kes(ucus_id, yolcu_id, koltuk_no)
        if ok:
            messagebox.showinfo("Başarılı", msg)
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
