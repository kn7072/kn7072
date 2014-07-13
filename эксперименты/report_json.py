# -*- coding: utf-8 -*-
import shutil, os, codecs, re

class ReportJeson:

    path_result = ' '
    def x (self):
        path_json = r"d:\src\sbis3-genie\ws\ws\lib\Control"
        path_control_tests = r"d:\src\sbis3-genie\test\integration\test_elements_input_flags.py"
        q = os.walk(path_json)
        contdir_result = []
        all_files = list()
        for top, dirs, files in os.walk(path_json):
            if not bool(dirs): continue
            for nm in files:
                if '.json' in nm and 'ws.controls' not in nm:
                    name_component = nm[:-5]
                    all_files.append([name_component, os.path.join(top, nm)])

        for name, path in all_files:
            if name == 'Button':
               line = codecs.open(path, encoding='utf-8', mode='r').readline()
               test = codecs.open(path_control_tests, encoding='utf-8', mode='r').readline()
               re.compile()
            continue
            print(i, w)
        path = os.getcwd()
        pass



if __name__ == "__main__":
    c = ReportJeson()
    c.x()