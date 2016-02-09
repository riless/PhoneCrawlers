#! /usr/bin/python2.7

from functions import *


class QuokaSpider(CrawlSpider):
	outputHandle = open('quoka.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date) VALUES')

	starttime = datetime.now()
	name = "quoka"
	allowed_domains = ["quoka.de"]
	start_urls = [
		"http://www.quoka.de/"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("quoka.de",), deny=('search',), allow=('autos-nach-marken', )),
			callback='parse_page', follow=True
		),
	)

	total =  6615980
	indicatif = '49'
	country = 'de'
	i = 1
	err = 0
	empty = 0
	wrongdata = 0


	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)

		try:
			location = hxs.select('//p[@class="detailLocation"]/strong/span[@class="address"]/a/span[@class="locality"]/text()').extract()[0].encode('utf8')
			norm_location = normalize( location )
			phone_links = hxs.select('//ul[@class="contacts"]/li/p/img/@src').extract()

			if len(phone_links) == 0:
				self.empty += 1
				if self.empty % 100 == 0:
					print "\n["+str(self.empty)+"] ERR >> "+response.url
			else:	
				for plink in phone_links:

					phone = strip(ocr(plink), '[^0-9]*') 

					if phone[0] == '0':
				 		phone = phone[1:]
				 	if phone[:2] != self.indicatif:
				 		phone = self.indicatif+phone

					crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

					duration = (datetime.now() - self.starttime).total_seconds()
					speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
					speedmin = math.ceil( ( self.i / duration ) * 60 )
					crawled = (self.i + self.err + self.empty + self.wrongdata)
					tSuccess = (self.i * 100) / crawled
					tEmpty = (self.empty * 100) / crawled
					tError = (self.err * 100) / crawled
					tWrongData = (self.wrongdata * 100) / crawled

					progression =  (crawled * 100) / self.total

					if len(phone) >=8 and len(phone) <=15 and len(location) != 0:
						self.outputHandle.write(u'("'+phone+'", "'+self.country+'", "'+location.decode('utf8')+'", "'+norm_location+'", "'+crawl_datetime+'"),'+"\n")
						print "[{}] {}% OK {}% Empty {}% Errors {} Wrong Data [Progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {}".format(self.i, tSuccess, tEmpty, tError,  progression, int(speedmin), int(speed), phone, crawl_datetime, location.decode('utf8'), norm_location )
						self.i += 1
					else:
						self.wrongdata += 1
						print "["+str(self.wrongdata)+"]ERROR >> wrong datas"
		except Exception as e:
			self.err += 1
			if self.err % 100 == 0:
				print "\n["+str(self.err)+"]EXC >> "+response.url
				

