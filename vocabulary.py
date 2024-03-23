import pandas as pd
from numpy.random import randint,rand

def runvocabulary(language:str)->None:
    path="dictionary_"+language+".csv"
    dictionary=pd.read_csv(path,sep=",")

    nw=int(input("¿Cuántas palabras vas a practicar?\t"))
    rownumber=randint(0,len(dictionary)+1,nw)
    rows=dictionary.iloc[rownumber]
    mode=int(input("¿De español a "+language+" (0), de "+language+" a español (1) o da igual (2)?\t"))

    corrects=0
    if mode==0:
        for index, row in rows.iterrows():
            if input(str(row["Español"])+"\n")==row[language]:
                print("¡Correcto!\n")
                corrects+=1
                dictionary.loc[index,"Box"]=dictionary.loc[index,"Box"]+1
            else:
                print("No es correcto, la palabra es",row[language],"\n")
    elif mode==1:
        for index, row in rows.iterrows():
            if input(str(row[language])+"\n")==row["Español"]:
                print("¡Correcto!\n")
                corrects+=1
                dictionary.loc[index,"Box"]=dictionary.loc[index,"Box"]+1
            else:
                print("No es correcto, la palabra es",row["Español"],"\n")
    else:
        for index, row in rows.iterrows():
            if rand()<0.5:
                if input(str(row[language])+"\n")==row["Español"]:
                    print("¡Correcto!\n")
                    corrects+=1
                    dictionary.loc[index,"Box"]=dictionary.loc[index,"Box"]+1
                else:
                    print("No es correcto, la palabra es",row["Español"],"\n")
            else:
                if input(str(row["Español"])+"\n")==row[language]:
                    print("¡Correcto!\n")
                    corrects+=1
                    dictionary.loc[index,"Box"]=dictionary.loc[index,"Box"]+1
                else:
                    print("No es correcto, la palabra es",row[language],"\n")

    print("Acertaste",corrects,"de",nw,"palabras\n\n")
    prop=float(corrects)/nw
    if prop<0.5:
        print("Necesitas estudiar más\n")
    elif prop==1:
        print("¡Perfecto! Has acertado todas!\n")
    else:
        print("¡Muy bien! Vas progresando correctamente\n")

    dictionary.to_csv(path,",",index=False)