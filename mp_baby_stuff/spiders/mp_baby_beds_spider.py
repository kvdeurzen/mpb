from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider

from mp_baby_stuff.items import MPBabyStuffItem

class MPBabyBedsSpider(Spider):
  name = "mp_baby_stuff"
  allowed_domains = ["marktplaats.nl"]
  start_urls = [
#      'https://www.marktplaats.nl/a/kinderen-en-baby-s/buggy-s/m1220231231-kinder-buggy.html?c=a2384ef0ece270f44503df9f8598c624&previousPage=lr&pos=7'
#      'https://www.marktplaats.nl/a/kinderen-en-baby-s/overige-kinderen-en-baby-s/a1009704838-universele-voetenzak-voetzak-voor-buggy-kinderwagen-401000.html?c=a2384ef0ece270f44503df9f8598c624&previousPage=lr&pos=8&casData=AvB_UI1O_8uYh32EBn_Jc7MR4brxGcqBj7Jh9a9fckCxQKCzhSvXDhLSwbi9qxFOXzTgx4G7xskZLKRpCyO-ahU2LCVsIClYdJ3W-YJvaS2DS43189wXVIP7IUbGbHpmvq19HHdhJGbxPHOg6AgYPsYBnXcTRyA0rojqx9PRAT3820Hvk0ORoz_89P84hYOw4bLJRL9dCQ3u5M1dIyksQuQKtk0c4aQ3GKxdqCO0GFbFM02sXTYtVyYFRJqVAUBhs0XmsK_DBKGd__QXFciCCPswiuWp8Tfi_It29QPwFck_JsSLsu3K1oPoPSohYcm-OoRj9NqGcB_pqYcfAV_8_5-g_k4OfxXALAWYbUrWYhNlnworCWQU0zXVwb_5OvF1ZvQykUrzHIMUI6i35fWRjZJ60Mm7r-BVpsPL3ippQI8OXlCmyeO_OwzrW547FUN21j9tZwvcfNMrdfgx3GFsug'
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
    asking_price_list    = Selector(response).xpath(self.ASKING_PRICE_EXTRACTOR).extract()

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
    if asking_price_list:    item ['asking_price']    = asking_price_list[0]

    return item
