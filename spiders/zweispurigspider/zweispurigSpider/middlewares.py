# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import time

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class ZweispurigspiderSpiderMiddleware:
    # Spider middleware is used to process requests and responses
    # as they pass through the spider and the downloader.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RandomUserAgentMiddleware:
    """
    Middleware to randomly select a User-Agent for each request
    to mimic requests coming from different browsers.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        request.headers['User-Agent'] = user_agent
        spider.logger.info(f'Using User-Agent: {user_agent}')


class RandomHeadersMiddleware:
    """
    Middleware to add random headers to each request
    to make requests look more human-like.
    """
    headers_list = [
        {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'},
        {'Accept-Language': 'en-US,en;q=0.5'},
        {'Accept-Encoding': 'gzip, deflate, br'},
        {'Connection': 'keep-alive'},
        {'Upgrade-Insecure-Requests': '1'},
    ]

    def process_request(self, request, spider):
        headers = random.choice(self.headers_list)
        for key, value in headers.items():
            request.headers[key] = value
        spider.logger.info(f'Using headers: {headers}')


class RandomDelayMiddleware:
    """
    Middleware to introduce random delays between requests
    to mimic human browsing behavior and avoid detection.
    """
    def process_request(self, request, spider):
        delay = random.uniform(2, 10)  # Random delay between 2 and 10 seconds
        spider.logger.info(f'Sleeping for {delay:.2f} seconds to mimic human behavior.')
        time.sleep(delay)


class ZweispurigspiderDownloaderMiddleware:
    # Downloader middleware is used to process requests and responses
    # as they pass through the downloader.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

