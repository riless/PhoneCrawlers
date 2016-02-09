#! /usr/bin/python2.7

from functions import *


class SondrioSpider(CrawlSpider):
	outputHandle = open('sondrio.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date, depart) VALUES')

	starttime = datetime.now()
	name = "sondrio"
	allowed_domains = ["sondrio.fr"]
	start_urls = [
		"http://sondrio.fr"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("sondrio.fr",)),
			callback='parse_page', follow=True
		),
	)

	total = 33300 #source google
	indicatif = '33'
	country = 'fr'
	i = 1
	err = 0

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)
		try:
			location = hxs.select('//div[@class="annonce-prixville-ville"]/h2/text()').extract()[0]
			phone = hxs.select('//span[@class="tel"]/img/@src').extract()[0]
			depart = match( location, '[0-9]{2}')
			phone = ocr(phone)
			phone = phone.replace(' ', '')
			if phone[0] == '0':
				phone = phone[1:]
			if phone[:2] != self.indicatif:
				phone = self.indicatif+phone

			location = strip(location, '[0-9 ]')
			norm_location = normalize( location )

			crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			duration = (datetime.now() - self.starttime).total_seconds()
			speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
			speedmin = math.ceil( ( self.i / duration ) * 60 )
			taux = (self.i * 100) / (self.i + self.err)

			progression =  ((self.i + self.err) * 100) / self.total

			if len(phone) == 11 and len(location) != '':
				self.outputHandle.write('("'+phone+'", "'+self.country+'", "'+location+'", "'+norm_location+'", "'+crawl_datetime+'", "'+depart+'"),'+"\n")
				print "[{}] {}% [progress: {}%] ({}/min - {}/24h) - {} - {} - {} - {} - {}".format(self.i, taux, progression, int(speedmin), int(speed), phone, crawl_datetime, location, norm_location, depart )

				self.i += 1
			else:
				self.err += 1
		except Exception as e:
			self.err += 1

