class InvalidJsonConfigFileException(Exception):
    def __init__(self, msg):
        super(InvalidJsonConfigFileException, self).__init__()
        print(f'Invalid JSON config file. "{msg}" not found.')
