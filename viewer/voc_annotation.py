# -*- coding: utf-8 -*-

import numpy as np
from xml.etree.ElementTree import parse


class PascalVocXmlParser(object):
    
    def __init__(self):
        pass
    
    def _root_tag(self, fname):
        tree = parse(fname)
        root = tree.getroot()
        return root
    
    def get_fname(self, annotation_file):
        root = self._root_tag(annotation_file)
        return root.find("filename").text

    def get_labels(self, annotation_file):
        root = self._root_tag(annotation_file)
        labels = []
        obj_tags = root.findall("object")
        for t in obj_tags:
            labels.append(t.find("name").text)
        return labels
    
    def get_boxes(self, annotation_file):
        root = self._root_tag(annotation_file)
        bbs = []
        obj_tags = root.findall("object")
        for t in obj_tags:
            box_tag = t.find("bndbox")
            x1 = box_tag.find("xmin").text
            y1 = box_tag.find("ymin").text
            x2 = box_tag.find("xmax").text
            y2 = box_tag.find("ymax").text
            box = np.array([int(x1), int(y1), int(x2), int(y2)])
            bbs.append(box)
        bbs = np.array(bbs)
        return bbs

from viewer.file_io import list_files
def get_voc_annotation(dirname="samples//voc//annotation"):
    parser = PascalVocXmlParser()
    files = list_files(dirname, "*.xml")

    list_boxes = []
    list_labels = []
    for fname in files:
        list_boxes.append(parser.get_boxes(fname))
        list_labels.append(parser.get_labels(fname))
    return list_boxes, list_labels

if __name__ == '__main__':
    list_boxes, list_labels = get_voc_annotation()
    print(list_labels)

