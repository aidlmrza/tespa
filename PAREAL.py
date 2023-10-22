import os
import json
import pwinput
from prettytable import PrettyTable
os.system('cls')


json_path_film = 'D:/01_CODE/DDP/PraktikumDDP/TESPA/dataData/film.json'
json_path_pay = 'D:/01_CODE/DDP/PraktikumDDP/TESPA/dataData/userpay.json'
json_path_free = 'D:/01_CODE/DDP/PraktikumDDP/TESPA/dataData/userfree.json'
json_path_admin = 'D:/01_CODE/DDP/PraktikumDDP/TESPA/dataData/admin.json'
with open(json_path_film,"r") as filmdata:
    film = json.loads(filmdata.read())
with open(json_path_free,"r") as userdata:
    userfree = json.loads(userdata.read())
with open(json_path_pay, "r") as userdata:
    userpay = json.loads(userdata.read())
with open(json_path_admin, "r") as admindata:
    admin = json.loads(admindata.read())


def daftarFilm():
    table = PrettyTable()
    table.field_names = ["No","Judul Film","Genre","Waktu Release"]
    for item in film:
        table.add_row(item)
    print(table)


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
