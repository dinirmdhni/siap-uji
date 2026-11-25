import psycopg2

from koneksi import buka_koneksi
from bantuan import garis, judul, jeda, ambil_data, jalankan, clear              

# =====================================
# MENAMPILKAN DAFTAR MATERI
# =====================================

def tampilkan_materi(semua=False):
    clear()
    judul("DAFTAR MATERI")

    if semua:
        daftar = ambil_data("""
            SELECT id_materi, nama_materi
            FROM materi
            ORDER BY id_materi
        """)
    else:
        daftar = ambil_data("""
            SELECT id_materi, nama_materi
            FROM materi
            WHERE status_aktif = TRUE
            ORDER BY id_materi
        """)

    print("+----+--------------------------+")
    print("| No | Nama Materi              |")
    print("+----+--------------------------+")

    for materi in daftar:
        print("| {:<2} | {:<24} |".format(
            materi[0], materi[1]
        ))

    print("+----+--------------------------+")

    return daftar

# =====================================
# PENGELOLAAN MATERI
# =====================================

def tambah_materi():
    while True:
        clear()
        judul("TAMBAH MATERI")

        daftar = ambil_data("""
            SELECT id_materi, nama_materi
            FROM materi
            ORDER BY id_materi
        """)
        
        print("+----+--------------------------+")
        print("| No | Nama Materi              |")
        print("+----+--------------------------+")

        for materi in daftar:
            print("| {:<2} | {:<24} |".format(
                materi[0], materi[1]
            ))

        print("+----+--------------------------+")

        nama = input("Nama Materi : ").strip()

        if not nama:
            print("\nNama materi tidak boleh kosong.")
            jeda()
            clear()
            judul("TAMBAH MATERI")
            return

        if not all(huruf.isalnum() or huruf in " &+-#." for huruf in nama):
            print("\nNama materi hanya boleh berisi huruf, angka, dan simbol &+-#.")
            jeda()
            return

        garis()
        print("[1] Simpan")
        print("[2] Batal")

        pilih = input("\nPilih menu: ").strip()

        if pilih == "1":
            jalankan("""
                INSERT INTO materi (nama_materi)
                VALUES (%s)
            """, (nama,))

            print("Materi berhasil ditambahkan.")

        elif pilih == "2":
            print("Penambahan dibatalkan.")

        else:
            print("Pilihan tidak valid.")

        jeda()

def ubah_materi():
    while True:
        clear()
        judul("UBAH MATERI")

        daftar = ambil_data("""
            SELECT id_materi, nama_materi
            FROM materi
            ORDER BY id_materi
        """)

        print("+----+--------------------------+")
        print("| No | Nama Materi              |")
        print("+----+--------------------------+")

        for materi in daftar:
            print("| {:<2} | {:<24} |".format(
                materi[0], materi[1]
            ))

        print("+----+--------------------------+")

        id_materi = input("ID Materi : ").strip()

        if not id_materi:
            print("\nID materi tidak boleh kosong.")
            jeda()
            clear()
            judul("UBAH MATERI")
            return

        if not id_materi.isdigit():
            print("\nID materi harus berupa angka.")
            jeda()
            return

        data = ambil_data("""
            SELECT nama_materi
            FROM materi
            WHERE id_materi = %s
        """, (id_materi,))

        if len(data) == 0:
            print("\nMateri tidak ditemukan.")
            jeda()
            continue

        print("Nama Materi Lama:", data[0][0])

        nama_baru = input("Nama Materi Baru : ").strip()

        if not nama_baru:
            print("\nNama materi baru tidak boleh kosong.")
            jeda()
            return

        if not all(huruf.isalnum() or huruf in " &+-#." for huruf in nama_baru):
            print("\nNama materi hanya boleh berisi huruf, angka, dan simbol &+-#.")
            jeda()
            return

        garis()
        print("[1] Simpan Perubahan")
        print("[2] Batal")

        pilih = input("\nPilih menu: ").strip()

        if pilih == "1":
            jalankan("""
                UPDATE materi
                SET nama_materi = %s
                WHERE id_materi = %s
            """, (nama_baru, id_materi))

            print("Materi berhasil diubah.")

        elif pilih == "2":
            print("Perubahan dibatalkan.")

        else:
            print("Pilihan tidak valid.")

        jeda()


