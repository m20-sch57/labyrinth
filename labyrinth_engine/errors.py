class LabyrinthError(Exception):
    pass


class LabyrinthLoadError(LabyrinthError):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self) -> str:
        return 'File "{}"\n{}'.format(self.file, self.msg)

# TODO: understand errors. to continue the list of errors. Issue #44
