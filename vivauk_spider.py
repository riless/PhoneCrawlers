#! /usr/bin/python2.7
# -*- coding: utf-8 -*- 

from functions import *


class VivaUkSpider(CrawlSpider):

	name = "vivauk"
	url = "vivastreet.co.uk"

	deny = ()
	allow = ('.*')

	country = 'uk'
	indicatif = '44'
	total =  20300000
	prefix = (
				( '71', '1' ),
				( '74', '2' ),
				( '75', '3' ),
				( '76', '4' ),
				( '77', '5' ),
				( '78', '6' ),
				( '79', '7' )
			)

	xpath_location = '//dl/dd/div/text()'
	xpath_phones = '//span[@id="phone_number"]/text()'

	split? = false;
	split_sep = ','
	split_index = 0

	strip_str = ''

	debug_link = false
	debug_infos = false

	i = 1 # avoid devision by 0
	err = 0
	wr = 0

	starttime = datetime.now()

	outputHandle = open(name+'.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date) VALUES')

	allowed_domains = [url]
	start_urls = [
		"http://"+url
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=(url,), deny=deny, allow=allow),
			callback='parse_page', follow=True
		),
	)
	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)

		# debug link
		if self.debug_link:
			print '[+]', response.url

		location = hxs.select(self.xpath_location).extract()
		phones = hxs.select(self.xpath_phones).extract()

		try:
			if len(phones)>0 and len(location)>0:
				location = location[0];
				
				# split
				if split?:
					location = location[0].split(self.split_sep)[self.split_index]

				location = strip(location, self.strip_str)

				location = location.strip().encode('utf8')
				norm_location = normalize( location )

				for phone in phones:
					phone = strip(phone, '[^0-9]')
					phone = strip(phone, '^0*')

					if phone[:len(self.indicatif)] != self.indicatif:
						phone = self.indicatif+phone
					
					# debug infos
					if self.debug_infos:
						print "<<",phone,">>", "[[", location, "]]"

					crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

					duration = (datetime.now() - self.starttime).total_seconds()
					speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
					speedmin = math.ceil( ( self.i / duration ) * 60 )
					t =  (self.i + self.err + self.wr)
					taux = (self.i * 100) / t
					tauxWr = (self.wr * 100) / t 

					progression =  ((self.i + self.err) * 100) / self.total

					regex_prefix = ""	
					for p in self.prefix:
						regex_prefix += p[0]+"[0-9]{"+p[1]+"}|"
					regex_prefix = regex_prefix[:-1] # get rid of the last |
					
					separator = ''
					if (t > 1):
						separator = ','

					regex_phone = '^'+self.indicatif+"("+regex_prefix+")")
					if ( match(phone, regex_phone ):
						self.outputHandle.write( '{}\n("{}", "{}", "{}", "{}", "{}")'.format(separator, phone, self.country, location, norm_location, crawl_datetime) );
						print "[{}] {}% OK {}% Wr [progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {}".format(self.i, taux,tauxWr, progression, int(speedmin), int(speed), phone, crawl_datetime, location, norm_location )

						self.i += 1
					else:
						self.wr += 1
			else:
				self.wr += 1

		except:
			self.err += 1

