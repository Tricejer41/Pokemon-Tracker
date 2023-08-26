import re
import json

MI_NOMBRE_DE_USUARIO = "fqfqwgewgr"

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
            datos_participantes['resultado'] = 'victoria'
        else:
            datos_participantes['resultado'] = 'derrota'
    
    if "'s team: " in linea:
        jugador_nombre = re.search(r"(\w+)'s team:", linea).group(1)
        nombres_pokemon = re.findall(r'\w+(?:-\w+)?', linea[linea.index(":") + 2:])
        if jugador_nombre == MI_NOMBRE_DE_USUARIO:
            datos_participantes['pokemons_yo'] = nombres_pokemon
        else:
            datos_participantes['pokemons_oponente'] = nombres_pokemon
    
    return datos_participantes

def procesar_archivo(archivo_entrada):
    datos_partida = {
        'yo': '',
        'oponente': '',
        'pokemons_yo': [],
        'pokemons_oponente': [],
        'resultado': ''
    }

    with open(archivo_entrada, 'r') as f:
        for linea in f:
            datos_partida = procesar_linea(linea, datos_partida)
    
    return datos_partida

if __name__ == "__main__":
    archivo_entrada = "chat_history.txt"  # Reemplaza con el nombre de tu archivo de entrada
    datos_partida = procesar_archivo(archivo_entrada)
    
    with open("team-datos.json", 'w') as f:
        json.dump(datos_partida, f, indent=4)
    
    print("Proceso completado.")
