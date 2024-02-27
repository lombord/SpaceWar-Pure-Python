from sys import exit
from time import sleep
from weakref import ref
from re import fullmatch as fmatch

from .field import Field
from .player import Player, PlayerBase, PlayerData
from .bots import *
from .settings import Settings


class Game:
    # menu options
    _mainMenu = ('startGame', 'setSettings', 'about', '_signIn', 'exitGame')
    _settingsMenu = ('changeMode', 'setFieldSize',
                     'setPlayerName', 'resetScore')
    _gameModes = {'easy': EasyBot, 'medium': MediumBot, 'hard': HardBot,
                  'veryHard': VeryHardBot, 'unreal': UnrealBot}

    def __init__(self) -> None:
        self.drawInfo('Welcome to Space Battle Game' + ' '*41)
        self.players = PlayerData()
        self.bots = BotData()
        self._signIn()
        self.drawMenu()

    # menu methods
    def drawMenu(self):
        """Game menu loop"""
        while True:
            self.drawInfo(
                f'Space Battle by Lombord{" "*self.mWidth}',
                'Main Menu',
                '1.Start Game',
                '2.Settings',
                '3.About',
                '4.Change Profile',
                '5.Exit')
            getattr(self, self._mainMenu[int(
                self.gInput('=> ', r'[1-5]')) - 1])()

    def setSettings(self):
        """Settings menu loop"""
        while True:
            self.drawInfo("Settings",
                          '1.Change Game Mode',
                          '2.Change Field Size',
                          '3.Change Name',
                          '4.Reset Score',
                          '5.Back to Menu')
            ch = int(self.gInput('=> ', r'[1-5]')) - 1
            if ch == 4:
                break
            getattr(self, self._settingsMenu[ch])()
            sleep(2)
    # end

    # setUp methods
    def _signIn(self):
        self.drawInfo('Enter Your Name')
        name = self.gInput(
            '=> ',
            r'(?a)[\w]+',
            "Name can contain only English letters, numbers and '_'")
        if name in self.players:
            self.player: Player = self.players[name]
            self.drawInfo(f'{name} Welcome Back!')
        else:
            self.player: Player = Player(name)
            self.players.savePlayer(self.player)
            self.drawInfo(
                f'{name} seems you are new to this game. We wish you luck!')
        sleep(2)

    def __setBot(self):
        """Changes bot Mode"""
        gM = self.settings.gameMode
        gM = f'{gM[0].upper()}{gM[1:]}Bot'
        try:
            self.bot: PlayerBase = self.bots[gM]
        except Exception:
            self.bot: PlayerBase = self._gameModes[self.settings.gameMode]()
            self.bots.savePlayer(self.bot)

    def __setRenderSettings(self):
        self.mWidth = (self.player.settings.fWidth+1)*4
        self.gap = self.mWidth - int(self.mWidth/2.3)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        self._player = player
        self.settings: Settings = self.player.settings

    @property
    def settings(self) -> Settings:
        return self._settings()

    @settings.setter
    def settings(self, settings):
        self._settings = ref(settings)
        self.__setRenderSettings()
        self.__setBot()

    def changeMode(self):
        """Changes game Mode"""
        self.drawInfo('Choose game mode',
                      '1.Easy mode',
                      '2.Medium mode',
                      '3.Hard mode',
                      '4.Very Hard mode',
                      '5.Unreal mode')
        self.settings.gameMode = tuple(self._gameModes.keys())[int(
            self.gInput('=> ', r'[1-5]')) - 1]
        self.__setBot()
        self.drawInfo('Game Mode has been changed!')

    def setFieldSize(self):
        """Changes field size"""
        self.drawInfo('Enter Field width and height')
        self.settings.fWidth, self.settings.fHeight = map(
            int, self.gInput('=> ',
                             r'\s*((?:[1][0-6]|[5-9])\s+(?:[1][0-6]|[5-9]))\s*',
                             'Incorrect Input! pattern should be [w h] '
                             'and sizes should be in range (5, 16)',
                             1).split())
        self.__setRenderSettings()
        self.drawInfo('Field size has been changed!')

    def setPlayerName(self):
        """Changes player name"""
        self.drawInfo('Enter your new Name')
        self.player.name = self.gInput(
            '=> ',
            r'(?a)[\w]+',
            "Name can contain only English letters, numbers and '_'")
        self.drawInfo('Your name has been changed!')

    def resetScore(self):
        self.player.wins = self.player.losses = 0
        self.drawInfo('Scores have been reseted!')

    def about(self):

        pass

    def exitGame(self):
        self.drawInfo('All changes have been saved!')
        exit(0)
    # end

    # GamePlay methods
    def startGame(self):
        self.__setUpGame()

        self.renderFields()
        while self.field1 and self.field2:
            isHit = self.attacking()
            self.showState(isHit)
            isHit or self.__swapPlayers()
        self.drawInfo(
            f'{self.attacking.name} win the game!!!')
        self.__updateScores()
        sleep(3)

    def __setUpGame(self):
        self.field1: Field = Field(
            self.settings.fWidth, self.settings.fHeight, False)
        self.field2: Field = Field(
            self.settings.fWidth, self.settings.fHeight, self.player.name != 'LombordTest')
        self.bot.eField = self.field1
        self.player.eField = self.field2
        self.attacking = self.player
        self.defending = self.bot

    def __swapPlayers(self):
        self.attacking, self.defending = self.defending, self.attacking

    def showState(self, isHit):
        self.renderFields()
        self.drawInfo(
            f"{self.attacking.name} {'hit' if isHit else 'miss'}!")
        if isHit and not isinstance(self.attacking, EasyBot):
            return
        sleep(2)

    def __updateScores(self):
        self.attacking.updateScores(True)
        self.defending.updateScores(False)
    # end

    # render & input methods
    def drawInfo(self, *infos: str, align='^'):
        """Draw box in console with info"""
        mWidth = self.mWidth if hasattr(self, 'mWidth') else 41
        gap = self.gap if hasattr(self, 'gap') else 41

        print()
        print('', '-'*(mWidth + 4), sep=' '*gap)
        for row in infos:
            while len(row) > mWidth:
                i = row.rfind(' ', None, mWidth) + \
                    1 or mWidth
                substr = row[:i].rstrip()
                print(
                    '', f"| {substr:{align}{mWidth}} |", sep=' '*gap)
                row = row[i:]
            print('', f"| {row:{align}{mWidth}} |", sep=' '*gap)
            print('', '-'*(mWidth + 4), sep=' '*gap)

    def gInput(self, prompt, regex, errorMsg='Incorrect input!', group=0):
        gap = self.gap if hasattr(self, 'gap') else 41
        # gap=
        prompt = f"{prompt:>{gap + len(prompt)}}"
        res = fmatch(regex, input(prompt))
        while not res:
            self.drawInfo(errorMsg)
            sleep(1)
            res = fmatch(regex, input(prompt))
        return res[group]

    def showPlayerStats(self):
        pass

    def renderFields(self):
        Field.renderParallel(self.field1, self.field2)
    # end


if __name__ == '__main__':
    pass
