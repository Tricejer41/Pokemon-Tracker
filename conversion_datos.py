import re
import json

MI_NOMBRE_DE_USUARIO = "Sdetic"

def procesar_linea(linea, datos_participantes):
    if "Battle started between" in linea:
        m = re.search(r'Battle started between (\w+) and (\w+)!', linea)
        if m:
            yo = m.group(1)
            oponente = m.group(2)
            if yo == MI_NOMBRE_DE_USUARIO:
                datos_participantes['yo'] = yo
                datos_participantes['oponente'] = oponente
            else:
                datos_participantes['yo'] = oponente
                datos_participantes['oponente'] = yo
    
    if "won the battle!" in linea:
        if MI_NOMBRE_DE_USUARIO in linea:
            datos_participantes['resultado'] = 'Victoria'
        else:
            datos_participantes['resultado'] = 'Derrota'
    
    if "'s team: " in linea:
        jugador_nombre = re.search(r"(\w+)'s team:", linea).group(1)
        nombres_pokemon = re.findall(r'\w+(?:-\w+)?(?: \w+(?:-\w+)?)*', linea[linea.index(":") + 2:])
        nombres_pokemon_ordenados = sorted(nombres_pokemon)  # Ordenar alfabéticamente
        if jugador_nombre == MI_NOMBRE_DE_USUARIO:
            datos_participantes['pokemons_yo'] = nombres_pokemon_ordenados
        else:
            datos_participantes['pokemons_oponente'] = nombres_pokemon_ordenados


    
    if "sent out" in linea:
        if "(" in linea:
            pokemon_name = linea.split("(")[1].split(")")[0].strip()
            pokemon_name = pokemon_name.rstrip("!")
            if len(datos_participantes['lead_oponente']) < 2:
                datos_participantes['lead_oponente'].append(pokemon_name)
        else:
            pokemon_name = linea.split("sent out")[1].strip()
            pokemon_name = pokemon_name.rstrip("!")
            if len(datos_participantes['lead_oponente']) < 2:
                datos_participantes['lead_oponente'].append(pokemon_name)
        
    if "Go!" in linea:
        if "(" in linea:
            pokemon_name = linea.split("(")[1].split(")")[0].strip()
            pokemon_name = pokemon_name.rstrip("!")
            if len(datos_participantes['lead_yo']) < 2:
                datos_participantes['lead_yo'].append(pokemon_name)
        else:
            pokemon_name = linea.split("Go!")[1].strip()
            pokemon_name = pokemon_name.rstrip("!")
            if len(datos_participantes['lead_yo']) < 2:
                datos_participantes['lead_yo'].append(pokemon_name)

    return datos_participantes

def procesar_archivo(archivo_entrada):
    combates = []  # Lista para almacenar los datos de cada combate

    with open(archivo_entrada, 'r') as f:
        datos_partida = None
        for linea in f:
            if "--- Combate ---" in linea:
                if datos_partida is not None:
                    combates.append(datos_partida)
                datos_partida = {
                    'yo': '',
                    'oponente': '',
                    'pokemons_yo': [],
                    'pokemons_oponente': [],
                    'lead_yo': [],
                    'lead_oponente': [],
                    'resultado': ''
                }
            else:
                datos_partida = procesar_linea(linea, datos_partida)
    
    return combates

if __name__ == "__main__":
    archivo_entrada = "all_logs.txt"  # Reemplaza con el nombre de tu archivo de entrada
    combates = procesar_archivo(archivo_entrada)
    
    with open("combates-datos.json", 'w') as f:
        json.dump(combates, f, indent=4)
    
    print("Proceso completado.")
