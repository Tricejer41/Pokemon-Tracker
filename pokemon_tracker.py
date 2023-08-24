import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup

# Configura el navegador (por ejemplo, Chrome)
driver = webdriver.Chrome()

# Navega a la página de Pokemon Showdown
battle_url = "https://play.pokemonshowdown.com/"
driver.get(battle_url)

# Definir función de espera personalizada
def url_changed(driver, old_url):
    return driver.current_url != old_url

# Variables para controlar si la información ya se ha guardado
previous_chat = ""
info_guardada = False

# ...
while True:
    try:
        old_url = driver.current_url
        # Espera a que ocurra un cambio en el URL (inicio de una nueva batalla)
        wait = WebDriverWait(driver, 120)  # Espera máximo 120 segundos
        new_battle_url = "https://play.pokemonshowdown.com/battle-gen9vgc2023regulationd"
        element_present = EC.url_contains(new_battle_url)
        wait.until(element_present)

        # Una vez que el URL ha cambiado, puedes continuar con la extracción de información
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Busca el bloque que contiene los nombres de los Pokémon del rival
        opponent_team_block = soup.find('div', {'aria-label': "Opponent's Team"})
        
        # Busca el bloque que contiene los nombres de tus Pokémon
        your_team_block = soup.find('div', {'aria-label': "Your Team"})
        
        # Busca el resultado de la batalla (ganaste o perdiste)
        battle_result_element = soup.find('div', class_='result')

        # Después de la extracción de los bloques opponent_team_block y your_team_block...
        chat_history = soup.find('div', class_='inner message-log')  # Cambio en la clase para seleccionar el chat completo

        if opponent_team_block and your_team_block and battle_result_element and chat_history and not info_guardada:
            # Encuentra todos los elementos con la clase picon dentro del bloque del rival
            opponent_pokemon_icons = opponent_team_block.find_all('span', class_='picon')

            # Encuentra todos los elementos con la clase picon dentro de tu bloque
            your_pokemon_icons = your_team_block.find_all('span', class_='picon')

            # Extrae los nombres de los Pokémon del rival del atributo aria-label
            opponent_pokemon_names = []
            for icon in opponent_pokemon_icons:
                name_parts = icon['aria-label'].split(" (")
                if len(name_parts) > 1:
                    name = name_parts[1][:-1]
                    if name != "active":
                        opponent_pokemon_names.append(name)
                else:
                    name = name_parts[0]
                    if name != "active":
                        opponent_pokemon_names.append(name)

            # Extrae los nombres de tus Pokémon del atributo aria-label
            your_pokemon_names = []
            for icon in your_pokemon_icons:
                name_parts = icon['aria-label'].split(" (")
                if len(name_parts) > 1:
                    name = name_parts[1][:-1]
                    if name != "active":
                        your_pokemon_names.append(name)
                else:
                    name = name_parts[0]
                    if name != "active":
                        your_pokemon_names.append(name)

            # Extrae el rating del rival
            opponent_rating = opponent_team_block.find('div', class_='trainersprite')['title'].replace('Rating: ', '')

            # Extrae tu nickname
            opponent_nickname = opponent_team_block.find('strong').get_text(strip=True)

            # Extrae el resultado de la batalla (ganaste o perdiste)
            battle_result = battle_result_element.get_text(strip=True)

            # Encuentra las líneas relevantes en el chat que indican los Pokémon enviados al combate
            chat_lines = chat_history.find_all('div', class_='battle-history')

            opponent_battle_pokemon_names = []
            your_battle_pokemon_names = []

            for line in chat_lines:
                line_text = line.get_text(strip=True)
                
                if "sent out" in line_text:
                    if "(" in line_text:
                        pokemon_name = line_text.split("(")[1].split(")")[0].strip()
                        opponent_battle_pokemon_names.append(pokemon_name)
                    else:
                        pokemon_name = line_text.split("sent out")[1].strip()
                        opponent_battle_pokemon_names.append(pokemon_name)
                elif "Go!" in line_text:
                    if "(" in line_text:
                        pokemon_name = line_text.split("(")[1].split(")")[0].strip()
                        your_battle_pokemon_names.append(pokemon_name)
                    else:
                        pokemon_name = line_text.split("sent out")[1].strip()
                        your_battle_pokemon_names.append(pokemon_name)

                if len(opponent_battle_pokemon_names) >= 2 and len(your_battle_pokemon_names) >= 2:
                    break

            # Guarda la información en un archivo de texto
            with open('battle_info.txt', 'a', encoding='utf-8') as file:
                file.write("Battle Result: {}\n".format(battle_result))
                file.write("\nRival's Pokemon:\n")
                for name in opponent_pokemon_names:
                    name_without_active = name.replace(" (active)", "")
                    file.write(name_without_active + '\n')

                file.write("\nYour Pokemon:\n")
                for name in your_pokemon_names:
                    name_without_active = name.replace(" (active)", "")
                    file.write(name_without_active + '\n')

                file.write("\nOpponent Rating: {}\n".format(opponent_rating))
                file.write("Opponent Nickname: {}\n".format(opponent_nickname))

                file.write("\nFirst Two Opponent Battle Pokemon:\n")
                for name in opponent_battle_pokemon_names:
                    file.write(name.rstrip('!') + '\n')  # Remove the trailing "!" character
        
                file.write("\nFirst Two Your Battle Pokemon:\n")
                for name in your_battle_pokemon_names:
                    file.write(name.rstrip('!') + '\n')  # Remove the trailing "!" character

                file.write("\n__________________________________________\n")

            # Marca la información como guardada
            info_guardada = True
        
        # Espera un tiempo antes de verificar de nuevo
        driver.implicitly_wait(5)
    
    except KeyboardInterrupt:
        # Si se presiona Ctrl+C, sale del bucle
        break

# Cierra el navegador al finalizar
driver.quit()