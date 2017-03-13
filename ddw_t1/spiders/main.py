import scrapy as sc
import time
# from pymongo import MongoClient

class BlogSpider(sc.Spider):
    name = "DDW'"
    start_urls = ['http://localhost:8000']
    cities = {}
    persons = {}
    headers = {"User-Agent" : name}

    def parse(self, response):
        for city in response.css("ul.cities li"):
            city_url = city.css("a::attr(href)").extract_first()
            yield sc.Request(response.urljoin(city_url), callback=self.parse_city)

    def parse_city(self, response):
        city = response.css("h1::text").extract_first()
        if not city in self.cities:
            self.cities[city] = []
            for person in response.css("ul.persons li"):
                person_url = person.css("a::attr(href)").extract_first()
                req = sc.Request(response.urljoin(person_url), callback=self.parse_person)
                req.meta["city_name"] = city
                yield req
        # self.cities[city] = self.cities[city][:]\

    def parse_person(self, response):
        person = response.css("div.person")
        city_name = response.meta["city_name"]
        person_name = person.css("span.name::text").extract_first()
        person_data = {
                "phone" : person.css("span.phone::text").extract_first(),
                "gender" : person.css("span.gender::text").extract_first(),
                "age": person.css("span.age::text").extract_first(),
                "city": city_name
            }
        if not person is self.persons:
            yield {person_name: person_data}
        self.cities[city_name].append(person_data)
        self.persons[person_name] = person_data
        for city in response.css("ul.cities li"):
            city_url = city.css("a::attr(href)").extract_first()
            yield sc.Request(response.urljoin(city_url), callback=self.parse_city)