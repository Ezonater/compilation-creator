# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Compilation++.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets

import download
import ffmpeg
from download import *
from config import *
import util
import os
import sys

config = Config()
print(config.options_dict)

thumbnail = None
playlist = None
title = ""
output_dir = ""
playlist_valid = None
compiling = False


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(941, 761)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.playlist_link = QtWidgets.QHBoxLayout()
        self.playlist_link.setObjectName("playlist_link")
        self.playlist_link_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playlist_link_label.sizePolicy().hasHeightForWidth())
        self.playlist_link_label.setSizePolicy(sizePolicy)
        self.playlist_link_label.setObjectName("playlist_link_label")
        self.playlist_link.addWidget(self.playlist_link_label)
        self.playlist_link_entry = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playlist_link_entry.sizePolicy().hasHeightForWidth())
        self.playlist_link_entry.setSizePolicy(sizePolicy)
        self.playlist_link_entry.setObjectName("playlist_link_entry")
        self.playlist_link.addWidget(self.playlist_link_entry)
        self.verticalLayout.addLayout(self.playlist_link)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.options = QtWidgets.QGridLayout()
        self.options.setObjectName("options")
        self.include_ambience = QtWidgets.QCheckBox(self.centralwidget)
        self.include_ambience.setObjectName("include_ambience")
        self.include_ambience.setChecked(config.options_dict['ambience'])
        self.options.addWidget(self.include_ambience, 3, 2, 1, 1)
        self.playlist_order = QtWidgets.QCheckBox(self.centralwidget)
        self.playlist_order.setObjectName("playlist_order")
        self.playlist_order.setChecked(config.options_dict['keep_order'])
        self.options.addWidget(self.playlist_order, 1, 0, 1, 1)
        self.set_output = QtWidgets.QPushButton(self.centralwidget)
        self.set_output.setObjectName("set_output")
        self.options.addWidget(self.set_output, 3, 1, 1, 1)
        self.title_container = QtWidgets.QHBoxLayout()
        self.title_container.setObjectName("title_container")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setObjectName("title_label")
        self.title_container.addWidget(self.title_label)
        self.title_entry = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_entry.sizePolicy().hasHeightForWidth())
        self.title_entry.setSizePolicy(sizePolicy)
        self.title_entry.setObjectName("title_entry")
        self.title_container.addWidget(self.title_entry)
        self.options.addLayout(self.title_container, 3, 0, 1, 1)
        self.generate_timestamps = QtWidgets.QCheckBox(self.centralwidget)
        self.generate_timestamps.setObjectName("generate_timestamps")
        self.generate_timestamps.setChecked(config.options_dict['generate_timestamps'])
        self.options.addWidget(self.generate_timestamps, 0, 2, 1, 1)
        self.normalize_audio = QtWidgets.QCheckBox(self.centralwidget)
        self.normalize_audio.setObjectName("normalize_audio")
        self.normalize_audio.setChecked(config.options_dict['normalize_audio'])
        self.options.addWidget(self.normalize_audio, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.video_bitrate_label = QtWidgets.QLabel(self.centralwidget)
        self.video_bitrate_label.setObjectName("video_bitrate_label")
        self.horizontalLayout_3.addWidget(self.video_bitrate_label)
        self.video_bitrate_entry = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_bitrate_entry.sizePolicy().hasHeightForWidth())
        self.video_bitrate_entry.setSizePolicy(sizePolicy)
        self.video_bitrate_entry.setObjectName("video_bitrate_entry")
        self.horizontalLayout_3.addWidget(self.video_bitrate_entry)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.options.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.audio_bitrate_label = QtWidgets.QLabel(self.centralwidget)
        self.audio_bitrate_label.setObjectName("audio_bitrate_label")
        self.horizontalLayout_4.addWidget(self.audio_bitrate_label)
        self.audio_bitrate_entry = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.audio_bitrate_entry.sizePolicy().hasHeightForWidth())
        self.audio_bitrate_entry.setSizePolicy(sizePolicy)
        self.audio_bitrate_entry.setObjectName("audio_bitrate_entry")
        self.horizontalLayout_4.addWidget(self.audio_bitrate_entry)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.options.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)
        self.stretch_image = QtWidgets.QCheckBox(self.centralwidget)
        self.stretch_image.setObjectName("stretch_image")
        self.options.addWidget(self.stretch_image, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.options)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.ambience_container_container = QtWidgets.QWidget()
        self.ambience_container = QtWidgets.QVBoxLayout()
        self.ambience_container.parent = self.ambience_container_container
        self.ambience_container.setObjectName("ambience_container")
        self.ambience_1 = QtWidgets.QHBoxLayout()
        self.ambience_1.setObjectName("ambience_1")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.ambience_1.addWidget(self.label_8)
        self.am_1_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.am_1_entry.setObjectName("am_1_entry")
        self.ambience_1.addWidget(self.am_1_entry)
        self.am_1_vol = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.am_1_vol.sizePolicy().hasHeightForWidth())
        self.am_1_vol.setSizePolicy(sizePolicy)
        self.am_1_vol.setOrientation(QtCore.Qt.Horizontal)
        self.am_1_vol.setObjectName("am_1_vol")
        self.ambience_1.addWidget(self.am_1_vol)
        self.ambience_container.addLayout(self.ambience_1)
        self.ambience_2 = QtWidgets.QHBoxLayout()
        self.ambience_2.setObjectName("ambience_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.ambience_2.addWidget(self.label_6)
        self.am_2_entry = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.am_2_entry.sizePolicy().hasHeightForWidth())
        self.am_2_entry.setSizePolicy(sizePolicy)
        self.am_2_entry.setObjectName("am_2_entry")
        self.ambience_2.addWidget(self.am_2_entry)
        self.am_2_vol = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.am_2_vol.sizePolicy().hasHeightForWidth())
        self.am_2_vol.setSizePolicy(sizePolicy)
        self.am_2_vol.setOrientation(QtCore.Qt.Horizontal)
        self.am_2_vol.setObjectName("am_2_vol")
        self.ambience_2.addWidget(self.am_2_vol)
        self.ambience_container.addLayout(self.ambience_2)
        self.ambience_3 = QtWidgets.QHBoxLayout()
        self.ambience_3.setObjectName("ambience_3")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.ambience_3.addWidget(self.label_7)
        self.am_3_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.am_3_entry.setObjectName("am_3_entry")
        self.ambience_3.addWidget(self.am_3_entry)
        self.am_3_vol = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.am_3_vol.sizePolicy().hasHeightForWidth())
        self.am_3_vol.setSizePolicy(sizePolicy)
        self.am_3_vol.setOrientation(QtCore.Qt.Horizontal)
        self.am_3_vol.setObjectName("am_3_vol")
        self.ambience_3.addWidget(self.am_3_vol)
        self.ambience_container.addLayout(self.ambience_3)
        self.verticalLayout.addLayout(self.ambience_container)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.thumbnail = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thumbnail.sizePolicy().hasHeightForWidth())
        self.thumbnail.setSizePolicy(sizePolicy)
        self.thumbnail.setMinimumSize(QtCore.QSize(320, 180))
        self.thumbnail.setObjectName("thumbnail")
        self.horizontalLayout_5.addWidget(self.thumbnail)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setObjectName("progress")
        self.verticalLayout.addWidget(self.progress)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setObjectName("start_button")
        self.verticalLayout.addWidget(self.start_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 941, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.open_ambience()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Compilation++"))
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        MainWindow.resize(0, 0)
        self.playlist_link_label.setText(_translate("MainWindow", "Playlist Link"))
        self.playlist_link_entry.textEdited.connect(
            lambda link=self.playlist_link_entry.text: self.update_playlist_link(link))
        self.title_entry.textEdited.connect(
            lambda text=self.title_entry.text: self.update_title(text))
        self.include_ambience.setText(_translate("MainWindow", "Include Ambience"))
        self.include_ambience.clicked.connect(self.open_ambience)
        self.playlist_order.setText(_translate("MainWindow", "Preserve Playlist Order"))
        self.playlist_order.setChecked(config.options_dict['keep_order'])
        self.playlist_order.clicked.connect(lambda: config.edit_config('keep_order', self.playlist_order.isChecked()))
        self.generate_timestamps.setText(_translate("MainWindow", "Generate Timestamps"))
        self.generate_timestamps.clicked.connect(
            lambda: config.edit_config('generate_timestamps', self.generate_timestamps.isChecked()))
        self.normalize_audio.setText(_translate("MainWindow", "Normalize Audio"))
        self.normalize_audio.clicked.connect(
            lambda: config.edit_config('normalize_audio', self.normalize_audio.isChecked()))
        self.video_bitrate_label.setText(_translate("MainWindow", "Video Bitrate"))
        self.video_bitrate_entry.setText(str(config.options_dict['video_bitrate']))
        self.video_bitrate_entry.textEdited.connect(
            lambda: config.edit_config('video_bitrate', self.video_bitrate_entry.text()))
        self.video_bitrate_entry.setValidator(QtGui.QIntValidator())
        self.label_4.setText(_translate("MainWindow", "kBps"))
        self.audio_bitrate_label.setText(_translate("MainWindow", "Audio Bitrate"))
        self.audio_bitrate_entry.setText(str(config.options_dict['audio_bitrate']))
        self.audio_bitrate_entry.setValidator(QtGui.QIntValidator())
        self.label_5.setText(_translate("MainWindow", "kBps"))
        self.label_8.setText(_translate("MainWindow", "Ambience #1"))
        self.label_6.setText(_translate("MainWindow", "Ambience #2"))
        self.label_7.setText(_translate("MainWindow", "Ambience #3"))
        self.thumbnail.setText(_translate("MainWindow", "Browse for thumbnail"))
        self.thumbnail.clicked.connect(self.browseFiles)
        self.thumbnail.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.set_output.clicked.connect(self.browseDirs)
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.set_output.setText(_translate("MainWindow", "Output Location..."))
        self.title_label.setText(_translate("MainWindow", "Title"))
        self.stretch_image.setText(_translate("MainWindow", "Stretch Image"))
        self.stretch_image.setChecked(config.options_dict['stretch_image'])
        self.stretch_image.clicked.connect(lambda: config.edit_config('stretch_image', self.stretch_image.isChecked()))
        self.am_1_vol.setValue(50)
        self.am_2_vol.setValue(50)
        self.am_3_vol.setValue(50)
        self.progress.setProperty("value", None)
        self.progress.setAlignment(QtCore.Qt.AlignCenter)
        self.progress.setFormat("")
        self.start_button.clicked.connect(lambda: self.start_download())
        self.start_button.setEnabled(False)

    def browseFiles(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Choose a thumbnail',
                                                         config.options_dict['last_thumb_dir'],
                                                         "Image files (*.jpg *.png)")
        global thumbnail
        thumbnail = filename[0]
        self.thumbnail.setStyleSheet("border-image : url(" + thumbnail + ");")
        if thumbnail != "":
            self.thumbnail.setText("")
            config.edit_config('last_thumb_dir', os.path.dirname(thumbnail))
        else:
            self.thumbnail.setText("Browse for a thumbnail")
        self.validate_start()
        print(thumbnail)

    def browseDirs(self):
        filedir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Output location')
        global output_dir
        output_dir = filedir
        print(output_dir)

    def update_playlist_link(self, link):
        global playlist
        playlist = link
        print(playlist)
        self.valid_link()

    def update_title(self, text):
        global title
        print(util.valid_filename(text))
        title = util.valid_filename(text)

    def open_ambience(self):
        ambience_container = [self.am_1_entry, self.am_1_vol, self.am_2_vol, self.am_2_entry, self.am_3_entry,
                              self.am_3_vol, self.label_6, self.label_7, self.label_8, self.line_3]
        if self.include_ambience.isChecked():
            for ambience in ambience_container:
                ambience.show()
        else:
            for ambience in ambience_container:
                ambience.hide()
        config.edit_config('ambience', self.include_ambience.isChecked())

    def valid_link(self):
        global playlist_valid
        playlist_valid = util.valid_link(playlist)
        print(playlist_valid)
        self.validate_start()

    def validate_start(self):
        print(thumbnail)
        if playlist_valid and thumbnail != "" and thumbnail is not None and not compiling:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def start_download(self):
        self.threads = []
        attr = {'playlist':playlist,'thumbnail':thumbnail,'config':config, 'title':title}
        amb = [{'link': self.am_1_entry.text(), 'vol':self.am_1_vol.value()},{'link': self.am_2_entry.text(), 'vol': self.am_2_vol.value()},{'link': self.am_3_entry.text(), 'vol': self.am_3_vol.value()}]
        downloader = DownloadThread(attr, amb)
        downloader.progress_update.connect(self.progress_update)
        downloader.start_button.connect(self.start_button_update)
        self.threads.append(downloader)
        downloader.start()
    
    def progress_update(self, data):
        if data[0] == 'increment':
            self.progress.setValue(data[1])
        if data[0] == 'format':
            self.progress.setFormat(data[1])
        if data[0] == 'maximum':
            self.progress.setMaximum(data[1])
    
    def start_button_update(self, data):
        self.start_button.setEnabled(data)

class DownloadThread(QtCore.QThread):

    progress_update = QtCore.pyqtSignal(object)
    start_button = QtCore.pyqtSignal(object)

    def __init__(self, attr, amb):
        QtCore.QThread.__init__(self)
        self.attr = attr
        self.amb = amb

    def run(self):
        global compiling
        compiling = True
        print("compiling started!")
        print(self.attr, self.amb)
        self.start_button.emit(False)
        util.clean_up()
        download.playlist_download(self, self.attr['playlist'], self.attr['config'].options_dict['audio_bitrate'])
        if self.attr['config'].options_dict['ambience']:
            download.ambience_download(self, self.amb, self.attr['config'].options_dict['audio_bitrate'])
        tracklist_length = util.generate_tracklist(self.attr['config'])
        if self.attr['config'].options_dict['stretch_image']:
            self.attr['thumbnail'] = util.stretch_image(self.attr['thumbnail'])
        title = self.attr['title']
        if title == "":
            title = self.attr['playlist'][self.attr['playlist'].index("=")+1:]
        ffmpeg.compile(self, title, self.attr['thumbnail'], int(self.attr['config'].options_dict['audio_bitrate'])*1000, int(self.attr['config'].options_dict['video_bitrate'])*1000, self.attr['config'].options_dict['normalize_audio'], self.attr['config'].options_dict['ambience'], tracklist_length)
        self.progress_update.emit(['format', ""])
        self.progress_update.emit(['increment', 0])
        util.clean_up()
        compiling = False
        self.start_button.emit(True)
        print("compiling finished!")

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())