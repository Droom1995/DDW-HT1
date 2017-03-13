import scrapy as sc
import time
import sys
import pprint


class HabrSpider(sc.Spider):
    name = 'habr'
    start_urls = ['http://habrahabr.ru']

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
        'DEPTH_LIMIT' : 100
    }

    # landing page parser
    def parse(self, response):
        hxs = sc.Selector(response)
        posts = hxs.xpath('.//h2[contains(@class, "post__title")]')
        for post in posts:
            post_url = post.xpath('.//a[contains(@class, "post__title_link")]/@href').extract()[0]
            yield sc.Request(response.urljoin(post_url), callback=self.parse_post)
        next_page_url = hxs.xpath('.//a[contains(@class, "arrows-pagination__item-link_next")]/@href').extract()[0]
        print(next_page_url)
        yield sc.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_post(self, response):
        item = {}
        hxs = sc.Selector(response)
        title = hxs.xpath('//div[contains(@class, "post__header")]')
        item["time"] = title.xpath('.//span[contains(@class, "post__time_published")]/text()').extract()[0]
        title_text = title.xpath('.//h1[contains(@class, "post__title")]')
        item["title"] = title_text.xpath('.//span/text()').extract()[0]
        author = hxs.xpath('.//a[contains(@class,"page-header__info-title")]/text()')
        if len(author) == 0:
            author = hxs.xpath('.//a[contains(@class,"page-header__username-link")]/text()')
        else:
            author = author[0]
        item["author"] = author.extract()

        yield item
