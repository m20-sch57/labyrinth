class LabyrinthError(Exception):
    pass


class LabyrinthLoadError(LabyrinthError):
    def __init__(self, msg, file):
        self.msg = msg
        self.file = file

    def __str__(self):
        return 'File "{}"\n{}'.format(self.file, self.msg)

# TODO: understand errors. to continue the list of errors. Issue #44