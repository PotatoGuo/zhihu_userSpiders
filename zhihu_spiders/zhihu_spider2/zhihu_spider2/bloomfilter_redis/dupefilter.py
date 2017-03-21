from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from .connection import get_redis_from_settings
from .bloomfilter import BloomFilter


class RFPDupeFilter(BaseDupeFilter):


    def __init__(self, server, key, debug=False):
        self.server = server
        self.debug = debug
        self.key = key
        self.bloomfilter = BloomFilter(server=server, key=key)

    @classmethod
    def from_settings(cls, settings):
        server = get_redis_from_settings(settings)
        key = settings.get('SCHEDULER_DUPEFILTER_KEY')
        return cls(server=server, key=key)

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.
        Parameters
        ----------
        crawler : scrapy.crawler.Crawler
        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.
        """
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """Returns True if request was already seen.
        Parameters
        ----------
        request : scrapy.http.Request
        Returns
        -------
        bool
        """
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        if self.bloomfilter.isContains(fp):
            return True
        else:
            self.bloomfilter.insert(fp)
            return False


    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.
        Parameters
        ----------
        request : scrapy.http.Request
        Returns
        -------
        str
        """
        return request_fingerprint(request)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.
        Parameters
        ----------
        reason : str, optional
        """
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        self.server.delete(self.key)