def hapus_materi():
    while True:
        clear()
        judul("NONAKTIFKAN MATERI")

        daftar = ambil_data("""
            SELECT id_materi, nama_materi
            FROM materi
            WHERE status_aktif = TRUE
            ORDER BY id_materi

        """)

        if not daftar:
            print("Tidak ada materi aktif.")
            jeda()
            return

        print("+----+--------------------------+")
        print("| No | Nama Materi              |")
        print("+----+--------------------------+")

        for materi in daftar:
            print("| {:<2} | {:<24} |".format(
                materi[0], materi[1]
            ))

        print("+----+--------------------------+")
        
        id_materi = input("ID Materi : ").strip()

        if not id_materi:
            print("\nID materi tidak boleh kosong.")
            jeda()
            clear()
            judul("NONAKTIFKAN MATERI")
            return

        if not id_materi.isdigit():
            print("\nID materi harus berupa angka.")
            jeda()
            return

        data = ambil_data("""
            SELECT nama_materi
            FROM materi
            WHERE id_materi = %s
            AND status_aktif = TRUE
        """, (id_materi,))


        if len(data) == 0:
            print("Materi tidak ditemukan.")
            jeda()
            return

        print("Nama Materi:", data[0][0])
        print("\nApakah Anda yakin ingin menonaktifkan materi ini?")
        print("[1] Ya, Nonaktifkan")
        print("[2] Batal")

        pilih = input("\nPilih menu: ").strip()

        if pilih == "1":
            jalankan("""
                UPDATE materi
                SET status_aktif = FALSE
                WHERE id_materi = %s
                AND status_aktif = TRUE
            """, (id_materi,))

            print("Materi berhasil dinonaktifkan.")

        elif pilih == "2":
            print("Penonaktifan dibatalkan.")

        else:
            print("Pilihan tidak valid.")

        jeda()


def aktifkan_materi():
    while True:
        clear()
        judul("AKTIFKAN KEMBALI MATERI")

        koneksi = buka_koneksi()

        if koneksi is None:
            return

        cursor = koneksi.cursor()

        try:
            cursor.execute("""
                SELECT id_materi, nama_materi
                FROM materi
                WHERE status_aktif = FALSE
                ORDER BY id_materi
            """)

            daftar = cursor.fetchall()

            if not daftar:
                print("Tidak ada materi nonaktif.")
                jeda()
                return

            print("+----+--------------------------+")
            print("| No | Nama Materi              |")
            print("+----+--------------------------+")

            for materi in daftar:
                print("| {:<2} | {:<24} |".format(
                    materi[0], materi[1]
                ))

            print("+----+--------------------------+")

            id_materi = input("ID Materi : ").strip()

            if not id_materi:
                print("\nID materi tidak boleh kosong.")
                jeda()
                return

            if not id_materi.isdigit():
                print("\nID materi harus berupa angka.")
                jeda()
                return

            cursor.execute("""
                SELECT nama_materi
                FROM materi
                WHERE id_materi = %s
                AND status_aktif = FALSE
            """, (id_materi,))

            data = cursor.fetchone()

            if data is None:
                print("Materi tidak ditemukan atau sudah aktif.")
                jeda()
                return

            print("Nama Materi:", data[0])
            print("\nApakah Anda yakin ingin mengaktifkan materi ini?")
            print("[1] Ya, Aktifkan")
            print("[2] Batal")

            pilih = input("\nPilih menu: ").strip()

            if pilih == "1":
                cursor.execute("""
                    UPDATE materi
                    SET status_aktif = TRUE
                    WHERE id_materi = %s
                    AND status_aktif = FALSE
                """, (id_materi,))

                if cursor.rowcount > 0:
                    koneksi.commit()
                    print("Materi berhasil diaktifkan kembali.")
                else:
                    print("Materi gagal diaktifkan.")

            elif pilih == "2":
                print("Pengaktifan dibatalkan.")

            else:
                print("Pilihan tidak valid.")

        except psycopg2.Error as error:
            koneksi.rollback()
            print("Gagal mengaktifkan materi:", error)

        finally:
            cursor.close()
            koneksi.close()

        jeda()


