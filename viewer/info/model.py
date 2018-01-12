# -*- coding: utf-8 -*-

import cv2
from viewer.info._annotation import AnnotationLoader


class Model(object):
    """
    # Attributes
        image_files : list of strings

    """
    def __init__(self, viewer):
        self._viewer = viewer
        self._image_files = []
        self._first_display_index = 0

        self._list_true_boxes = None
        self._list_predict_boxes = None
        self._true_labels = None
        self._predict_labels = None
        self.ann_dir_truth = None
        self.ann_dir_predict = None

    def changed(self,
                image_files=None,
                index_change=None,
                ann_dir_truth=None,
                ann_dir_predict=None):
        if image_files:
            self._image_files = image_files
        if index_change:
            self._update_index(index_change)
        if ann_dir_truth:
            self._list_true_boxes, self._true_labels = self._update_annotation(ann_dir_truth)
            self.ann_dir_truth = ann_dir_truth
        if ann_dir_predict:
            self._list_predict_boxes, self._predict_labels = self._update_annotation(ann_dir_predict)
            self.ann_dir_predict = ann_dir_predict

        self.notify_viewer()

    def notify_viewer(self):
        self._viewer.update()

    def get_image(self, index, plot_true_box, plot_predict_box):
        """
        # Arguments
            index : int
            plot_true_box : bool
            plot_predict_box : bool
        
        # Returns
            image : array, shape of (n_rows, n_cols, n_ch)
            filename : str
        """
        if index + self._first_display_index < len(self._image_files):
            filename = self._image_files[index + self._first_display_index]

            image = cv2.imread(filename)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if plot_true_box and self._list_true_boxes:
                boxes = self._list_true_boxes[index + self._first_display_index]
                labels = self._true_labels[index + self._first_display_index]
                self._draw_box(image, boxes, labels, (255, 0, 0))
            if plot_predict_box and self._list_predict_boxes:
                boxes = self._list_predict_boxes[index + self._first_display_index]
                labels = self._predict_labels[index + self._first_display_index]
                self._draw_box(image, boxes, labels, (0, 0, 255))
            return image, filename
        else:
            return None, None

    def _update_annotation(self, ann_file):
        """
        ann_file : annotation directory
        """
        from viewer.voc_annotation import get_voc_annotation
        dirname = ann_file
        list_boxes, list_labels = get_voc_annotation(dirname)
        return list_boxes, list_labels

    def _update_index(self, amount):
        self._first_display_index += amount

        if self._first_display_index < 0:
            self._first_display_index = len(self._image_files) - abs(amount)
        elif self._first_display_index >= len(self._image_files):
            self._first_display_index = 0

    def _draw_box(self, image, boxes, labels, color):
        """image 에 bounding boxes 를 그리는 함수.

        # Arguments
            image : array, shape of (n_rows, n_cols, n_ch)
            boxes : Boxes instance
            color : tuple, (Red, Green, Blue)
        """
        for box, label in zip(boxes, labels):
            x1, y1, x2, y2 = box.astype(int)
            h, w, _ = image.shape
            length = min(h, w)
            thickness = max(int(length / 100), 1)
            # cv2.putText(image, label, (x1, int((y1+y2)/3)), cv2.FONT_HERSHEY_SIMPLEX, thickness, color=255, thickness=thickness)
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

