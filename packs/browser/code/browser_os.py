#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Mani Jamali. GNU General Public License v3.0
#
#  Official Website: 		http://pyabr.rf.gd
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Gap channel: 			@pyabr
#  Gap group:   			@pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

from libbrowser import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from libabr import Res, Files, Control

res = Res()
files = Files()
control = Control()

user = files.readall('/proc/info/su')

if user=='root':
    path = f'/root'
else:
    path = f'/desk/{user}'

if not files.isfile(f'{user}/bookmark.json'):
    files.copy('/usr/share/templates/bookmark.json',f'{user}/bookmark.json')

if not files.isfile(f'{user}/history.txt'):
    files.copy('/usr/share/templates/history.txt',f'{user}/history.txt')

class MainApp(QMainWindow):
    def __init__(self,ports, parent=None):
        super(MainApp, self).__init__(parent)  # super(subClass, instance).__init__(parent)

        self.setGeometry(10, 10, 1000, 800)  # setGeometry(topLeftX, topLeftY, width, height)

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.Widget.SetWindowTitle(res.get('@string/app_name'))
        self.Widget.SetWindowIcon(QIcon(res.get('@icon/logo')))

        self.addressBar = QLineEdit()
        self.addressBar.setPlaceholderText(res.get('@string/search'))

        self.createBrowser()  # Method that creates graphics view

        # ---------------------Toolbar buttons section-----------------------
        tb = self.addToolBar(res.get('@string/file'))
        tb.setMovable(False)
        self.backAction = QAction(QIcon(res.get('@icon/back')), res.get('@string/ba'), self)
        self.backAction.setShortcut('Ctrl+B')
        self.backAction.triggered.connect(self.browser.page.backButtonPush)

        self.forwardAction = QAction(QIcon(res.get('@icon/forward')), res.get('@string/fw'), self)
        self.forwardAction.setShortcut('Ctrl+F')
        self.forwardAction.triggered.connect(self.browser.page.forwardButtonPush)

        self.refreshAction = QAction(QIcon(res.get('@icon/refresh')), res.get('@string/rl'), self)
        self.refreshAction.setShortcut('Ctrl+R')
        self.refreshAction.triggered.connect(self.browser.page.refreshButtonPush)

        self.homeAction = QAction(QIcon(res.get('@icon/home')), res.get('@string/hm'), self)
        self.homeAction.setShortcut('Ctrl+H')
        self.homeAction.triggered.connect(self.browser.page.homeButtonPush)

        self.goAction = QAction(QIcon(res.get('@icon/search')), res.get('@string/go'), self)
        self.goAction.setShortcut(Qt.Key_Return)
        self.goAction.triggered.connect(lambda: self.browser.page.goButtonPush(self.addressBar.text()))

        self.bookmarkAction = QAction(QIcon(res.get('@icon/star')), res.get('@string/addb'), self)
        self.bookmarkAction.setShortcut('Ctrl+B')
        self.bookmarkAction.triggered.connect(self.browser.page.addBookmarkPush)

        self.historyAction = QAction(QIcon(res.get('@icon/history')), res.get('@string/hist'), self)
        self.historyAction.setShortcut('Ctrl+H')
        self.historyAction.triggered.connect(self.browser.page.historyButtonPush)

        self.bookmarksAction = QAction(QIcon(res.get('@icon/bookmarks')), res.get('@string/bookm'), self)
        self.bookmarksAction.setShortcut('Ctrl+V')
        self.bookmarksAction.triggered.connect(self.browser.page.bookmarksButtonPush)

        tb.addAction(self.backAction)
        tb.addAction(self.forwardAction)
        tb.addAction(self.refreshAction)
        tb.addAction(self.homeAction)
        tb.addWidget(self.addressBar)
        tb.addAction(self.goAction)
        tb.addAction(self.bookmarkAction)
        tb.addAction(self.historyAction)
        tb.addAction(self.bookmarksAction)

    def createBrowser(self):
        self.browser = Browser(self)
        self.setCentralWidget(self.browser)

    def closeEvent(self, event):

        file = open('history.txt', 'a+',
                    encoding='utf-8')  # a+ mode opens in read+write, appending to end of file and creating file if it doesn't exist

        for i in self.browser.page.history:
            file.write((i + '\n'))

        file.close()

        event.accept()