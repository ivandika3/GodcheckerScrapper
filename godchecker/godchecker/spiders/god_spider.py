import scrapy

class GodSpider(scrapy.Spider):
    name = 'god'

    start_urls = ['https://www.godchecker.com/']

    def parse(self, response):
        mythology_page_links = response.css('.pullout-panel li a')
        yield from response.follow_all(mythology_page_links, self.parse_mythology)

    def parse_mythology(self, response):
        pantheons_page_link = response.css('.leftbar-tile a')
        yield response.follow(pantheons_page_link, self.parse_pantheon)
    
    def parse_pantheon(self, response):
        god_page_links = response.css('.search-result a')
        yield response.follow(god_page_links, self.parse_god)

    def parse_god(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        
        attributes = [ attr.strip()[:-1] for attr in response.css('div.pullout-panel p::text').getall()]
        values = response.css('div.pullout-panel strong::text').getall()
        facts_and_figures = dict(zip(attributes, values))
        yield facts_and_figures

        
