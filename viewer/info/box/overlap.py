# -*- coding: utf-8 -*-

import numpy as np

class Overlap(object):
    """ bounding boxes 간에 overlap region 을 연산하는 책임.

    # Arguments
        boxes : Boxes instance
        true_boxes : Boxes instance
    """

    def __init__(self, boxes, true_boxes):
        self.boxes = boxes
        self.true_boxes = true_boxes

    def calc_ious_per_truth(self):
        return self._calc()

    def calc_maximun_ious(self):
        ious_for_each_gt = self._calc()
        ious = np.max(ious_for_each_gt, axis=0)
        return ious

    def _calc(self):
        ious_for_each_gt = []

        np_boxes = self.true_boxes.get_pos(["y1", "y2", "x1", "x2"])

        y1_gts = np_boxes[:, 0]
        y2_gts = np_boxes[:, 1]
        x1_gts = np_boxes[:, 2]
        x2_gts = np_boxes[:, 3]

        for y1_gt, y2_gt, x1_gt, x2_gt in zip(y1_gts, y2_gts, x1_gts, x2_gts):
            np_boxes = self.boxes.get_pos(["y1", "y2", "x1", "x2"])

            y1 = np_boxes[:, 0]
            y2 = np_boxes[:, 1]
            x1 = np_boxes[:, 2]
            x2 = np_boxes[:, 3]

            xx1 = np.maximum(x1, x1_gt)
            yy1 = np.maximum(y1, y1_gt)
            xx2 = np.minimum(x2, x2_gt)
            yy2 = np.minimum(y2, y2_gt)

            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)

            intersections = w*h
            As = (x2 - x1 + 1) * (y2 - y1 + 1)
            B = (x2_gt - x1_gt + 1) * (y2_gt - y1_gt + 1)

            ious = intersections.astype(float) / (As + B -intersections)
            ious_for_each_gt.append(ious)

        # (n_truth, n_boxes)
        ious_for_each_gt = np.array(ious_for_each_gt)
        return ious_for_each_gt

