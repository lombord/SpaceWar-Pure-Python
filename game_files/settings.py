
class Settings:

    def __init__(self, fWidth=12, fHeight=12, gameMode='easy'):
        self.fWidth = fWidth
        self.fHeight = fHeight
        self.gameMode = gameMode

    def toJS(self):
        return self.__dict__


if __name__ == '__main__':
    pass
