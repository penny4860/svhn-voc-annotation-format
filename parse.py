# -*- coding: utf-8 -*-
import json
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


from xml.etree.ElementTree import Element, SubElement, tostring, dump
json_data=open("imgs//annotation.json").read()
anns = json.loads(json_data)
for ann in anns:
    boxes = []
    root = Element('annotation')
    fname = SubElement(root, "filename")
    fname.text = ann["filename"]
    
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
    dump(root)
    print("======================================================")


        

