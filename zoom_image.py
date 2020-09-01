from PySide2 import QtWidgets, QtCore, QtGui
from photo_viewer import PhotoViewer


class ZoomImage(QtWidgets.QWidget):
    def __init__(self, label_gui):
        self.label_gui = label_gui
        super(ZoomImage, self).__init__()
        self.setGeometry(500, 300, 800, 600)
        self.viewer = PhotoViewer(self)
        self.x_new = 0
        self.y_new = 0
        # 'Load image' button
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)
        # Button to change from drag/pan to getting pixel info
        self.btnPixInfo = QtWidgets.QToolButton(self)
        self.btnPixInfo.setText('Enter pixel info mode')
        self.btnPixInfo.clicked.connect(self.pixInfo)
        self.editPixInfo = QtWidgets.QLineEdit(self)
        self.editPixInfo.setReadOnly(True)
        self.viewer.photoClicked.connect(self.photoClicked)
        self.image_path = None
        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)
        HBlayout.addWidget(self.btnPixInfo)
        HBlayout.addWidget(self.editPixInfo)
        VBlayout.addLayout(HBlayout)

    def setImagePath(self, path):
        self.image_path = path
        self.loadImage()

    def loadImage(self):
        self.viewer.setPhoto(QtGui.QPixmap(self.image_path))

    def pixInfo(self):
        self.viewer.toggleDragMode()

    def photoClicked(self, pos):
        if self.viewer.dragMode() == QtWidgets.QGraphicsView.NoDrag:
            self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))
            self.x_new = pos.x()
            self.y_new = pos.y()
            self.label_gui.set_x_y(self.x_new, self.y_new)

    def get_x_y(self):
        return self.x_new, self.y_new
