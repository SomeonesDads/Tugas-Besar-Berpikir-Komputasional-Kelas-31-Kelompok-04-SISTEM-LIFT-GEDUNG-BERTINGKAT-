# 🚪 Sistem Lift Gedung Bertingkat

Proyek ini merupakan implementasi simulasi sistem kerja lift pada gedung bertingkat sebagai bagian dari **Tugas Besar 2 - Pengenalan Komputasi** (WI1102) di Sekolah Teknik Elektro dan Informatika, Institut Teknologi Bandung.

## 📌 Deskripsi
Program ini mensimulasikan operasi beberapa lift di sebuah gedung berdasarkan permintaan pengguna. Sistem akan menentukan **lift tercepat** yang paling efisien untuk memenuhi permintaan berdasarkan:
- Posisi lift
- Arah gerak
- Kapasitas muatan
- Waktu tempuh
- Status servis (jumlah trip yang sudah dilakukan)

## ✨ Fitur Utama
- **Pemilihan Lift Tercepat**: Menghitung waktu tempuh optimal untuk menentukan lift terbaik.
- **Visualisasi Posisi Lift**: Menampilkan posisi lift pada setiap lantai.
- **Simulasi Otomatis**: Permintaan pengguna dihasilkan secara acak.
- **Mode Input Manual**: Pengguna dapat memasukkan permintaan secara langsung.
- **Penanganan Overload**: Sistem otomatis membuat perjalanan tambahan jika kapasitas terlampaui.
- **Servis Otomatis**: Lift akan berhenti beroperasi setelah mencapai batas trip tertentu.

## 🛠️ Teknologi
- **Python 3.x**
- Library standar Python (tanpa dependency tambahan)

## 📂 Struktur Proyek
├── main.py # Source code utama simulasi
├── laporan_akhir.pdf # Laporan akhir tugas besar
├── ppt_presentasi.pptx # Slide presentasi
└── README.md # Dokumentasi proyek
