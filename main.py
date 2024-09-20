from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_wikipedia(query):
    browser = webdriver.Chrome()
    browser.get('https://ru.wikipedia.org/')

    search_box = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "searchInput"))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    return browser

def list_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for index, paragraph in enumerate(paragraphs):
        print(f"Параграф {index + 1}: {paragraph.text}")
        more = input("Хотите увидеть следующий параграф? (да/нет): ").strip().lower()
        if more != 'да':
            break


def list_linked_articles(browser):
    links = browser.find_elements(By.XPATH, "//div[@id='bodyContent']//a[@href]")
    for index, link in enumerate(links[:10]):
        print(f"{index + 1}: {link.text} ({link.get_attribute('href')})")
    return links


def main():
    query = input("Введите запрос для поиска на Википедии: ").strip()
    browser = search_wikipedia(query)

    while True:
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")
        choice = input("Введите номер действия: ").strip()

        if choice == '1':
            list_paragraphs(browser)
        elif choice == '2':
            links = list_linked_articles(browser)
            link_choice = int(input("Введите номер статьи для перехода: ").strip()) - 1
            if 0 <= link_choice < len(links):
                browser.get(links[link_choice].get_attribute('href'))
                print("\nВы перешли на новую статью.")
            else:
                print("Некорректный выбор.")
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор, попробуйте снова.")

    browser.quit()

if __name__ == "__main__":
    main()