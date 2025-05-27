from bs4 import BeautifulSoup, Tag, ResultSet
import csv
from pathlib import Path
import requests
from requests import Response
from urllib.parse import urljoin


BASE_URL: str = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"

def main() -> None:
    animals_count: dict[str, int] = {}
    next_page: str | None = BASE_URL
    page_num: int = 1

    while next_page:
        print(f"Обработка страницы {page_num}...")
        response: Response = requests.get(next_page)
        response.raise_for_status()
        soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')

        animals_by_page: ResultSet[Tag] = soup.select("#mw-pages > div.mw-content-ltr > div > div > ul li")

        if not animals_by_page:
            print("Животных на странице не найдено, завершаем.")
            break

        first_animal_text: str = animals_by_page[0].get_text(strip=True)
        if not first_animal_text:
            print("Пустое название животного, завершаем.")
            break

        first_letter: str = first_animal_text[0].upper()

        if not ('А' <= first_letter <= 'Я'):
            print(f"Имя животного на иностранном языке: {first_letter}. Завершаем сбор данных.")
            break

        print(f"Обрабатываем букву: {first_letter}")
       
        for animal in animals_by_page:
            text: str = animal.get_text(strip=True)
            if text:
                letter: str = text[0].upper()
                if 'А' <= letter <= 'Я':
                    animals_count[letter] = animals_count.get(letter, 0) + 1

        page_num += 1

        next_link: Tag | None = soup.find('a', string='Следующая страница')
        if next_link:
            next_page = urljoin(BASE_URL, next_link['href'])
            print("Переходим к следующей странице...\n")
        else:
            print("Следующая страница не найдена, завершаем парсинг.")
            next_page = None

    current_dir: Path = Path(__file__).parent
    print("Записываем результаты в beasts.csv...")
    
    with open(str(current_dir / "beasts.csv"), "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for letter in sorted(animals_count.keys()):
            writer.writerow([letter, animals_count[letter]])
        
    print("Готово, результаты записаны в beasts.csv")


if __name__ == "__main__":
    main()


#Реализовал сначала на Selenium,т.к. мне это ближе). Но это избыточно, долго работает, и вам пришлось бы устанавливать хром с соответствующей версией хромдрайвера

# import csv
# from pathlib import Path
# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# BASE_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"

# current_dir = Path(__file__).parent

# def main():
#     options = Options()
#     options.add_argument("--headless")
#     chromedriver_path = current_dir / "chromedriver"
#     service = Service(str(chromedriver_path))
#     driver = webdriver.Chrome(service=service)
#     wait = WebDriverWait(driver, 10)

#     animals_count: dict = {}

#     try:
#         driver.get(BASE_URL)

#         while True:
#             animals_by_page = wait.until(EC.presence_of_all_elements_located(
#                 (By.CSS_SELECTOR, "#mw-pages > div.mw-content-ltr > div > div > ul li")
#             ))

#             for animal in animals_by_page:
#                 text = animal.text
#                 if not text:
#                     continue
#                 first_letter = text[0].upper()
#                 if not ('А' <= first_letter <= 'Я'):
#                     break
                    
#                 animals_count[first_letter] = animals_count.get(first_letter, 0) + 1
                
#             try:
#                 next_link = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='mw-pages']//a[text()='Следующая страница']")))
            
#                 next_link[0].click()
#                 wait.until(EC.staleness_of(animals_by_page[0]))
#             except:
#                 break
        
#         with open("beasts.csv", "w", encoding="utf-8", newline="") as f:
#             writer = csv.writer(f)
#             for letter in sorted(animals_count.keys()):
#                 writer.writerow([letter, animals_count[letter]])

#         print("Готово, результаты записаны в beasts.csv")
#         print(animals_count)

#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     main()
