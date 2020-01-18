import io
import re

import requests
from django.core.management.base import BaseCommand
from tqdm import tqdm

from scraper.serializers import ECBRSSSerializer
from scraper.utils import remove_rdf_from_parsed_rss, CustomXMLParser

RSS_URL_PATTERN = r'class=\"rss\" href=\"(?P<rss_url>/rss/fx.*)\"'


class Command(BaseCommand):

    def handle(self, *args, **options):
        ecb_rss_list_url = 'https://www.ecb.europa.eu/home/html/rss.en.html'
        ecb_rss_list_response = requests.get(ecb_rss_list_url).text
        matched_rss_url = re.findall(RSS_URL_PATTERN, ecb_rss_list_response)
        for url in tqdm(matched_rss_url):
            rss_feed = requests.get(f'https://www.ecb.europa.eu{url}').text
            improved_rss_feed = rss_feed.replace('channel>\n<item', 'channel><items><item').replace('/item>\n</rdf', '/item></items></rdf')
            stream = io.StringIO(improved_rss_feed)
            parsed_xml = remove_rdf_from_parsed_rss(CustomXMLParser().parse(stream=stream))
            deserialized_xml = ECBRSSSerializer(data=parsed_xml)
            deserialized_xml.is_valid()
            deserialized_xml.save()
