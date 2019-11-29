import requests
import scrapy


class PoemsScrapper(scrapy.Spider):
    """
    A scrapper getting Baudelaire's poems from Internet.
    """

    name = "poems-scrapper"
    start_urls = ["https://www.poesie-francaise.fr/poemes-charles-baudelaire/"]

    def parse(self, response):
        for poeme_link_container in response.css(".poemes-auteurs"):
            yield response.follow(
                poeme_link_container.css("a::attr(href)").extract_first(),
                callback=self.parse_poem_page,
            )

    def parse_poem_page(self, response):
        title = response.css("h2.titrepoeme::text").extract_first()
        collection = response.css("p.soustitre a::text").extract_first()
        text = response.css(".postpoetique p").extract_first()
        yield {
            "title": title.replace("Titre : ", ""),
            "collection": collection,
            "text": text.replace("<p>", "")
            .replace("</p>", "")
            .replace("<br>", "\n")
            .replace("Sonnet.\n\n", "")
            .replace('<span class="decalage2"></span>', ""),
        }
