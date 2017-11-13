from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider

from mp_baby_stuff.items import MPBabyStuffItem

class MPBabyBedsSpider(Spider):
  name = "mp_baby_stuff"
  allowed_domains = ["marktplaats.nl"]
  start_urls = [
#       "https://www.marktplaats.nl/a/kinderen-en-baby-s/babywiegjes-en-ledikanten/m1224575734-kinderledikantje.html?c=efb2ef4dc323389c4f92ed10afa33e3a&previousPage=lr&pos=1"
#       ]
      "https://www.marktplaats.nl/z/z.html?categoryId=577&startDateFrom=yesterday&sortBy=SortIndex",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/babyvoeding-en-toebehoren.html?categoryId=1489&sortBy=SortIndex&startDateFrom=yesterday",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/kinderwagen.html?query=kinderwagen&categoryId=565&sortBy=SortIndex&startDateFrom=yesterday",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/kinderkamer-commodes-en-kasten/comode.html?query=comode&categoryId=2773&sortBy=SortIndex&startDateFrom=yesterday",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/kinderkamer-bedden.html?categoryId=579&sortBy=SortIndex&startDateFrom=yesterday",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/boxen.html?categoryId=580&sortBy=SortIndex&startDateFrom=yesterday",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/traphekjes.html?categoryId=619&sortBy=SortIndex&startDateFrom=yesterday",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/babydragers-en-draagdoeken.html?categoryId=581&sortBy=SortIndex&startDateFrom=yesterday",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/kinderwagens-en-combinaties.html?categoryId=603&sortBy=SortIndex&startDateFrom=yesterday",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/buggy-s.html?categoryId=2132&sortBy=SortIndex&startDateFrom=yesterday",
      "https://www.marktplaats.nl/z/kinderen-en-baby-s/autostoeltjes-en-veiligheidszitjes.html?categoryId=566&sortBy=SortIndex&startDateFrom=yesterday",

  ]

  PRODUCT_EXTRACTOR         = '//article[contains(@class, "search-result")]'
  ID_EXTRACTOR              = '@data-item-id'
  TITLE_EXTRACTOR           = 'div//h2/a/span/text()'
  URL_EXTRACTOR             = 'div//a/@href'
  SELLER_EXTRACTOR          = '//div[contains(@id, "vip-seller")]//h2[contains(@class, "name")]/@title'
  SELLER_URL_EXTRACTOR      = '//*[@id="vip-seller"]/div[1]/div[1]/a/@href'
  DATE_POSTED_EXTRACTOR     = '//*[@id="displayed-since"]/span[3]/text()'
  LOCATION_EXTRACTOR        = 'normalize-space(//*[@id="vip-map-show"]/text())'
  CONDITION_EXTRACTOR       = '//td[3][preceding::*/text()[normalize-space(.)="Conditie"]/parent::*]/text()'
  TYPE_EXTRACTOR            = '//td[3][preceding::*/text()[normalize-space(.)="Type"]/parent::*]/text()'
  DESCRIPTION_EXTRACTOR     = '//div[@id="vip-ad-description"]/text()'
  BRAND_EXTRACTOR           = '//td[3][preceding::*/text()[normalize-space(.)="Merk"]/parent::*]/text()'
  CHARACTERISTICS_EXTRACTOR = '//td[3][preceding::*/text()[normalize-space(.)="Eigenschappen"]/parent::*]/text()'
  CATEGORY_EXTRACTOR        = '//meta[@name="twitter:data2"]/@content'
  ASKING_PRICE_EXTRACTOR    = '//*[@id="vip-ad-price-container"]/span/text()'


  def parse(self, response):

    products = Selector(response).xpath(self.PRODUCT_EXTRACTOR)

    for product in products:

      item          = MPBabyStuffItem()
      item['_id']   = product.xpath(self.ID_EXTRACTOR).extract()[0]
      item['title'] = product.xpath(self.TITLE_EXTRACTOR).extract()[0]
      item['url']   = product.xpath(self.URL_EXTRACTOR).extract()[0]

      yield Request(item['url'], self.parse_item, meta={'item':item})

    NEXT_PAGE_EXTRACTOR = '//*[@id="pagination"]/a[2]/@href'
    next_page = Selector(response).xpath(NEXT_PAGE_EXTRACTOR).extract_first()
    if next_page:
      yield Request(response.urljoin(next_page), callback=self.parse)

  def parse_item(self, response):
    item = response.meta['item']

# FOR TESTING A SPECIFIC ITEM
#  def parse(self,response):
#    item = MPBabyStuffItem()
#    item['_id'] = 'test'

    #item['title']       = 'test'
    seller_list          = Selector(response).xpath(self.SELLER_EXTRACTOR).extract()
    seller_url_list      = Selector(response).xpath(self.SELLER_URL_EXTRACTOR).extract()
    description_list     = Selector(response).xpath(self.DESCRIPTION_EXTRACTOR).extract()
    location_list        = Selector(response).xpath(self.LOCATION_EXTRACTOR).extract()
    date_posted_list     = Selector(response).xpath(self.DATE_POSTED_EXTRACTOR).extract()
    condition_list       = Selector(response).xpath(self.CONDITION_EXTRACTOR).extract()
    type_list            = Selector(response).xpath(self.TYPE_EXTRACTOR).extract()
    brand_list           = Selector(response).xpath(self.BRAND_EXTRACTOR).extract()
    characteristics_list = Selector(response).xpath(self.CHARACTERISTICS_EXTRACTOR).extract()
    category_list        = Selector(response).xpath(self.CATEGORY_EXTRACTOR).extract()
    asking_price_list    = Selector(response).xpath(self.ASKING_PRICE_EXTRACTOR).extract()[0].replace(',','.').replace('\u20AC ','')

    if seller_list:          item ['seller']          = seller_list[0]
    if seller_url_list:      item ['seller_url']      = seller_url_list[0]
    if description_list:     item ['description']     = " ".join(description_list)
    if location_list:        item ['location']        = location_list[0]
    if date_posted_list:     item ['date_posted']     = date_posted_list[0]
    if condition_list:       item ['condition']       = condition_list[0]
    if type_list:            item ['type']            = type_list[0]
    if brand_list:           item ['brand']           = brand_list[0]
    if characteristics_list: item ['characteristics'] = characteristics_list[0]
    if category_list:        item ['category']        = category_list[0]
    if asking_price_list:    item ['asking_price']    = asking_price_list

    return item
