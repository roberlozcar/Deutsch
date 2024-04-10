from vocabulary import runvocabulary
from verbs import runverbs
from nouns import runNouns

database=input("Escribe el nombre de la base de datos con el diccionario y la gramatica "
               "(Recuerda que debes tener la base de datos en el formato correcto en la misma carpeta)\n")

while True:
    selectscript=input("¿Quieres practicar verbos (verbos), vocabulario (vocabulario) o nombres (nombres)?\n")
    if selectscript=="vocabulario":
        prop=runvocabulary(database)
    elif selectscript=="verbos":
        prop=runverbs(database)
    elif selectscript=="nombres":
        prop=runNouns(database)
    else:
        print("Entrada incorrecta, solo se admite \"verbos\" o \"vocabulario\"\nInténtelo de nuevo\n")

    if prop<0.5:
        print("Necesitas estudiar más\n")
    elif prop==1:
        print("¡Perfecto! Has acertado todas!\n")
    else:
        print("¡Muy bien! Vas progresando correctamente\n")
