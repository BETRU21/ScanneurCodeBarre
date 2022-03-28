from PyQt5.QtWidgets import QAbstractButton, QSizePolicy
from PyQt5.Qt import QPainter, QSize

class QIconButton(QAbstractButton):
    def __init__(self, image=None, imageSelected=None, parent=None):
        super(QIconButton, self).__init__(parent)
        self.image = image
        if imageSelected is None:
            self.imageSelected = image
        else:
            self.imageSelected = imageSelected
        self.pressed.connect(self.update)
        self.pressed.connect(self.toggle)
        self.setInitialSizePolicy()
        self.status = False

    def setStatus(self, boolean):
        self.status = boolean
        self.update()

    def paintEvent(self, event):
        if self.underMouse():
            img = self.imageSelected
        elif self.isDown():
            img = self.image
        elif self.status:
            img = self.image
        else:
            img = self.image
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), img)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(100, 100)

    def setIcons(self, image, imageSelected=None):
        self.image = image
        if imageSelected is None:
            self.imageSelected = image
        else:
            self.imageSelected = imageSelected
        self.update()

    def setInitialSizePolicy(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

    def toggle(self):
        self.status = not self.status