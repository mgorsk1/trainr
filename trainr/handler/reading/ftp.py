from trainr.handler.reading import ReadingHandler


class FTPReadingHandler(ReadingHandler):
    @property
    def reading_type(self):
        return 'ftp'
