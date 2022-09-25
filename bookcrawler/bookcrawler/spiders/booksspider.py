import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        'http://bibliadocaminho.com/ocaminho/TXavieriano/TXIndexLivros.htm',
    ]

    def parse(self, response):
        book_links = response.css('blockquote p a')
        yield from response.follow_all(book_links, self.parse_book)

    def parse_book(self, response):
        chapter_links = response.css('blockquote p a')
        yield from response.follow_all(chapter_links, self.parse_chapter)

    def parse_chapter(self, response):
        heading = response.css('h1 i::text').get().strip().split('—')
        book_title = heading[0].strip()
        book_author = heading[1].strip()
        book_medium = 'Chico Xavier'
        chapter_number = response.css('h4::text').get('').strip()
        chapter_name = response.css('h2::text').get('').strip()

        epigraph = response.css('blockquote p.BT')
        chapter_epigraph_text = ''
        chapter_epigraph_author = ''
        chapter_epigraph_ref = ''
        if epigraph:
            chapter_epigraph_text = (
                epigraph.css('::text').get('')
                .replace('—', '')
                .strip()
            )
            chapter_epigraph_author = (
                epigraph.css('i::text').get('')
                .replace('.', '')
                .strip()
            )
            chapter_epigraph_ref = epigraph.css('a::text').get()

        chapter_text = (
            response
            .css('blockquote')
            .css('p:not([class="BT"]):not([class="Sgn"]):not([class="FnT"])::text, p:not([class="BT"]):not([class="Sgn"]):not([class="FnT"]) a::text')
            .getall()
        )
        chapter_text = '\n'.join(
            [self._remove_extra_spaces(p.strip()) for p in chapter_text]
        )
        return {
            'book_title': self._remove_extra_spaces(book_title),
            'book_author': self._remove_extra_spaces(book_author),
            'book_medium': book_medium,
            'chapter_number': chapter_number,
            'chapter_name': chapter_name,
            'chapter_epigraph_text': chapter_epigraph_text,
            'chapter_epigraph_author': chapter_epigraph_author,
            'chapter_epigraph_ref': chapter_epigraph_ref,
            'chapter_text': chapter_text,
        }

    def _remove_extra_spaces(self, s):
        return ' '.join(s.split())
