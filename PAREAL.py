import os
import json
import pwinput
from prettytable import PrettyTable
os.system('cls')


json_path_film = 'C:/Aidil/01_CODING/Semester1/PA/dataData/film.json'
json_path_pay = 'C:/Aidil/01_CODING/Semester1/PA/dataData/userpay.json'
json_path_free = 'C:/Aidil/01_CODING/Semester1/PA/dataData/userfree.json'
json_path_admin = 'C:/Aidil/01_CODING/Semester1/PA/dataData/admin.json'
with open(json_path_film,"r") as filmdata:
    film = json.loads(filmdata.read())
with open(json_path_free,"r") as userFreeData:
    userfree = json.loads(userFreeData.read())
with open(json_path_pay, "r") as userPayData:
    userpay = json.loads(userPayData.read())
with open(json_path_admin, "r") as admindata:
    admin = json.loads(admindata.read())


print("------------------------------------------------------------------------------")
print("-                                                                            -")
print("-                                   SI-FLIX                                  -")
print("-                                                                            -")
print("------------------------------------------------------------------------------")


def tampilkan_daftar_film():
    table_film = PrettyTable()
    table_film.field_names =  ["No","Judul Film","Genre","Waktu Release"]
    for item in film:
        table_film.add_row(item)
    print(table_film)


def register():
    print("Silahkan lakukan Registrasi")
    while True:
        username = input("Masukkan username: ").lower()
        pw = pwinput.pwinput("Masukkan password: ")
        notAvailable = False #VARIABLE YANG DIGUNAKAN UNTUK MENGECEK APAKAH USERNAME TERDAFTAR ATAU TIDAK
        for admin_acc in admin:
            if admin_acc["adminName"].lower() == username:
                print("username sudah digunakan cobalagi yang lain")
                notAvailable = True #VARIABLE BERUBAH MENJADI TRUE SAAT USERNAME SUDAH TIDAK TERSEDIA
                break
        for user in userfree:
            if user["username"].lower() == username:
                print("username sudah digunakan cobalagi yang lain")
                notAvailable = True #VARIABLE BERUBAH MENJADI TRUE SAAT USERNAME SUDAH TIDAK TERSEDIA
                break
        for user in userpay:
            if user["username"].lower() == username:
                print("username sudah digunakan cobalagi yang lain")
                notAvailable = True #VARIABLE BERUBAH MENJADI TRUE SAAT USERNAME SUDAH TIDAK TERSEDIA
                break
        #JIKA USERNAME TERSEDIA DAN VARIBLENYA MASIH BERNILAI FALSE MAKA AKAN BERHASIL MENAMBAHKAN AKUN BARU
        if not notAvailable:
            akun_baru = {"username": username, "password": pw, "saldo": 0}
            userfree.append(akun_baru)
            print("berhasil membuat akun")
            with open (json_path_free, "w") as sn:
                json.dump(userfree,sn,indent=4)
            break

#FUNCTION UNTUK LOGIN
def login():
    print("Silahkan Login")
    while True:
        username = input("Masukkan username: ").lower()
        pw = pwinput.pwinput("Masukkan password: ")
        akunAda = False #SEBUAH VARIABLE YANG DIGUNAKAN UNTUK MENGECEK APAKAH USERNAME TERDAFTAR ATAU TIDAK
        for admin_acc in admin:
            if admin_acc["adminName"].lower() == username and admin_acc["pwAdmin"]==pw:
                akunAda = True
                print("Berhasil login sebagai admin")
                return menu_admin()
                break
        for user in userfree:
            if user["username"].lower() == username:
                akunAda = True#JIKA USERNAME DITEMUKAN MAKA VARIABLE AKAN MENJADI TRUE
                if user["password"] == pw:
                    print("berhasil login sebagai user free")
                else:
                    print("Password yang anda masukkan salah")
                break
        for user in userpay:
            if user["username"].lower() == username:
                akunAda = True#JIKA USERNAME DITEMUKAN MAKA VARIABLE AKAN MENJADI TRUE
                if user["password"] == pw:
                    print("berhasil login sebagai user premium")
                else:
                    print("Password yang anda masukkan salah")
                break
        if not akunAda: #JIKA USERNAME TIDAK DITEMUKAN MAKA AKAN MENGEKSEKUSI COMMAND INI
            print("akun anda tidak dikenal")
            break

