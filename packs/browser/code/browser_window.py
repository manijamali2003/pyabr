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

import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
from libabr import Res, Files, Control

res = Res()
files = Files()
control = Control()

class Window(QGraphicsScene):

    def __init__(self, view):
        super(Window, self).__init__(view)

        _layout = QVBoxLayout(view)

        self.view = view
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.currentChanged.connect(self.currentTabChanged)
        self.tabs.tabCloseRequested.connect(self.closeCurrentTab)

        self.history = []  # list of strings, string = "title;URL" needed for writing history in a file
        self.historyForEachTab = {}  # key = tabIndex, value = tabIndexHistory - needed for back and forward methods
        self.addNewTab()

        button = QPushButton(QIcon(res.get('@icon/plus')), '')
        button.clicked.connect(self.addNewTab)
        self.tabs.setCornerWidget(button, Qt.TopLeftCorner)

        self.setBackgroundBrush(QBrush(QColor(230, 230, 230)))

        _layout.addWidget(self.tabs)


        self.lines = files.readall('history.txt')

    def addNewTab(self):

        qurl = QUrl(control.read_record('default-site','/etc/webconfig'))

        web = QWebView()
        web.load(QUrl(control.read_record('default','/etc/webconfig')))

        i = self.tabs.addTab(web, control.read_record('default-name','/etc/webconfig'))

        self.tabs.setCurrentIndex(i)

        web.urlChanged.connect(lambda qurl, web=web: self.update_urlbar(qurl, web))
        web.loadFinished.connect(lambda _, i=i, web=web: self.tabs.setTabText(i, web.title()))
        web.loadFinished.connect(lambda _, qurl=qurl, web=web: self.addToHistory(web.title(), web.url().toString()))

        self.historyForEachTab[i] = self.tabs.currentWidget().page().history()

    def addToHistory(self, title, link):

        if (len(self.history) == 0):
            self.history.append(''.join((title, ';', link)))
            return

        if (self.history[-1] != ''.join((title, ';', link))):
            self.history.append(''.join((title, ';', link)))

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        self.parent().parent().addressBar.setText(q.toString())

    def currentTabChanged(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.updateTitle(self.tabs.currentWidget())

    def updateTitle(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().title()
        self.view.parent().setWindowTitle(title)

    def closeCurrentTab(self, i):

        print(i)
        if self.tabs.count() < 2:
            return

        for j in range(i, self.tabs.count() - 1):
            self.historyForEachTab[j] = self.historyForEachTab[j + 1]

        for j in range(i, self.tabs.count()):
            self.tabs.widget(j).loadFinished.disconnect()
            self.tabs.widget(j).loadFinished.connect(
                lambda _, i=j - 1, web=self.tabs.widget(j): self.tabs.setTabText(i, web.title()))
            self.tabs.widget(j).loadFinished.connect(
                lambda _, web=self.tabs.widget(j): self.addToHistory(web.title(), web.url().toString()))

        self.tabs.removeTab(i)

    # History Button
    def historyButtonPush(self):
        self.popUp = QWidget()

        self.popUp.setWindowTitle(res.get('@string/hist'))
        self.popUp.setMinimumSize(400, 400)

        layout = QVBoxLayout()

        self.list = QListWidget()

        for line in self.lines:
            list = line.split(';')
            url = QUrl(list[1])
            self.list.addItem(QListWidgetItem(list[0].strip() + '  -  ' + list[1].strip()))

        for line in self.history:
            list = line.split(';')
            url = QUrl(list[1])
            self.list.addItem(QListWidgetItem(list[0].strip() + '  -  ' + list[1].strip()))

        button = QPushButton(res.get('@string/delh'))
        button.clicked.connect(self.deleteAllHistory)

        layout = QVBoxLayout()
        layout.addWidget(self.list)
        layout.addWidget(button)
        self.popUp.setLayout(layout)

        self.list.itemActivated.connect(self.doubleClickHistory)
        self.list.itemClicked.connect(self.leftClickOnHistoryListElement)

        self.popUp.show()

    def doubleClickHistory(self, item):
        list = item.text().split('  -  ')
        self.tabs.currentWidget().load(QUrl(list[1]))

        self.popUp.close()

    def leftClickOnHistoryListElement(self, item):

        self.popUp.setContextMenuPolicy(Qt.CustomContextMenu)

        self.historyRightClickMenu = QMenu()

        self.item = item

        menuItem = self.historyRightClickMenu.addAction(res.get('@string/open'))
        menuItem.triggered.connect(self.openHistory)

        menuItem = self.historyRightClickMenu.addAction(res.get('@string/openn'))
        menuItem.triggered.connect(self.openHistoryInNewTab)

        menuItem = self.historyRightClickMenu.addAction(res.get('@string/bookp'))
        menuItem.triggered.connect(self.addBookmarkFromHistory)

        self.popUp.customContextMenuRequested.connect(self.showHistoryRightClickMenu)

    def deleteAllHistory(self):
        self.history = []
        self.lines = []

        files.create('history.txt')

        self.popUp.close()

    def showHistoryRightClickMenu(self, QPos):
        parentPosition = self.popUp.mapToGlobal(QPoint(0, 0))
        menuPosition = parentPosition + QPos
        self.historyRightClickMenu.move(menuPosition)
        self.historyRightClickMenu.show()

    def openHistory(self):
        list = self.item.text().split('  -  ')
        self.tabs.currentWidget().load(QUrl(list[1]))

        print(list[1])

        self.popUp.close()

    def openHistoryInNewTab(self):
        list = self.item.text().split('  -  ')
        q = QUrl(list[1])

        web = QWebView()
        web.load(q)
        web.setMinimumHeight(qApp.primaryScreen().size().height() - 160)

        i = self.tabs.addTab(web, control.read_record('default-name','/etc/webconfig'))

        self.tabs.setCurrentIndex(i)

        web.urlChanged.connect(lambda qurl, web=web: self.update_urlbar(qurl, web))
        web.loadFinished.connect(lambda _, i=i, web=web: self.tabs.setTabText(i, web.title()))
        web.loadFinished.connect(lambda _, web=web: self.addToHistory(web.title(), web.url().toString()))

        self.historyForEachTab[i] = self.tabs.currentWidget().page().history()

        self.popUp.close()

    def addBookmarkFromHistory(self):
        list = self.item.text().split('  -  ')
        print(list[0])
        self.popUp = QDialog()
        layout = QVBoxLayout()

        button = QPushButton(res.get('@string/dn'))
        self.add = QLineEdit()
        self.add.setPlaceholderText(res.get('@string/name'))
        self.inCategory = QLineEdit()
        self.inCategory.setPlaceholderText(res.get('@string/folder'))

        layout.addWidget(self.inCategory)
        layout.addWidget(self.add)
        layout.addWidget(button)

        self.popUp.setLayout(layout)

        button.clicked.connect(lambda _, title=list[0], url=list[1]: self.saveBookmark(title, url))

        self.popUp.setWindowTitle(res.get('@string/booked'))
        self.popUp.setMaximumSize(300, 200)

        self.popUp.show()

    #############################################

    # Bookmark Button

    def bookmarksButtonPush(self):
        self.popUp = QWidget()

        self.popUp.setWindowTitle(res.get('@string/bookm'))
        self.popUp.setMinimumSize(400, 400)

        self.list = QListWidget()

        file = open(files.input('bookmarks.json'), 'r')

        categories = json.load(file)

        for category in categories:
            self.list.addItem(QListWidgetItem('- - - - - ' + category['name'] + f' {res.get("@string/folder")} - - - - -'))
            for (name, link) in category['elements'].items():
                self.list.addItem(QListWidgetItem(name.strip()))

        file.close()

        layout = QVBoxLayout()
        layout.addWidget(self.list)

        self.popUp.setLayout(layout)

        self.list.itemClicked.connect(self.leftClickOnBookmarkListElement)

        self.list.itemActivated.connect(self.doubleClickBookmark)

        self.popUp.show()

    def doubleClickBookmark(self, item):
        file = open(files.input('bookmarks.json'), 'r')

        categories = json.load(file)

        for category in categories:
            if (item.text().strip() in category['elements']):
                q = QUrl(category['elements'][item.text().strip()].strip())
                if (q.scheme() == ""):
                    q.setScheme("http")
                self.tabs.currentWidget().load(q)
                self.popUp.close()

        file.close()

    def leftClickOnBookmarkListElement(self, item):

        self.popUp.setContextMenuPolicy(Qt.CustomContextMenu)

        self.bookmarkRightClickMenu = QMenu()

        self.item = item
        menuItem = self.bookmarkRightClickMenu.addAction(res.get('@string/open'))
        menuItem.triggered.connect(self.openBookmark)

        menuItem = self.bookmarkRightClickMenu.addAction(res.get('@string/openn'))
        menuItem.triggered.connect(self.openBookmarkInNewTab)

        menuItem = self.bookmarkRightClickMenu.addAction(res.get('@string/delb'))
        menuItem.triggered.connect(self.deleteBookmark)

        self.popUp.customContextMenuRequested.connect(self.showBookmarkRightClickMenu)

    def showBookmarkRightClickMenu(self, QPos):
        parentPosition = self.popUp.mapToGlobal(QPoint(0, 0))
        menuPosition = parentPosition + QPos
        self.bookmarkRightClickMenu.move(menuPosition)
        self.bookmarkRightClickMenu.show()

    def openBookmarkInNewTab(self):

        file = open(files.input('bookmarks.json'), 'r')

        global q
        q = ''
        categories = json.load(file)

        for category in categories:
            if (self.item.text().strip() in category['elements']):
                q = QUrl(category['elements'][self.item.text().strip()].strip())
                if (q.scheme() == ""):
                    q.setScheme("http")
                    self.popUp.close()

        file.close()

        if (q == ''):
            return

        web = QWebView()
        web.load(q)
        web.setMinimumHeight(qApp.primaryScreen().size().height() - 160)

        i = self.tabs.addTab(web, control.read_record('default-name','/etc/webconfig'))

        self.tabs.setCurrentIndex(i)

        web.urlChanged.connect(lambda qurl, web=web: self.update_urlbar(qurl, web))
        web.loadFinished.connect(lambda _, i=i, web=web: self.tabs.setTabText(i, web.title()))

        self.historyForEachTab[i] = self.tabs.currentWidget().page().history()

    def openBookmark(self):
        file = open(files.input('bookmarks.json'), 'r')

        categories = json.load(file)

        for category in categories:
            if (self.item.text().strip() in category['elements']):
                q = QUrl(category['elements'][self.item.text().strip()].strip())
                if (q.scheme() == ""):
                    q.setScheme("http")
                self.tabs.currentWidget().load(q)
                self.popUp.close()

        file.close()

    def deleteBookmark(self):
        file = open(files.input('bookmarks.json'), 'r')

        categories = json.load(file)

        file.close()
        file = open(files.input('bookmarks.json'), 'w+')

        delete = 0
        element = ''

        for category in categories:
            if (self.item.text() in category['elements']):
                category['elements'].pop(self.item.text())
                self.item.setHidden(True)
                if (not category['elements']):
                    delete = 1
                    element = category

        if (delete == 1):
            categories.pop(categories.index(element))

        json.dump(categories, file)
        file.close()

    #################################################

    # AddBookmark Button

    def addBookmarkPush(self):
        self.popUp = QDialog()
        layout = QVBoxLayout()

        button = QPushButton(res.get('@string/done'))
        self.add = QLineEdit()
        self.add.setPlaceholderText(res.get('@string/name'))
        self.inCategory = QLineEdit()
        self.inCategory.setPlaceholderText(res.get('@string/folder'))

        layout.addWidget(self.inCategory)
        layout.addWidget(self.add)
        layout.addWidget(button)

        self.popUp.setLayout(layout)

        button.clicked.connect(self.saveBookmark)

        self.popUp.setWindowTitle(res.get('@string/booked'))
        self.popUp.setMaximumSize(300, 200)

        self.popUp.show()

    def saveBookmark(self, title=None, url=None):

        if (url is None):
            qtitle = self.add.text().strip()
            qurl = self.tabs.currentWidget().url().toString().strip()
        else:
            qtitle = title
            qurl = url

        file = open(files.input('bookmarks.json'), 'r')

        categories = json.load(file)

        file.close()

        if (self.add.text().strip() == '' or self.inCategory.text().strip() == ''):
            return

        for category in categories:
            if (self.add.text() in category['elements']):
                return

        file = open(files.input('bookmarks.json'), 'w+')

        s = 0
        for category in categories:
            if (category['name'].strip() == self.inCategory.text().strip()):
                s = 1
                category['elements'][qtitle] = qurl

        if (s == 0):
            categories.append({'name': self.inCategory.text().strip(), 'elements': {qtitle: qurl}})

        json.dump(categories, file)

        self.popUp.close()
        file.close()

    ###########################################

    def forwardButtonPush(self):
        self.historyForEachTab[self.tabs.currentIndex()].forward()

    def backButtonPush(self):
        self.historyForEachTab[self.tabs.currentIndex()].back()

    def refreshButtonPush(self):
        self.tabs.currentWidget().reload()

    def homeButtonPush(self):
        self.tabs.currentWidget().load(QUrl(control.read_record('default','/etc/webconfig')))

    def goButtonPush(self, address):
        tmp = address

        if (tmp == ''):
            return

        q = QUrl(tmp)
        if (q.scheme() == ""):
            q.setScheme("http")

        if (tmp.find('.') != -1 and tmp.find(' ') == -1):
            self.tabs.currentWidget().load(q)

        else:
            l = tmp.split()
            link = f'{control.read_record("default","/etc/webconfig")}/search?q=' + l[0]
            for i in range(1, len(l)):
                link += '+' + l[i]
            self.tabs.currentWidget().load(QUrl(link))

