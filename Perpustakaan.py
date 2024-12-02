import streamlit as st
import json
import pandas as pd
import os
os.system ('cls')
# Fungsi untuk membaca data dari file JSON
def baca_data_dari_file(nama_file):
    if os.path.exists(nama_file):
        with open(nama_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError:
                st.error(f"Format data dalam file '{nama_file}' tidak valid.")
                return None
    else:
        st.error(f"File '{nama_file}' tidak ditemukan.")
        return None

# Fungsi untuk mencari buku berdasarkan kategori
def cari_buku(kategori_dicari, data):
    for kategori in data:
        if kategori['kategori'].lower() == kategori_dicari.lower():
            return kategori['buku']
    return None

# Set page config as the first Streamlit command
st.set_page_config(page_title="Pencarian Buku Laporan PKL", layout="wide")

# Sidebar
st.sidebar.header("Pencarian Buku Laporan PKL")
st.sidebar.markdown("""
Gunakan aplikasi ini untuk mencari lokasi buku Laporan PKL di perpustakaan POLITEKNIK NEGERI PONTIANAK.
Pilih kategori buku pada kolom di bawah dan tekan tombol 'Cari'.
""")

# Judul aplikasi
st.title("📚 Pencarian Buku Laporan PKL Prodi Teknik Informatika Perpustakaan POLITEKNIK NEGERI PONTIANAK")
 
# Nama file JSON yang ingin dibaca
nama_file = 'C://TUGAS MAKUL ALGORITMA PEMROGRAMAN//TUGAS AKHIR//Perpustakaan//datajsonbuku.json'

# Membaca data dari file JSON
data_perpustakaan = baca_data_dari_file(nama_file)

# Jika data berhasil dibaca
if data_perpustakaan:
    # Ambil daftar kategori buku
    daftar_kategori = ["Pilih kategori buku"] + [kategori['kategori'] for kategori in data_perpustakaan]

    # Input pengguna
    kategori_yang_dicari = st.selectbox("Pilih Kategori Buku:", daftar_kategori)

    # Tombol untuk mencari
    if st.button("Cari"):
        if kategori_yang_dicari != "Pilih kategori buku laporan PKL Prodi Teknik Informatika Tahun 2020/2021":
            # Cari buku berdasarkan kategori yang dipilih
            buku_ditemukan = cari_buku(kategori_yang_dicari, data_perpustakaan)
            
            # Buat DataFrame untuk menampilkan hasil
            if buku_ditemukan:
                df = pd.DataFrame(buku_ditemukan)
                df['No'] = range(1, len(df) + 1)  # Tambah kolom No dengan nomor urut dimulai dari 1
                df = df.rename(columns={'Letak_Buku_Laporan_PKL': 'Letak Buku Laporan PKL', 'Nomor_Urut_Arsip': 'Nomor Urut Arsip', 
                                        'Tahun_Pelaksanaan': 'Tahun Pelaksanaan', 'NIM_Mahasiswa': 'NIM Mahasiswa',
                                        'Nama_Mahasiswa': 'Nama Mahasiswa', 'Judul_Laporan_PKL': 'Judul Laporan PKL', 'Nama_Dosen_Pembimbing': 'Nama Dosen Pembimbing',
                                        'Nama_Tempat_Pelaksanaan': 'Nama Tempat Pelaksanaan', 'Kabupaten_Kota_Pelaksanaan': 'Kabupaten Kota Pelaksanaan'})  # Tambahkan kolom status
                df = df[['No', 'Letak Buku Laporan PKL', 'Nomor Urut Arsip', 'Tahun Pelaksanaan', 'NIM Mahasiswa', 'Nama Mahasiswa', 'Judul Laporan PKL', 'Nama Dosen Pembimbing', 'Nama Tempat Pelaksanaan', 'Kabupaten Kota Pelaksanaan']]  # Susun ulang kolom
                st.subheader(f"Buku-buku dalam kategori '{kategori_yang_dicari}':")
                st.write(df.to_html(index=False), unsafe_allow_html=True)  # Tampilkan tabel tanpa indeks
            else:
                st.warning("Tidak ada buku yang ditemukan dalam kategori ini.")
        else:
            st.warning("Silakan pilih kategori buku.")
else:
    st.error("Data perpustakaan tidak tersedia.")
