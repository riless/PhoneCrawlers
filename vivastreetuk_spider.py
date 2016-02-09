#! /usr/bin/python2.7

from functions import *


class VivastreetukSpider(CrawlSpider):
	outputHandle = open('vivastreetuk.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date, depart) VALUES')

	starttime = datetime.now()
	name = "vivastreetuk"
	allowed_domains = ["vivastreet.co.uk"]
	start_urls = [
		"http://vivastreet.co.uk"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("vivastreet.co.uk",), deny=('northern-ireland') ),
			callback='parse_page', follow=True
		),
	)

	total = 1411978 - 80902 # - Irlande
	indicatif = '44'
	country = 'uk'
	i = 1
	err = 0
	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)

		try:
			location = hxs.select('//dl/dd/div/text()').extract()[0]
			phone = hxs.select('//span[@id="phone_number"]/text()').extract()[0]
			phone = phone.replace(' ', '')
			depart = 'gb'
			if phone[0] == '0':
				phone = phone[1:]
			if phone[:2] != self.indicatif:
				phone = self.indicatif+phone

	
			location = location.split(',')[2].strip()
			norm_location = normalize( location )

			crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			duration = (datetime.now() - self.starttime).total_seconds()
			speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
			speedmin = math.ceil( ( self.i / duration ) * 60 )
			taux = (self.i * 100) / (self.i + self.err)

			progression =  ((self.i + self.err) * 100) / self.total

			if len(phone) >= 8 and len(location) != '':
				# write it
				self.outputHandle.write('("'+phone+'", "'+self.country+'", "'+location+'", "'+norm_location+'", "'+crawl_datetime+'"),'+"\n")
			
				# print it
				print "[{}] {}% [progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {} | {}".format(self.i, taux, progression, int(speedmin), int(speed), phone, crawl_datetime, location, norm_location, depart )

				self.i += 1
			else:
				self.err += 1
		except:
			self.err += 1

