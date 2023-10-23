import os
import json
import pwinput
from prettytable import PrettyTable
os.system('cls')


json_path_film = 'D:/01_CODE/DDP/PraktikumDDP/TESPA/dataData/film.json'
json_path_admin = 'D:/01_CODE/DDP/PraktikumDDP/TESPA/dataData/admin.json'
json_path_user = 'D:/01_CODE/DDP/PraktikumDDP/TESPA/dataData/user.json'
with open(json_path_film,"r") as filmdata:
    film = json.loads(filmdata.read())
with open(json_path_admin, "r") as admindata:
    admin = json.loads(admindata.read())
with open(json_path_user,"r") as userdata:
    dataUser = json.loads(userdata.read())


print("==============================================================================")
print("|                                                                            |")
print("|                                   SI-FLIX                                  |")
print("|                                                                            |")
print("==============================================================================")


def daftarFilm():
    table_film = PrettyTable()
    table_film.field_names =  ["ID","Judul Film","Genre","Waktu Release"]
    for item in film:
        table_film.add_row(item)
    print(table_film)


def register():
    print("Silahkan lakukan Registrasi")
    while True:
        username = input("Masukkan username: ").lower()
        password = pwinput.pwinput("Masukkan password: ")
        notAvailable = False #VARIABLE YANG DIGUNAKAN UNTUK MENGECEK APAKAH USERNAME TERDAFTAR ATAU TIDAK
        for admin_acc in admin:
            if admin_acc["adminName"].lower() == username:
                print("username sudah digunakan cobalagi yang lain")
                notAvailable = True #VARIABLE BERUBAH MENJADI TRUE SAAT USERNAME SUDAH TIDAK TERSEDIA
                break
        for user in dataUser:
            if user["username"].lower() == username:
                print("username sudah digunakan cobalagi yang lain")
                notAvailable = True #VARIABLE BERUBAH MENJADI TRUE SAAT USERNAME SUDAH TIDAK TERSEDIA
                break
        #JIKA USERNAME TERSEDIA DAN VARIBLENYA MASIH BERNILAI FALSE MAKA AKAN BERHASIL MENAMBAHKAN AKUN BARU
        if not notAvailable:
            akun_baru = {"username": username, "password": password, "saldo": 0, "privilage": "free"}
            dataUser.append(akun_baru)
            print("berhasil membuat akun")
            with open (json_path_user, "w") as sn:
                json.dump(dataUser,sn,indent=4)
            break

#FUNCTION UNTUK LOGIN
def login():
    print("Silahkan Login")
    while True:
        username = input("Masukkan username: ").lower()
        password = pwinput.pwinput("Masukkan password: ")
        akunAda = False #SEBUAH VARIABLE YANG DIGUNAKAN UNTUK MENGECEK APAKAH USERNAME TERDAFTAR ATAU TIDAK
        for admin_acc in admin:
            if admin_acc["adminName"].lower() == username and admin_acc["pwAdmin"]==password:
                akunAda = True
                print("Berhasil login sebagai admin")
                return menu_admin()
        for user in dataUser:
            if user["username"].lower() == username:
                akunAda = True#JIKA USERNAME DITEMUKAN MAKA VARIABLE AKAN MENJADI TRUE
                if user["password"] == password:
                    if user["privilage"] == "free":
                        print("\nBerhasil login sebagai user Free")
                        return menuUserFree()
                    elif user["privilage"] == "premium":
                        print("\nBerhasil login sebagai user Premium")
                        return menuUserPremium()
                else:
                    print("Password yang anda masukkan salah")
                break
        if not akunAda: #JIKA USERNAME TIDAK DITEMUKAN MAKA AKAN MENGEKSEKUSI COMMAND INI
            print("akun anda tidak dikenal")
            break




def menuUserFree():
    while True:
        print("==============================================================================")
        print("|                                                                            |")
        print("|                                                                            |")
        print("|                                1. Daftar Film                              |")
        print("|                                2. Beli Premium                             |")
        print("|                                3. Isi Saldo                                |")
        print("|                                0. Keluar                                   |")
        print("|                                                                            |")
        print("|                                                                            |")
        print("==============================================================================")
        ask = input("Pilih opsi (1/2/3/0): ")
        if ask == "1":
            userFree()
        elif ask == "2":
            premium()
        elif ask == "3":
            topup()
        elif ask == "0":
            break
        else:
            print("Maaf input anda invalid, coba untuk input sesuai pilihan yang ada.")




def userFree():
    while True:
        daftarFilm()
        print("1. Pilih ID Film")
        print("0. Keluar")
        ask = input("Pilih opsi: ")
        if ask == "1":
            ask = int(input("Pilih ID Film yang ingin dimainkan: "))
            print("Kamu perlu beralih ke akun premium jika ingin memainkan film.")
            ask = input("Apakah kamu ingin beralih ke premium? (y/n): ").lower()
            if ask == "y":
                return premium()
            elif ask == "n":
                break
            else:
                print("Maaf input anda invalid.")
        elif ask == "0":
            break
        else:
            print("Maaf input anda invalid.")



