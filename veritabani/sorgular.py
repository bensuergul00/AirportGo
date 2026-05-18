import hashlib
from veritabani.baglanti import baglanti_al


def sifre_hashle(sifre: str) -> str:
    return hashlib.sha256(sifre.encode("utf-8")).hexdigest()


def kullanici_ekle(kullanici_adi: str, sifre: str, rol: str = "personel") -> tuple[bool, str]:

    if not kullanici_adi or not sifre:
        return False, "Kullanıcı adı ve şifre boş olamaz."

    if rol not in ("admin", "personel"):
        return False, "Rol geçersiz."

    conn = baglanti_al()
    if not conn:
        return False, "Veritabanı bağlantısı kurulamadı."

    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO kullanicilar (kullanici_adi, sifre, rol)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (kullanici_adi.strip(), sifre_hashle(sifre), rol))
        conn.commit()
        return True, "Kayıt başarılı."

    except Exception as e:
        if "Duplicate" in str(e) or "unique" in str(e).lower():
            return False, "Bu kullanıcı adı zaten kayıtlı."
        return False, f"Hata oluştu: {e}"

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def giris_kontrol(kullanici_adi: str, sifre: str) -> tuple[bool, str, dict]:
    if not kullanici_adi or not sifre:
        return False, "Kullanıcı adı ve şifre boş olamaz.", {}

    conn = baglanti_al()
    if not conn:
        return False, "Veritabanı bağlantısı kurulamadı.", {}

    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT id, kullanici_adi, rol, sifre
            FROM kullanicilar
            WHERE kullanici_adi = %s
            LIMIT 1
        """
        cursor.execute(sql, (kullanici_adi.strip(),))
        user = cursor.fetchone()

        if not user:
            return False, "Kullanıcı bulunamadı.", {}

        if user["sifre"] != sifre_hashle(sifre):
            return False, "Şifre hatalı.", {}

        user.pop("sifre", None)
        return True, "Giriş başarılı.", user

    except Exception as e:
        return False, f"Hata oluştu: {e}", {}

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def admin_var_mi() -> bool:

    conn = baglanti_al()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM kullanicilar WHERE rol='admin'")
        (adet,) = cursor.fetchone()
        return adet > 0

    except Exception:
        return False

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass




def ucuslari_getir(sadece_aktif: bool = False) -> list[dict]:
    """Uçuşları listeler."""
    conn = baglanti_al()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        if sadece_aktif:
            cursor.execute("SELECT * FROM ucuslar WHERE durum='aktif' ORDER BY kalkis_saati DESC")
        else:
            cursor.execute("SELECT * FROM ucuslar ORDER BY kalkis_saati DESC")
        return cursor.fetchall()

    except Exception as e:
        print("Uçuşlar getirilemedi:", e)
        return []

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def ucus_ekle(ucus_kodu: str, kalkis: str, varis: str, kalkis_saati: str, varis_saati: str, kapasite: int) -> tuple[bool, str]:

    if not all([ucus_kodu, kalkis, varis, kalkis_saati, varis_saati]) or kapasite is None:
        return False, "Tüm alanlar doldurulmalıdır."

    conn = baglanti_al()
    if not conn:
        return False, "Veritabanı bağlantısı kurulamadı."

    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO ucuslar (ucus_kodu, kalkis_havalimani, varis_havalimani, kalkis_saati, varis_saati, kapasite, durum)
            VALUES (%s, %s, %s, %s, %s, %s, 'aktif')
        """
        cursor.execute(sql, (ucus_kodu.strip(), kalkis.strip(), varis.strip(), kalkis_saati.strip(), varis_saati.strip(), kapasite))
        conn.commit()
        return True, "Uçuş eklendi."

    except Exception as e:
        if "Duplicate" in str(e) or "unique" in str(e).lower():
            return False, "Bu uçuş kodu zaten kayıtlı."
        return False, f"Hata: {e}"

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def ucus_getir_by_id(ucus_id: int) -> dict | None:

    conn = baglanti_al()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ucuslar WHERE id=%s LIMIT 1", (ucus_id,))
        return cursor.fetchone()

    except Exception as e:
        print("Uçuş getirilemedi:", e)
        return None

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def ucus_guncelle(ucus_id: int, ucus_kodu: str, kalkis: str, varis: str, kalkis_saati: str, varis_saati: str, kapasite: int) -> tuple[bool, str]:
    conn = baglanti_al()
    if not conn:
        return False, "Veritabanı bağlantısı kurulamadı."

    try:
        cursor = conn.cursor()
        sql = """
            UPDATE ucuslar
            SET ucus_kodu=%s,
                kalkis_havalimani=%s,
                varis_havalimani=%s,
                kalkis_saati=%s,
                varis_saati=%s,
                kapasite=%s
            WHERE id=%s
        """
        cursor.execute(sql, (ucus_kodu.strip(), kalkis.strip(), varis.strip(), kalkis_saati.strip(), varis_saati.strip(), kapasite, ucus_id))
        conn.commit()

        if cursor.rowcount == 0:
            return False, "Uçuş bulunamadı veya değişiklik yapılmadı."
        return True, "Uçuş güncellendi."

    except Exception as e:
        if "Duplicate" in str(e) or "unique" in str(e).lower():
            return False, "Bu uçuş kodu zaten kayıtlı."
        return False, f"Hata: {e}"

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def ucus_iptal_et(ucus_id: int) -> tuple[bool, str]:
    conn = baglanti_al()
    if not conn:
        return False, "Veritabanı bağlantısı kurulamadı."

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE ucuslar SET durum='iptal' WHERE id=%s", (ucus_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return False, "Uçuş bulunamadı."
        return True, "Uçuş iptal edildi."

    except Exception as e:
        return False, f"Hata: {e}"

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass




