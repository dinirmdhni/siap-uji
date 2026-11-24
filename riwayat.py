from bantuan import judul, jeda, ambil_data, clear

# =====================================
# RIWAYAT LATIHAN
# =====================================


def tampilkan_riwayat(id_pengguna):
    while True:
        clear()
        judul("RIWAYAT LATIHAN")

        daftar = ambil_data("""
            SELECT
                riwayat_latihan.id_riwayat,
                materi.nama_materi,
                riwayat_latihan.tanggal_pengerjaan,
                riwayat_latihan.nilai
            FROM riwayat_latihan
            JOIN materi
            ON riwayat_latihan.id_materi = materi.id_materi
            WHERE riwayat_latihan.id_pengguna = %s
            ORDER BY riwayat_latihan.tanggal_pengerjaan DESC
        """, (id_pengguna,))

        if len(daftar) == 0:
            print("\nBelum ada riwayat latihan.")
            jeda()
            return

        print("\nBerikut riwayat latihan Anda.")
        print("Riwayat terbaru ditampilkan paling atas.\n")

        print("=" * 75)
        print("{:<6} {:<8} {:<35} {:<15} {:>8}".format(
            "NO", "ID", "MATERI", "TANGGAL", "NILAI"
        ))
        print("-" * 75)

        for nomor, data in enumerate(daftar, start=1):
            tanggal = data[2].strftime("%d-%m-%Y")

            print("{:<6} {:<8} {:<35} {:<15} {:>8.2f}".format(
                nomor,
                data[0],
                data[1][:35],
                tanggal,
                float(data[3])
            ))

        print("=" * 75)

        print("\n[1] Lihat Detail Riwayat")
        print("[2] Kembali")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            id_riwayat = input("\nPilih ID Riwayat: ").strip()

            if not id_riwayat:
                print("\nID riwayat tidak boleh kosong.")
                jeda()
                continue

            if not id_riwayat.isdigit():
                print("\nID riwayat harus berupa angka.")
                jeda()
                continue

            id_riwayat = int(id_riwayat)
            detail_riwayat(id_pengguna, id_riwayat)

        elif pilih == "2":
            return

        else:
            print("\nPilihan tidak tersedia.")
            jeda()



def detail_riwayat(id_pengguna, id_riwayat):
    clear()
    judul("DETAIL RIWAYAT LATIHAN")

    data = ambil_data("""
        SELECT
            riwayat_latihan.id_riwayat,
            materi.nama_materi,
            riwayat_latihan.tanggal_pengerjaan,
            riwayat_latihan.jumlah_soal,
            riwayat_latihan.jumlah_benar,
            riwayat_latihan.jumlah_salah,
            riwayat_latihan.nilai
        FROM riwayat_latihan
        JOIN materi
        ON riwayat_latihan.id_materi = materi.id_materi
        WHERE riwayat_latihan.id_riwayat = %s
        AND riwayat_latihan.id_pengguna = %s
    """, (id_riwayat, id_pengguna))

    if len(data) == 0:
        print("\nRiwayat tidak ditemukan.")
        jeda()
        return

    riwayat = data[0]

    print()
    print("=" * 50)
    print("INFORMASI LATIHAN")
    print("=" * 50)

    print(f"ID Riwayat       : {riwayat[0]}")
    print(f"Materi           : {riwayat[1]}")
    print(f"Tanggal          : {riwayat[2].strftime('%d-%m-%Y')}")

    print("\n" + "-" * 50)
    print("HASIL EVALUASI")
    print("-" * 50)

    print(f"Jumlah Soal      : {riwayat[3]}")
    print(f"Jawaban Benar    : {riwayat[4]}")
    print(f"Jawaban Salah    : {riwayat[5]}")

    print("\n" + "-" * 50)
    print("NILAI")
    print(f"Nilai            : {float(riwayat[6]):.2f}")
    print("=" * 50)

    print("\n[1] Kembali ke Riwayat Latihan")

    while True:
        pilih = input("\nPilih menu: ")

        if pilih == "1":
            return

        else:
            print("\nPilihan tidak tersedia.")
            jeda()

            clear()
            judul("DETAIL RIWAYAT LATIHAN")

            print()
            print("=" * 50)
            print("INFORMASI LATIHAN")
            print("=" * 50)

            print(f"ID Riwayat       : {riwayat[0]}")
            print(f"Materi           : {riwayat[1]}")
            print(f"Tanggal          : {riwayat[2].strftime('%d-%m-%Y')}")

            print("\n" + "-" * 50)
            print("HASIL EVALUASI")
            print("-" * 50)

            print(f"Jumlah Soal      : {riwayat[3]}")
            print(f"Jawaban Benar    : {riwayat[4]}")
            print(f"Jawaban Salah    : {riwayat[5]}")

            print("\n" + "-" * 50)
            print("NILAI")
            print(f"Nilai            : {float(riwayat[6]):.2f}")
            print("=" * 50)

            print("\n[1] Kembali ke Riwayat Latihan")
