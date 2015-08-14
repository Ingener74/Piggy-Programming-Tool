#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from string import maketrans

from PySide.QtCore import (QSettings)
from PySide.QtGui import (QApplication, QFileDialog, QSystemTrayIcon, QMenu, QIcon, QPixmap)


COMPANY = 'Shnaider Pavel'
APPNAME = 'Piggy'


# noinspection PyPep8Naming
class LastDirectory(object):
    LAST_DIRECTORY = 'last_directory'

    @staticmethod
    def get():
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        return settings.value(LastDirectory.LAST_DIRECTORY, os.path.dirname(os.path.realpath(sys.argv[0])))

    @staticmethod
    def set(file):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        settings.setValue(LastDirectory.LAST_DIRECTORY, file)


# noinspection PyPep8Naming
def getFileNew():
    fileNames, fileFilters = QFileDialog.getOpenFileNames(dir=LastDirectory.get())
    if len(fileNames) != 0:
        LastDirectory.set(fileNames[0])

    full_ = ''
    for i in fileNames:
        full_ += i if fileNames[-1] == i else i + ';'

    global app
    clipboard = app.clipboard()
    clipboard.setText(str(full_).translate(maketrans('\\', '/')))


# noinspection PyPep8Naming
def getDirectoryNew():
    directory_ = QFileDialog.getExistingDirectory()
    global app
    clipboard = app.clipboard()
    clipboard.setText(str(directory_).translate(maketrans('\\', '/')))


# noinspection PyPep8Naming
def getToolFileName(tool, comment):
    pyside_rcc, _ = QFileDialog.getOpenFileName(caption=u"Открыть {0}.exe, {1}".format(tool, comment), filter='*.exe')
    return pyside_rcc


# noinspection PyPep8Naming
def getTool(tool, comment):
    settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
    tool_file_name = settings.value(tool, None) # , getToolFileName(tool, comment)
    if tool_file_name is None:
        tool_file_name = getToolFileName(tool, comment)
    settings.setValue(tool, tool_file_name)
    return tool_file_name


# noinspection PyPep8Naming
def processQrcFile():
    qrcFileName, _ = QFileDialog.getOpenFileName(caption=u'Выбери qrc файл', filter='*.qrc', dir=LastDirectory.get())
    LastDirectory.set(qrcFileName)

    pyFileName, _ = QFileDialog.getSaveFileName(
        caption=u'Сохрани py файл, незабудь "resources.qrc" -> "resources_rc.qrc"', filter='*.py',
        dir=LastDirectory.get())
    LastDirectory.set(pyFileName)

    startinfo = subprocess.STARTUPINFO()
    startinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.call(
        [getTool('pyside_rcc', u'он где то тут: Python27/Lib/site-packages/PySide/pyside-rcc.exe'), qrcFileName, '-o',
         pyFileName], startupinfo=startinfo)


# noinspection PyPep8Naming
def processUiFile():
    qrcFileName, _ = QFileDialog.getOpenFileName(caption=u'Выбери UI файл', filter='*.ui', dir=LastDirectory.get())
    LastDirectory.set(qrcFileName)

    pyFileName, _ = QFileDialog.getSaveFileName(caption=u'Сохрани py файл', filter='*.py', dir=LastDirectory.get())
    LastDirectory.set(pyFileName)

    startinfo = subprocess.STARTUPINFO()
    startinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(
        [getTool('pyside_uic', u'он где то тут: Python27/Scripts/pyside-uic.exe'), qrcFileName, '-o', pyFileName],
        startupinfo=startinfo)


def main():
    global app
    app = QApplication(sys.argv)

    settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
    print settings.fileName()

    tray_menu = QMenu()

    tray_menu.addAction(QIcon(QPixmap('data/file.png')), u'Получить пути файлов', getFileNew)
    tray_menu.addAction(QIcon(QPixmap('data/directory.png')), u'Получить путь директории', getDirectoryNew)
    tray_menu.addSeparator()
    tray_menu.addAction(QIcon(QPixmap('data/qrc.png')), u'Преобразовать .qrc в .py', processQrcFile)
    tray_menu.addAction(QIcon(QPixmap('data/ui.png')), u'Преозразовать .ui в .py', processUiFile)
    tray_menu.addSeparator()
    tray_menu.addAction(QIcon(QPixmap('data/close.png')), u'Выход', app.quit)

    tray = QSystemTrayIcon()
    tray.setIcon(QIcon(QPixmap('data//piggy.png')))
    tray.setContextMenu(tray_menu)
    tray.show()

    return app.exec_()


if __name__ == '__main__':
    main()
