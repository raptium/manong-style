# -*- coding:utf-8 -*-
"""Formats for Pattern Serialization.

- Base64 Encoded 
- YAML/JSON
"""
import json

from manong.specs import Pattern, Element, Series


class JsonFormat:
    @staticmethod
    def parse(pattern):
        if isinstance(pattern, str):
            pattern = json.loads(pattern)
        v = JsonFormat.parse_series(pattern['vertical'])
        h = JsonFormat.parse_series(pattern.get('horizontal'))
        return Pattern(v, h, pattern.get('line_width', 2))

    @staticmethod
    def serialize(p):
        return {
            "vertical": JsonFormat.serialize_series(p.vertical),
            "horizontal": JsonFormat.serialize_series(p.horizontal),
            "line_width": p.line_width
        }

    @staticmethod
    def serialize_series(s):
        return list(map(JsonFormat.serialize_element, s.elements))

    @staticmethod
    def serialize_element(e):
        result = {}
        if e.element is not None:
            result["element "] = JsonFormat.serialize_element(e.element)
        else:
            result["color"] = '#%02x%02x%02x' % (e.color[0], e.color[1],
                                                 e.color[2])
        if e.repeat != 1:
            result["repeat"] = e.repeat
        return result

    @staticmethod
    def parse_series(s):
        if s is None:
            return
        elements = []
        for e in s:
            element = JsonFormat.parse_element(e)
            elements.append(element)
        return Series(elements)

    @staticmethod
    def parse_element(e):
        if 'element' in e:
            c = JsonFormat.parse_element(e['element'])
        else:
            c = e['color']
        repeat = e.get('repeat', 1)
        return Element(c, repeat)
