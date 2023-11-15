#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Jul 5 14:28:22 2023
@author: rod
"""

# Importando la biblioteca spaCy
import spacy

# Leyendo el contenido del archivo 'cuento.txt' en una cadena de texto
cuento = open('cuento.txt', 'r').read()

# Función para encontrar el verbo más cercano a entidades específicas
def closest_verb(entities, tokens):
    for entity in entities:
        # Verifica si la entidad es de tipo 'PER' (persona) o 'MISC' (miscelánea)
        if entity[1] in ['PER', 'MISC']:
            start, end = entity[2], entity[3]
            # Verifica si no hay un sujeto nominal entre la entidad
            if not 'nsubj' in [token[2] for token in tokens[start:end]]:
                no_actions.append([tokens[start:end], entity])
                continue
            # Itera sobre los tokens después de la entidad para encontrar el verbo más cercano
            for i in range(end, len(tokens)):
                if tokens[i][1] == 'VERB':
                    range_to_check = tokens[end:i]  # Rango para verificar la ausencia de sujeto nominal
                    # Verifica si no hay un sujeto nominal antes del verbo
                    if 'nsubj' not in [token[2] for token in range_to_check]:
                        print(f'La entidad "{entity[0]}" comienza en la posición "{start}", '
                              f'termina en la posición "{end-1}" y tiene el verbo más cercano "{tokens[i][0]}" '
                              f'en la posición "{i}".\n')
                        
                        # Imprime la frase que contiene la entidad y el verbo
                        print(" ".join([token[0] for token in tokens[start:i+1]]), end=" ")
                        j = i+1
                        # Continúa imprimiendo la oración hasta encontrar un signo de puntuación
                        while True:
                            if tokens[j][1] == "PUNCT":
                                print("\n")
                                break
                            print(tokens[j][0], end=" ")
                            j+=1
                        print("-"*30)
                    else:
                        errors.append([entity[0], start, tokens[i][0], i])    
                    break # Termina la iteración después de encontrar un verbo

# Carga el modelo de spaCy en español para reconocimiento de entidades nombradas
nlp = spacy.load("es_core_news_lg")

# Procesamiento del texto con spaCy para reconocimiento de entidades
doc = nlp(cuento)

# Almacenando entidades nombradas y su tipo en una lista
entities = [(ent.text, ent.label_, ent.start, ent.end) for ent in doc.ents]

# Carga el modelo de spaCy en español para análisis gramatical
nlp = spacy.load('es_dep_news_trf')

# Procesamiento del texto con spaCy para análisis gramatical
doc = nlp(cuento)

# Almacenando tokens, su categoría gramatical y etiqueta de dependencia en una lista
tokens = [(token.text, token.pos_, token.dep_) for token in doc]

# Inicializando listas para errores y entidades sin acciones
errors = []
no_actions = []

# Llamada a la función para encontrar el verbo más cercano
closest_verb(entities, tokens)
