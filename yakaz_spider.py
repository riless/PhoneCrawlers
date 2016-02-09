#! /usr/bin/python2.7

from functions import *


class YakazSpider(CrawlSpider):
	outputHandle = open('yakaz.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date, depart) VALUES')

	starttime = datetime.now()
	name = "yakaz"
	allowed_domains = ["yakaz.com"]
	start_urls = [
		"http://yakaz.com/"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("yakaz.com",)),
			callback='parse_page', follow=True
		),
	)

	total = 106000
	indicatif = '33'
	country = 'fr'
	i = 1
	err = 0
	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)

		try:
			location = hxs.select('//span[@class="placeNameHl"]/text()').extract()[0]
			print "\n\nlocation: "+location
			phone = hxs.select('//span[@class="bigPhoneContainer"]/span/img/@src').extract()[0]
			phone = ocr(phone).replace(' ', '')
			print "phone: "+phone
			if phone[0] == '0':
				phone = phone[1:]
			if phone[:2] != self.indicatif:
				phone = self.indicatif+phone

			depart = hxs.select('//span[@class="msgPlaceMark de"]').extract()[0]
			depart = match(depart, '[0-9]{5}')[:2]
			print depart
			
			norm_location = normalize( location )

			crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			duration = (datetime.now() - self.starttime).total_seconds()
			speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
			speedmin = math.ceil( ( self.i / duration ) * 60 )
			taux = (self.i * 100) / (self.i + self.err)

			progression =  ((self.i + self.err) * 100) / self.total

			if len(phone) == 11 and len(location) != '':
				self.outputHandle.write('("'+phone+'", "'+self.country+'", "'+location+'", "'+norm_location+'", "'+crawl_datetime+'", "'+depart+'"),'+"\n")
				print "[{}] {}% [progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {} | {}".format(self.i, taux, progression, int(speedmin), int(speed), phone, crawl_datetime, location, norm_location, depart )

				self.i += 1
			else:
				self.err += 1
		except:
			self.err += 1

