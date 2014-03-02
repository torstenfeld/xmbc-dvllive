__author__ = 'Torsten'


from bs4 import BeautifulSoup
import urllib2
# import pprint
import urlparse

# pp = pprint.PrettyPrinter(indent=4)


class Dvllive(object):
    _page_videos = 'http://www.dvllive.tv/videos'
    videos_found = []

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
            if str(page_number) >= '2':
                break
        self.videos_found = videos

    def play_video(self, partial_url):
        url = urlparse.urljoin(self._page_videos, partial_url)
        # print '\n\n\n\n\n\n'
        # print url
        page_html = urllib2.urlopen(url)
        page_soup = BeautifulSoup(page_html.read())
        # print page_soup
        embed_url = page_soup.find('textarea', class_='code').iframe['src']
        # print embed_url
        embed_html = urllib2.urlopen(embed_url)
        embed_soup = BeautifulSoup(embed_html.read())
        # print embed_soup
        try:
            asset = embed_soup.find('a', class_='asset')['href']
        except KeyError:
            print 'href not found'
            # print embed_soup
            img = embed_soup.find('img')['data-src']
            print img
            result = {
                'label': 'asdf',
                # 'type': 'image',
                'path': img
                # 'is_playable': True
            }
        else:
            print asset
            result = {
                'label': 'asdf',
                # 'type': 'video',
                'path': asset
                # 'path': asset.encode('utf-8')
                # 'is_playable': True
            }
        finally:
            print result
            return result
        # asset = embed_soup.find('a', class_='asset')
        # except NoneT
        # print page_soup.body.div.div.div.a['href']


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
                    'path': link['href'],
                    # 'thumb': link.find('img')['src'],
                    'label': link['title'],
                    # 'date': link.find('span', class_='date').string.encode('utf-8'),
                    'is_playable': True
                }
                vids_on_this_page.append(single_vid)
        return vids_on_this_page

def main():
    dvllive = Dvllive()
    dvllive.get_videos()
    # dvllive.play_video('embed/1f08c1507c3e013157697054d2ab7c84')
    for video in dvllive.videos_found:
        # print video['link']
        dvllive.play_video(video['link'])
    # dvllive.play_video(dvllive.videos_found[0]['link'])


if __name__ == '__main__':
    main()

