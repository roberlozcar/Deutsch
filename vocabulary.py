from reader import reader
from numpy.random import rand,choice

def checkPolisemic(answer:str,polisemics:list[tuple[str]])->bool:
    for p in polisemics:
        if answer==p[0]:
            return True
    return False

def runvocabulary(file:str)->None:
    r=reader(file)
    nw=int(input("¿Cuántas palabras vas a practicar?\t"))
    rownumbers=choice(r.getSize("Diccionario")+1,nw)
    corrects=0
    languages=r.getLanguages()
    mode=int(input("¿De "+languages[0]+" a "+languages[1]+" (0), de "+languages[1]+" a "+languages[0]+
                   " (1) o da igual (2)?\t"))

    corrects=0
    # Idioma2 (Español) a Idioma1 (Alemán)
    if mode==1:
        for n in rownumbers:
            words=r.readRowid(n)
            polisemic=r.getPolisemicWords(languages[0],languages[1],words[0])
            answer=input(words[0]+"\n")
            if checkPolisemic(answer,polisemic):
                print("¡Correcto!\n")
                corrects+=1
            else:
                print("No es correcto, la palabra es",words[1],"\n")
    # Idioma1 (Alemán) a Idioma2 (Español)
    elif mode==0:
        for n in rownumbers:
            words=r.readRowid(n)
            polisemic=r.getPolisemicWords(languages[1],languages[0],words[1])
            answer=input(words[1]+"\n")
            if checkPolisemic(answer,polisemic):
                print("¡Correcto!\n")
                corrects+=1
            else:
                print("No es correcto, la palabra es",words[0],"\n")
    # Da igual (random)
    else:
        for n in rownumbers:
            words=r.readRowid(n)
            if rand()<0.5:
                polisemic=r.getPolisemicWords(languages[1],languages[0],words[1])
                answer=input(words[1]+"\n")
                if checkPolisemic(answer,polisemic):
                    print("¡Correcto!\n")
                    corrects+=1
                else:
                    print("No es correcto, la palabra es",words[0],"\n")
            else:
                polisemic=r.getPolisemicWords(languages[0],languages[1],words[0])
                answer=input(words[0]+"\n")
                if checkPolisemic(answer,polisemic):
                    print("¡Correcto!\n")
                    corrects+=1
                else:
                    print("No es correcto, la palabra es",words[1],"\n")

    print("Acertaste",corrects,"de",nw,"palabras\n\n")
    prop=float(corrects)/nw
    if prop<0.5:
        print("Necesitas estudiar más\n")
    elif prop==1:
        print("¡Perfecto! Has acertado todas!\n")
    else:
        print("¡Muy bien! Vas progresando correctamente\n")