import pandas as pd
from numpy.random import randint
import json

pronouns=["ich ","du ","er/sie/es ","wir ","ihr ","sie "]

def regularform(verb:str,person:int)->str:

    if person==3 or person==5:
        return verb

    lexem=verb.rstrip("en")
    if person==0:
        return lexem+"e"
    if person==1:
        return lexem+"st"
    if person==2 or person==4:
        return lexem+"t"
    


def runverbs(language:str)->None:
    path="verbs_"+language+".json"
    verbs=pd.read_json(path,)
    nw=int(input("¿Cuántos verbos vas a practicar?\t"))
    rownumber=randint(0,len(verbs)+1,nw)
    rows=verbs.iloc[rownumber]
    corrects=0

    for index,row in rows.iterrows():
        fail=False
        print("Verb:",row["verb"])
        for i,p in enumerate(pronouns):
            answer=input(p)
            if row["present"]:
                if row["present"][i]==answer:
                    print("\tCorrecto")
                else:
                    print("\tIncorrecto")
                    fail=True
            else:
                if answer==regularform(row["verb"],i):
                    print("\tCorrecto")
                else:
                    print("\tIncorrecto")
                    fail=True
        if fail:
            print("\nHas fallado en alguna forma verbal de",row["verb"])
            print("La conjugación correcta es:")
            if row["present"]:
                for i,form in enumerate(row["present"]):
                    print(pronouns[i],form)
            else:
                for i in range(6):
                    print(pronouns[i],regularform(row["verb"],i))
            print()
        else:
            corrects+=1
            verbs.loc[index,"Box"]=verbs.loc[index,"Box"]+1
            print("\nHas acertado todas las formas verbales de",row["verb"],"\n")

    print("Acertaste",corrects,"de",nw,"palabras\n\n")
    prop=float(corrects)/nw
    if prop<0.5:
        print("Necesitas estudiar más\n")
    elif prop==1:
        print("¡Perfecto! Has acertado todas!\n")
    else:
        print("¡Muy bien! Vas progresando correctamente\n")

    verbs.to_json(path,orient="records")

runverbs("Deutsch")