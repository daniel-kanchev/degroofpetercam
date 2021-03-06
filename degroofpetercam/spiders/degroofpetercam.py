import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from degroofpetercam.items import Article


class DegroofpetercamSpider(scrapy.Spider):
    name = 'degroofpetercam'
    start_urls = ['https://www.degroofpetercam.ch/en/news']

    def parse(self, response):
        links = response.xpath('//div[@class="read-more"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@property="content:encoded"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