def yolculari_getir(sadece_aktif: bool = True) -> list[dict]:
    conn = baglanti_al()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        if sadece_aktif:
            cursor.execute("SELECT * FROM yolcular WHERE durum='aktif' ORDER BY id DESC")
        else:
            cursor.execute("SELECT * FROM yolcular ORDER BY id DESC")
        return cursor.fetchall()

    except Exception as e:
        print("Yolcular getirilemedi:", e)
        return []

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def yolcu_ekle(ad: str, soyad: str, tc_no: str = "", telefon: str = "") -> tuple[bool, str]:
    if not ad or not soyad:
        return False, "Ad ve soyad zorunludur."

    conn = baglanti_al()
    if not conn:
        return False, "Veritabanı bağlantısı kurulamadı."

    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO yolcular (ad, soyad, tc_no, telefon, durum)
            VALUES (%s, %s, %s, %s, 'aktif')
        """
        tc_deger = tc_no.strip() if tc_no and tc_no.strip() else None
        cursor.execute(sql, (ad.strip(), soyad.strip(), tc_deger, telefon.strip()))
        conn.commit()
        return True, "Yolcu eklendi."

    except Exception as e:
        if "Duplicate" in str(e) or "unique" in str(e).lower():
            return False, "Bu TC No zaten kayıtlı."
        return False, f"Hata: {e}"

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def yolcu_getir_by_id(yolcu_id: int) -> dict | None:

    conn = baglanti_al()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM yolcular WHERE id=%s LIMIT 1", (yolcu_id,))
        return cursor.fetchone()

    except Exception as e:
        print("Yolcu getirilemedi:", e)
        return None

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def yolcu_guncelle(yolcu_id: int, ad: str, soyad: str, tc_no: str = "", telefon: str = "") -> tuple[bool, str]:

    if not ad or not soyad:
        return False, "Ad ve soyad zorunludur."

    conn = baglanti_al()
    if not conn:
        return False, "Veritabanı bağlantısı kurulamadı."

    try:
        cursor = conn.cursor()
        sql = """
            UPDATE yolcular
            SET ad=%s, soyad=%s, tc_no=%s, telefon=%s
            WHERE id=%s
        """
        tc_deger = tc_no.strip() if tc_no and tc_no.strip() else None
        cursor.execute(sql, (ad.strip(), soyad.strip(), tc_deger, telefon.strip(), yolcu_id))
        conn.commit()

        if cursor.rowcount == 0:
            return False, "Yolcu bulunamadı veya değişiklik yapılmadı."
        return True, "Yolcu güncellendi."

    except Exception as e:
        if "Duplicate" in str(e) or "unique" in str(e).lower():
            return False, "Bu TC No zaten kayıtlı."
        return False, f"Hata: {e}"

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def yolcu_pasif_et(yolcu_id: int) -> tuple[bool, str]:
    conn = baglanti_al()
    if not conn:
        return False, "Veritabanı bağlantısı kurulamadı."

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE yolcular SET durum='pasif' WHERE id=%s", (yolcu_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return False, "Yolcu bulunamadı."
        return True, "Yolcu pasif edildi."

    except Exception as e:
        return False, f"Hata: {e}"

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

def bilet_kes(ucus_id: int, yolcu_id: int, koltuk_no: str) -> tuple[bool, str]:
    if not koltuk_no or not koltuk_no.strip():
        return False, "Koltuk numarası boş olamaz."

    conn = baglanti_al()
    if not conn:
        return False, "Veritabanı bağlantısı kurulamadı."

    try:
        cursor = conn.cursor()

        sql = """
            INSERT INTO biletler (ucus_id, yolcu_id, koltuk_no)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (ucus_id, yolcu_id, koltuk_no.strip()))
        conn.commit()
        return True, "Bilet başarıyla kesildi."

    except Exception as e:
        if "Duplicate" in str(e) or "unique" in str(e).lower():
            return False, "Bu koltuk numarası zaten kullanılmış."
        return False, f"Hata: {e}"

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass
