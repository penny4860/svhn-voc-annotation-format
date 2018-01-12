# -*- coding: utf-8 -*-

# external modules
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

# internal modules
from viewer.info.model import Model
from viewer.file_io import list_files

UI_FILENAME = os.path.join(os.path.dirname(__file__),
                           'ui',
                           'main.ui')

class ImageViewer(QMainWindow):
    def __init__(self, ui_filename=UI_FILENAME):
        super(ImageViewer, self).__init__()
        uic.loadUi(ui_filename, self)
        self.model = Model(self)

        self.show()
        self.init_ui()
        self.setup_signal_slots()

    def init_ui(self):
        # 1. Create FigureCanvas instance
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # 2. Create toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        self.display_layout.addWidget(self.toolbar)
        self.display_layout.addWidget(self.canvas)

    def setup_signal_slots(self):
        self.actionLoad_images.triggered.connect(self._open_img_dir_dialog)
        self.sp_n_rows.valueChanged.connect(self._disply_option_changed)
        self.sp_n_cols.valueChanged.connect(self._disply_option_changed)
        self.btn_next.clicked.connect(lambda : self._update_index(self.sp_n_rows.value()*self.sp_n_cols.value()))
        self.btn_back.clicked.connect(lambda : self._update_index(-self.sp_n_rows.value()*self.sp_n_cols.value()))
        self.tb_truth_ann.clicked.connect(lambda : self._open_ann_dir_dialog("truth"))
        self.tb_predict_ann.clicked.connect(lambda : self._open_ann_dir_dialog("predict"))
        self.cb_plot_truth_box.stateChanged.connect(self._disply_option_changed)
        self.cb_plot_predict_box.stateChanged.connect(self._disply_option_changed)

    def _disply_option_changed(self):
        self.update()

    def _update_index(self, amount):
        self.model.changed(index_change=amount)

    def _open_img_dir_dialog(self):
        dirname = QFileDialog.getExistingDirectory(self, "Select Image Directory")
        files = list_files(dirname, "*.png") + list_files(dirname, "*.jpg")
        if files:
            self.model.changed(image_files=files)
        else:
            pass

    def _open_ann_dir_dialog(self, ann_kinds):
        dirname = QFileDialog.getExistingDirectory(self, 'Select Annotation Directory')
        
        if ann_kinds == "truth":
            self.model.changed(ann_dir_truth=dirname)
        elif ann_kinds == "predict":
            self.model.changed(ann_dir_predict=dirname)

    def update(self):
        self.figure.clear()
        n_rows = self.sp_n_rows.value()
        n_cols = self.sp_n_cols.value()

        for i in range(n_rows * n_cols):
            image, filename = self.model.get_image(i,
                                                   self._is_cb_checked(self.cb_plot_truth_box),
                                                   self._is_cb_checked(self.cb_plot_predict_box))
            if filename:
                ax = self.figure.add_subplot(n_rows, n_cols, i+1)
                ax.imshow(image)
                ax.set_title(os.path.basename(filename))
        # refresh canvas
        self.canvas.draw()

        self.te_truth_ann.setText(self.model.ann_dir_truth)
        self.te_predict_ann.setText(self.model.ann_dir_predict)

    def _is_cb_checked(self, cb):
        is_checked = True if cb.checkState() > 0 else False
        return is_checked


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    sys.exit(app.exec_())
