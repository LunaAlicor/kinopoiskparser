import pprint
import time
import re
from .models import Movie
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def index(request):
    return render(request, 'kinobd/startbutton.html')


def parse(request):
    """
        Функция parse(request)
        Описание:
        Эта функция выполняет парсинг данных о фильмах с веб-страниц kinopoisk.ru и сохраняет полученные данные в базе данных Django.

        Параметры:
        request: Объект запроса Django.
        Возвращаемое значение:
        Объект ответа Django, возвращающий сообщение об успешном выполнении парсинга.
        Внешние зависимости:
        pprint: Используется для красивого вывода отладочной информации.
        time: Используется для добавления временной задержки при загрузке страницы.
        re: Используется для работы с регулярными выражениями.
        BeautifulSoup (из bs4): Используется для парсинга HTML-кода страниц.
        selenium: Используется для автоматизации действий веб-браузера.
        django.http.HttpResponse: Используется для возвращения ответа HTTP.
        django.shortcuts.render: Используется для отображения HTML-шаблонов.
        webdriver.Chrome: Используется для управления браузером Chrome.
        By, WebDriverWait, EC (из selenium.webdriver.common.by, selenium.webdriver.support.ui, selenium.webdriver.support.expected_conditions): Используются для настройки ожиданий при загрузке элементов страницы.
        Внутренние функции и методы:
        index(request): Функция отображения стартовой страницы.
        parse(request): Функция для выполнения парсинга данных о фильмах.
        Локальные переменные:
        chrome_options: Опции для настройки веб-драйвера Chrome.
        base_urs: Базовый URL для парсинга данных о фильмах.
        num_pages: Количество страниц для парсинга.
        urls: Список URL-адресов страниц с фильмами.
        driver: Экземпляр веб-драйвера Chrome.
        all_movie_links: Список ссылок на все найденные фильмы.
        Возвращаемые значения:
        HttpResponse: Объект ответа Django с сообщением об успешном выполнении парсинга.
    """

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # отключено для открытия браузера на компьютере

    base_urs = "https://www.kinopoisk.ru/"
    num_pages = 17  # кол-во страниц с фильмами
    other_film_pages = ["country--2"]
    urls = [f"{base_urs}lists/movies/{j}/?page={i}" for i in range(1, num_pages + 1) for j in other_film_pages]
    # генерация списка ссылок

    driver = webdriver.Chrome(options=chrome_options)
    # pprint.pprint(urls)  # Вывод ссылок с фильмами
    all_movie_links = []  # список где будут храниться ссылки на все фильмы
    all_movie_title = set()
    for url in urls:
        driver.get(url)  # открытие странички
        time.sleep(20)  # ожидание чтобы не прилетела капча и прогрузилась страничка
        html = driver.page_source  # html код странички
        soup = BeautifulSoup(html, 'html.parser')  # инициализация BS
        links = soup.find_all("a")  # поиск всех ссылок в html
        # pprint.pprint(links)  # вывод всех ссылок
        for link in links:  # сортируем ссылки оставляя только те которые содержат ссылку на страницу фильма
            # print("Тут должна была быть ссылка!")
            href = link.get("href")
            if "film" in str(link):
                if href and re.search(r'\/film\/\d+\/', href):  # регулярное выражения для поиска ссылок на фильм
                    all_movie_links.append(base_urs + href)  # добавляем ссылку на фильм в список ссылок
        # break   # Чтобы не 500 фильмов тестить а только 50

    all_movie_links = list(set(all_movie_links))  # удаляем дубликаты
    pprint.pprint(all_movie_links)  # вывод ссылок на фильмы
    for i_film in all_movie_links:  # начинаем иттерацию по фильмам
        driver.get(i_film)  # получаем страничку фильма
        time.sleep(3)  # ждем чтобы не прилетела капча
        html = driver.page_source  # получаем html код страницы фильма
        soup = BeautifulSoup(html, 'html.parser')
        print("#" * 100)  # для разделения вывода фильмов в консоле при желании можно удалить

        title_span = soup.find("span",
                               {"data-tid": "75209b22"})  # получаем основное название которое указано в кинопоиске
        if title_span:
            title = title_span.text
            if title in all_movie_title:
                break
            else:
                all_movie_title.add(title)
            print("Название - ", title)
        mpaa_span = soup.find("span", {"data-tid": "5c1ffa33"})  # получаем mpa рейтинг

        original_title_span = soup.find('span',
                                        class_='styles_originalTitle__JaNKM')  # получаем оригинальное название если таковое имеется
        if original_title_span:
            original_title = original_title_span.text
            print("Оригинальное название:", original_title)
        else:
            print("Оригинальное название не найдено.")
            original_title = "-"

        if mpaa_span:
            mpaa = mpaa_span.text
            print("MPA - ", mpaa)

        rating = soup.find("span", {"data-tid": "7f8f8841"})  # получаем рейтинг кинопоиска
        if rating:
            rating_count = rating.text
            # TODO При желании можешь перевести тут во float и запустить парсер по новой или обрабатывать уже после извлечения
            # rating_count = float(rating_count)
            print("Рейтинг Кинопоиска- ", rating_count)

        try:
            rating_span = soup.find('div', class_='styles_countBlock__jxRDI').find('span',
                                                                                   class_='styles_count__iOIwD')  # получаем кол-во оценок на кинопоиске
            if rating_span:
                rating = rating_span.text
                # rating = int(rating)
                print("Кол-во оценок кинопоиск:", rating)
            else:
                print("Оценки не найдены.")
                # rating = 0
                rating = "-"
        except AttributeError:
            rating = "-"
            print("Информация о рейтинге не обнаружена")


        try:
            imdb_rating_div = soup.find('div', class_='film-sub-rating')  # получаем кол-во оценок imbd
            if imdb_rating_div:
                imdb_ratings_count = imdb_rating_div.find('span', class_='styles_count__89cAz').text
                # imdb_ratings_count = int(imdb_ratings_count)
                print("Количество оценок IMDb:", imdb_ratings_count)
            else:
                print("Информация о количестве оценок IMDb не найдена.")
                imdb_ratings_count = "-"
        except AttributeError:
            imdb_ratings_count = "-"


        try:
            imdb_rating_div = soup.find('div', class_='film-sub-rating')  # получаем оценки imbd
            if imdb_rating_div:
                imdb_rating = imdb_rating_div.find('span', class_='styles_valueSection__0Tcsy').text.split(':')[-1].strip()
                print("Рейтинг IMDb:", imdb_rating)
            else:
                print("Рейтинг IMDb не найден.")
                imdb_rating = "-"
        except AttributeError:
            imdb_rating = "-"

        try:
            rating_div = soup.find('div',
                                   class_='styles_filmRatingBar__Mks7X')  # получаем положительные и отрицательные оценки критиков если таковые имеются
            if rating_div:
                positive_ratings = rating_div.find('div', class_='styles_greenBar__NAQmT').text
                negative_ratings = rating_div.find('div', class_='styles_redBar__b_rlR').text
                print("Количество положительных оценок критиков:", positive_ratings)
                print("Количество отрицательных оценок критиков:", negative_ratings)
            else:
                print("Информация о количестве оценок не найдена.")
                positive_ratings = "-"
                negative_ratings = "-"
        except AttributeError:
            positive_ratings = "-"
            negative_ratings = "-"

        try:
            country_film = soup.find('div', text='Страна').find_next_sibling('div').text.strip()  # получаем страну съемки
            if country_film:
                print("Страна съемки - ", country_film)
        except AttributeError:
            print("Страна не найдена")
            country_film = "-"

        try:
            film_genre = soup.find('div', text='Жанр').find_next_sibling('div').text.strip().replace("слова",                                                                                     "")  # получаем жанры фильма
            if film_genre:
                print("Жанры фильма - ", film_genre)
        except AttributeError:
            film_genre = '-'


        try:
            director = soup.find('div', text='Режиссер').find_next_sibling('div').text.strip()  # получаем режиссера фильма
            if director:
                print("Режиссер - ", director)
        except AttributeError:
            director = "-"

        try:
            budget = soup.find('div', text='Бюджет').find_next_sibling(
                'div').text.strip()  # получаем бюджет если таковой имеется
            if budget:
                print("Бюджет - ", budget)
        except AttributeError:
            print("Информация о бюджете не найдена")
            budget = "-"

        try:
            worldwide_gross = soup.find("div", text="Сборы в мире")
            if worldwide_gross:
                worldwide_gross = worldwide_gross.find_next_sibling("div", class_="styles_valueDark__BCk93").text.replace("сборы", "")
                # if "=" in worldwide_gross:
                #     worldwide_gross = worldwide_gross.split("=")
                #     worldwide_gross = worldwide_gross[1]
                print("Сборы в мире:", worldwide_gross)
            else:
                print("Информация о сборах в мире не найдена")
                worldwide_gross = "-"

        except AttributeError:
            print("Информация о мировой кассе не найдена")
            worldwide_gross = "-"

        if worldwide_gross == "-":
            try:
                worldwide_gross_container = soup.find("div", class_="styles_rowLight__P8Y_1")
                if worldwide_gross_container:
                    worldwide_gross = worldwide_gross_container.find("a", class_="styles_linkLight__cha3C").text
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Сборы в мире:", worldwide_gross)
                else:
                    print("Информация о сборах в мире не найдена")
                    worldwide_gross = "-"
            except AttributeError:
                print("Информация о мировой кассе не найдена")
                worldwide_gross = "-"

        # except IndexError:
        #     world_gross_div = soup.find('div', text='Сборы в мире').find_next_sibling('div').text.strip().replace(
        #         "сборы", "")
        #     if world_gross_div:
        #         print("Сборы в мире:", world_gross_div)
        #     else:
        #         print("Информация о сборах в мире не найдена.")

        try:
            russian_gross_block = soup.find('div', text='Сборы в России').find_next_sibling('div').text.strip().replace(
                "сборы", "")  # сборы в России
            if russian_gross_block:
                print("Сборы в России -", russian_gross_block)
        except AttributeError:
            print("Информация о сборах в России не найдена")
            russian_gross_block = "-"

        try:
            premiere_date_str = soup.find('div', text='Премьера в мире').find_next_sibling('div').find(
                'a').text.strip()  # примьера если таковая имеется
            # premiere = datetime.strptime(premiere_date_str, "%d %B %Y")  можно перевести datetime при желании
            if premiere_date_str:
                print("Примьера - ", premiere_date_str)
        except AttributeError:
            print("Примьера не обнаружена")
            premiere_date_str = "-"


        try:
            duration = soup.find('div', text='Время').find_next_sibling('div').text.strip()  # длительность фильма
            if duration:
                duration = duration
                print("Длительность - ", duration)
        except AttributeError:
            director = "-"


        try:
            actor_div = soup.find('div', class_='styles_actors__wn_C4')  # получаем список актеров
            if actor_div:
                actors_tags = actor_div.find_all('a', class_='styles_link__Act80')
                actors = [actor_tag.text for actor_tag in actors_tags]
                actor_str = ""
                for i_a in actors:
                    actor_str += i_a + " , "  # для последующего сплита при извлечении данных
                print("Актеры -", actors)
            else:
                print("Информация об актерах не найдена.")
                actors_str = "-"
        except AttributeError:
            actor_str = '-'


        # создание экземпляра класса Movie с параметрами выше
        movie = Movie(
            title=title,
            original_title=original_title,
            mpaa=mpaa,
            rating=rating,
            rating_count=rating_count,
            imdb_ratings_count=imdb_ratings_count,
            imdb_rating=imdb_rating,
            positive_ratings=positive_ratings,
            negative_ratings=negative_ratings,
            country_film=country_film,
            film_genre=film_genre,
            director=director,
            budget=budget,
            worldwide_gross=worldwide_gross,
            russian_gross=russian_gross_block,
            premiere_date=premiere_date_str,
            duration=duration,
            actors=actor_str
        )

        # Сохраняем объект Movie в базе данных
        movie.save()

    return HttpResponse("Функция parse выполнена успешно!")  # возращаем сообщение об успешном парсинге
