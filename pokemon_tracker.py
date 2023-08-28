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

# Variable para controlar el combate actual
current_battle_url = None
combat_ended = True

while True:
    try:
        # Espera a que ocurra un cambio en el URL (inicio de una nueva batalla)
        wait = WebDriverWait(driver, 1000)  # Espera máximo 120 segundos
        new_battle_url = "https://play.pokemonshowdown.com/battle-gen9vgc2023regulationd"
        element_present = EC.url_contains(new_battle_url)
        wait.until(element_present)

        # Una vez que el URL ha cambiado, puedes continuar con la extracción de información
        current_url = driver.current_url
        if current_url != current_battle_url:
            current_battle_url = current_url
            combat_ended = False

        if not combat_ended:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            end_of_battle_text = "winning)"
            end_of_battle_text2 = "losing)"  # Mensaje que indica el final de la batalla
            if end_of_battle_text and end_of_battle_text2 in soup.get_text():
                combat_ended = True
                chat_history = soup.find('div', class_='inner message-log')

                # Agregar un encabezado que indique el inicio del combate
                with open('all_logs.txt', 'a', encoding='utf-8') as all_logs_file:
                    all_logs_file.write("\n--- Combate ---\n")

                    # Obtener y guardar cada línea del chat en el archivo de logs
                    chat_lines = chat_history.find_all('div', class_=True)
                    for line in chat_lines:
                        cleaned_line = line.get_text().strip()
                        all_logs_file.write(cleaned_line + '\n')

    except KeyboardInterrupt:
        # Si se presiona Ctrl+C, sale del bucle
        break

# Cierra el navegador al finalizar
driver.quit()