def menu_materi():
    while True:
        clear()
        judul("PENGELOLAAN MATERI")

        print("[1] Lihat Daftar Materi")
        print("[2] Tambah Materi")
        print("[3] Ubah Materi")
        print("[4] Nonaktifkan Materi")
        print("[5] Aktifkan Kembali Materi")
        print("[6] Kembali")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            tampilkan_materi(semua=True)
            jeda()

        elif pilih == "2":
            tambah_materi()

        elif pilih == "3":
            ubah_materi()

        elif pilih == "4":
            hapus_materi()

        elif pilih == "5":
            aktifkan_materi()

        elif pilih == "6":
            break

        else:
            print("Pilihan tidak valid.")
            jeda()


# =====================================
# MENAMPILKAN DAFTAR SOAL
# =====================================

def tampilkan_daftar_soal(judul_tabel ="DAFTAR SOAL"):
    clear()
    judul(judul_tabel)

    daftar = ambil_data("""
        SELECT
            materi.id_materi,
            materi.nama_materi,
            COUNT(soal.id_soal) FILTER (WHERE soal.status_aktif = TRUE)
        FROM materi
        LEFT JOIN soal
        ON materi.id_materi = soal.id_materi
        GROUP BY materi.id_materi, materi.nama_materi
        ORDER BY materi.id_materi
    """)

    print("+----+----------------------+----------------+")
    print("| ID | Materi               | Jumlah Soal    |")
    print("+----+----------------------+----------------+")

    for data in daftar:
        print("| {:<2} | {:<20} | {:<14} |".format(
            data[0], data[1], data[2]
        ))

    print("+----+----------------------+----------------+")

    return daftar


def lihat_soal_materi():
    while True:
        clear()
        daftar = tampilkan_daftar_soal()

        if len(daftar) == 0:
            print("Belum ada materi.")
            jeda()
            return

        id_materi = input("\nID Materi: ").strip()

        if not id_materi:
            print("\nID materi tidak boleh kosong.")
            jeda()
            return

        if not id_materi.isdigit():
            print("\nID materi harus berupa angka.")
            jeda()
            return

        materi = ambil_data("""
            SELECT nama_materi
            FROM materi
            WHERE id_materi = %s
        """, (id_materi,))

        if len(materi) == 0:
            print("Materi tidak ditemukan.")
            jeda()
            continue

        clear()
        judul("DAFTAR SOAL")

        print("\nID Materi:", id_materi)
        print("Nama Materi:", materi[0][0])

        soal = ambil_data("""
            SELECT
                id_soal, pertanyaan, pilihan_a, pilihan_b,
                pilihan_c, pilihan_d, kunci_jawaban, pembahasan,
                status_aktif
            FROM soal
            WHERE id_materi = %s
            ORDER BY id_soal
        """, (id_materi,))

        if len(soal) == 0:
            print("Belum ada soal pada materi tersebut atau materi tidak ditemukan.")

        for data in soal:
            print("\nID Soal:", data[0])
            print("Pertanyaan:", data[1])
            print("A.", data[2])
            print("B.", data[3])
            print("C.", data[4])
            print("D.", data[5])
            print("Kunci Jawaban:", data[6])
            print("Pembahasan:", data[7])
            print("Status:", "Aktif" if data[8] else "Nonaktif")

        jeda()

# =====================================
# TAMBAH, UBAH, DAN HAPUS SOAL
# =====================================

