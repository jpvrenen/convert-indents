import os
import re

files_path = 'D:/tmp/'
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

def modify_files_affected(files_affected):
  for file in files_affected:
    reg_expr = r'^(\t+)(.*)$'
    REG_match = re.compile(reg_expr, re.M|re.I)
    with open(file, 'r') as f:
      read_file = f.readlines()
 
    work_file = open(file, 'w')
    for line in read_file:
      match_line = REG_match.match(line)
      if match_line:
        no_spaces = len(match_line.group(1))*4
        work_file.write(" "*no_spaces + match_line.group(2) + "\n")
      else:
        work_file.write(line)
      
    work_file.close()

files_affected = find_files_affected(files_path)
print('Files affected:', files_affected)
modify_files_affected(files_affected)
