import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

while True:
    # Paso 1: Cargar datos JSON
    with open('combates-datos.json') as json_file:
        data = json.load(json_file)

    # Paso 2: Crear DataFrame con pandas
    df = pd.DataFrame(data)
    df['indice'] = range(1, len(df) + 1)  # Agregar índices numéricos a las partidas

    # Menú de opciones
    print("Elija una opción:")
    print("1. Apariciones de Pokémon Rival en Derrotas")
    print("2. Combinaciones de Leads Rival en Derrotas")
    print("3. Porcentaje de Victorias y Derrotas")
    print("4. Evolución de mi Rating Anterior")
    print("5. Salir")

    opcion = input("Ingrese el número de la opción que desea visualizar: ")

    if opcion == '1':
        # Paso 3: Filtrar derrotas
        derrotas = df[df['resultado'] == 'Derrota']

        # Paso 4: Contar apariciones de Pokémon en el equipo rival en derrotas
        rival_pokemon_counts = {}
        for index, row in derrotas.iterrows():
            for pokemon in row['pokemons_oponente']:
                if pokemon in rival_pokemon_counts:
                    rival_pokemon_counts[pokemon] += 1
                else:
                    rival_pokemon_counts[pokemon] = 1

        # Paso 5: Ordenar los Pokémon por cantidad de apariciones en derrotas
        rival_pokemon_counts_sorted = dict(sorted(rival_pokemon_counts.items(), key=lambda item: item[1]))

        # Crear visualización de apariciones de Pokémon
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(rival_pokemon_counts_sorted.keys()), y=list(rival_pokemon_counts_sorted.values()))
        plt.title('Apariciones de Pokémon Rival en Derrotas')
        plt.xlabel('Pokémon Rival')
        plt.ylabel('Número de Apariciones')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()

    elif opcion == '2':
        # Paso 3: Filtrar derrotas
        derrotas = df[df['resultado'] == 'Derrota']

        # Paso 4: Contar combinaciones de leads del rival en derrotas
        rival_lead_combinations_count = Counter(map(tuple, derrotas['lead_oponente']))

        # Paso 5: Crear visualización de combinaciones de leads
        plt.figure(figsize=(10, 6))
        sns.barplot(x=[', '.join(comb) for comb in rival_lead_combinations_count.keys()],
                    y=list(rival_lead_combinations_count.values()))
        plt.title('Combinaciones de Leads Rival en Derrotas')
        plt.xlabel('Combinación de Leads Rival')
        plt.ylabel('Número de Apariciones')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()

    elif opcion == '3':
        # Paso 3: Filtrar victorias y derrotas
        victorias = df[df['resultado'] == 'Victoria']
        derrotas = df[df['resultado'] == 'Derrota']

        total_combates = len(df)
        total_victorias = len(victorias)
        total_derrotas = len(derrotas)

        # Crear gráfico circular de porcentajes
        plt.figure(figsize=(6, 6))
        porcentajes = [total_victorias, total_derrotas]
        etiquetas = [f'Victorias\n{total_victorias}', f'Derrotas\n{total_derrotas}']
        colores = ['green', 'red']

        plt.pie(porcentajes, labels=etiquetas, colors=colores, autopct='%1.1f%%', startangle=140)
        plt.title('Porcentaje de Victorias y Derrotas')
        plt.axis('equal')  # Hace que el gráfico sea circular

        plt.show()

    elif opcion == '4':
        
         # Paso 3: Filtrar combates en los que tienes información de rating_anterior_yo
        combates_con_rating = df[df['rating_anterior_yo'].notnull()]

        # Paso 4: Crear visualización de evolución de rating_anterior_yo
        plt.figure(figsize=(10, 6))
        plt.plot(combates_con_rating['indice'], combates_con_rating['rating_anterior_yo'], marker='o', linestyle='-')
        plt.title('Evolución de mi Rating Anterior')
        plt.xlabel('Índice del Combate')
        plt.ylabel('Rating Precedente Yo')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Agregar números encima de los puntos
        for x, y, numero in zip(combates_con_rating['indice'], combates_con_rating['rating_anterior_yo'], combates_con_rating['rating_anterior_yo']):
            plt.annotate(str(numero), xy=(x, y), xytext=(5, 5), textcoords='offset points')

        plt.show()
        
    elif opcion == '5':
        print("Saliendo del programa...")
        break

    else:
        print("Opción no válida. Por favor, elija una opción válida.")
