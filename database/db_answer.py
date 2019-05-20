from enum import IntEnum


class DBAnswer:
    def __init__(self, ok, error, info):
        self.ok = ok
        self.error = error
        self.info = info

    def __str__(self):
        if self.ok:
            return 'OK. {}'.format(self.info)
        else:
            return 'ERROR. {} (CODE: {})'.format(self.info, self.error)


class DBError(IntEnum):
    AlwaysOk = 0
    IncorrectUsername = 10
    IncorrectPassword = 11
    IncorrectAvatar = 12
    IncorrectUser = 20
    RoomAlreadyExist = 30
    RoomNotExist = 31
    IncorrectRoomName = 32
    LabyrinthAlreadyExist = 40
    LabyrinthNotExist = 41


OK = DBError.AlwaysOk
