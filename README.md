# tree_size

## Purpose
This program aims at determining the number of files included in a directory and its children. A user defines the 
parent directory in which the search should take place and how many files the directory should contain at least (by 
considering all children directories) in order to be listed. Finally, the result is shown as a dictionary in your 
console that represents the file tree including the aggregated number of files per directory (which is at least as high 
as your defined threshold value, if provided).

## File structure
    |-- .gitignore
    |-- LICENSE
    |-- main.py
    |-- README.md

## Starting the program
1. cd to the directory that contains this program
2. execute python main.py -h for showing the help to this program, including the required arguments
3. execute the following command: python main.py <your_target_path> --count_threshold <your_integer_value>
