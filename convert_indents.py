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

print(args)

files_path = args.path
files_affected = dict()

def find_files_affected(path):
    result = dict()
    for filename in os.listdir(path):
        tempfile = path + filename
        with open(tempfile, 'r') as f:
            read_data = f.readlines()

        reg_tab_expr = r'^(\t+)(.*)$'
        REG_TAB_match = re.compile(reg_tab_expr, re.M|re.I)

        for line in read_data:
            match_line = REG_TAB_match.match(line)
            if match_line:
                #print(len(match_line.group(1)),match_line.group(2))
                result[tempfile] = '1'
                break
    return result

def modify_files_affected(files):
    for file in files:
        reg_expr = r'^(\t+)(.*)$'
        REG_match = re.compile(reg_expr, re.M|re.I)
        with open(file, 'r') as f:
            read_file = f.readlines()

        work_file = open(file, 'w')
        for line in read_file:
            match_line = REG_match.match(line)
            if match_line:
                spaces = " "*(len(match_line.group(1))*4)
                work_file.write(spaces + match_line.group(2) + "\n")
            else:
                work_file.write(line)

        work_file.close()

files_affected = find_files_affected(files_path)
print('Files affected:', files_affected)
modify_files_affected(files_affected)
