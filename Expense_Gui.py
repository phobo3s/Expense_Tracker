import sqlite3
import os
import platform
from prettytable import PrettyTable
import PySimpleGUI as sg
import matplotlib.pyplot as plt

# Application path
# for mac os and windows is different i don't know why
if platform.system() == "Windows":
    myPath = os.path.dirname(__file__) + "\\"
    DBPath = myPath + "Data.db"
else:
    myPath = os.getcwd() + "/"
    DBPath = myPath + "Data.db"

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

def ConnectDB():
    # Create Connection (if there is not database will created)
    conn = sqlite3.connect(DBPath)
    return conn

def EnterRecord(conn,t):
    # conn = Connected Database
    # Create Cursor Object
    curs = conn.cursor()
    curs.execute("INSERT INTO expenses (tarih,harcamakonusu,miktar) VALUES (?,?,?)",t)
    conn.commit()

def Main():
    if ControlDatabase():
        conn = ConnectDB()
    else:
        CreateDatabase()
    while True:
        menuSelection = MainMenu()
        if menuSelection == "1":
            GetRecordMenu(conn)
        elif menuSelection == "2":
            DBMenu(conn)
        elif menuSelection == "3":
            #data = DrawGraph(conn)
            DrawGraph(data)
        elif menuSelection == "0":
            CloseDatabase(conn)
            quit()
        else:
            print("İnanılmaz bir hata!!!")
 
def DrawGraph(conn):   
    data = DumpDB(conn)
    sg.theme("DarkAmber")
    layout = [[sg.Text("HARCAMA GRAFİĞİ", size=(40,1), justification="Center")],
            [sg.Canvas(size=(640,480), key= "canvas")],
            [sg.Button("Çıkış",focus=True)]]
    window = sg.Window("Harcama Grafiği", layout)

    # Plotting
    data = DumpDB(conn)
    headers = data[0]
    records = data[1]
    #plt.plot(records)


    # Plotting
    while True:
        event, value = window.read()
        if event in (None,"Çıkış"):
            break
        else:
            pass
    window.close()
    Main()


def GetRecordMenu(conn):
    sg.theme("DarkAmber")
    layout = [[sg.Text("Kayıt Verisini Giriniz...")],
            [sg.Text("Harcama Tarihi      :  ",justification="Left"),sg.In("",size=(20,1),focus=True,key=("date"),justification="Right")],
            [sg.Text("Harcama Konusu      : ",justification="Left"),sg.In("",size=(20,1),key=("subject"),justification="Right")],
            [sg.Text("Harcama Miktarı(TL) : ",justification="Left"),sg.In("",size=(15,1),key=("amoun"),justification="Right")],
            [sg.Text("")],
            [sg.Button("Kaydet"),sg.Button("İptal"),sg.Button("Çıkış")]]
    window = sg.Window("Veri Tabanı Menü", layout)

    while True:
        event, value = window.read()
        if event in (None,"Çıkış"):
            break
        elif event in (None,"İptal"):
            window["date"].update("")
            #Set Focus???
            window["subject"].update("")
            window["amoun"].update("")
        elif event in (None,"Kaydet"):
            # Value Format Controls

            # Value Format Controls
            t = (value["date"],value["subject"],value["amoun"])
            EnterRecord(conn, t)
            sg.popup("Kayıt Tamamlandı...")
            window["date"].update("")
            #Set Focus???
            window["subject"].update("")
            window["amoun"].update("")
            
            pass
        else:
            pass
    window.close()
    Main()
  
def DumpDB(conn):
    # Create Cursor Object
    curs = conn.cursor()
    dump = curs.execute("SELECT * FROM expenses").fetchall()
    headerlist = []
    for i in curs.execute("PRAGMA table_info('expenses')").fetchall():
        headerlist.append(i[1]) 
    data = (headerlist, dump)
    return data

def SweetPrint(headers, records):
    table = PrettyTable(headers)
    for rec in records:    
        table.add_row(rec)
    return table

def MainMenu():
    sg.theme("DarkAmber")
    layout = [[sg.Text("Lütfen İşlem Seçiminizi Yapınız...")],
            [sg.Button("Veri Girişi",key="1")], 
            [sg.Button("Database Görüntüle",key="2")],
            [sg.Button("Harcama Grafiği",key="3")],
            [sg.Text("")],
            [sg.Button("Çıkış",key="0")]]

    window = sg.Window("Ana Menü", layout)

    while True:
        event, value = window.read()
        if event in (None,"0"):
            break
        else:
            break
    window.close()
    return event

def DBMenu(conn):
    data = DumpDB(conn)
    sg.theme("DarkAmber")
    layout = [[sg.Text("Veri Tabanı İçeriği Aşağıdadır...")],
            [sg.Output(size=(80, 20),key="output")],
            [sg.Text("")],
            [sg.Button("Çıkış"),sg.Button("Göster")]]
    window = sg.Window("Veri Tabanı Menü", layout)

    while True:
        event, value = window.read()
        if event in (None,"Çıkış"):
            break
        elif event in (None,"Göster"):
            window["output"].update(SweetPrint(data[0], data[1]))
        else:
            pass
    window.close()
    Main()

if __name__ == "__main__":
    #GetRecordMenu()
    Main()
