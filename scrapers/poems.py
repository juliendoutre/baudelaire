#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy
import re


class PoemsScrapper(scrapy.Spider):
    """
    A scrapper getting Baudelaire's poems from Internet.
    """

    name = "poems-scrapper"
    start_urls = ["https://www.poesie-francaise.fr/poemes-charles-baudelaire/"]
    reg1 = re.compile(r"\<span class=\"decalage\d+\"\>\<\/span\>")
    reg2 = re.compile(r"\<i class=\"poemes-auteurs\">\u00c9crit en \d\d\d\d\.\<\/i\>")
    reg3 = re.compile(r"\n+")

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
            "text": [
                line.strip()
                for line in self.reg3.sub(
                    "\n",
                    self.reg1.sub(
                        "",
                        self.reg2.sub(
                            "",
                            text.replace("<p>", "")
                            .replace("</p>", "")
                            .replace("<b>", "")
                            .replace("</b>", "")
                            .replace("<br>", "\n")
                            .replace("Sonnet.", ""),
                        ),
                    ),
                ).split("\n")
                if len(line) != 0
            ],
        }
