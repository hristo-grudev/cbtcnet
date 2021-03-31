import scrapy

from scrapy.loader import ItemLoader

from ..items import CbtcnetItem
from itemloaders.processors import TakeFirst


class CbtcnetSpider(scrapy.Spider):
	name = 'cbtcnet'
	start_urls = ['https://cbtcnet.com/news']

	def parse(self, response):
		post_links = response.xpath('//a[@class="news-article"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//article/h1/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::h1 | ancestor::h4)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//h4/text()').get()

		item = ItemLoader(item=CbtcnetItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
