#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 14:28:22 2023

@author: rod
"""

# Importa las librerias necesarias

import spacy

# Tu cuento en una cadena de texto
cuento = open('cuento.txt', 'r').read()

def closest_verb(entities, tokens):
    for entity in entities:
        if entity[1] in ['PER', 'MISC']:
            start, end = entity[2], entity[3]
            if not 'nsubj' in [token[2] for token in tokens[start:end]]:
                no_actions.append([tokens[start:end], entity])
                
                continue
            for i in range(end, len(tokens)): # Buscar hacia adelante desde la entidad
                if tokens[i][1] == 'VERB':
                    
                    range_to_check = tokens[end:i]  # +1 para incluir el token actual,
                    
                    if 'PROPN' not in [token[1] for token in range_to_check]:
                        print(f'La entidad "{entity[0]}" comienza en la la posición "{start}", termina en la posición "{end-1}" y tiene el verbo más cercano "{tokens[i][0]}" en la posición "{i}".\n')
                        
                        
                        print(" ".join([token[0] for token in tokens[start:i+1]]), end= " ")
                        j = i+1
                        while True:
                            print(tokens[j][0], end=" ")
                            j+=1
                            if tokens[j][1] == "PUNCT":
                                print("\n")
                                break
                        print("-"*30)
                    else:
                      errors.append([entity[0], start, tokens[i][0], i])    
                    break # Salir del bucle una vez que hemos encontrado un verbo
                    
                        
# Carga el modelo de Spacy para español
nlp = spacy.load("es_core_news_lg")

# Procesa el texto con Spacy
doc = nlp(cuento)

# Guarda en una lista las entidades nombradas y su tipo como tupla
entities = [(ent.text, ent.label_, ent.start, ent.end) for ent in doc.ents]

nlp = spacy.load('es_dep_news_trf')

doc = nlp(cuento)

# Guarda en una lista los tokens, su categoría gramatical y su etiqueta de POS como tupla
tokens = [(token.text, token.pos_, token.dep_) for token in doc]

errors = []

no_actions = []

closest_verb(entities, tokens)

