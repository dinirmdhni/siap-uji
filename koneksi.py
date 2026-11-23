import psycopg2


def buka_koneksi():
    koneksi = psycopg2.connect(
        host="localhost",
        database="db_siapuji",
        user="postgres",
        password="dini19",
        port="5432"
    )

    return koneksi

