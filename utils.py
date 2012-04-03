#-*- coding: utf-8 -*-
"""
    Python bindings to worksnaps API
    Copyright (C) 2012  Crystalnix company

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = 'Kirill Yakovenko, kirill.yakovenko@gmail.com'
__ALL__ = ["convert_xml_to_dict", "convert_dict_to_xml"]

from collections import Container
from xml.etree import cElementTree as ET

def convert_xml_to_dict( file_like ):
    root = ET.parse( file_like ).getroot()
    return {root.tag: convert_xml_to_dict_recursively(root) }

def convert_xml_to_dict_recursively(xmlnode):
    nodes = {}

    for child in xmlnode:
        item = convert_xml_to_dict_recursively(child)
        if nodes.has_key(child.tag):
            # found duplicate tag, force a list
            if type(nodes[child.tag]) is type([]):
                # append to existing list
                nodes[child.tag].append(item)
            else:
                # convert to list
                nodes[child.tag] = [nodes[child.tag], item]
        else:
            nodes[child.tag] = item

    if not nodes:
        if xmlnode.text:
            nodes = xmlnode.text.strip()
        else:
            nodes = ''

    return nodes

def convert_dict_to_xml(root_tag, dictionary):
    root = ET.Element(root_tag)
    convert_dict_to_xml_recursively(root, dictionary)
    return ET.tostring(root)

def convert_dict_to_xml_recursively(root, data):
    for key, item in data.items():
        if isinstance(item, basestring):
            ET.SubElement(root, key).text = item
        elif isinstance(item, Container):
            for ch in item:
                convert_dict_to_xml( ET.SubElement(root, key), ch)
        else:
            ET.SubElement(root, key).text = item if item is not None else ''