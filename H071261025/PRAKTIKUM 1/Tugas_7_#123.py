import os
import random
from datetime import datetime

FOLDER_INVOICE = "invoices"
FILE_RIWAYAT = "trx_history.txt"


def ambil_inisial(nama):
    """Inisial nama kasir (huruf kapital), mis. 'Kiki Lestari Sari' -> 'KLS'."""
    return "".join(kata[0] for kata in nama.split()).upper()


def buat_id_transaksi(nama_kasir, waktu):
    """Format: INISIAL + YY + MM + DD + HHMM + 3 digit acak (100-999)."""
    inisial = ambil_inisial(nama_kasir)
    angka_acak = random.randint(100, 999)
    return inisial + waktu.strftime("%y%m%d%H%M") + str(angka_acak)


def input_angka(pesan, tipe=int):
    """Meminta input angka positif sampai valid."""
    while True:
        try:
            nilai = tipe(input(pesan))
            if nilai > 0:
                return nilai
            print("Nilai harus lebih dari 0.")
        except ValueError:
            print("Input tidak valid, masukkan angka.")


def input_produk():
    """Input satu atau lebih produk dalam satu transaksi."""
    daftar = []
    while True:
        nama = input("Nama produk   : ").strip()
        if nama == "":
            print("Nama produk tidak boleh kosong.")
            continue
        harga = input_angka("Harga produk  : Rp. ")
        jumlah = input_angka("Jum  lah        : ")
        daftar.append({"nama": nama, "harga": harga, "jumlah": jumlah})

        while True :
            lagi = str(input("Tambah produk lagi? (y/n): ")).strip().lower()
            if lagi not in ["y","n"]:
                print("Tidak bisa di lanjutkan kalo angka")
                continue
            else :
                break
        if lagi == "y" or lagi == "yes" or lagi == "ya":
            continue
        elif lagi == "n" or lagi == "no" or lagi == "tidak":
            break
        print()
    return daftar


def susun_isi_invoice(id_trx, nama_kasir, waktu, daftar_produk):
    """Menyusun teks invoice dan mengembalikan (teks, total)."""
    garis = "=" * 56
    baris = [
        garis,
        "INVOICE".center(56),
        garis,
        f"ID Transaksi : {id_trx}",
        f"Waktu        : {waktu.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Kasir        : {nama_kasir}",
        garis,
        f"{'Produk':<20}{'Harga':>12}{'Jml':>6}{'Subtotal':>14}",
        "-" * 56,
    ]
    total = 0
    for p in daftar_produk:
        subtotal = p["harga"] * p["jumlah"]
        total += subtotal
        baris.append(
            f"{p['nama'][:20]:<20}{p['harga']:>12}{p['jumlah']:>6}{subtotal:>14}"
        )
    baris += [
        "-" * 56,
        f"{'TOTAL':<38}Rp. {total:>10}",
        garis,
        "Terima kasih telah berbelanja!".center(56),
    ]
    return "\n".join(baris) + "\n", total


def simpan_invoice(id_trx, isi):
    """Menyimpan invoice ke folder invoices/<ID>.txt."""
    os.makedirs(FOLDER_INVOICE, exist_ok=True)
    path = os.path.join(FOLDER_INVOICE, id_trx + ".txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(isi)
    return path


def catat_riwayat(waktu, id_trx, total):
    """Menambah satu baris ke trx_history.txt (header dibuat jika file baru)."""
    garis = "=" * 66
    baru = not os.path.exists(FILE_RIWAYAT)
    with open(FILE_RIWAYAT, "a", encoding="utf-8") as f:
        if baru:
            f.write(garis + "\n")
            f.write(
                f"| {'Waktu':^19} | {'ID Transaksi':^17} | {'Nominal Transaksi':^18} |\n"
            )
            f.write(garis + "\n")
        f.write(
            f"| {waktu.strftime('%Y-%m-%d %H:%M:%S'):<19} | {id_trx:<17} | "
            f"{'Rp. ' + str(total):<18} |\n"
        )
        f.write(garis + "\n")


def transaksi_baru():
    """Soal 1 + 3: buat transaksi, invoice, dan catat riwayat."""
    print("\n--- TRANSAKSI BARU ---")
    nama_kasir = ""
    while nama_kasir == "":
        nama_kasir = input("Nama kasir    : ").strip()

    daftar_produk = input_produk()

    waktu = datetime.now()
    id_trx = buat_id_transaksi(nama_kasir, waktu)
    isi, total = susun_isi_invoice(id_trx, nama_kasir, waktu, daftar_produk)

    simpan_invoice(id_trx, isi)
    catat_riwayat(waktu, id_trx, total)

    print("\nTransaksi berhasil!")
    print(f"Invoice tersimpan: {FOLDER_INVOICE}/{id_trx}.txt")
    print("\n" + isi)


def cari_invoice():
    """Soal 2: cari invoice berdasarkan ID transaksi (tanpa .txt) lalu tampilkan."""
    print("\n--- CARI INVOICE ---")
    id_trx = input("Masukkan ID transaksi: ").strip().upper()
    path = os.path.join(FOLDER_INVOICE, id_trx + ".txt")

    if id_trx != "" and os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            print("\n" + f.read())
    else:
        print(f"Invoice dengan ID '{id_trx}' tidak ditemukan.")


def tampilkan_menu():
    print("=" * 30)
    print("      APLIKASI KASIR")
    print("=" * 30)
    print("1. Transaksi baru")
    print("2. Cari invoice")
    print("3. Keluar")


# ---- Program utama (tanpa fungsi main) ----
while True:
    tampilkan_menu()
    pilihan = input("Pilih menu (1-3): ").strip()

    if pilihan == "1":
        transaksi_baru()
    elif pilihan == "2":
        cari_invoice()
    elif pilihan == "3":
        print("Terima kasih. Program selesai.")
        break
    else:
        print("Pilihan tidak valid.\n")
    print()