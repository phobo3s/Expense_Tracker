import sqlite3
import os
import time
from prettytable import PrettyTable
import PySimpleGUI as sg

# Application path
myPath = os.path.dirname(__file__) + "/"
DBPath = myPath + "Data.db"

class Database():
    pass


def ControlDatabase():
    result = os.path.isfile(DBPath)
    return result

def CreateDatabase():
    # Create Connection (if there is not database will created)
    conn = sqlite3.connect(DBPath)
    # Create Cursor Object
    curs = conn.cursor()
    curs.execute("CREATE TABLE expenses(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, tarih DATE NOT NULL, harcamakonusu TEXT NOT NULL, miktar REAL NOT NULL)")


    conn.commit()
    CloseDatabase(conn)

def CloseDatabase(conn):
    conn.close()
    os.system("cls")

def ConnectDB():
    # Create Connection (if there is not database will created)
    conn = sqlite3.connect(DBPath)
    return conn

def Menu():
    print(50*"=")
    print("Ne Yapmak İstiyorsunuz?... ")
    print("[1] - Veri Gir")
    print("[2] - Database'i Görüntüle")
    print("")
    print("[0] - Çıkış")
    print(50*"=")
    selection = input("Seçiminizi Tuşlayınız ve 'enter'a Basınız...")
    return selection

def Main():
    while True:
        if ControlDatabase():
            conn = ConnectDB()
            while True:
                os.system("cls")
                menuSelection = Menu()
                if menuSelection == "1":
                    GetandSetRecord(conn)
                elif menuSelection == "2":
                    DumpDB(conn)
                elif menuSelection == "0":
                    CloseDatabase(conn)
                    quit()
                else:
                    print("Hatalı Seçim Yaptınız lütfen tekrar deneyiniz.")
                    input("Hata Düzeltme İçin 'enter'a Basınız...")
        else:
            # No Database
            CreateDatabase()

def GetandSetRecord(conn):
    while True:
        os.system("cls")
        print("Lütfen Veri Giriniz...")
        date = input("Harcama Tarihi      :")
        subject = str(input("Harcama Konusu      :"))
        while True:
            try:
                amoun = float(input("Harcama Miktarı(TL) :"))
                break
            except ValueError:
                print("Para miktarını hatalı formatta girdiniz...")
        
        sel = input("Kaydet? E/H/Q")

        if sel == "E" or sel == "e":
            t = (date,subject,amoun)
            EnterRecord(conn, t)
            print("Veri Girildi...")
            time.sleep(2)
            break
        elif sel == "H" or sel == "h":
            input("Yeniden Denemek için 'enter'a basınız...")
        elif sel == "Q" or sel == "q":
            print("Veri Girişinden Çıkılıyor...")
            time.sleep(2)
            break
        else:
            input("Yanlış seçim yapıldı. Yeniden Denemek için 'enter'a basınız...")
              
def EnterRecord(conn,t):
    # conn = Connected Database
    # Create Cursor Object
    curs = conn.cursor()
    curs.execute("INSERT INTO expenses (tarih,harcamakonusu,miktar) VALUES (?,?,?)",t)
    conn.commit()

def DumpDB(conn):
    # Clear page
    os.system("cls")
    # Create Cursor Object
    curs = conn.cursor()
    dump = curs.execute("SELECT * FROM expenses").fetchall()
    headerlist = []
    for i in curs.execute("PRAGMA table_info('expenses')").fetchall():
        headerlist.append(i[1]) 
    SweetPrint(headerlist, dump)
    input("Geri Dönmek İçin 'enter'a Basınız...")
    
def SweetPrint(headers, records):
    table = PrettyTable(headers)
    for rec in records:    
        table.add_row(rec)
    print(table)

def MainMenu():
    layout = [[sg.Text("Lütfen İşlem Seçiminizi Yapınız...")],
            [sg.Button("Veri Girişi")], 
            [sg.Button("Database Görüntüle")],
            [sg.Text("")],
            [sg.Button("Çıkış")]]

    window = sg.Window("Ana Menü", layout)

    while True:
        event, value = window.read()
        if event in (None,"Çıkış"):
            break
    window.close()
    return event

    

def DBMenu():
    layout = [[sg.Text("Veri Tabanı İçeriği Aşağıdadır...")],
            [sg.Output(size=(80, 20))],
            [sg.Text("")],
            [sg.Button("Çıkış"),sg.Button("Run")]]
    window = sg.Window("Veri Tabanı Menü", layout)

    # Print The Database
    
    # End of Database
    window.Refresh()
    print("asfalkş")
    window.Refresh()
    while True:
        event, value = window.read()
        if event in (None,"Çıkış"):
            break
        else:
            print("asfalkş")
    window.close()
    return event

       

if __name__ == "__main__":
    
    #MainMenu()
    DBMenu()
    #quit()

    #Main()
