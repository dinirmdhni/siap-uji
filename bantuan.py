import psycopg2
from koneksi import buka_koneksi
from pyfiglet import Figlet
from colorama import init, Fore, Style
import os
import time

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# =====================================
# FUNGSI BANTUAN
# =====================================

def garis():
    print("=" * 50)


def judul(teks):
    garis()
    print(teks.center(50))
    garis()


def jeda():
    input("\nTekan ENTER untuk kembali...")


def ambil_data(sql, data=()):
    koneksi = buka_koneksi()
    cursor = koneksi.cursor()

    try:
        cursor.execute(sql, data)
        hasil = cursor.fetchall()
        return hasil

    except psycopg2.Error as error:
        print("Terjadi kesalahan:", error)
        return []

    finally:
        cursor.close()
        koneksi.close()


def jalankan(sql, data=()):
    koneksi = buka_koneksi()
    cursor = koneksi.cursor()

    try:
        cursor.execute(sql, data)
        koneksi.commit()
        return cursor.rowcount

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Terjadi kesalahan:", error)
        return 0

    finally:
        cursor.close()
        koneksi.close()


def banner():
    figlet = Figlet(font="ansi_shadow", width=100)
    tulisan = figlet.renderText("SiapUji")

    print("=" * 80)

    # Menampilkan tulisan SiapUji
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT, end="")
    for baris in tulisan.splitlines():
        print(baris.center(80))

    # Menampilkan deskripsi program
    print()
    print(
        Fore.WHITE
        + "SISTEM EVALUASI KESIAPAN UJIAN".center(80)
    )

    print(Style.RESET_ALL)
    print("=" * 80)
