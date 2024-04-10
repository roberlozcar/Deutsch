from reader import reader
from numpy.random import choice

def runNouns(file:str)->float:
    r=reader(file)
    nw=int(input("¿Cuántos nombres vas a practicar?\t"))
    rownumbers=choice(range(1,r.getSize("Nombres")+1),nw)
    corrects=0

    for number in rownumbers:
        noun=r.readNoun(number)
        fail=False
        print(noun[0])

        if input("Plural:\t")==noun[1]:
            print("\tCorrecto")
        else:
            print("\tIncorrecto, el plural es ",noun[1])
            fail=True
        
        if input("Género:\t")==noun[2]:
            print("\tCorrecto")
        else:
            print("\tIncorrecto, el género es ",noun[2])
            fail=True

        if not fail:
            corrects+=1

    print("Acertaste",corrects,"de",nw,"palabras\n\n")
    return float(corrects)/nw