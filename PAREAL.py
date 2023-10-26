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
        notAvailable = False
        username = input("Masukkan username: ").lower().lstrip()
        if " " in username:
            print("username tidak boleh mengandung spasi")
            continue
        if username == "":
            print("Username tidak boleh kosong")
            continue
        password = pwinput.pwinput("Masukkan password: ").strip()
        if password == "":
            print("Passsword tidak boleh kosong")
            print("")
        if all (x.isalpha()for x in username):
            for admin_acc in admin:
                if admin_acc["adminName"].lower() == username:
                    print("username sudah digunakan cobalagi yang lain")
                    notAvailable = True
                    break
            for user in dataUser:
                if user["username"].lower() == username:
                    print("username sudah digunakan cobalagi yang lain")
                    notAvailable = True 
                    break
        if not notAvailable:
            akun_baru = {"username": username, "password": password, "saldo": 0, "privilage": "free"}
            dataUser.append(akun_baru)
            print("berhasil membuat akun")
            with open (json_path_user, "w") as sn:
                json.dump(dataUser,sn,indent=4)
            break
        else:
            print("Username Harus huruf")
            continue



#FUNCTION UNTUK LOGIN
def login():
    print("Silahkan Login")
    while True:
        username = input("Masukkan username: ").lower()
        password = pwinput.pwinput("Masukkan password: ")
        akunAda = False 
        for admin_acc in admin:
            if admin_acc["adminName"].lower() == username and admin_acc["pwAdmin"]==password:
                akunAda = True
                print("\n-------------------------Berhasil login sebagai admin-------------------------")
                return menuAdmin()
        for user in dataUser:
            if user["username"].lower() == username:
                akunAda = True
                if user["password"] == password:
                    if user["privilage"] == "free":
                        print("\n-----------------------Berhasil login sebagai user Free-----------------------")
                        return menuUserFree()
                    elif user["privilage"] == "premium":
                        print("\n----------------------Berhasil login sebagai user Premium---------------------")
                        return menuUserPremium()
                else:
                    print("Password yang anda masukkan salah")
                break
        if not akunAda: 
            print("akun anda tidak dikenal")
            break




