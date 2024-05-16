import scrapy
import re
import os
import hashlib
from datetime import datetime

class ZweispurigSpider(scrapy.Spider):
    name = 'zweispurig'
    allowed_domains = ['zweispurig.at']
    start_urls = ['https://www.zweispurig.at/autohaendler/']

    dealer_section_css = '.page-content[style="margin-top:15px"] .container .col-md-8.col-md-pull-4'
    dealer_info_css = '.col-md-9.col-sm-9'

    date_stamp = datetime.now().strftime("%Y%m%d")
    json_file_name = f"{date_stamp}_crawled.json"
    xlsx_file_name = f"{date_stamp}_crawled.xlsx"

    seen_items = set()
    current_page_number = 1

    potential_duplicates = []
    checking_duplicates = False
    dealer_name_for_duplicates = None

    def normalize_string(self, input_string):
        if input_string is None:
            return ''
        lowercased = input_string.lower()
        normalized = re.sub(r'\W+', '', lowercased)
        return normalized

    def generate_hash(self, *args):
        hasher = hashlib.sha256()
        for arg in args:
            normalized_arg = self.normalize_string(arg)
            hasher.update(normalized_arg.encode('utf-8'))
        return hasher.hexdigest()

    def search_url(self, dealer_name):
        return f"https://www.zweispurig.at/autohaendler/?firmenname={dealer_name}&plz=&ort=&vertragshaendler=0&werkstatt=&order=firmenname&search=1"

    def parse(self, response):
        dealer_section = response.css(self.dealer_section_css)
        dealers = dealer_section.css('.row')

        if not dealers:
            self.logger.info(f"No dealers found on page {self.current_page_number}. Stopping crawl.") #LAST PAGE COMMENT
            if not self.checking_duplicates:
                yield from self.check_duplicates()
            return
                
        for dealer in dealers:
            dealer_info = dealer.css(self.dealer_info_css)
            for info in dealer_info:
                item = {
                    'name': self.extract_name(info),
                    'street_address': self.extract_street_address(info),
                    'postleitzahl': self.extract_postleitzahl(info),
                    'ort': self.extract_ort(info),
                    'bundesland': self.extract_bundesland(info),
                    'stadt': self.extract_stadt(info),
                    'phone': self.extract_phone(info),
                    'mobile': self.extract_mobile(info),
                    'fax': self.extract_fax(info),
                    'website': self.extract_website(info),
                    'num_cars': self.extract_num_cars(info),
                }

                item_hash = self.generate_hash(item['name'], item['street_address'], item['postleitzahl'], item['ort'], item['bundesland'], item['stadt'], item['phone'], item['mobile'], item['fax'], item['website'], item['num_cars'])
                if item_hash not in self.seen_items:
                    yield item
                    self.seen_items.add(item_hash)
                else:
                    if not self.checking_duplicates:
                        self.potential_duplicates.append(item)

        if not self.checking_duplicates:
            self.current_page_number += 1
            next_page_url = f"https://www.zweispurig.at/autohaendler/?seite={self.current_page_number}"
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.current_page_number += 1
            next_page_url = f"https://www.zweispurig.at/autohaendler/?firmenname={self.dealer_name_for_duplicates}&plz=&ort=&vertragshaendler=0&werkstatt=&order=firmenname&search={self.current_page_number}"
            yield scrapy.Request(next_page_url, callback=self.parse)

    def check_duplicates(self):
        self.logger.info("Checking duplicates")
        if len(self.potential_duplicates) <= 0:
            self.logger.info("No potential duplicates to check.")
            return 
        else:
            self.logger.info(f"Starting to check duplicates for {len(self.potential_duplicates)} items.")
            self.checking_duplicates = True 
            current_page_number = 1
            for item in self.potential_duplicates:
                self.dealer_name_for_duplicates = item['name']
                search_url = self.search_url(item['name'])
                yield scrapy.Request(search_url, callback=self.parse, dont_filter=True)

    # Extraction functions
    def extract_name(self, selector):
        return selector.css('h3.det_label::text').get() or " "

    def extract_street_address(self, selector):
        return selector.xpath('.//h3/following-sibling::text()[1]').get().strip()

    def extract_postleitzahl(self, selector):
        address_parts = selector.css('h4.det_kontakt_daten::text').getall()
        if address_parts and " " in address_parts[0]:
            return address_parts[0].split(' ', 1)[0]
        return " "

    def extract_ort(self, selector):
        address_parts = selector.css('h4.det_kontakt_daten::text').getall()
        return address_parts[1] if len(address_parts) > 1 else " "

    def extract_bundesland(self, selector):
        address_parts = selector.css('h4.det_kontakt_daten::text').getall()
        return address_parts[2] if len(address_parts) > 2 else " "

    def extract_stadt(self, selector):
        # Implement as needed
        return " "

    def extract_phone(self, selector):
        phone = selector.xpath('.//i[contains(@class, "fa-phone")]/following-sibling::text()').get()
        return phone.strip() if phone else " "

    def extract_mobile(self, selector):
        mobile = selector.xpath('.//i[contains(@class, "fa-mobile")]/following-sibling::text()').get()
        return mobile.strip() if mobile else " "

    def extract_fax(self, selector):
        fax = selector.xpath('.//i[contains(@class, "fa-fax")]/following-sibling::text()').get()
        return fax.strip() if fax else " "

    def extract_website(self, selector):
        return selector.css('a[title*="Webseite von"]::attr(href)').get() or " "

    def extract_num_cars(self, selector):
        cars_link_text = selector.xpath('.//a[contains(@class, "btn_hvz_right") and .//i[contains(@class, "fa-car")]]/text()').get()
        if cars_link_text:
            match = re.search(r'\((\d+)\)', cars_link_text)
            return match.group(1) if match else "0"
        return "0"
