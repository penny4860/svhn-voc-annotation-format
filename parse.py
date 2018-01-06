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
    for b in ann['boxes']:
        x1 = b["left"]
        y1 = b["top"]
        x2 = b["left"] + b["width"]
        y2 = b["top"] + b["height"]
        minmax_box = (x1, y1, x2, y2)
        boxes.append(minmax_box)

    root = Element('annotation')
    child = SubElement(root, "filename")
    child.text = ann["filename"]
    indent(root)
    dump(root)
    break


        

