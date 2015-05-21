#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import subprocess

from string import maketrans

from PySide.QtGui import QApplication, QFileDialog, QSystemTrayIcon, QMenu, QIcon, QPixmap


class LastDirectory(object):
    LAST_DIRECTORY = 'last_directory'
    CONFIG_FILE    = 'config.json'
    
    @staticmethod
    def get():
        json_ = json.load(open(LastDirectory.CONFIG_FILE, mode='r+'))
    
        lastDir = json_[LastDirectory.LAST_DIRECTORY] if os.path.isdir(json_[LastDirectory.LAST_DIRECTORY]) else os.path.dirname(os.path.realpath(sys.argv[0]))
    
        if len(lastDir) == 0:
            raise SystemExit
    
        json_[LastDirectory.LAST_DIRECTORY] = lastDir
        with open(LastDirectory.CONFIG_FILE, 'w') as json_file:
            json.dump(json_, json_file, sort_keys=True, indent=4, separators=(',', ':'))
        
        return lastDir
    
    @staticmethod
    def set(file):
        json_ = json.load(open(LastDirectory.CONFIG_FILE, mode='r+'))
    
        lastDir = os.path.dirname(os.path.realpath(file))
    
        if len(lastDir) == 0:
            raise SystemExit
    
        json_[LastDirectory.LAST_DIRECTORY] = lastDir
        with open(LastDirectory.CONFIG_FILE, 'w') as json_file:
            json.dump(json_, json_file, sort_keys=True, indent=4, separators=(',', ':'))


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


def getDirectoryNew():
    directory_ = QFileDialog.getExistingDirectory()
    global app
    clipboard = app.clipboard()
    clipboard.setText(str(directory_).translate(maketrans('\\', '/')))


def getToolFileName(tool, comment):
    pyside_rcc, _ = QFileDialog.getOpenFileName(caption=u"Открыть {0}.exe, {1}".format(tool, comment), filter='*.exe')
    return pyside_rcc

def getTool(tool, comment):
    CONFIG_FILE = 'config.json'

    json_ = json.load(open(CONFIG_FILE, mode='r+'))

    toolFileName = json_[tool] if os.path.exists(json_[tool]) else getToolFileName(tool, comment)

    if len(toolFileName) == 0:
        raise SystemExit

    json_[tool] = toolFileName
    with open(CONFIG_FILE, 'w') as json_file:
        json.dump(json_, json_file, sort_keys=True, indent=4, separators=(',', ':'))
    
    return toolFileName

def processQrcFile():
    qrcFileName, _ = QFileDialog.getOpenFileName(caption=u'Выбери qrc файл', filter='*.qrc', dir=LastDirectory.get())
    LastDirectory.set(qrcFileName)
    
    pyFileName, _ = QFileDialog.getSaveFileName(caption=u'Сохрани py файл, незабудь "resources.qrc" -> "resources_rc.qrc"', filter='*.py', dir=LastDirectory.get())
    LastDirectory.set(pyFileName)
    
    subprocess.Popen([getTool('pyside_rcc', u'он где то тут: Python27/Lib/site-packages/PySide/pyside-rcc.exe'), qrcFileName, '-o', pyFileName])

def processUiFile():
    qrcFileName, _ = QFileDialog.getOpenFileName(caption=u'Выбери UI файл', filter='*.ui', dir=LastDirectory.get())
    LastDirectory.set(qrcFileName)
    
    pyFileName, _ = QFileDialog.getSaveFileName(caption=u'Сохрани py файл', filter='*.py', dir=LastDirectory.get())
    LastDirectory.set(pyFileName)
    
    subprocess.Popen([getTool('pyside_uic', u'он где то тут: Python27/Scripts/pyside-uic.exe'), qrcFileName, '-o', pyFileName])


def main():
    global app
    app = QApplication(sys.argv)

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

