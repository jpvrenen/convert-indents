"""
We like to fix indents from tab to space or vice versa
We can convert all files in given directory
We can convert only given file

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
        [-t, --tabs    specify number of tabs per space, default is 1]
        [-p, --path    convert all files in given path location]
        [-f, --file    convert specific file]
        [-e, --ext     convert file with specific extension]
        [-w, --wldcd   use with care, convert file(s) using wildcard]

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
                    default=1,
                    help="specify number of tabs per space, default is 1")
parser.add_argument('-p', '--path',
                    dest='path',
                    default=False,
                    help="convert all files in given path location")
parser.add_argument('-f', '--file',
                    dest='file',
                    default=False,
                    help="convert specific file")
parser.add_argument('-e', '--extn',
                    dest='ext',
                    default=False,
                    help="convert file with specific extension")
parser.add_argument('-w', '--wldcd',
                    dest='wldcd',
                    default=False,
                    help="use with care, convert file(s) using wildcard")
args = parser.parse_args()

action = args.action
path = args.path
file = args.file
wldcd = args.wldcd
files_affected = dict()


def tab_indent(_lines):
    """ if tab indent found return True """
    reg_tab_expr = r'^(\t+)(\S+.*)$'
    REG_TAB_match = re.compile(reg_tab_expr, re.M|re.I)
    for line in _lines:
        match_line = REG_TAB_match.match(line)
        if match_line:
            return True
    return False

def space_indent(_lines):
    """ if space indent found return True """
    reg_space_expr = r'^( +)(\S+.*)$'
    REG_SPACE_match = re.compile(reg_space_expr, re.M|re.I)
    for line in _lines:
        match_line = REG_SPACE_match.match(line)
        if match_line:
            return True
    return False

def find_files_affected(_path, _file, _wldcd, _action):
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
    elif _wldcd:
        pass

    return result

def convert_tab_indent(_work_file, _org_file):
    """ if tab indent found convert to space """
    reg_tab_expr = r'^(\t+)(\S+.*)$'
    REG_TAB_match = re.compile(reg_tab_expr, re.M|re.I)
    work_file = open(_work_file, 'w')
    for line in _org_file:
        match_line = REG_TAB_match.match(line)
        if match_line:
            spaces = " "*(len(match_line.group(1))*4)
            work_file.write(spaces + match_line.group(2) + "\n")
        else:
            work_file.write(line)
    work_file.close()

def convert_space_indent(_work_file, _org_file):
    """ if space indent found convert to tab """
    reg_space_expr = r'^( +)(\S+.*)$'
    REG_SPACE_match = re.compile(reg_space_expr, re.M|re.I)
    work_file = open(_work_file, 'w')
    for line in _org_file:
        match_line = REG_SPACE_match.match(line)
        if match_line:
            tabs = "\t"*(int(len(match_line.group(1))/4))
            work_file.write(tabs + match_line.group(2) + "\n")
        else:
            work_file.write(line)
    work_file.close()

def modify_files_affected(_files, _wldcd, _action):
    """ fix indents """
    for _file in _files:
        with open(_file, 'r') as f:
            read_file = f.readlines()

        if _action == 't2s':
            convert_tab_indent(_file, read_file)
        elif _action == 's2t':
            convert_space_indent(_file, read_file)


files_affected = find_files_affected(path, file, wldcd, action)
print('Files affected:', files_affected)
#modify_files_affected(files_affected, wldcd, action)