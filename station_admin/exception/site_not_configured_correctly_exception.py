class SiteNotConfiguredCorrectlyException(Exception):
    def __init__(self, message='Site is not configured correctly.'):
        self.message = message
        super().__init__(self.message)