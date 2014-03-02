__author__ = 'Torsten'


from bs4 import BeautifulSoup
import urllib2
import pprint

pp = pprint.PrettyPrinter(indent=4)


class Dvllive(object):
    _page_videos = 'http://www.dvllive.tv/videos'

    def __init__(self):
        pass

    def get_videos(self):
        videos = []
        page_html = urllib2.urlopen(self._page_videos)
        page_soup = BeautifulSoup(page_html.read())
        videos += self._get_video_per_page(page_soup)
        pages = self._get_last_video_page(page_soup)
        for page_number in pages:
            sub_page_html = urllib2.urlopen(self._page_videos + '?page=' + str(page_number))
            sub_page_soup = BeautifulSoup(sub_page_html.read())
            videos += self._get_video_per_page(sub_page_soup)
        pp.pprint(videos)

    @staticmethod
    def _get_last_video_page(soup):
        last_page_number = int(soup.find('div', class_='pagination').span.find_all('a')[-2].span.text)
        return range(2, last_page_number + 1)

    @staticmethod
    def _get_video_per_page(soup):
        vids_on_this_page = []
        tag_videos_items = soup.find('div', id='videos').ol
        for list_item in tag_videos_items.contents:
            try:
                link = list_item.a
            except AttributeError:
                continue
            else:
                single_vid = {
                    'link': link['href'],
                    'thumb': link.find('img')['src'],
                    'title': link['title'].encode('utf-8'),
                    'date': link.find('span', class_='date').string.encode('utf-8')
                }
                vids_on_this_page.append(single_vid)
        return vids_on_this_page

def main():
    dvllive = Dvllive()
    dvllive.get_videos()


if __name__ == '__main__':
    main()

