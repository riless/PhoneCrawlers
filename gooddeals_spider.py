#! /usr/bin/python2.7

from functions import *
from time import sleep


class GooddealsSpider(CrawlSpider):
	outputHandle = open('gd.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date) VALUES')

	starttime = datetime.now()
	name = "gooddeals"
	allowed_domains = ["good-deals.lu"]
	start_urls = [
		"http://good-deals.lu"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("good-deals.lu",)),
			callback='parse_page', follow=True
		),
	)

	total = 123000
	indicatif = '352'
	country = 'lu'
	i = 1
	err = 0
	wr = 0
	

	def parse_page(self, response):
		sleep(0.1)
		hxs = HtmlXPathSelector(response)

		location = hxs.select('//span[@itemprop="locality"]/text()').extract()
		raw = hxs.select('//ul[@id="gdAdvertiserInfosList"]/li/text()').extract()
		try:

			# print "[+]" , response.url

			if len(location)>0:

				location = location[0]
				for line in raw:

					phone = strip(line, '[^0-9]')
					phone = strip(phone, '^0*')
					
					if (phone):
						if phone[:3] != self.indicatif:
							phone = self.indicatif+phone

						#print phone

						norm_location = normalize( location )
						crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

						duration = (datetime.now() - self.starttime).total_seconds()
						speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
						speedmin = math.ceil( ( self.i / duration ) * 60 )
						t =  (self.i + self.err + self.wr)
						taux = (self.i * 100) / t
						tauxWr = (self.wr * 100) / t 

						progression =  ((self.i + self.err) * 100) / self.total

						if ( match(phone, '^'+self.indicatif+'6(21|28|61|68|91|98)') ):
							self.outputHandle.write(u'("'+phone+'", "'+self.country+'", "'+location+'", "'+norm_location+'", "'+crawl_datetime+'"),'+"\n")
							print "[{}] {}% OK {}% Wr [progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {}".format(self.i, taux,tauxWr, progression, int(speedmin), int(speed), phone, crawl_datetime, location.decode('utf8'), norm_location )
							self.i += 1
						else:
							self.wr += 1
			else:
				self.wr += 1
		except:
			self.err += 1

