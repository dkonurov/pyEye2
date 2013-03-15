#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# openfiledialog.py

import sys
import Queue
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from PIL import Image
from PIL import ImageOps
import shutil
import os

class MainWindows(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setWindowTitle('Eye')
		self.resize(500, 500)
		self.setWindowIcon(QtGui.QIcon('bullet.jpg'))
		QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))
		
		self.fileName = ""
		self.fileName2= ""
		self.image = QImage()
		self.label = QtGui.QLabel()
		self.label.setBackgroundRole(QtGui.QPalette.Base)
		self.label.setSizePolicy(QtGui.QSizePolicy.Ignored, 
			QtGui.QSizePolicy.Ignored)
		self.label.setScaledContents(True)
		self.pix = QPixmap()
		self.x1 = 0
		self.y1 = 0
		self.x2 = 0
		self.y2 = 0
		self.dx = 0
		self.dy = 0
		self.cordx1=0
		self.cordy1=0
		self.cordx2=0
		self.cordy2=0
		self.const = 0
		self.handled = True

		self.outfilename = ""

		self.scaleFactor = 1.0
		self.flag = False
		self.direct = ""



		self.ScrollArea = QtGui.QScrollArea()
		self.ScrollArea.setBackgroundRole(QtGui.QPalette.Dark)
		self.ScrollArea.setWidget(self.label)
		self.ScrollArea.eventFilter

		#Buttons
		self.resetSize = QtGui.QPushButton('resetSize', self)
		self.resetSize.setShortcut('Ctrl+F')
		self.resetSize.setGeometry(0, 0, 0, 0)
		self.connect(self.resetSize, QtCore.SIGNAL('clicked()'), self.ResetSize)
		self.resetSize.setEnabled(False)

		self.reset = QtGui.QPushButton('Reset', self)
		self.reset.setGeometry(0, 0, 0, 0)
		self.reset.setShortcut('Ctrl+Z')
		self.reset.setEnabled(False)
		self.connect(self.reset, QtCore.SIGNAL('clicked()'), self.Rerturn)

		#Menu

		self.open = QtGui.QAction(QtGui.QIcon('icons/open.png'), u'Открыть', self)
		self.open.setShortcut('Ctrl+O')
		self.open.setStatusTip(u'Открыть')
		self.connect(self.open, QtCore.SIGNAL('triggered()'), self.ShowDialog)

		self.zoomIn = QtGui.QAction(QtGui.QIcon('icons/zoomin.png'), u'Увеличить', self)
		self.zoomIn.setShortcut('+')
		self.zoomIn.setStatusTip('ZoomIn')
		self.zoomIn.setEnabled(False)
		self.connect(self.zoomIn, QtCore.SIGNAL('triggered()'), self.ZoomIn)

		self.zoomOut = QtGui.QAction(QtGui.QIcon('icons/zoomout.png'), u'Уменьшить', self)
		self.zoomOut.setShortcut('-')
		self.zoomOut.setStatusTip('ZoomOut')
		self.zoomOut.setEnabled(False)
		self.connect(self.zoomOut, QtCore.SIGNAL('triggered()'), self.ZoomOut)

		self.normalSize = QtGui.QAction(QtGui.QIcon('icons/normalsize.png'), u'Исходный размер', self)
		self.normalSize.setShortcut('Ctrl+0')
		self.normalSize.setStatusTip('Normal size')
		self.normalSize.setEnabled(False)
		self.connect(self.normalSize, QtCore.SIGNAL('triggered()'), self.normall)

		self.handle = QtGui.QAction(QtGui.QIcon('icons/handle.png'), u'Обработать', self)
		self.handle.setShortcut(Qt.Key_Return)
		self.handle.setStatusTip(u'Обработать')
		self.handle.setEnabled(False)
		self.connect(self.handle, QtCore.SIGNAL('triggered()'), self.Main)

		self.save = QtGui.QAction(QtGui.QIcon('icons/save.png'), u'Сохранить', self)
		self.save.setShortcut('Ctrl+S')
		self.save.setStatusTip(u'Сохранить')
		self.save.setEnabled(False)
		self.connect(self.save, QtCore.SIGNAL('triggered()'), self.Save)

		self.exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), u'Выход', self)
		self.exit.setShortcut('Ctrl+Q')
		self.exit.setStatusTip(u'Выход')
		self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

		self.help = QtGui.QAction(QtGui.QIcon('icons/help.gif'), u'Справка', self)
		self.help.setShortcut('F1')
		self.help.setStatusTip('Help')
		self.connect(self.help, QtCore.SIGNAL('triggered()'), self.helpchik)

		self.statusBar()
		menubar = self.menuBar()
		file = menubar.addMenu(u'&Файл')
		file.addAction(self.open)
		file.addAction(self.handle)
		file.addAction(self.save)
		file.addAction(self.exit)

		image1 = menubar.addMenu(u'&Изображение')
		image1.addAction(self.zoomIn)
		image1.addAction(self.zoomOut)
		image1.addAction(self.normalSize)

		help1 = menubar.addMenu(u'&Справка')
		help1.addAction(self.help)

		#Bar

		toolbar = self.addToolBar('Bar')
		toolbar.addAction(self.open)
		toolbar.addAction(self.handle)
		toolbar.addAction(self.save)
		toolbar.addAction(self.exit)

		self.setCentralWidget(self.ScrollArea)

	def clearImage(self):
		self.image.load(self.fileName)
		self.update()

	def EnterEvent(self,event):
		print "Enter!" 

	def mousePressEvent(self, event):
		if (event.buttons() & QtCore.Qt.RightButton):
			self.setCursor(QtCore.Qt.ClosedHandCursor)
			self.X =event.x()
			self.Y =event.y()
		if event.button() == QtCore.Qt.LeftButton & self.handled:
			self.cordx1 = int((event.x()-self.label.x())/self.scaleFactor)
			self.cordy1 = int((event.y()-self.label.y()-44)/self.scaleFactor)
			self.handle.setEnabled(False)
			self.flag = False
			self.x1 =event.x()-self.label.x()
			self.y1 =event.y()-self.label.y()

	def mouseMoveEvent(self, event):
		if (event.buttons() & QtCore.Qt.RightButton):
			vBar = self.ScrollArea.verticalScrollBar()
			hBar = self.ScrollArea.horizontalScrollBar()
			vBar.setValue(self.dy+(self.Y-event.y()))
			hBar.setValue(self.dx+(self.X-event.x()))
		if (event.buttons() & QtCore.Qt.LeftButton & self.handled):
			self.drawLineTo(event.x()-self.label.x(), event.y()-self.label.y())
			self.flag = True

	def mouseReleaseEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		if event.button() & QtCore.Qt.LeftButton & self.handled :
			self.drawLineTo(event.x()-self.label.x(), event.y()-self.label.y())
			self.cordx2 = int((event.x()-self.label.x())/self.scaleFactor)
			self.cordy2 = int((event.y()-self.label.y()-44)/self.scaleFactor)
			if (self.flag):
				self.handle.setEnabled(True)
		vBar = self.ScrollArea.verticalScrollBar()
		hBar = self.ScrollArea.horizontalScrollBar()
		self.dx = hBar.value()
		self.dy = vBar.value()

	def drawLineTo(self, x2, y2):
		self.clearImage()
		
		painter = QtGui.QPainter(self.image)
		painter.setPen(QtCore.Qt.green)
		painter.drawRect((self.x1-2)/self.scaleFactor, (self.y1-44)/self.scaleFactor, (x2 - self.x1)/self.scaleFactor, (y2 - self.y1)/self.scaleFactor)
		self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
		self.update()

	def ShowDialog(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self,u"Открыть файл",self.direct)
		if fileName != "":
			self.handled = True
			k=0
			for i in xrange(0,fileName.length()):
				if (fileName[i] == "/"):
					k=i

			self.direct = fileName[0:k+1]
			self.fileName= fileName
			self.image.load(self.fileName)
			self.pix.fromImage(self.image)
			self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
			self.label.adjustSize()
		
			self.fileName2=fileName
			self.fileName2 = unicode(self.fileName2).encode("UTF-8")

			self.save.setEnabled(True)
			self.zoomOut.setEnabled(True)
			self.zoomIn.setEnabled(True)
			self.reset.setEnabled(True)
			self.normalSize.setEnabled(True)
			self.resetSize.setEnabled(True)

	def Rerturn(self ):
		self.image.load(self.fileName)
		self.pix.fromImage(self.image)
		self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
		self.label.adjustSize()
		self.scaleFactor=1.0
		self.handled = True



	def ZoomIn(self):
		self.scaleImage(1.25)

	def ZoomOut(self):
		self.scaleImage(0.75)

	def normall(self):
		self.scaleFactor = 1.0
		self.label.resize(self.scaleFactor * self.label.pixmap().size())

	def ResetSize(self):
		while (self.label.height()>self.ScrollArea.height() or self.label.width()>self.ScrollArea.width()):
			self.scaleImage(0.95)

	def wheelEvent(self, wheelEvent):
		vscroll = self.ScrollArea.verticalScrollBar()
		if wheelEvent.modifiers() == QtCore.Qt.ControlModifier and wheelEvent.delta()>0:
			self.scaleImage(1.25)
		elif wheelEvent.modifiers() == QtCore.Qt.ControlModifier and wheelEvent.delta()<0:
			self.scaleImage(0.75)
		elif wheelEvent.delta()>0 or wheelEvent.delta()<0:
			wheelEvent.ignore()

	def scaleImage(self, factor):
		self.scaleFactor *= factor
		self.label.resize(self.scaleFactor * self.label.pixmap().size())

	def helpchik(self):
		QtGui.QMessageBox.information(self, "Help", u"\
			<p>Ctrl+O - открытие изображения</p>\
			<p>Enter - обработка изображения</p>\
			<p>Ctrl+Q - выход из программы</p>\
			     <p>+ , - , Ctrl+прокрутка колесика мыши - увеличение или уменьшение изображения</p>\
			                   <p>Ctrl+0 - нормальный(исходный) размер изображения</p>\
		<p>Ctrl+Z - отменить последнне действие</p>\
		<p>Ctrl+F - изображение под размер окна</p>\
		<p>Ctrl+S - сохранить изображение</p>\
		<p>ПКМ+перемещение мыши - перемещение изображения</p>\
		<p>F1 - справка</p>")
	
	def Save(self):
		outfilename = QtGui.QFileDialog.getSaveFileName(self.label, u"Сохранение файла", self.fileName[:-4]+"_changed" + ".JPG")
		self.image.save(outfilename)

	def closeEvent(self, event):
		if self.outfilename != "":
			os.remove(self.outfilename)

	def Main(self):
		self.handled = False
		name = str(self.fileName2)
		self.outfilename = name.decode("UTF-8")[:-4] + "_cache.png"
		image = Image.open(name.decode("utf-8"))

		x1 = min(self.cordx1,self.cordx2)
		y1 = min(self.cordy1,self.cordy2)
		x2 = max(self.cordx1,self.cordx2)
		y2 = max(self.cordy1,self.cordy2)

		box=(x1+1, y1+1, x2, y2)
		image = image.crop(box)

		w, h = image.size

		ylist = []
		for i in xrange(w):
			for j in xrange(h):
				color = image.getpixel((i,j))
				r = color[0]
				g = color[1]
				b = color[2]	
				s = r+g+b
				ylist.append(s)
			gg = range(h)
			gg.reverse()
			ylist.reverse()
			asd = []
			z=0
			del ylist[0]
			while ylist[z]<=ylist[z+1]:
				del ylist[z]
				asd.append(gg.pop(0))


			for q in asd:
				image.putpixel((i, q), (255, 255, 255))



		for i in xrange(w):
			for j in xrange(h):
				color = image.getpixel((i,j))
				r = color[0]
				g = color[1]
				b = color[2]
				c = 190
				if (r>c) and (g>c) and (b>c):
					image.putpixel((i, j), (255, 255, 255))	

		image.save(self.outfilename)
		self.image = QtGui.QImage(self.outfilename)
		self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
		self.label.adjustSize()
		os.remove(self.outfilename)



app = QtGui.QApplication(sys.argv)
okno = MainWindows()
okno.show()
app.installEventFilter(okno)
sys.exit(app.exec_())
