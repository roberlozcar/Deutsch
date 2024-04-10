from vocabulary import runvocabulary
from verbs import runverbs

database=input("Escribe el nombre de la base de datos con el diccionario y la gramatica "
               "(Recuerda que debes tener la base de datos en el formato correcto en la misma carpeta)\n")

while True:
    selectscript=input("¿Quieres practicar verbos (verbos), vocabulario (vocabulario) o nombres (nombres)?\n")
    if selectscript=="vocabulario":
        runvocabulary(database)
    elif selectscript=="verbos":
        runverbs(database)
    elif selectscript=="nombres":
        runverbs(database)
    else:
        print("Entrada incorrecta, solo se admite \"verbos\" o \"vocabulario\"\nInténtelo de nuevo\n")
