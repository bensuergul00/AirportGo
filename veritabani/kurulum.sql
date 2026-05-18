
CREATE DATABASE IF NOT EXISTS airport_go_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_turkish_ci;

USE airport_go_db;


CREATE TABLE kullanicilar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kullanici_adi VARCHAR(50) NOT NULL UNIQUE,
    sifre VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'personel') NOT NULL,
    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE ucuslar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ucus_kodu VARCHAR(20) NOT NULL UNIQUE,
    kalkis_havalimani VARCHAR(100) NOT NULL,
    varis_havalimani VARCHAR(100) NOT NULL,
    kalkis_saati DATETIME NOT NULL,
    varis_saati DATETIME NOT NULL,
    kapasite INT NOT NULL
);


CREATE TABLE yolcular (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    tc_no VARCHAR(11) UNIQUE,
    telefon VARCHAR(20)
);


CREATE TABLE biletler (
    id INT AUTO_INCREMENT PRIMARY KEY,
    yolcu_id INT NOT NULL,
    ucus_id INT NOT NULL,
    koltuk_no VARCHAR(5),
    satin_alma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_yolcu
        FOREIGN KEY (yolcu_id) REFERENCES yolcular(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_ucus
        FOREIGN KEY (ucus_id) REFERENCES ucuslar(id)
        ON DELETE CASCADE
);
