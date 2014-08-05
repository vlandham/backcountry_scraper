import scrapy

#from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from backcountry_scraper.items import BackcountryScraperItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class BackcountrySpider(CrawlSpider):
  name = 'back'
  allowed_domains = ['http://www.backcountry.com/', 'www.backcountry.com']

  start_urls = ['http://www.backcountry.com/Store/catalog/categoryLanding.jsp?categoryId=bcsCat110004&page=0']

  rules = (Rule (SgmlLinkExtractor(restrict_xpaths=('//li[@class="pag-next"]'))
    , callback="parse_items", follow= True),
    )

  def parse_start_url(self, response):
    return self.parse_items(response)

  #def parse_links(self, response):
  #  hxs = HtmlXPathSelector(response)
  #  links = hxs.select('//a')
  #  for link in links:
  #    title = ''.join(link.select('./@title').extract())
  #    url = ''.join(link.select('./@href').extract())
  #    meta={'title':title,}
  #    cleaned_url = "%s/?1" % url if not '/' in url.partition('//')[2] else "%s?1" % url
  #    yield Request(cleaned_url, callback = self.parse_page, meta=meta,)
  

  def parse_items(self, response):
    products = response.css("#products").css(".product")
    items = []
    for product in products:
      title_text = product.css('.product-name::text').extract()
      brand_text = product.css('.brand-name::text').extract()
      item = BackcountryScraperItem()
      item['title'] = title_text
      item['brand'] = brand_text
      items.append(item)
    return items