def topup():
    username = input("Masukkan username: ")
    pw = pwinput.pwinput("Masukkan Password: ")
    for user in userfree:
            if user["username"].lower() == username:
                if user["password"] == pw:
                    saldo = int(input("Masukkan jumlah saldo yang ingin diisi: "))
                    user["saldo"]+=saldo
                    akunAda = True
                    with open (json_path_free, "w") as sn:
                        json.dump(userfree, sn, indent=4)
                else:
                    print("Password yang anda masukkan salah")
                
                break
    for user in userpay:
        if user["username"].lower() == username:
            if user["password"] == pw:
                saldo = int(input("Masukkan jumlah saldo yang ingin diisi: "))
                user["saldo"]+=saldo
                akunAda = True
                with open (json_path_pay, "w") as sn:
                    json.dump(userpay,sn,indent=4)
            else:
                print("Password yang anda masukkan salah")
            break
    if not akunAda: 
        print("akun anda tidak dikenal")


#FUNCTION UNTUK BERALIH KE AKUN PREMIUM
def premium():
    while True:
        username = input("Masukkan username: ")
        pw = pwinput.pwinput("Masukkan Password: ")
        akunAda = False
        for user in userfree:
                if user["username"].lower() == username:
                    akunAda = True
                    if user["password"] == pw:
                        bayar = input("Apakah kamu yakin ingin beralih ke akun premium? (y/t): ").lower()
                        if bayar == "y":
                            if user["saldo"] < 50000:
                                ask = input(f"Saldo anda tidak mencukupi, saldo anda sisa {user['saldo']}, apakah mau isi saldo? (y/t) :").lower()
                                if ask == "y":
                                    topup()
                                elif ask == "t":
                                    break
                                else:
                                    print("Invalid")
                            elif user["saldo"] >= 50000:
                                print("Anda beralih ke akun premium")
                                break
                        elif bayar == "t":
                            break
                        else:
                            print("Invalid")
                    else:
                        print("Password yang anda masukkan salah")
                    break
        if not akunAda: 
            print("akun anda tidak dikenal")


def menu_admin():
    while True:
        print("1. Tampilkan Daftar Film")
        print("2. Tambah Film")
        print("3. Ubah Film")
        print("4. Hapus Film")
        print("5. Keluar")
        pilihan = input("Pilihan Anda: ")

        if pilihan == "1":
            tampilkan_daftar_film()
        elif pilihan == "2":
            tambah()
        elif pilihan == "3":
            ubah()
        elif pilihan == "4":
            Hapus()
        elif pilihan == "5":
            print("---Terima kasih telah menggunakan aplikasi.---")
            break
        else:
            print("---Pilihan tidak valid. Silakan coba lagi.---")

def tambah():
    nomorMaks = max([item[0] for item in film])
    nomorFilm = nomorMaks + 1
    judulFilm = input("Masukkan Nama Film: ")
    Genre = (input("Masukkan Genre: "))
    tanggalRelease = (input("Masukkan Tanggal Release: "))
    tambahan = [nomorFilm, judulFilm, Genre, tanggalRelease]
    film.append(tambahan)
    with open (json_path_film,"w") as sn:
        json.dump(film,sn, indent=4)
    print("------------------------Film berhasil ditambahkan.--------------------------")

def ubah():
    tampilkan_daftar_film()
    nomorFilm = int(input("Masukkan No film yang akan diubah: "))
    for i in range(len(film)):
        if film[i][0] == nomorFilm:
            judulFilm = input("Masukkan Judul Film baru: ")
            Genre = input("Masukkan Genre Film baru: ")
            waktuRelease = input("Masukkan waktu release Film baru: ")
            film[i][1] = judulFilm
            film[i][2] = Genre
            film[i][3] = waktuRelease
            with open (json_path_film,"w") as sn:
                json.dump(film,sn, indent=4)
            print("------------------------Film berhasil ubah.--------------------------")
    else:
        print("Maaf Perhiasan dengan ID tersebut tidak ditemukan.")

def Hapus():
    tampilkan_daftar_film()
    nomorFilm = int(input("Masukan No Film yang akan dihapus: "))
    ada = False
    for i in range(len(film)):
        if film[i][0] == nomorFilm:
            del film[i]
            ada = True
            break
    if ada:
        for i in range(len(film)):
            film[i][0] = i + 1
        with open (json_path_film,"w") as sn:
            json.dump(film,sn, indent=4)
        print("------------------------Film berhasil Dihapus.--------------------------")
    else:
        print("Maaf Film dengan No tersebut tidak ditemukan.")


while True:
    print("==============================================================================")
    print("|                                                                            |")
    print("|                                                                            |")
    print("|                                 1. Register                                |")
    print("|                                 2. Login                                   |")
    print("|                                 0. Keluar                                  |")
    print("|                                                                            |")
    print("|                                                                            |")
    print("==============================================================================")
    ask = input("Pilih opsi (1/2/0): ")
    if ask == "1":
        register()
    elif ask == "2":
        login()
    elif ask == "0":
        print("----------------------------Terima Kasih--------------------------------")
        break
    else:
        print("Maaf Perhiasan dengan ID tersebut tidak ditemukan.")

