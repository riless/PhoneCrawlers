#! /usr/bin/python2.7
# -*- coding: utf-8 -*- 

from functions import *


class OkSpider(CrawlSpider):
	outputHandle = open('ok.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date) VALUES')

	starttime = datetime.now()
	name = "ok"
	allowed_domains = ["www.ouedkniss.com"]
	start_urls = [
		"http://www.ouedkniss.com/"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("www.ouedkniss.com",)),
			callback='parse_page', follow=True
		),
	)

	total =  6630000
	indicatif = '213'
	country = 'dz'
	i = 0
	err = 0
	wr = 0
	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)

		location = hxs.select('//p[@class="Adresse"]/text()').extract()
		phone = hxs.select('//p[@class="Phone"]/img/@src').extract()
	

		try:
			if len(phone)>0 and len(location)>0:
				location = match(location[0], '^[\S]+').encode('utf8')
				norm_location = normalize( location )
				
				phones = ocr(phone[0]).split('_')
				for phone in phones:
					phone = strip(phone, '[^0-9]*')	
					phone = phone.lstrip('0')	 		
					if phone[:3] != self.indicatif:
						phone = self.indicatif+phone

					crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

					duration = (datetime.now() - self.starttime).total_seconds()
					speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
					speedmin = math.ceil( ( self.i / duration ) * 60 )
					t =  (self.i + self.err + self.wr)
					taux = (self.i * 100) / t
					tauxWr = (self.wr * 100) / t 

					progression =  ((self.i + self.err) * 100) / self.total

					if len(phone) ==12 and len(norm_location) != 0:
						self.outputHandle.write(u'("'+phone+'", "'+self.country+'", "'+location.decode('utf8')+'", "'+norm_location+'", "'+crawl_datetime+'"),'+"\n")
						print "[{}] {}% OK {}% Wr [progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {}".format(self.i, taux,tauxWr, progression, int(speedmin), int(speed), phone, crawl_datetime, location.decode('utf8'), norm_location )
						self.i += 1
					else:
						self.wr += 1
			else:
				self.wr += 1

		except:
			self.err += 1

