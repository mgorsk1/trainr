from trainr.backend.handler.reading import ReadingHandler


class HRReadingHandler(ReadingHandler):
    @property
    def reading_type(self):
        return 'hr'
