#! /usr/bin/python2.7

from functions import *


class DhdSpider(CrawlSpider):
	outputHandle = open('dhd.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date) VALUES')

	starttime = datetime.now()
	name = "dhd"
	allowed_domains = ["dhd24.com"]
	start_urls = [
		"http://dhd24.com"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("dhd24.com",), deny=('minireg.php', 'login.php')),
			callback='parse_page', follow=True
		),
	)

	total = 2630000
	indicatif = '49'
	country = 'de'
	i = 0
	err = 0
	wr = 0
	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)

		location = hxs.select('//div[@id="preis"]/following-sibling::div[1]/span/a[1]/text()').extract()
		phone = hxs.select('//li[@class="phone"]/span[@class="invisible"]/text()').extract()

		try:
			if len(phone)>0 and len(location)>0:
				phone = strip(phone[0], '[^0-9]*')

				if phone[0] == '0':
		 			phone = phone[1:]
		 		if phone[:2] != self.indicatif:
		 			phone = self.indicatif+phone

				location = strip(location[0], '[0-9(&nbsp;)]+\W*').strip()

				norm_location = normalize( location )
				crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

				duration = (datetime.now() - self.starttime).total_seconds()
				speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
				speedmin = math.ceil( ( self.i / duration ) * 60 )
				t =  (self.i + self.err + self.wr)
				taux = (self.i * 100) / t
				tauxWr = (self.wr * 100) / t 

				progression =  ((self.i + self.err) * 100) / self.total

				if len(phone) >=8 and len(phone) <=15 and len(location) != 0:
					self.outputHandle.write(u'("'+phone+'", "'+self.country+'", "'+location.decode('utf8')+'", "'+norm_location+'", "'+crawl_datetime+'"),'+"\n")
					print "[{}] {}% OK {}% Wr [progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {}".format(self.i, taux,tauxWr, progression, int(speedmin), int(speed), phone, crawl_datetime, location.decode('utf8'), norm_location )
					self.i += 1
				else:
					self.wr += 1
			else:
				self.wr += 1

		except:
			self.err += 1

