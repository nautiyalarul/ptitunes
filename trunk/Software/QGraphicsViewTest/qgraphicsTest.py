#!/usr/bin/env python
import sys
from PyQt4 import QtGui,QtCore

app = QtGui.QApplication(sys.argv)

timer = QtCore.QTimer()

qscene = QtGui.QGraphicsScene()
qpoly = QtGui.QPolygonF()
qpt=[QtCore.QPointF(1.0,2.0), QtCore.QPointF(20,0), QtCore.QPointF(20,20), QtCore.QPointF(0,20),QtCore.QPointF(0,0)] 
for pt in qpt:
	qpoly.append(pt)
qscene.addPolygon(qpoly)
unpressed= QtGui.QPixmap("../images/sensorUnpressed.png")
pressed= QtGui.QPixmap("../images/sensorPressed.png")
qgpmapitem = QtGui.QGraphicsPixmapItem(unpressed)
qscene.addItem(qgpmapitem)

qview = QtGui.QGraphicsView(qscene)

#widget = QtGui.QWidget()
qview.resize(271, 231)
qview.setWindowTitle('simple')
qview.show()
timer.start(500)

count = 0
def changePic():
	global count
	count += 1
	qgpmapitem.setPixmap(pressed if count%2 else unpressed)	

QtCore.QObject.connect(timer,QtCore.SIGNAL("timeout()"),changePic)

sys.exit(app.exec_())

#todo : create a class = 1 sensor pad with changing states (ie != callbacks ?)
#todo : position things nicely on GraphicsVIews
