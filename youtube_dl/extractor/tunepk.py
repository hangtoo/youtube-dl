from __future__ import unicode_literals

import re

from .common import InfoExtractor


class TunepkIE(InfoExtractor):
    _VALID_URL = r'(?:https?://|\.)(tune\.pk)/(?:player|video|play)/(?:[\w\.\?]+=)?(?P<id>\d+)'
    _TEST = {
        'url': 'https://tune.pk/video/6919541/maudie-2017-international-trailer-1-ft-ethan-hawke-sally-hawkins',
        'md5': '0C537163B7F6F97DA3C5DD1E3EF6DD55',
        'info_dict': {
            'id': '6919541',
            'ext': 'mp4',
            'title': 'Maudie (2017) | International Trailer # 1 ft Ethan Hawke, Sally Hawkins',
            'thumbnail': r're:^https?://.*\.jpg$'
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        html = webpage.replace('\n\r', '').replace('\r', '').replace('\n', '').replace('\\', '')
        sources = re.compile('"sources"\s*:\s*\[(.+?)\]').findall(html)[0]
        sources = re.compile("{(.+?)}").findall(sources)

        formats = []

        for source in sources:
            video_link = str(re.compile('"file":"(.*?)"').findall(source)[0])
            video_type = str(re.compile('"type":"(.*?)"').findall(source)[0])
            video_bitrate = str(re.compile('"bitrate":(\d+)').findall(source)[0])
            formats.append({
                'url': video_link,
                'ext': video_type,
                'format_id': video_bitrate
            })

        self._sort_formats(formats)

        return {
            'id': video_id,
            'formats': formats,
            'title': self._html_search_meta(r'title', webpage, 'title'),
            'description': self._html_search_meta(r'description', webpage, 'description'),
            'thumbnail': self._html_search_meta(r'thumbnail', webpage, 'thumbnail'),
            'uploader': self._html_search_meta(r'author', webpage, 'author'),
            'average_rating': self._html_search_meta(r'rating', webpage, 'rating')
        }
