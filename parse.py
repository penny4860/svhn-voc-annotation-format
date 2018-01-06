# -*- coding: utf-8 -*-

from xml.etree.ElementTree import Element, SubElement, ElementTree, dump
import os
import json
import argparse

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
def get_box_text(box):
    x1 = str(int(box["left"]))
    y1 = str(int(box["top"]))
    x2 = str(int(box["left"] + box["width"]))
    y2 = str(int(box["top"] + box["height"]))
    return x1, y1, x2, y2

def get_label_text(box):
    label_str = str(int(box["label"]))
    return label_str

def get_size_text(img_folder, fname):
    import matplotlib.pyplot as plt
    img = plt.imread(os.path.join(img_folder, fname))
    h, w, _ = img.shape
    return str(w), str(h), str(3)

class VocAnnGenerator(object):
    def __init__(self, ann_file, img_folder):
        self._ann_file = ann_file
        self._img_folder = img_folder
    
    def run(self):
        json_data=open(self._ann_file).read()
        anns = json.loads(json_data)
        for ann in anns:
            boxes = []
            root = Element('annotation')
            fname = SubElement(root, "filename")
            fname.text = ann["filename"]
            
            w, h, depth = get_size_text(self._img_folder, ann["filename"])
            size_tag = SubElement(root, "size")
            w_tag = SubElement(size_tag, "width")
            h_tag = SubElement(size_tag, "height")
            depth_tag = SubElement(size_tag, "depth")
            w_tag.text = w
            h_tag.text = h
            depth_tag.text = depth
            
            for b in ann['boxes']:
                x1, y1, x2, y2 = get_box_text(b)
        
                obj = SubElement(root, "object")
                
                label = SubElement(obj, "name")
                label.text = get_label_text(b)
                bndbox = SubElement(obj, "bndbox")
        
                xmin = SubElement(bndbox, "xmin")
                ymin = SubElement(bndbox, "ymin")
                xmax = SubElement(bndbox, "xmax")
                ymax = SubElement(bndbox, "ymax")
                xmin.text = x1
                ymin.text = y1
                xmax.text = x2
                ymax.text = y2
                
            
            indent(root)
            xml_fname = os.path.splitext(ann["filename"])[0] + ".xml"
            ElementTree(root).write(xml_fname)

argparser = argparse.ArgumentParser(description='Train and validate YOLO_v2 model on any dataset')
argparser.add_argument('-f',
                       '--file',
                       default=os.path.join("json_format_annotation", "train.json"),
                       help='annotation file')

argparser.add_argument('-d',
                       '--directory',
                       default="train",
                       help='image direcotry path')

if __name__ == '__main__':
    args = argparser.parse_args()
    gen = VocAnnGenerator(args.file, args.directory)
    gen.run()
    


        

