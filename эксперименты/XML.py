# -*- coding: utf-8 -*-
import xml.dom.minidom as dom_
from xml.etree.ElementTree import ElementTree
import os

doc_elm = dom_.parse(r'xml_doc.xml')

def fun(array):
        count = len(array)
        count_x = len(x)
        if count > count_x:
            for i in range(count-count_x):
                x.append([])
        for i in range(count):
            x[i].append(array[i])
        return array[0]

class XMLParser:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.temp = []
        if not os.path.isfile(path_to_file):
            raise Exception("Переданный путь %s не указывает на файл" % path_to_file)

    def rec(self, elm0, list_of_name, i=0, winelem=None):
        chaild_elm = list(elm0.getiterator('options'))
        for elm in chaild_elm:
            if elm.get('name') == list_of_name[i]:
                if i < len(list_of_name)-1:
                    k = i+1
                    self.rec(elm, list_of_name, i=k, winelem=None)
                else:
                    winelem = elm
                    self.temp.append(elm)
        return winelem

    def searchelements(self, search_path):
        tree = ElementTree(file=self.path_to_file)
        # формат path = 'dataSource > filterParams'
        list_of_name = search_path.split(' > ')
        # поиск осуществляется в tag options
        iterator_tag = list(tree.iter(tag='component'))
        for elm in iterator_tag:
            self.rec(elm, list_of_name, i=0)

        print()

pars = XMLParser(path_to_file=r'xml_doc.xml')
pars.searchelements('dataSource > filterParams')
print()
################################################################
list_elm_tag = doc_elm.getElementsByTagName('component')
for x in list_elm_tag:
    if x.getAttribute('data-component') == 'xxx3.CORE.TableView':
        print()

tree = ElementTree(file=r'xml_doc.xml')
list_tree = tree.findall('component')  #
list_tree2 = tree.getiterator('options')  # итератор в порядке следования
items_attribute = list_tree[0].findall('options')[0].items()

with open(r'xml_doc.xml', encoding='utf:8') as f:
    dom_.parse(r'xml_doc.xml')
    print()


