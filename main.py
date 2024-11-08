from bs4 import BeautifulSoup
import requests
from typing import Union, List
import json
from tqdm import tqdm
from time import sleep
import logging


logging.basicConfig(
    filename="log.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class Scraper:
    page: Union[int] = 0
    stop: Union[int] = 658

    films: Union[List] = []
    films_detail: Union[List] = []

    def __init__(self) -> None: ...

    def save(self):
        with open("films.json", "w") as file:
            json.dump(self.films, file, indent=4)

    def save_detail(self):
        with open("films-detail.json", "w") as file:
            json.dump(self.films_detail, file, indent=4)

    def get_films(self):
        self.progress = tqdm(total=self.stop)
        while self.page <= self.stop:
            self.page += 1
            html = requests.get(
                "http://asilmedia.org/films/tarjima_kinolar/page/{}/".format(self.page),
                "html.parser",
            )
            soup = BeautifulSoup(html.content)
            try:
                films = soup.find(id="dle-content").find_all("article")
            except AttributeError:
                continue
            for film in films:
                self.films.append(film.find("a")["href"])
            self.progress.update(1)
            self.save()

    def read_films(self):
        with open("films.json", "r") as file:
            return json.load(file)

    def scraper(self):
        films = self.read_films()
        progress = tqdm(total=len(films))
        for film in films:
            try:
                detail = self.get_film(film)
                self.films_detail.append(detail)
            except Exception as e:
                logging.error(e)
                sleep(10)
                continue
            progress.update(1)
            self.save_detail()

    def get_film(self, url):
        response = requests.get(
            url
        )
        soup = BeautifulSoup(response.content, "html.parser")
        desc = soup.find(attrs={"class": "full-body mb-4"}).find("div").text
        info = soup.find_all(attrs={"class": "fullinfo-list mb-2"})
        genre = [i.text for i in info[0].find_all("a")]
        rejisor = [i.text for i in info[1].find_all("a")]
        actor = [i.text for i in info[2].find_all("a")]

        data = soup.find_all(attrs={"class": "fullmeta-seclabel"})
        year = data[0].text
        country = data[1].text
        duration = data[2].text
        images = [
            i["data-src"]
            for i in soup.find(
                attrs={"class": "xfieldimagegallery flx justify-content-between"}
            ).find_all("img")
        ]
        urls = [
            i["href"]
            for i in soup.find(
                attrs={"class": "downlist-inner flx flx-column"}
            ).find_all("a")
            if i.text != "Telegram orqali yuklash olish"
        ]
        image = (
            soup.find(attrs={"class": "fullcol-left mr-4"})
            .find(attrs={"class": "full-sticky"})
            .find("img")["data-src"]
        )
        kp = soup.find(attrs={"class": "txt-big r-kp txt-bold500 pfrate-count"}).text
        im = soup.find(attrs={"class": "txt-big r-im txt-bold500 pfrate-count"}).text
        name = soup.find(attrs={"class": "title is-4 mb-2"}).text

        return {
            "name": name,
            "desc": desc,
            "image": image,
            "images": images,
            "urls": urls,
            "actor": actor,
            "genre": genre,
            "rejisor": rejisor,
            "year": year,
            "country": country,
            "duration": duration,
            "kp": kp,
            "im": im,
        }


obj = Scraper()
print(obj.scraper())
