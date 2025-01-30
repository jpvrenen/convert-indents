"""
blub
We like to fix indents from tab to space or vice versa
We can convert all files in given directory
We can convert a single given file

@author: Jeroen van Renen, jpvrenen@hotmail.com
"""
import os
import re
import sys
import argparse

def msg():
    """ usage """
    return ("{0}".format(os.path.basename(sys.argv[0])))+'''
        [-h, --help    show howto invoke and possible arguments]
        [-a, --action  specify action, t2s(tab 2 space) or s2t(space 2 tab)]
        [-s, --spaces  specify number of spaces per tab, default is 4]
        [-t, --tabs    specify tab per x number of spaces, default is 4 spaces per tab]
        [-p, --path    convert all files in given path location]
        [-f, --file    convert specific file]

        example:
        1) convert given file indents from tab to spaces, using 4 spaces (default) per tab
        convert_indents.py -a t2s -f fix_my_tab_indents.txt
        '''

#Arguments section
parser = argparse.ArgumentParser(description='Convert indents', usage=msg())
parser.add_argument('-a', '--action',
                    required=True,
                    help="specify action, t2s(tab 2 space) or s2t(space 2 tab)")
parser.add_argument('-s', '--spaces',
                    default=4,
                    help="specify number of spaces per tab, default is 4")
parser.add_argument('-t', '--tabs',
                    default=4,
                    help="specify tab per x number of spaces, default is 4 spaces per tab")
parser.add_argument('-p', '--path',
                    dest='path',
                    default=False,
                    help="convert all files in given path location")
parser.add_argument('-f', '--file',
                    dest='file',
                    default=False,
                    help="convert specific file")
args = parser.parse_args()

try:
    valid_action = ['t2s', 's2t']
    action = args.action
    if action not in valid_action:
        print("Valid actions are 't2s' or 's2t', current action '{0}' ignored".format(action))
        sys.exit()
except Exception as e:
    print(e)

try:
    path = args.path
    file = args.file
    if (not path) and (not file):
        print("Please use program with option 'path' or 'file'")
        sys.exit()
except Exception as e:
    print(e)

space_ratio = args.spaces
tab_ratio = args.tabs
files_affected = dict()


def tab_indent(_lines):
    """ if tab indent or empty line found return True """
    reg_tab_expr = r'^(\t+)(\S+.*)$'
    REG_TAB_match = re.compile(reg_tab_expr, re.M|re.I)
    reg_ws_expr = r'^(\t+)$'
    REG_WS_match = re.compile(reg_ws_expr, re.M|re.I)
    for line in _lines:
        match_line_tab = REG_TAB_match.match(line)
        match_line_ws = REG_WS_match.match(line)
        if match_line_ws or match_line_tab:
            return True
    return False

def space_indent(_lines):
    """ if space indent or empty line found return True """
    reg_space_expr = r'^( +)(\S+.*)$'
    REG_SPACE_match = re.compile(reg_space_expr, re.M|re.I)
    reg_ws_expr = r'^( +)$'
    REG_WS_match = re.compile(reg_ws_expr, re.M|re.I)
    for line in _lines:
        match_line_tab = REG_SPACE_match.match(line)
        match_line_ws = REG_WS_match.match(line)
        if match_line_ws or match_line_tab:
            return True
    return False

def find_files_affected(_path, _file, _action):
    """ find files that need a fix """
    result = dict()
    if _path:
        for filename in os.listdir(_path):
            tempfile = _path + filename
            with open(tempfile, 'r') as f:
                read_data = f.readlines()
            if (_action == 't2s') and tab_indent(read_data):
                result[tempfile] = '1'
            elif (_action == 's2t') and space_indent(read_data):
                result[tempfile] = '1'
    elif _file:
        with open(_file, 'r') as f:
            read_data = f.readlines()
        if (_action == 't2s') and tab_indent(read_data):
            result[_file] = '1'
        elif (_action == 's2t') and space_indent(read_data):
            result[_file] = '1'
    return result

def convert_tab_indent(_work_file, _org_file, _tab_ratio):
    """ if tab indent found convert to space """
    reg_tab_expr = r'^(\t+)(\S+.*)$'
    REG_TAB_match = re.compile(reg_tab_expr, re.M|re.I)
    reg_ws_expr = r'^(\t+)$'
    REG_WS_match = re.compile(reg_ws_expr, re.M|re.I)
    work_file = open(_work_file, 'w')
    for line in _org_file:
        match_line_tab = REG_TAB_match.match(line)
        match_line_ws = REG_WS_match.match(line)
        if match_line_ws:
            work_file.write("\n")
        elif match_line_tab:
            spaces = " "*(len(match_line_tab.group(1))*_tab_ratio)
            work_file.write(spaces + match_line_tab.group(2) + "\n")
        else:
            work_file.write(line)
    work_file.close()

def return_nr_tabs(_no_of_spaces, _space_ratio):
    if not _no_of_spaces%_space_ratio:
        result = int(_no_of_spaces/space_ratio)
        return result
    elif _no_of_spaces%_space_ratio:
        print("Irregular space found cannot divide, space ratio '-s, -> {0}' ".format(_space_ratio))
        return 0
    else:
        return 0

def convert_space_indent(_work_file, _org_file, _space_ratio):
    """ if space indent found convert to tab """
    reg_space_expr = r'^( +)(\S+.*)$'
    REG_SPACE_match = re.compile(reg_space_expr, re.M|re.I)
    reg_ws_expr = r'^( +)$'
    REG_WS_match = re.compile(reg_ws_expr, re.M|re.I)
    work_file = open(_work_file, 'w')
    for line in _org_file:
        match_line_space = REG_SPACE_match.match(line)
        match_line_ws = REG_WS_match.match(line)
        if match_line_ws:
            work_file.write("\n")
        elif match_line_space:
            tabs = "\t"*(return_nr_tabs(len(match_line_space.group(1)),_space_ratio))
            if tabs:
                work_file.write(tabs + match_line_space.group(2) + "\n")
            else:
                work_file.write("###correct_indent_manual###" + match_line_space.group(2) + "\n")
        else:
            work_file.write(line)
    work_file.close()

def modify_files_affected(_files, _action, _space_ratio, _tab_ratio):
    """ fix indents """
    for _file in _files:
        with open(_file, 'r') as f:
            read_file = f.readlines()

        if _action == 't2s':
            convert_tab_indent(_file, read_file, _tab_ratio)
        elif _action == 's2t':
            convert_space_indent(_file, read_file, _space_ratio)

if __name__ == '__main__':
    files_affected = find_files_affected(path, file, action)
    print('Files affected:', files_affected)
    modify_files_affected(files_affected, action, space_ratio, tab_ratio)
