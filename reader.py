import sqlite3
import os

class reader:

    def check(self)-> bool:
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables:list[str]=self.cur.fetchall()
        tables.sort()
        tablesinlist=[]
        for table in tables:
            tablesinlist.append(table[0])
        correcttables=["Diccionario","GlobalMetadata","Nombres",
                       "Pronombres","Verbos"]
        return correcttables==tablesinlist


    def __init__(self,file:str) -> None:
        if not os.path.exists(file):
            raise Exception("No database file found")
        else:
            self.con=sqlite3.connect(file)
            self.cur=self.con.cursor()
            if not self.check():
                raise("Database has wrong schema")
        self.dictstmt="SELECT Espanol,Aleman FROM Diccionario WHERE ROWID=?"
        self.nounstmt="SELECT Nombre,Plural,Genero FROM Nombres WHERE ROWID=?"
        self.verbstmt="SELECT Verbo,Regular,PS,SS,TS,PP,SP,TP FROM Verbos WHERE ROWID=?"
        self.sizestmt="SELECT COUNT(*) FROM "

    def __del__(self):
        self.cur.close()
        self.con.close()

    def readRowid(self,i:int)->tuple[str]:
        self.cur.execute(self.dictstmt,(str(i),))
        return self.cur.fetchone()


    def readNoun(self,i:int)->tuple[str]:
        self.cur.execute(self.nounstmt,(str(i),))
        return self.cur.fetchone()
    
    def readVerb(self,i:int)->tuple[str]:
        self.cur.execute(self.verbstmt,(str(i),))
        return self.cur.fetchone()
    
    def getSize(self,table:str)->int:
        self.cur.execute(self.sizestmt+table)
        return int(self.cur.fetchone()[0])

    def getPronouns(self)->list[str]:
        self.cur.execute("SELECT Pronombre FROM Pronombres")
        probadform=self.cur.fetchall()
        prolist=[]
        for pro in probadform:
            prolist.append(pro[0])
        return prolist

    def getLanguages(self)->tuple[str]:
        self.cur.execute("SELECT Idioma1,Idioma2 FROM GlobalMetadata")
        return self.cur.fetchone()
    
    def getPolisemicWords(self,language0:str,language1:str,word:str)->list[tuple[str]]:
        self.cur.execute("SELECT "+language0+" FROM Diccionario WHERE "+language1+"=?",(word,))
        return self.cur.fetchall()
