from numpy.random import choice
from reader import reader

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
    

def runverbs(file:str)->float:
    r=reader(file)
    nw=int(input("¿Cuántos verbos vas a practicar?\t"))
    rownumbers=choice(range(1,r.getSize("Verbos")+1),nw)
    corrects=0
    pronouns=r.getPronouns()

    for number in rownumbers:
        verb=r.readVerb(number)
        fail=False

        print(verb[0])
        if verb[1]==1:
            for i,p in enumerate(pronouns):
                answer=input(p+" ")
                if answer==regularform(verb[0],i):
                    print("\tCorrecto")
                else:
                    print("\tIncorrecto")
                    fail=True
        else:
            for i,p in enumerate(pronouns):
                answer=input(p+" ")
                if answer==verb[2+i]:
                    print("\tCorrecto")
                else:
                    print("\tIncorrecto")
                    fail=True

        if fail:
            print("\nHas fallado en alguna forma verbal de",verb[0])
            print("La conjugación correcta es:")
            if verb[1]==0:
                for i,form in enumerate(verb[2:]):
                    print(pronouns[i],form)
            else:
                for i in range(6):
                    print(pronouns[i],regularform(verb[0],i))
        else:
            corrects+=1
            print("\nHas acertado todas las formas verbales de",verb[0],"\n")

    print("Acertaste",corrects,"de",nw,"palabras\n\n")
    return float(corrects)/nw