def menuUserFree():
    while True:
        print("==============================================================================")
        print("|                                                                            |")
        print("|                                   SI-FLIX                                  |")
        print("|                                  USER-FREE                                 |")
        print("|                                                                            |")
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
            ask = input("Apakah kamu ingin beralih ke premium? (y/t): ").lower()
            if ask == "y":
                return premium()
            elif ask == "t":
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
    akunAda = False
    try:
        for user in dataUser:
                if user["username"].lower() == username:
                    if user["password"] == password:
                        akunAda = True
                        topup = int(input("Masukkan jumlah saldo yang ingin diisi: "))
                        if topup < 10000:
                            print ("minimal topup 10000")
                        elif topup > 20000000:
                            print("")
                        else:
                            user["saldo"]+=topup
                            with open ("historytopup.txt","a") as history:
                                print(f"""
                                ==================================================
                                    Berhasil Menambahkan Saldo sebesar {topup}
                                    Saldo sekarang {user['saldo']}
                                ==================================================
                                """, file=history)
                            
                            print("==================================================")
                            print(f"  Berhasil Menambahkan Saldo sebesar {topup}")
                            print(f"  Saldo Sekarang Berjumlah {user['saldo']}")
                            print("==================================================\n")
                            with open (json_path_user, "w") as sn:
                                json.dump(dataUser, sn, indent=4)
                    else:
                        print("Password yang anda masukkan salah")
                    break
        if not akunAda: 
            print("----------------------------akun anda tidak dikenal---------------------------\n")
    except ValueError:
        print("Saldo harus berupa angka")





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
                    bayar = input("Apakah kamu ingin beralih ke akun premium dengan harga Rp800.000? (y/t): ").lower()
                    if bayar == "y":
                        if user["saldo"] < 800000:
                            ask = input(f"Saldo anda tidak mencukupi, saldo anda sisa {user['saldo']}, apakah mau isi saldo? (y/t) :").lower()
                            if ask == "y":
                                topup()
                            elif ask == "t":
                                break
                            else:
                                print("Invalid")
                        elif user["saldo"] >= 800000:
                            saldoAwal = user["saldo"]
                            user["privilage"] = "premium"
                            user["saldo"]-=800000
                            with open (json_path_user,"w") as sn:
                                json.dump(dataUser,sn,indent=4)
                            print("--------Anda berhasil beralih ke akun premium-------\n")
                            with open ("historypembelian.txt","a") as history:
                                print(f"""
        =====================================================

                            SI-FLIX INVOICE              
                            
        =====================================================

            Upgrade Premium Account            800.000    
                    
        -----------------------------------------------------

            Total                             800000    
            Saldo Awal                        {saldoAwal}   
            Saldo Sisa                        {user['saldo']}
                        
        -----------------------------------------------------
        """,file=history)
                            # print("====================================================")
                            # print("                                                    ")
                            # print("                  SI-FLIX INVOICE                   ")
                            # print("                                                    ")
                            # print("====================================================")
                            # print("                                                    ")
                            # print("  Upgrade Premium Account            800.000    ")
                            # print("                                                    ")
                            # print("----------------------------------------------------")
                            # print("                                                    ")
                            # print("   Total                             800.000    ")
                            # print(f"  Saldo Awal                        {saldoAwal}    ")
                            # print(f"  Saldo Sisa                        {user['saldo']}")
                            # print("                                                    ")
                            # print("----------------------------------------------------")
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
        print("|                                   SI-FLIX                                  |")
        print("|                                   PREMIUM                                  |")
        print("|                                                                            |")
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
    while True:
        daftarFilm()
        filmAda = False
        try:
            print("0 untuk keluar")
            ask = int(input("Pilih ID Film: "))
            if ask == 0:
                break
            for i in range(len(film)):
                if film[i][0] == ask:
                    filmAda = True
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
                    input("Enter untuk keluar")
                    return
            if not filmAda:
                print("Maaf ID yang anda pilih tidak ada.")
        except ValueError:
            print("Pilih ID dengan menggunakan angka")



def menuAdmin():
    while True:
        print("==============================================================================")
        print("|                                                                            |")
        print("|                                Menu ADMIN                                  |")
        print("|                             1. Tampilkan Daftar Film                       |")
        print("|                             2. Tambah Film                                 |")
        print("|                             3. Ubah Film                                   |")
        print("|                             4. Hapus Film                                  |")
        print("|                             0. Keluar                                      |")
        print("|                                                                            |")
        print("==============================================================================")
        pilihan = input("Pilihan Anda: ")
        if pilihan == "1":
            daftarFilm()
        elif pilihan == "2":
            tambah()
        elif pilihan == "3":
            ubah()
        elif pilihan == "4":
            Hapus()
        elif pilihan == "0":
            print("---Terima kasih telah menggunakan aplikasi---")
            break
        else:
            print("---Pilihan tidak valid, Silakan coba lagi---")




def tambah():
    while True:
        IDMaks = max([item[0] for item in film])
        IDFilm = IDMaks + 1
        judulFilm = input("Masukkan Nama Film: ").strip()
        if judulFilm == "":
            print("Judul Film tidak boleh kosong")
            continue
        genre = (input("Masukkan Genre: ")).strip()
        if genre == "":
            print("Genre Film tidak boleh kosong")
            continue
        tanggalRelease = (input("Masukkan Tanggal Release: ")).strip()
        if tanggalRelease == "":
            print("Tanggal release tidak boleh kosong")
            continue
        tambahan = [IDFilm, judulFilm, genre, tanggalRelease]
        film.append(tambahan)
        with open (json_path_film,"w") as sn:
            json.dump(film,sn, indent=4)
        print("------------------------Film berhasil ditambahkan--------------------------")
        break




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
