# Convert indents, because why not!
We like to fix indents from tab to space or vice versa

We can convert all files in given directory

We can convert a single given file

```
usage: convert_indents.py
        [-h, --help    show howto invoke and possible arguments]
        [-a, --action  specify action, t2s(tab 2 space) or s2t(space 2 tab)]
        [-s, --spaces  specify number of spaces per tab, default is 4]
        [-t, --tabs    specify tab per x number of spaces, default is 4 spaces per tab]
        [-p, --path    convert all files in given path location]
        [-f, --file    convert specific file]

        example:
        1) convert given file indents from tab to spaces, using 4 spaces (default) per tab
        convert_indents.py -a t2s -f fix_my_tab_indents.txt

convert_indents.py: error: the following arguments are required: -a, --action
```
