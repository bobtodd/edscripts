#!/usr/bin/env python3.1

# salary.py
# A script to arrange data in the form teacher-salary vs. student-grades

import sys, os, csv
import FileManip as fm

def get_headers(infilename, headfilename=None):
    """Get column names.

    This function plucks out the names of columns in a CSV file
    either from the file itself or from a separate, designated
    header file.

    Returns a tuple
        (headers, ifile),
    where headers is a list of column titles, and ifile is a
    csv file object containing the input file.
    """
    
    # open input file & header file (if different)
    ifile           = csv.reader(open(  infilename, 'r'))  # open file for reading
    if headfilename:
        hbasename, hext = os.path.splitext(headfilename)
    
    # get the column headers
    # from this file or a separate file
    headers = []
    if headfilename:
        if hext == '.csv':
            hfile    = csv.reader(open(headfilename, 'r'))  # open file for reading
            for line in hfile:
                headers += line                   # column headers may be spread over several lines
        else:
            hfile = open(headfilename, 'r')
            for line in hfile:
                headers += fm.extract_fields(line)
            hfile.close()
    else:
        for line in ifile:
            headers += line
            break                             # should only have header in first line
  
    # get rid of leading and trailing whitespace (including newlines)
    # in each column label
    for i in range(len(headers)):
        headers[i] = headers[i].strip()                # in case headers are split over multiple lines
    if '' in headers:
        headers.pop(headers.index(''))
    
    return headers, ifile


# open files
# default columns to be processed
options = []
headerfilename = None
outfilename = 'output.txt'
error = "Use --help option for assistance"

# check for options
if len(sys.argv) > 1:
    if sys.argv[1] in ('-h', '-help', '--help'):
        print("Usage: ", sys.argv[0], " [OPTIONS] [-hd headerfile] datafile")
        print("""
  headerfile: The file from which you get the column names.
  datafile:   The file containing the data to be processed.

  Valid OPTIONS:
    -h, -help, --help:
              Evidently you've already discovered this one

              """)
        sys.exit(1)

# read options
while len(sys.argv) > 2:
    option = sys.argv[1]
    del sys.argv[1]
    if option in ('-hd', '-head', '--header'):
        headerfilename = sys.argv[1]
        del sys.argv[1]
    elif option in ('-o', '-oth', '--other'):
        options.append(sys.argv[1])
        del sys.argv[1]
    else:
        print(sys.argv[0] + ":",'invalid option', option)
        print(error)
        sys.exit(1)

# get file names
try:
    datafilename = sys.argv[1]
except:
    print("Usage:", sys.argv[0], "[options] [-hd headerfile] datafile")
    print(error)
    sys.exit(1)

# open input file
headers, ifile = get_headers(datafilename, headerfilename)


# get school codes, throw them all into a list or dict
# perhaps best to just iterate through the teacher file
# and just pluck out the schools codes.  simple as that.
schools = []
colnum = headers.index('campus')
for line in ifile:
    schools.append(line[colnum])
    print(schools[-1])

# with the school codes in hand, now choose a subject
# let's say Math

# open the teacher file
# go through each teacher,
# see if he teaches Math, and if so,
# add his salary to a list associated with the school code

# so now we have, for each school code,
# an associated list containing all the
# Math teacher salaries for that code

# average those salaries,
# creating a dict, say, with school code as the key,
# and average salary for Math teachers as the value

# that finishes the salary part of things

# now on to the scores

# go through the scores file, e.g. the TAKS data
# for each line, record the school code and the Math score
# stick these in a dict, so that the key is the
# school code, and the value is a list of Math scores
# for all the students in that school

# average these scores,
# creating a dict, with school code as key,
# and average Math score as value

# the UPSHOT:
# we have two dicts, whose key:value pairs look like
# schoolID:avgMathTeacherSalary
# and
# schoolID:avgTAKSscoreForMath

# create two lists, one of average salaries, the other of
# associated Math average Math scores, linking via
# schoolID:
#             List 1                   List 2
# Element 0   salary0 -> (schoolID) -> score0
# Element 1   salary1 -> (schoolID) -> score1
# etc.

# order the lists according to the numeric order
# of the salaries, if need be

# output lists to file, List 1 as 1st column
# List 2 as 2nd column

# done... use the output for regression, graphing, etc.
