import sys
from os.path import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from libabr import Res

res = Res()

class MainApp(QMainWindow):

    def __init__(self, args):
        super(MainApp, self).__init__()

        self.Backend = args[0]
        self.Env = args[1]
        self.Widget = args[2]
        self.AppName = args[3]
        self.External = args[4]

        # self.currentFile = '/'
        self.currentPlaylist = QMediaPlaylist()
        self.player = QMediaPlayer()
        self.userAction = -1  # 0- stopped, 1- playing 2-paused
        self.player.mediaStatusChanged.connect(self.qmp_mediaStatusChanged)
        self.player.stateChanged.connect(self.qmp_stateChanged)
        self.player.positionChanged.connect(self.qmp_positionChanged)
        self.player.volumeChanged.connect(self.qmp_volumeChanged)
        self.player.setVolume(60)
        # Add Status bar
        self.statusBar().showMessage('No Media :: %d' % self.player.volume())
        self.homeScreen()

    def homeScreen(self):
        # Set title of the MainWindow
        self.Widget.SetWindowTitle('SoundBox Audio Player')
        self.Widget.SetWindowIcon(QIcon(res.get('@logo/soundbox')))

        # Create Menubar
        self.createMenubar()

        # Create Toolbar
        self.createToolbar()

        # Add info screen
        # infoscreen = self.createInfoScreen()

        # Add Control Bar
        controlBar = self.addControls()

        # need to add both infoscreen and control bar to the central widget.
        centralWidget = QWidget()
        centralWidget.setLayout(controlBar)
        self.setCentralWidget(centralWidget)

        # Set Dimensions of the MainWindow
        self.Widget.Resize(self,400, 200)

        # show everything.
        self.show()

    def createMenubar(self):
        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        filemenu.addAction(self.fileOpen())
        filemenu.addAction(self.songInfo())
        filemenu.addAction(self.folderOpen())
        filemenu.addAction(self.exitAction())

    def createToolbar(self):
        pass

    def addControls(self):
        controlArea = QVBoxLayout()  # centralWidget
        seekSliderLayout = QHBoxLayout()
        controls = QHBoxLayout()
        playlistCtrlLayout = QHBoxLayout()

        # creating buttons
        playBtn = QPushButton('Play')  # play button
        pauseBtn = QPushButton('Pause')  # pause button
        stopBtn = QPushButton('Stop')  # stop button
        volumeDescBtn = QPushButton('V (-)')  # Decrease Volume
        volumeIncBtn = QPushButton('V (+)')  # Increase Volume

        # creating playlist controls
        prevBtn = QPushButton('Prev Song')
        nextBtn = QPushButton('Next Song')

        # creating seek slider
        seekSlider = QSlider()
        seekSlider.setMinimum(0)
        seekSlider.setMaximum(100)
        seekSlider.setOrientation(Qt.Horizontal)
        seekSlider.setTracking(False)
        seekSlider.sliderMoved.connect(self.seekPosition)
        # seekSlider.valueChanged.connect(self.seekPosition)

        seekSliderLabel1 = QLabel('0.00')
        seekSliderLabel2 = QLabel('0.00')
        seekSliderLayout.addWidget(seekSliderLabel1)
        seekSliderLayout.addWidget(seekSlider)
        seekSliderLayout.addWidget(seekSliderLabel2)

        # Add handler for each button. Not using the default slots.
        playBtn.clicked.connect(self.playHandler)
        pauseBtn.clicked.connect(self.pauseHandler)
        stopBtn.clicked.connect(self.stopHandler)
        volumeDescBtn.clicked.connect(self.decreaseVolume)
        volumeIncBtn.clicked.connect(self.increaseVolume)

        # Adding to the horizontal layout
        controls.addWidget(volumeDescBtn)
        controls.addWidget(playBtn)
        controls.addWidget(pauseBtn)
        controls.addWidget(stopBtn)
        controls.addWidget(volumeIncBtn)

        # playlist control button handlers
        prevBtn.clicked.connect(self.prevItemPlaylist)
        nextBtn.clicked.connect(self.nextItemPlaylist)
        playlistCtrlLayout.addWidget(prevBtn)
        playlistCtrlLayout.addWidget(nextBtn)

        # Adding to the vertical layout
        controlArea.addLayout(seekSliderLayout)
        controlArea.addLayout(controls)
        controlArea.addLayout(playlistCtrlLayout)
        return controlArea

    def playHandler(self):
        self.userAction = 1
        self.statusBar().showMessage('Playing at Volume %d' % self.player.volume())
        if self.player.state() == QMediaPlayer.StoppedState:
            if self.player.mediaStatus() == QMediaPlayer.NoMedia:
                # self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.currentFile)))
                print(self.currentPlaylist.mediaCount())
                if self.currentPlaylist.mediaCount() == 0:
                    self.openFile()
                if self.currentPlaylist.mediaCount() != 0:
                    self.player.setPlaylist(self.currentPlaylist)
            elif self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
                self.player.play()
            elif self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
                self.player.play()
        elif self.player.state() == QMediaPlayer.PlayingState:
            pass
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()

    def pauseHandler(self):
        self.userAction = 2
        self.statusBar().showMessage('Paused %s at position %s at Volume %d' % \
                                     (self.player.metaData(QMediaMetaData.Title), \
                                      self.centralWidget().layout().itemAt(0).layout().itemAt(0).widget().text(), \
                                      self.player.volume()))
        self.player.pause()

    def stopHandler(self):
        self.userAction = 0
        self.statusBar().showMessage('Stopped at Volume %d' % (self.player.volume()))
        if self.player.state() == QMediaPlayer.PlayingState:
            self.stopState = True
            self.player.stop()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.stop()
        elif self.player.state() == QMediaPlayer.StoppedState:
            pass

    def qmp_mediaStatusChanged(self):
        if self.player.mediaStatus() == QMediaPlayer.LoadedMedia and self.userAction == 1:
            durationT = self.player.duration()
            self.centralWidget().layout().itemAt(0).layout().itemAt(1).widget().setRange(0, durationT)
            self.centralWidget().layout().itemAt(0).layout().itemAt(2).widget().setText(
                '%d:%02d' % (int(durationT / 60000), int((durationT / 1000) % 60)))
            self.player.play()

    def qmp_stateChanged(self):
        if self.player.state() == QMediaPlayer.StoppedState:
            self.player.stop()

    def qmp_positionChanged(self, position, senderType=False):
        sliderLayout = self.centralWidget().layout().itemAt(0).layout()
        if senderType == False:
            sliderLayout.itemAt(1).widget().setValue(position)
        # update the text label
        sliderLayout.itemAt(0).widget().setText('%d:%02d' % (int(position / 60000), int((position / 1000) % 60)))

    def seekPosition(self, position):
        sender = self.sender()
        if isinstance(sender, QSlider):
            if self.player.isSeekable():
                self.player.setPosition(position)

    def qmp_volumeChanged(self):
        msg = self.statusBar().currentMessage()
        msg = msg[:-2] + str(self.player.volume())
        self.statusBar().showMessage(msg)

    def increaseVolume(self):
        vol = self.player.volume()
        vol = min(vol + 5, 100)
        self.player.setVolume(vol)

    def decreaseVolume(self):
        vol = self.player.volume()
        vol = max(vol - 5, 0)
        self.player.setVolume(vol)

    def fileOpen(self):
        fileAc = QAction('Open File', self)
        fileAc.setShortcut('Ctrl+O')
        fileAc.setStatusTip('Open File')
        fileAc.triggered.connect(self.openFile)
        return fileAc

    def openFile(self):
        fileChoosen = QFileDialog.getOpenFileUrl(self, 'Open Music File', expanduser('~'), 'Audio (*.mp3 *.ogg *.wav)',
                                                 '*.mp3 *.ogg *.wav')
        if fileChoosen != None:
            self.currentPlaylist.addMedia(QMediaContent(fileChoosen[0]))

    def folderOpen(self):
        folderAc = QAction('Open Folder', self)
        folderAc.setShortcut('Ctrl+D')
        folderAc.setStatusTip('Open Folder (Will add all the files in the folder) ')
        folderAc.triggered.connect(self.addFiles)
        return folderAc

    def addFiles(self):
        folderChoosen = QFileDialog.getExistingDirectory(self, 'Open Music Folder', expanduser('~'))
        if folderChoosen != None:
            it = QDirIterator(folderChoosen)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    print(it.filePath(), fInfo.suffix())
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav'):
                        print('added file ', fInfo.fileName())
                        self.currentPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
                it.next()

    def songInfo(self):
        infoAc = QAction('Info', self)
        infoAc.setShortcut('Ctrl+I')
        infoAc.setStatusTip('Displays Current Song Information')
        infoAc.triggered.connect(self.displaySongInfo)
        return infoAc

    def displaySongInfo(self):
        metaDataKeyList = self.player.availableMetaData()
        fullText = '<table class="tftable" border="0">'
        for key in metaDataKeyList:
            value = self.player.metaData(key)
            fullText = fullText + '<tr><td>' + key + '</td><td>' + str(value) + '</td></tr>'
        fullText = fullText + '</table>'
        infoBox = QMessageBox(self)
        infoBox.setWindowTitle('Detailed Song Information')
        infoBox.setTextFormat(Qt.RichText)
        infoBox.setText(fullText)
        infoBox.addButton('OK', QMessageBox.AcceptRole)
        infoBox.show()

    def prevItemPlaylist(self):
        self.player.playlist().previous()

    def nextItemPlaylist(self):
        self.player.playlist().next()

    def exitAction(self):
        exitAc = QAction('&Exit', self)
        exitAc.setShortcut('Ctrl+Q')
        exitAc.setStatusTip('Exit App')
        exitAc.triggered.connect(self.closeEvent)
        return exitAc

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure ?.', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            qApp.quit()
        else:
            try:
                event.ignore()
            except AttributeError:
                pass