# -*- coding: utf-8 -*-

import json
import numpy as np
from viewer.info.box.box import Box


class AnnotationLoader:
    """ *.json format 의 annotation file 을 load 하는 책임. """
    def __init__(self, filename):
        self._annotations = json.loads(open(filename).read())

    def get_list_of_boxes(self):
        """Annotation list 에 정의되어있는 boxes, labels 를 (N, D, 5) 로 정리해서 반환하는 함수.

        # Returns
            list_of_boxes : list of ndarray
                
        """
        list_of_boxes = []
        for ann_for_one_img in self._annotations:
            boxes = [box for box in self._generate_box(ann_for_one_img["boxes"])]
            boxes = np.array(boxes)
            list_of_boxes.append(boxes)
        return list_of_boxes
    
    def get_list_of_labels(self):
        list_labels = []
        for ann_for_one_img in self._annotations:
            labels = [label for label in self._generate_label(ann_for_one_img["boxes"])]
            list_labels.append(labels)
        return list_labels
        
    def _generate_box(self, annotation_boxes):
        for annotation in annotation_boxes:
            maps = _interpret_ann(annotation)
            box = Box(**maps)
            yield box.get_pos(["x1", "y1", "x2", "y2"])

    def _generate_label(self, annotation_boxes):
        for annotation in annotation_boxes:
            maps = _interpret_ann(annotation)
            box = Box(**maps)
            yield box.get_label()


def _interpret_ann(box_dict):
    maps = {"y1": box_dict["top"],
            "x1": box_dict["left"],
            "w": box_dict["width"],
            "h": box_dict["height"],
            "label": str(int(box_dict["label"]))}
    return maps

if __name__ == "__main__":
    loader = AnnotationLoader("annotation.json")
    list_boxes = loader.get_list_of_boxes()
    list_labels = loader.get_list_of_labels()
    print(list_boxes)
    print(list_labels)

    
