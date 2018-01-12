# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication
from viewer.app import ImageViewer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    sys.exit(app.exec_())
    