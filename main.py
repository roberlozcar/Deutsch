from vocabulary import runvocabulary
import verbs

language=input("¿Qué idioma quieres practicar? (Recuerda que debes tener el diccionario en el formato correcto en la misma carpeta con el nombre dictionary_Idioma.csv)\n")

understood=False
while not understood:
    selectscript=input("¿Quieres practicar verbos (verbos) o vocabulario (vocabulario)?\n")
    if selectscript=="vocabulario":
        runvocabulary(language)
    elif selectscript=="verbos":
        verbs
    else:
        print("Entrada incorrecta, solo se admite \"verbos\" o \"vocabulario\"\nInténtelo de nuevo\n")