def tambah_soal():
    while True:
        clear()
        judul("TAMBAH SOAL")

        tampilkan_daftar_soal(judul_tabel ="TAMBAH SOAL")

        id_materi = input("\nID Materi : ")

        if not id_materi:
            print("\nID materi tidak boleh kosong.")
            jeda()
            return

        if not id_materi.isdigit():
            print("\nID materi harus berupa angka.")
            jeda()
            return

        materi = ambil_data("""
            SELECT nama_materi
            FROM materi
            WHERE id_materi = %s
        """, (id_materi,))

        if len(materi) == 0:
            print("Materi tidak ditemukan.")
            jeda()
            continue

        clear()
        judul("TAMBAH SOAL")

        print("\nID Materi:", id_materi)
        print("Nama Materi:", materi[0][0])
        
        pertanyaan = input("\nPertanyaan  : ").strip()
        if not pertanyaan:
            print("Pertanyaan tidak boleh kosong.")
            jeda()
            return

        a = input("Pilihan A   : ").strip()
        if not a:
            print("Pilihan A tidak boleh kosong.")
            jeda()
            return

        b = input("Pilihan B   : ").strip()
        if not b:
            print("Pilihan B tidak boleh kosong.")
            jeda()
            return

        c = input("Pilihan C   : ").strip()
        if not c:
            print("Pilihan C tidak boleh kosong.")
            jeda()
            return

        d = input("Pilihan D   : ").strip()
        if not d:
            print("Pilihan D tidak boleh kosong.")
            jeda()
            return

        kunci = input("Kunci Jawaban (A/B/C/D) : ").strip().upper()
        if not kunci:
            print("Kunci jawaban tidak boleh kosong.")
            jeda()
            return

        if kunci not in ["A", "B", "C", "D"]:
            print("Kunci jawaban harus A, B, C, atau D.")
            jeda()
            return

        pembahasan = input("Pembahasan  : ").strip()
        if not pembahasan:
            print("Pembahasan tidak boleh kosong.")
            jeda()
            return

        garis()
        print("[1] Simpan Soal")
        print("[2] Batal")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            jalankan("""
                INSERT INTO soal (
                    id_materi, pertanyaan, pilihan_a, pilihan_b,
                    pilihan_c, pilihan_d, kunci_jawaban, pembahasan
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_materi, pertanyaan, a, b, c, d, kunci, pembahasan))

            print("Soal berhasil ditambahkan.")

        elif pilih == "2":
            print("Penambahan dibatalkan.")

        else:
            print("Pilihan tidak valid.")

        jeda()



def ubah_soal():
    while True:
        clear()
        judul("UBAH SOAL")

        tampilkan_daftar_soal(judul_tabel ="UBAH SOAL")

        id_materi = input("\nID Materi : ").strip()

        if not id_materi:
            print("\nID materi tidak boleh kosong.")
            jeda()
            return

        if not id_materi.isdigit():
            print("\nID materi harus berupa angka.")
            jeda()
            return

        materi = ambil_data("""
            SELECT nama_materi
            FROM materi
            WHERE id_materi = %s
        """, (id_materi,))

        if len(materi) == 0:
            print("Materi tidak ditemukan.")
            jeda()
            continue

        clear()
        judul("UBAH SOAL")

        print("ID Materi:", id_materi)
        print("Nama Materi:", materi[0][0])
        print("-" * 40)

        soal = ambil_data("""
            SELECT id_soal, pertanyaan
            FROM soal
            WHERE id_materi = %s
            ORDER BY id_soal
        """, (id_materi,))

        if len(soal) == 0:
            print("Belum ada soal pada materi tersebut.")
            jeda()
            return

        for data in soal:
            print("\nID Soal:", data[0])
            print("Pertanyaan:", data[1])

        id_soal = input("\nID Soal : ").strip()

        if not id_soal:
            print("\nID soal tidak boleh kosong.")
            jeda()
            return

        if not id_soal.isdigit():
            print("\nID soal harus berupa angka.")
            jeda()
            return

        data = ambil_data("""
            SELECT pertanyaan, pilihan_a, pilihan_b,
                   pilihan_c, pilihan_d, kunci_jawaban, pembahasan
            FROM soal
            WHERE id_soal = %s AND id_materi = %s
        """, (id_soal, id_materi))

        if len(data) == 0:
            print("Soal tidak ditemukan pada materi tersebut.")
            jeda()
            continue

        clear()
        judul("UBAH SOAL")

        print("ID Materi:", id_materi)
        print("Nama Materi:", materi[0][0])
        print("ID Soal:", id_soal)
        print("-" * 40)

        print("\nSilakan masukkan data soal yang baru.")
        print("\nPertanyaan Lama:", data[0][0])
        pertanyaan = input("\nPertanyaan baru  : ").strip()
        if not pertanyaan:
            print("Pertanyaan tidak boleh kosong.")
            jeda()
            return

        a = input("Pilihan A   : ").strip()
        if not a:
            print("Pilihan A tidak boleh kosong.")
            jeda()
            return

        b = input("Pilihan B   : ").strip()
        if not b:
            print("Pilihan B tidak boleh kosong.")
            jeda()
            return

        c = input("Pilihan C   : ").strip()
        if not c:
            print("Pilihan C tidak boleh kosong.")
            jeda()
            return

        d = input("Pilihan D   : ").strip()
        if not d:
            print("Pilihan D tidak boleh kosong.")
            jeda()
            return

        kunci = input("Kunci Jawaban (A/B/C/D) : ").strip().upper()
        if not kunci:
            print("Kunci jawaban tidak boleh kosong.")
            jeda()
            return

        if kunci not in ["A", "B", "C", "D"]:
            print("Kunci jawaban harus A, B, C, atau D.")
            jeda()
            return

        pembahasan = input("Pembahasan  : ").strip()
        if not pembahasan:
            print("Pembahasan tidak boleh kosong.")
            jeda()
            return

        garis()
        print("[1] Simpan Perubahan")
        print("[2] Batal")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            jalankan("""
                UPDATE soal
                SET pertanyaan = %s,
                    pilihan_a = %s,
                    pilihan_b = %s,
                    pilihan_c = %s,
                    pilihan_d = %s,
                    kunci_jawaban = %s,
                    pembahasan = %s
                WHERE id_soal = %s AND id_materi = %s
            """, (pertanyaan, a, b, c, d, kunci, pembahasan,
                  id_soal, id_materi))

            print("Soal berhasil diubah.")

        elif pilih == "2":
            print("Pengubahan dibatalkan.")

        else:
            print("Pilihan tidak valid.")

        jeda()


def hapus_soal():
    while True:
        clear()
        judul("NONAKTIFKAN SOAL")

        tampilkan_daftar_soal(judul_tabel ="NONAKTIFKAN SOAL")

        id_materi = input("\nID Materi : ").strip()

        if not id_materi:
            print("\nID materi tidak boleh kosong.")
            jeda()
            return

        if not id_materi.isdigit():
            print("\nID materi harus berupa angka.")
            jeda()
            return

        materi = ambil_data("""
            SELECT nama_materi
            FROM materi
            WHERE id_materi = %s AND status_aktif = TRUE
        """, (id_materi,))

        if len(materi) == 0:
            print("Materi tidak ditemukan atau Nonaktif.")
            jeda()
            continue

        clear()
        judul("NONAKTIFKAN SOAL")

        print("ID Materi:", id_materi)
        print("Nama Materi:", materi[0][0])
        print("-" * 40)

        soal = ambil_data("""
            SELECT id_soal, pertanyaan, status_aktif
            FROM soal
            WHERE id_materi = %s AND status_aktif = TRUE
            ORDER BY id_soal
        """, (id_materi,))

        if len(soal) == 0:
            print("Belum ada soal pada materi tersebut.")
            jeda()
            return

        for data in soal:
            print("\nID Soal:", data[0])
            print("Pertanyaan:", data[1])

        id_soal = input("\nID Soal yang ingin dinonaktifkan : ").strip()

        if not id_soal:
            print("ID soal tidak boleh kosong.")
            jeda()
            return

        if not id_soal.isdigit():
            print("ID soal harus berupa angka.")
            jeda()
            return

        clear()
        judul("NONAKTIFKAN SOAL")

        print("ID Materi:", id_materi)
        print("Nama Materi:", materi[0][0])
        print("ID Soal:", id_soal)
        print("-" * 40)

        data = ambil_data("""
            SELECT pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d,
                kunci_jawaban, pembahasan
            FROM soal
            WHERE id_soal = %s
            AND id_materi = %s
            AND status_aktif = TRUE
        """, (id_soal, id_materi))
        
        if len(data) == 0:
            print("Soal tidak ditemukan pada materi tersebut.")
            jeda()
            continue

        print("\nPertanyaan:", data[0][0])
        print("A.", data[0][1])
        print("B.", data[0][2])
        print("C.", data[0][3])
        print("D.", data[0][4])
        print("Kunci Jawaban:", data[0][5])
        print("Pembahasan:", data[0][6])

        print("\nApakah Anda yakin ingin menonaktifkan soal ini?")
        print("[1] Ya, Nonaktifkan")
        print("[2] Batal")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            jalankan("""
                UPDATE soal
                SET status_aktif = FALSE
                WHERE id_soal = %s AND id_materi = %s
            """, (id_soal, id_materi))

            print("Soal berhasil dinonaktifkan.")

        elif pilih == "2":
            print("Penonaktifan dibatalkan.")

        else:
            print("Pilihan tidak valid.")

        jeda()


def aktifkan_soal():
    while True:
        clear()
        judul("AKTIFKAN KEMBALI SOAL")

        tampilkan_daftar_soal(judul_tabel="AKTIFKAN KEMBALI SOAL")

        id_materi = input("\nID Materi : ").strip()

        if not id_materi:
            print("ID materi tidak boleh kosong.")
            jeda()
            return

        if not id_materi.isdigit():
            print("ID materi harus berupa angka.")
            jeda()
            return

        materi = ambil_data("""
            SELECT nama_materi
            FROM materi
            WHERE id_materi = %s AND status_aktif = TRUE
        """, (id_materi,))

        if len(materi) == 0:
            print("Materi tidak ditemukan.")
            jeda()
            continue

        clear()
        judul("AKTIFKAN KEMBALI SOAL")

        soal = ambil_data("""
            SELECT id_soal, pertanyaan
            FROM soal
            WHERE id_materi = %s AND status_aktif = FALSE
            ORDER BY id_soal
        """, (id_materi,))

        if len(soal) == 0:
            print("Tidak ada soal nonaktif pada materi tersebut.")
            jeda()
            return

        for data in soal:
            print("\nID Soal:", data[0])
            print("Pertanyaan:", data[1])

        id_soal = input("\nID Soal yang ingin diaktifkan : ").strip()

        if not id_soal:
            print("ID soal tidak boleh kosong.")
            jeda()
            return

        if not id_soal.isdigit():
            print("ID soal harus berupa angka.")
            jeda()
            return

        data = ambil_data("""
            SELECT pertanyaan, pilihan_a, pilihan_b, pilihan_c,
                   pilihan_d, kunci_jawaban, pembahasan
            FROM soal
            WHERE id_soal = %s
            AND id_materi = %s
            AND status_aktif = FALSE
        """, (id_soal, id_materi))

        if len(data) == 0:
            print("Soal tidak ditemukan pada materi tersebut.")
            jeda()
            continue

        clear()
        judul("AKTIFKAN KEMBALI SOAL")

        print("ID Materi:", id_materi)
        print("Nama Materi:", materi[0][0])
        print("ID Soal:", id_soal)
        print("-" * 40)

        print("\nPertanyaan:", data[0][0])
        print("A.", data[0][1])
        print("B.", data[0][2])
        print("C.", data[0][3])
        print("D.", data[0][4])
        print("Kunci Jawaban:", data[0][5])
        print("Pembahasan:", data[0][6])

        print("\nApakah Anda yakin ingin mengaktifkan soal ini?")
        print("[1] Ya, Aktifkan")
        print("[2] Batal")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            jalankan("""
                UPDATE soal
                SET status_aktif = TRUE
                WHERE id_soal = %s AND id_materi = %s
            """, (id_soal, id_materi))

            print("Soal berhasil diaktifkan kembali.")

        elif pilih == "2":
            print("Pengaktifan dibatalkan.")

        else:
            print("Pilihan tidak valid.")

        jeda()

def menu_soal():
    while True:
        clear()
        judul("PENGELOLAAN BANK SOAL")

        print("[1] Lihat Daftar Soal")
        print("[2] Tambah Soal")
        print("[3] Ubah Soal")
        print("[4] Nonaktifkan Soal")
        print("[5] Aktifkan Kembali Soal")
        print("[6] Kembali")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            lihat_soal_materi()

        elif pilih == "2":
            tambah_soal()

        elif pilih == "3":
            ubah_soal()

        elif pilih == "4":
            hapus_soal()

        elif pilih == "5":
            aktifkan_soal()

        elif pilih == "6":
            break

        else:
            print("Pilihan tidak tersedia.")
            jeda()


# =====================================
# MENU ADMIN
# =====================================


def menu_admin():
    while True:
        clear()
        judul("MENU ADMIN")

        print()
        print("Selamat Datang, Admin!")
        print("\nKelola data yang tersedia pada SiapUji.")

        print("\n" + "-" * 50)
        print("[1] Pengelolaan Materi")
        print("[2] Pengelolaan Bank Soal")
        print("[3] Logout")
        print("-" * 50)

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            menu_materi()

        elif pilih == "2":
            menu_soal()

        elif pilih == "3":
            print("\nApakah Anda yakin ingin logout?")
            print("[1] Ya")
            print("[2] Tidak")

            keluar = input("\nPilih menu: ")

            if keluar == "1":
                print("\nBerhasil logout.")
                break

        else:
            print("\nPilihan tidak tersedia.")
            jeda()


# =====================================
# MENENTUKAN KATEGORI NILAI
# =====================================

def tentukan_kategori(nilai):
    if nilai >= 80:
        return "TINGGI"

    elif nilai >= 60:
        return "SEDANG"

    else:
        return "PERLU DITINGKATKAN"


# =====================================
# MENYIMPAN HASIL LATIHAN
# =====================================

def simpan_hasil(id_pengguna, id_materi, benar, salah, daftar_jawaban):
    koneksi = buka_koneksi()
    cursor = koneksi.cursor()

    jumlah_soal = benar + salah
    nilai = benar / jumlah_soal * 100

    try:
        cursor.execute("""
            INSERT INTO riwayat_latihan (
                id_pengguna, id_materi, tanggal_pengerjaan,
                jumlah_soal, jumlah_benar, jumlah_salah, nilai
            )
            VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s)
            RETURNING id_riwayat
        """, (id_pengguna, id_materi, jumlah_soal,
              benar, salah, nilai))

        id_riwayat = cursor.fetchone()[0]

        for jawaban in daftar_jawaban:
            cursor.execute("""
                INSERT INTO detail_latihan (
                    id_riwayat, id_soal,
                    jawaban_pengguna, status_jawaban
                )
                VALUES (%s, %s, %s, %s)
            """, (id_riwayat, jawaban[0], jawaban[1], jawaban[2]))

        koneksi.commit()
        return id_riwayat

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal menyimpan hasil:", error)
        return None

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# MEMULAI LATIHAN
# =====================================

def mulai_latihan(id_pengguna):
    while True:
        clear()
        daftar = tampilkan_materi()
        print("[1] Pilih Materi")
        print("[2] Kembali")

        pilih = input("\nMasukkan pilihan: ")

        if pilih == "2":
            return

        if pilih != "1":
            print("Pilihan tidak tersedia.")
            jeda()
            continue

        id_materi = input("Masukkan ID Materi: ").strip()

        if id_materi == "":
            print("\nID materi tidak boleh kosong.")
            jeda()
            continue

        if not id_materi.isdigit():
            print("\nID materi harus berupa angka.")
            jeda()
            continue

        id_materi = int(id_materi)

        materi = ambil_data("""
            SELECT nama_materi
            FROM materi
            WHERE id_materi = %s
            AND status_aktif = TRUE
        """, (id_materi,))

        if len(materi) == 0:
            print("Materi tidak ditemukan.")
            jeda()
            continue

        nama_materi = materi[0][0]

        soal = ambil_data("""
            SELECT
                id_soal, pertanyaan, pilihan_a, pilihan_b,
                pilihan_c, pilihan_d, kunci_jawaban, pembahasan
            FROM soal
            WHERE id_materi = %s
            AND status_aktif = TRUE
            ORDER BY id_soal
        """, (id_materi,))

        if len(soal) == 0:
            print("Belum ada soal untuk materi ini.")
            jeda()
            continue

        break

    benar = 0
    salah = 0
    daftar_jawaban = []

    for nomor, data in enumerate(soal, start=1):
        clear()
        judul("LATIHAN SiapUji")

        print("Materi :", nama_materi)
        print("Soal   :", nomor, "dari", len(soal))
        print("\n" + "-" * 50)

        print(data[1])
        print("\nA.", data[2])
        print("B.", data[3])
        print("C.", data[4])
        print("D.", data[5])

        while True:
            jawaban = input("\nJawaban (A/B/C/D): ").upper()
            if jawaban in ["A", "B", "C", "D"]:
                break

            print("\nPilihan tidak valid. Silakan masukkan A, B, C, atau D.")
            input("\nTekan ENTER untuk mencoba lagi...")

            clear()

            judul("LATIHAN SiapUji")
            print("Materi :", nama_materi)
            print("Soal   :", nomor, "dari", len(soal))
            print("\n" + "-" * 50)

            print(data[1])
            print("\nA.", data[2])
            print("B.", data[3])
            print("C.", data[4])
            print("D.", data[5])

        if jawaban == data[6]:
            benar += 1
            status = True
            print("Jawaban benar!")

        else:
            salah += 1
            status = False
            print("Jawaban salah.")
            print("Kunci jawaban:", data[6])

        print("Pembahasan:", data[7])

        daftar_jawaban.append((data[0], jawaban, status))
        input("\nTekan ENTER untuk soal berikutnya...")

    id_riwayat = simpan_hasil(
        id_pengguna, id_materi, benar, salah, daftar_jawaban
    )

    jumlah_soal = len(soal)
    nilai = benar / jumlah_soal * 100
    kategori = tentukan_kategori(nilai)

    
    clear()
    judul("HASIL LATIHAN")
    
    print()
    print("Materi              :", nama_materi)

    print("\n" + "-" * 50)
    print("HASIL EVALUASI")
    print("-" * 50)

    print(f"Jumlah Soal         : {jumlah_soal}")
    print(f"Jawaban Benar       : {benar}")
    print(f"Jawaban Salah       : {salah}")

    print("\n" + "-" * 50)
    print("NILAI")
    print(f"Nilai               : {nilai:.2f}")

    print("\nKATEGORI PENGUASAAN")
    print("Kategori            :", kategori)

    print("-" * 50)


    if id_riwayat is not None:
        print("\n[1] Lihat Prioritas Belajar")
        print("[2] Kembali ke Menu Mahasiswa")

        while True:
            pilih = input("\nPilih menu: ").strip()

            if pilih == "1":
                tampilkan_prioritas(id_pengguna)
                jeda()
                break

            elif pilih == "2":
                return

            elif pilih == "":
                print("\nPilihan tidak boleh kosong.")  
                jeda()
                clear()
                judul("HASIL LATIHAN")

                print()
                print("Materi              :", nama_materi)
                print(f"Jumlah Soal         : {jumlah_soal}")
                print(f"Jawaban Benar       : {benar}")
                print(f"Jawaban Salah       : {salah}")
                print(f"Nilai               : {nilai:.2f}")
                print("Kategori Penguasaan:", kategori)

                print("\n[1] Lihat Prioritas Belajar")
                print("[2] Kembali ke Menu Mahasiswa")

            else:
                print("\nPilihan tidak tersedia.")
                jeda()
                clear()
                judul("HASIL LATIHAN")

                print(f"Materi         : {nama_materi}")
                print(f"\nJumlah Soal    : {jumlah_soal}")
                print(f"Jawaban Benar  : {benar}")
                print(f"Jawaban Salah  : {salah}")
                print(f"\nNilai          : {nilai:.2f}")
                print(f"\nKategori Penguasaan: {kategori}")
                print("\n[1] Lihat Prioritas Belajar")
                print("[2] Kembali ke Menu Mahasiswa")

# =====================================
# PRIORITAS BELAJAR
# =====================================



def tampilkan_prioritas(id_pengguna):
    clear()
    judul("PRIORITAS BELAJAR")

    daftar = ambil_data("""
        SELECT
            materi.nama_materi,
            riwayat_latihan.nilai
        FROM riwayat_latihan
        JOIN materi
        ON riwayat_latihan.id_materi = materi.id_materi
        WHERE riwayat_latihan.id_pengguna = %s
        AND riwayat_latihan.id_riwayat = (
            SELECT MAX(r2.id_riwayat)
            FROM riwayat_latihan r2
            WHERE r2.id_pengguna = riwayat_latihan.id_pengguna
            AND r2.id_materi = riwayat_latihan.id_materi
        )
        ORDER BY riwayat_latihan.nilai ASC
    """, (id_pengguna,))

    if len(daftar) == 0:
        print("\nBelum ada hasil latihan.")
        return

    print("\nUrutan materi berdasarkan nilai latihan terbaru.")
    print("Materi dengan nilai terendah menjadi prioritas belajar.\n")

    print("=" * 55)
    print("{:<5} {:<30} {:>10}".format(
        "NO", "MATERI", "NILAI"
    ))
    print("-" * 55)

    for nomor, data in enumerate(daftar, start=1):
        nama_materi = data[0]
        nilai = float(data[1])

        print("{:<5} {:<30} {:>10.2f}".format(
            nomor, nama_materi[:30], nilai
        ))

    print("=" * 55)

    print("\nMATERI PRIORITAS BELAJAR")
    print("Materi :", daftar[0][0])
    print("Nilai  :", format(float(daftar[0][1]), ".2f"))
    print("\nPelajari kembali materi tersebut untuk")
    print("meningkatkan pemahamanmu.")