def topup():
    username = input("Masukkan username: ")
    password = pwinput.pwinput("Masukkan Password: ")
    for user in dataUser:
            if user["username"].lower() == username:
                if user["password"] == password:
                    saldo = int(input("Masukkan jumlah saldo yang ingin diisi: "))
                    user["saldo"]+=saldo
                    akunAda = True
                    with open (json_path_user, "w") as sn:
                        json.dump(dataUser, sn, indent=4)
                else:
                    print("Password yang anda masukkan salah")
                break
    if not akunAda: 
        print("akun anda tidak dikenal")


#FUNCTION UNTUK BERALIH KE AKUN PREMIUM
def premium():
    print("==============================================================================")
    print("|                                                                            |")
    print("|                            Beralih Akun Premium                            |")
    print("|                                                                            |")
    print("==============================================================================")
    username = input("Masukkan username: ")
    password = pwinput.pwinput("Masukkan Password: ")
    akunAda = False
    for user in dataUser:
            if user["username"].lower() == username:
                akunAda = True
                if user["password"] == password:
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
                            user["privilage"] = "premium"
                            with open (json_path_user,"w") as sn:
                                json.dump(dataUser,sn,indent=4)
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
        print("----------------------------akun anda tidak dikenal---------------------------")


def menuUserPremium():
    while True:
        print("==============================================================================")
        print("|                                                                            |")
        print("|                                                                            |")
        print("|                                1. Daftar Film                              |")
        print("|                                0. Keluar                                   |")
        print("|                                                                            |")
        print("|                                                                            |")
        print("==============================================================================")
        ask = input("Pilih Opsi (1/0): ")
        if ask == "1":
            nontonPremium()
        elif ask == "0":
            break




def nontonPremium():
    daftarFilm()
    ask = int(input("Pilih ID Film: "))
    for i in range(len(film)):
        if film[i][0] == ask:
            print("Memainkan film ")
            print(f"Judul          : {film[i][1]}")
            print(f"Genre          : {film[i][2]}")
            print(f"Tanggal Tayang : {film[i][3]}")
            print("==============================================================================")
            print("||                                                                          ||")
            print("||                                                                          ||")
            print("||                                                                          ||")
            print("||                                                                          ||")
            print("||                                                                          ||")
            print("||                               ||        ||                               ||")
            print("||                               ||        ||                               ||")
            print("||                               ||        ||                               ||")
            print("||                               ||        ||                               ||")
            print("||                               ||        ||                               ||")
            print("||                                                                          ||")
            print("||                                                                          ||")
            print("||                                                                          ||")
            print("||                                                                          ||")
            print("||                                                                          ||")
            print("==============================================================================")
            break
        else:
            print("Maaf ID yang anda pilih tidak ada.")




def menu_admin():
    while True:
        print("1. Tampilkan Daftar Film")
        print("2. Tambah Film")
        print("3. Ubah Film")
        print("4. Hapus Film")
        print("5. Keluar")
        pilihan = input("Pilihan Anda: ")
        if pilihan == "1":
            daftarFilm()
        elif pilihan == "2":
            tambah()
        elif pilihan == "3":
            ubah()
        elif pilihan == "4":
            Hapus()
        elif pilihan == "5":
            print("---Terima kasih telah menggunakan aplikasi---")
            break
        else:
            print("---Pilihan tidak valid, Silakan coba lagi---")

def tambah():
    IDMaks = max([item[0] for item in film])
    IDFilm = IDMaks + 1
    judulFilm = input("Masukkan Nama Film: ")
    Genre = (input("Masukkan Genre: "))
    tanggalRelease = (input("Masukkan Tanggal Release: "))
    tambahan = [nomorFilm, judulFilm, Genre, tanggalRelease]
    film.append(tambahan)
    with open (json_path_film,"w") as sn:
        json.dump(film,sn, indent=4)
    print("------------------------Film berhasil ditambahkan--------------------------")

def ubah():
    daftarFilm()
    IDFilm = int(input("Masukkan No film yang akan diubah: "))
    for i in range(len(film)):
        if film[i][0] == IDFilm:
            judulFilm = input("Masukkan Judul Film baru: ")
            Genre = input("Masukkan Genre Film baru: ")
            waktuRelease = input("Masukkan waktu release Film baru: ")
            film[i][1] = judulFilm
            film[i][2] = Genre
            film[i][3] = waktuRelease
            with open (json_path_film,"w") as sn:
                json.dump(film,sn, indent=4)
            print("------------------------Film berhasil ubah--------------------------")
    else:
        print("Maaf Perhiasan dengan ID tersebut tidak ditemukan.")

def Hapus():
    daftarFilm()
    IDFilm = int(input("Masukan No Film yang akan dihapus: "))
    ada = False
    for i in range(len(film)):
        if film[i][0] == IDFilm:
            del film[i]
            ada = True
            break
    if ada:
        for i in range(len(film)):
            film[i][0] = i + 1
        with open (json_path_film,"w") as sn:
            json.dump(film,sn, indent=4)
        print("------------------------Film berhasil Dihapus--------------------------")
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
        print("--------------------------------Terima Kasih----------------------------------")
        break
    else:
        print("Maaf input anda invalid, coba untuk input sesuai pilihan yang ada.")
