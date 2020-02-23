import sqlite3
import time
import datetime

db = sqlite3.connect("tietokanta.db")
db.isolation_level = None

c = db.cursor()



    

while(True):
    
    valinta = input("Valitse toiminto 1-9: ")
    if valinta=="1":
        
        try:
            c.execute("CREATE TABLE Paikat (id INTEGER PRIMARY KEY, nimi TEXT UNIQUE);")
            c.execute("CREATE TABLE Asiakkaat (id INTEGER PRIMARY KEY, nimi TEXT UNIQUE);")
            c.execute("CREATE TABLE Paketit (id INTEGER PRIMARY KEY, asiakas_id INTEGER, seurantakoodi INTEGER UNIQUE);")
            c.execute("CREATE TABLE Tapahtumat (id INTEGER PRIMARY KEY, paketti_id INTEGER, paikka_id INTEGER, kuvaus TEXT, aika DATETIME);")
            c.execute("CREATE INDEX idx_asiakas_id ON Paketit (asiakas_id);")
            c.execute("CREATE INDEX idx_paketti_id ON Tapahtumat (paketti_id);")
            print("Tietokanta luotu!")

        except:
            print("Tietokannan luominen epäonnistui.")


    if valinta=="2":
        paikanNimi = input("Kirjoita paikannimi: ")
        try:
            c.execute("INSERT INTO Paikat (nimi) VALUES (?);",[paikanNimi])
            print("Paikka " + paikanNimi + " lisätty onnistuneesti!")
        except:
            print("Paikan lisääminen epäonnistui! Onhan tietokanta varmasti luotu jo? Sama nimi voi olla vain yhdellä paikalla.")

    if valinta=="3":
        asiakasNimi = input("Kirjoita asiakkaan nimi: ")
        try:
            c.execute("INSERT INTO Asiakkaat (nimi) VALUES (?);",[asiakasNimi])
            print("Asiakas " + asiakasNimi + " lisätty onnistuneesti!")
        except:
            print("Asiakkaan lisääminen epäonnistui! Onhan tietokanta varmasti luotu jo? Sama nimi voi olla vain yhdellä asiakkaalla.")

    if valinta=="4":
        seurantaKoodi = input("Kirjoita seurantakoodi: ")
        pakettiAsiakas = input("Kirjoita asiakkaan nimi: ")

        try:
            c.execute("SELECT id FROM Asiakkaat WHERE nimi = ?",[pakettiAsiakas])
            asiakasID = c.fetchone()
            
            if asiakasID != None:
                c.execute("INSERT INTO Paketit (asiakas_id, seurantakoodi) VALUES (?, ?);", [asiakasID[0], seurantaKoodi])
            else:
                print("Asiakasta ei löytynyt.")

        except:
            print("Paketin lisääminen epäonnistui! Seurantakoodit voivat sisältää vain numeroita.")
            print(e)


    if valinta=="5":
        seurantaKoodi = input("Kirjoita seurantakoodi: ")
        paikanNimi = input("Kirjoita tapahtumapaikan nimi: ")
        tapahtumaKuvaus = input("Kirjoita tapahtuman kuvaus: ")

        try:
            c.execute("SELECT id FROM Paketit WHERE seurantakoodi = ?",[seurantaKoodi])
            pakettiID = c.fetchone()
            c.execute("SELECT id FROM Paikat WHERE nimi = ?", [paikanNimi])
            paikkaID = c.fetchone()

            if pakettiID!= None and paikkaID != None:
                c.execute("INSERT INTO Tapahtumat(paketti_id, paikka_id, kuvaus, aika) VALUES (?, ?, ?, ?)", [pakettiID[0], paikkaID[0], tapahtumaKuvaus, datetime.datetime.now().strftime('%d.%m.%Y %H:%M')])


        except:
            print("Jokin meni vikaan. Oliko paikka tai seurantakoodi varmasti oikein?")
            

    if valinta=="6":
        seurantaKoodi = input("Kirjoita paketin seurantakoodi: ")
        try:
            c.execute("SELECT id FROM Paketit WHERE seurantakoodi = ?",[seurantaKoodi])
            pakettiID = c.fetchone()
            c.execute("SELECT paikka_id, kuvaus, aika  FROM Tapahtumat WHERE paketti_id = ?",[pakettiID[0]])
            tapahtumat = c.fetchall()

            for i in tapahtumat:
                for k in i:
                    if isinstance(k, int):
                        c.execute("SELECT nimi FROM Paikat WHERE id = ?",[k])
                        paikkaNimi = c.fetchone()
                        print(paikkaNimi[0],end='')
                        print(", ", end='')
                    else:
                        print(k, end = '')
                        print(", ", end = '')
                print("\n")
                                   
        
        except :
            print("Jokin meni vikaan. Kirjoititko seurantakoodin varmasti oikein?")

    if valinta=="7":
        nimi = input("Anna asiakkaan nimi: ")
        try:
            c.execute("SELECT id FROM Asiakkaat WHERE nimi = ?",[nimi])
            asiakasID = c.fetchone()
            c.execute("SELECT seurantakoodi, id FROM Paketit WHERE asiakas_id = ?",[asiakasID[0]])
            paketit = c.fetchall()

            for i in paketit:
                print (i[0], end='')
                c.execute("SELECT COUNT(id) FROM Tapahtumat WHERE paketti_id = ?",[i[1]])
                tapahtumaMaara = c.fetchone()
                print(", " + str(tapahtumaMaara[0]) + " tapahtumaa")
                
            
        except:
            print("Jokin meni vikaan. Kirjoititko asiakkaan nimen oikein?")

    if valinta=="8":
        paikanNimi = input("Anna paikannimi: ")
        try:
            c.execute("SELECT id from Paikat WHERE nimi = ?",[paikanNimi])
            paikkaID = c.fetchone()
            pvm = input("Anna päivämäärä: ")
            pvm = "%"+pvm+"%"

            c.execute("SELECT COUNT(id) FROM Tapahtumat WHERE paikka_id = ? AND aika LIKE ?",[paikkaID[0],pvm])
            tapahtumaMaara = c.fetchone()
            print("Tapahtumia: "+str(tapahtumaMaara[0]))
        except:
            print("Jokin meni vikaan. Kirjoititko varmasti paikannimen oikein?")

    if valinta=="9":
        c.execute("BEGIN TRANSACTION;")
        kokoalkuaika = time.time()

        i = 0
        alkuaika = time.time()
        while i<1000:
            c.execute("INSERT INTO Paikat(nimi) VALUES (?);",["P"+str(i)])
            i=i+1
        
        loppuaika = time.time()
        print(loppuaika-alkuaika)

        i = 0
        alkuaika = time.time()
        while i<1000:
            c.execute("INSERT INTO Asiakkaat(nimi) VALUES (?);",["A"+str(i)])
            i=i+1
        
        loppuaika = time.time()
        print(loppuaika-alkuaika)

        i = 0
        alkuaika = time.time()
        while i<1000:
            c.execute("INSERT INTO Paketit(asiakas_id, seurantakoodi) VALUES (?, ?);",[str(i),i+i])
            i=i+1
        
        loppuaika = time.time()
        print(loppuaika-alkuaika)

        i = 0
        alkuaika = time.time()
        while i<1000000:
            c.execute("INSERT INTO Tapahtumat(paketti_id, paikka_id, kuvaus, aika) VALUES (?, ?, ?, ?);",[200,5,"Testi",datetime.datetime.now().strftime('%d.%m.%Y %H:%M')])
            i=i+1

        i = 0
        alkuaika = time.time()
        while i<1000:
            c.execute("SELECT COUNT(id) FROM Paketit WHERE asiakas_id = ?",[i])
            i=i+1
        
        loppuaika = time.time()
        print(loppuaika-alkuaika)
        

        c.execute("COMMIT;")
        loppuaika = time.time()
        print(loppuaika-alkuaika)

        i = 0
        alkuaika = time.time()
        while i<1000:
            c.execute("SELECT COUNT(id) FROM Tapahtumat WHERE paketti_id = ?",[i])
            i=i+1
        
        loppuaika = time.time()
        print(loppuaika-alkuaika)

        


        
        lopullineloppuaika = time.time()
        print("Koko testin tulos: " + str((lopullineloppuaika-kokoalkuaika)))

    

        
            
            
        

    
        
    
