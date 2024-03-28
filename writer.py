import pandas as pd
import sqlite3
import os
from enum import Enum
import sys

class writer:

    def initDatabase(self)->None:
        # Setup sqlite
        self.cur.execute("PRAGMA journal_mode = wal")
        self.cur.execute("PRAGMA synchronous = normal")
        self.cur.execute("PRAGMA foreign_keys = on")
        self.con.commit()

        # Insert pronoums
        self.cur.execute("CREATE TABLE Pronombres ("
                    "Pronombre TEXT NOT NULL UNIQUE)")
        pronombres=["Ich","Du","Er, sie, es","Wie","Ihr","Sie"]
        for pronombre in pronombres:
            self.cur.execute("INSERT INTO Pronombres (Pronombre) VALUES(?)",(pronombre,))
        self.con.commit()

        # Create tables
        self.cur.execute("CREATE TABLE Verbos ("
                    "Verbo TEXT UNIQUE NOT NULL, "
                    "Regular BOOLEAN NOT NULL, "
                    "PS TEXT, "
                    "SS TEXT, "
                    "TS TEXT, "
                    "PP TEXT, "
                    "SP TEXT, "
                    "TP TEXT, "
                    "PRIMARY KEY(Verbo))"
                    )

        self.cur.execute("CREATE TABLE Nombres ("
                    "Nombre TEXT UNIQUE NOT NULL, "
                    "Plural TEXT, "
                    "Genero TEXT NOT NULL, "
                    "PRIMARY KEY(Nombre))"
                    )

        self.cur.execute("CREATE TABLE Diccionario ("
                    "Aleman TEXT NOT NULL, "
                    "Espanol TEXT NOT NULL)"
                    )
        
        self.cur.execute("CREATE TABLE GlobalMetadata ("
                         "Version TEXT NOT NULL UNIQUE)")
        self.cur.execute("INSERT INTO GlobalMetadata (Version) VALUES('1.0')")

        self.con.commit()

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
            self.con=sqlite3.connect(file)
            self.cur=self.con.cursor()
            self.initDatabase()
        else:
            self.con=sqlite3.connect(file)
            self.cur=self.con.cursor()
            if not self.check():
                raise("Database has wrong schema")
        self.dictstmt="INSERT INTO Diccionario (Espanol,Aleman) VALUES (?,?)"
        self.nounstmt="INSERT INTO Nombres (Nombre,Plural,Genero) VALUES(?,?,?)"
        self.verbstmt="INSERT INTO Verbos (Verbo,Regular,PS,SS,TS,PP,SP,TP) "\
            "VALUES(?,?,?,?,?,?,?,?)"  
        self.mode=Enum('Mode',["Nombre","Verbo","Resto"])

    # The first element of the tuples must be Espanol 
    # and the second one Aleman
    def writeNoun(self,nount:tuple[str])-> None:
        self.writeDict(nount[:1])
        self.cur.execute(self.nounstmt,nount[1:])

    def writeDict(self,dictt:tuple[str])->None:
        self.cur.execute(self.dictstmt,dictt)
    
    def writeVerb(self,verbt:tuple[str,int])->None:
        self.writeDict(verbt[:1])
        self.cur.execute(self.verbstmt,verbt[1:])

    def fromjson(self,jsonfile:str):

        df=pd.read_json(jsonfile)
        if "present" in df.columns:
            verbs=df[["Español","verb","present"]]
            for row in verbs.itertuples():
                self.cur.execute(self.dictstmt,row[1:3])
                if not row[3]:
                    inputtuple=(row[2],1,None,None,None,None,None,None)
                    self.cur.execute(self.verbstmt,inputtuple)
                else:
                    presentuple=tuple(row[3])
                    self.cur.execute(self.verbstmt,(row[2],0)+presentuple)
            self.con.commit()
        elif {"Plural","Género"}.issubset(df.columns):
            nouns=df[["Español","Deutsch","Plural","Género"]]
            for noun in nouns.itertuples():
                german=noun[2]
                if isinstance(noun[1],list):
                    for n in noun[1]:
                        self.cur.execute(self.dictstmt,(n,german))
                else:
                    self.cur.execute(self.dictstmt,noun[1:3])
                
                if noun[3]=="":
                    plural=None
                else:
                    plural=noun[3]
                if noun[4]=="":
                    genre=None
                else:
                    genre=noun[4]
                self.cur.execute(self.nounstmt,(german,plural,genre))
            
            self.con.commit()
        elif {"Español","Deutsch"}.issubset(df.columns):
            for row in df.itertuples():
                self.writeDict(row)
        else:
            raise RuntimeError("The json file does not have the correct "
                               "columns")



    # CSV file must have the column ordered this way:
    # spanish, german, (plural, genre)/(present)/(Nothing)
    # (noun/verb/rest)
    def fromcsv(self,csvfile:str):
        with open(csvfile) as f:
            lines=f.readlines()
            splited=lines[0].split(",")
            if len(splited)==4:
                for line in lines:
                    nlist=line.split(",")
                    ntuple=tuple(nlist)
                    self.writeNoun(ntuple)
            elif len(splited)==2:
                for line in lines:
                    rlist=line.split(",")
                    rtuple=tuple(rlist)
                    self.writeNoun(rtuple)
            elif len(splited)==8:
                for line in lines:
                    vlist=line.split(",")
                    vtuple=tuple(vlist)
                    self.writeVerb(vtuple)
            else:
                raise RuntimeError("The CSV does not contain the correct "
                                   "number of columns")                

# First database name, second file to read
def main(argv:list[str], arc:int):
    if arc!=3:
        raise RuntimeError("This script needs two arguments")
    
    try:
        database=argv[1]
        file=argv[2]
        w=writer(database)
        if file[-3:]=="csv":
            w.fromcsv(file)
        elif file[-4:]=="json":
            w.fromjson(file)
        else:
            raise RuntimeError("The format of the file is not correct")
    except sqlite3.Error as err:
        print(err)
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main(sys.argv,len(sys.argv))