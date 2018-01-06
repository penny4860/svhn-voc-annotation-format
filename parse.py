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

from xml.etree.ElementTree import Element, SubElement, tostring, dump
json_data=open("imgs//annotation.json").read()
anns = json.loads(json_data)
for ann in anns:
    boxes = []
    root = Element('annotation')
    fname = SubElement(root, "filename")
    fname.text = ann["filename"]
    
    for b in ann['boxes']:
        x1 = str(int(b["left"]))
        y1 = str(int(b["top"]))
        x2 = str(int(b["left"] + b["width"]))
        y2 = str(int(b["top"] + b["height"]))
        label_str = str(int(b["label"]))

        obj = SubElement(root, "object")
        
        label = SubElement(obj, "name")
        label.text = label_str
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


        

