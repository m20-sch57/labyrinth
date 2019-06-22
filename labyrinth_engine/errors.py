class LabyrinthError(Exception):
    pass


class LabyrinthLoadError(LabyrinthError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'File "{}"\n{}'.format(self.file, self.msg)

# TODO: understand errors. To continue the list of errors. Issue #44
