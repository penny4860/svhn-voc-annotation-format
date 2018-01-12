# -*- coding: utf-8 -*-

import numpy as np

"""
    Box
        Bounding Box 1개를 저장하는 자료구조.
    Boxes
        Box instance 여러개를 저장하는 자료구조.
"""


class Box:
    """Bounding Box 1개를 저장하는 자료구조.

    # Attributes
        _x1 : int
        _x2 : int
        _y1 : int
        _y2 : int
        _label : int
    """

    _keys = ["x1", "x2", "y1", "y2", "cx", "cy", "w", "h"]

    def __init__(self,
                 x1=None,
                 x2=None,
                 y1=None,
                 y2=None,
                 cx=None,
                 cy=None,
                 w=None,
                 h=None,
                 label=None):

        x_params = self._get_valid_axis_params(x1, x2, cx, w)
        y_params = self._get_valid_axis_params(y1, y2, cy, h)

        if len(x_params) != 2 or len(y_params) != 2:
            raise ValueError
        else:
            self._x1, self._x2 = self._set_point(x_params)
            self._y1, self._y2 = self._set_point(y_params)

        if label:
            self._label = label
        else:
            self._label = None

    def get_pos(self, keys):
        """Get bounding box in the specific order

        # Arguments
            keys : list of str
                allowed str : "x1", "x2", "y1" ,"y2", "cx", "cy", "w", "h"

        # Return
            box : array, shape of (n_keys, )
        """
        box = []
        for key in keys:
            value = self._get_coordinate(key)
            box.append(value)
        return np.array(box)

    def get_label(self):
        return self._label

    def _set_point(self, params):
        """ Set 2-points from arbitrary params

        # Arguments
            params : dict
                "p1", "p2", "center", "length"
        # Returns
            p1 : int
            p2 : int
        """
        if "p1" in params.keys() and "p2" in params.keys():
            p1 = params["p1"]
            p2 = params["p2"]
        elif "p1" in params.keys() and "center" in params.keys():
            p1 = params["p1"]
            p2 = params["p1"] + 2*(params["center"] - params["p1"])
        elif "p1" in params.keys() and "length" in params.keys():
            p1 = params["p1"]
            p2 = params["p1"] + params["length"]
        elif "p2" in params.keys() and "center" in params.keys():
            p1 = params["p2"] - 2*(params["p2"] - params["center"])
            p2 = params["p2"]
        elif "p2" in params.keys() and "length" in params.keys():
            p1 = params["p2"] - params["length"]
            p2 = params["p2"]
        elif "center" in params.keys() and "length" in params.keys():
            p1 = int(params["center"] - params["length"]/2)
            p2 = int(params["center"] + params["length"]/2)
        return p1, p2

    def _get_valid_axis_params(self, p1, p2, center, length):
        """
        # Arguments
            p1 : int
            p2 : int
            center : int
            length : int

        # Returns
            valid_params : dict
        """
        # 1. x1, x2, cx, w 중 2개가 set
        params = {"p1": p1, "p2": p2, "center": center, "length": length}
        valid_params = {}
        # for param, value in enumerate(params):
        for param, value in zip(params.keys(), params.values()):
            if value is not None:
                valid_params[param] = value
        return valid_params

    def _get_coordinate(self, key):
        if key == "x1":
            value = self._x1
        elif key == "x2":
            value = self._x2
        elif key == "y1":
            value = self._y1
        elif key == "y2":
            value = self._y2
        elif key == "w":
            value = self._x2 - self._x1
        elif key == "h":
            value = self._y2 - self._y1
        elif key == "cx":
            value = (self._x2 + self._x1) / 2
        elif key == "cy":
            value = (self._y2 + self._y1) / 2
        return float(value)
