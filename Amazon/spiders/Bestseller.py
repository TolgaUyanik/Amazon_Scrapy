"""
import scrapy
import time

class BestsellerSpider(scrapy.Spider):
    name = "Bestseller"
    #allowed_domains = ["www.amazon.com.tr"]
    start_urls = ["https://www.amazon.com.tr/gp/bestsellers/electronics/13709879031?ref_=Oct_d_obs_S&pd_rd_w=ceAdY&content-id=amzn1.sym.023cc355-76de-49c1-930a-f269b45780bd&pf_rd_p=023cc355-76de-49c1-930a-f269b45780bd&pf_rd_r=6SED0B5XAEYK0YP96AAS&pd_rd_wg=NPcg8&pd_rd_r=1ad43d39-9933-4182-824e-4ac91761f68b"]

    def parse(self, response):
        itembox = response.css("div._cDEzb_iveVideoWrapper_JJ34T div.p13n-sc-uncoverable-faceout")
        for item in itembox:
            yield{
                #"number"       : itembox.css("div::text").get(), Number index'e eşit
                "product"      : itembox.css("a:nth-child(2) span div::text").getall(),
                "starcount"    : itembox.css("div div a i span::text").getall(),
                "commentcount" : itembox.css("div div a span.a-size-small::text").getall()
            }
            
        
        next_page = response.css("div.a-text-center a::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)   
        """

import scrapy
from Amazon.items import AmazonItem

class aitemsSpider(scrapy.Spider):
    name = 'Bestseller'

    def start_requests(self):
        url = "https://www.amazon.com.tr/gp/bestsellers/electronics/13709879031?ref_=Oct_d_obs_S&pd_rd_w=ceAdY&content-id=amzn1.sym.023cc355-76de-49c1-930a-f269b45780bd&pf_rd_p=023cc355-76de-49c1-930a-f269b45780bd&pf_rd_r=6SED0B5XAEYK0YP96AAS&pd_rd_wg=NPcg8&pd_rd_r=1ad43d39-9933-4182-824e-4ac91761f68b"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        amazon_item = AmazonItem()
        for aitem in response.css("div._cDEzb_iveVideoWrapper_JJ34T div.p13n-sc-uncoverable-faceout"):
            amazon_item['starcount'] = aitem.css("div div a i span::text").get()
            amazon_item['commentcount'] = aitem.css("div div span.a-size-small::text").get()
            amazon_item['product'] = aitem.css('a:nth-child(2) span div::text').get()
            yield amazon_item

        next_page = "https://www.amazon.com.tr/gp/bestsellers/electronics/13709879031/ref=zg_bs_pg_2_electronics?ie=UTF8&pg=2"

        if next_page is not None:
            next_page_url = next_page
            yield response.follow(next_page_url, callback= self.parse)
# scrapy crawl Bestseller -O test1.csv
