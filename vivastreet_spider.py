#! /usr/bin/python2.7

from functions import *


class VivastreetSpider(CrawlSpider):
	outputHandle = open('vivastreet.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date, depart) VALUES')

	starttime = datetime.now()
	name = "vivastreet"
	allowed_domains = ["vivastreet.com"]
	start_urls = [
		"http://vivastreet.com"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("vivastreet.com",)),
			callback='parse_page', follow=True
		),
	)

	total = 2660661
	indicatif = '33'
	country = 'fr'
	i = 1
	err = 0
	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)

		try:
			location = hxs.select('//dl/dd/div/text()').extract()[0]
			phone = hxs.select('//span[@id="phone_number"]/text()').extract()[0]
			phone = phone.replace(' ', '')
			if phone[0] == '0':
				phone = phone[1:]
			if phone[:2] != self.indicatif:
				phone = self.indicatif+phone

			raw_location = location.split(',')

			depart = raw_location[1].strip()
			location = strip( raw_location[len(raw_location) - 1], '[0-9]' ).strip('\n\r\t- ')

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

