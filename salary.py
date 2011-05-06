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
    ifile = csv.reader(open(  infilename, 'r'))  # open file for reading
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
year = None
dheaderfilename = None
theaderfilename = None
outfilename = 'output.txt'
error = "Use --help option for assistance"


# check for options
if len(sys.argv) > 1:
    if sys.argv[1] in ('-h', '-help', '--help'):
        print("Usage: ", sys.argv[0], " [OPTIONS] teacherfile datafile")
        print("""
  headerfile: The file from which you get the column names.
  datafile:   The file containing the data to be processed.

  Valid OPTIONS:
    -h, -help, --help:
              Evidently you've already discovered this one

              """)
        sys.exit(1)

# read options
while len(sys.argv) > 3:
    option = sys.argv[1]
    del sys.argv[1]
    if option in ('-hd', '-hdata', '--headerdata'):
        dheaderfilename = sys.argv[1]
        del sys.argv[1]
    elif option in ('-ht', '-hteach', '--headerteacher'):
        theaderfilename = sys.argv[1]
        del sys.argv[1]
    elif option in ('-y', '-yr', '--year'):
        year = sys.argv[1]
        del sys.argv[1]
    elif option in ('-o', '-oth', '--other'):   # Just a placeholder, useless for now
        options.append(sys.argv[1])
        del sys.argv[1]
    else:
        print(sys.argv[0] + ":",'invalid option', option)
        print(error)
        sys.exit(1)

# get file names
try:
    teacherfilename = sys.argv[1]
    datafilename    = sys.argv[2]
except:
    print("Usage:", sys.argv[0], "[options] teacherfile datafile")
    print(error)
    sys.exit(1)

# open input file with student data
dHeaders, dFile = get_headers(datafilename, dheaderfilename)


# get school codes, throw them all into a list or dict
# perhaps best to just iterate through the teacher file
# and just pluck out the schools codes.  simple as that.
schools = []
colnum = dHeaders.index('campus')
for line in dFile:
    idnum = line[colnum]
    if idnum not in schools:
        schools.append(idnum)

# with the school codes in hand, now choose a subject
# let's say Math

# open the teacher file
# go through each teacher,
# see if he teaches Math, and if so,
# add his salary to a list associated with the school code
tHeaders, tFile = get_headers(teacherfilename, theaderfilename)


subjectNames = []      # each teacher teaches lots of subjects
for title in tHeaders: # make a list of columns with subject names
    if "SUBJECT AREA NAME" in title:
        subjectNames.append(title)

salaries = {}                 # dict to hold pairs "schoolID":[array of salaries]
for idnum in schools:
    salaries[idnum] = []

count = 0
for line in tFile:                 # look at each row in the teacher file
    teachesMath = False
    for subject in subjectNames:   # check the columns that contain the subjects taught
        if "math" in line[tHeaders.index(subject)].lower(): # if even one says "Math"
            teachesMath = True                              # take note
            count += 1
            break
    if teachesMath:
        thisSchool = line[tHeaders.index("CAMPUS NUMBER")].strip()
        thisSalary = float(line[tHeaders.index("BASE PAY")].strip())
        if thisSchool not in salaries.keys():
            schools.append(thisSchool)
            salaries[thisSchool] = []
        salaries[thisSchool].append(thisSalary)

print("Found", count, "Math teachers in file", teacherfilename, "...")

# so now we have, for each school code,
# an associated list containing all the
# Math teacher salaries for that code

# average those salaries,
# creating a dict, say, with school code as the key,
# and average salary for Math teachers as the value
avgSalaries = {}
for idnum in salaries.keys():
    money = salaries[idnum]
    avgSalaries[idnum] = sum(money) / len(money) if len(money) > 0 else None

# that finishes the salary part of things

# just a quick little sanity check
count = 0
for idnum in avgSalaries.keys():
    print("School:", idnum, "Avg Salary:", avgSalaries[idnum])
    if count > 10:
        break
    count += 1

# now on to the scores

# go through the scores file, e.g. the TAKS data
# for each line, record the school code and the Math score
# stick these in a dict, so that the key is the
# school code, and the value is a list of Math scores
# for all the students in that school
dHeaders, dFile = get_headers(datafilename, dheaderfilename)

scores = {}
for idnum in schools:
    scores[idnum] = []

count = 0
for line in dFile:                                        # go through each line in student data
    thisYear   = line[dHeaders.index("year")].strip()     # get the year for that score
    thisSchool = line[dHeaders.index("campus")].strip()   # get student's school ID
    scoreStr   = line[dHeaders.index("m_raw")].strip()
    thisScore  = float(scoreStr) if scoreStr != '' else None # get student's Math score
    if count < 10:
        print("thisSchool:", thisSchool, "thisScore:", thisScore, "thisYear:", thisYear)
    if (thisYear == year or year == None) and thisScore != None:
        # If it's the year we want (or all years)
        # and there's a score
        if thisSchool not in scores.keys():               # make sure that school's on the list, and
            schools.append(thisSchool)
            scores[thisSchool] = []
        scores[thisSchool].append(thisScore)              # add the score to the list for that school
    count += 1
        
count = 0
for idnum in scores.keys():
    if scores[idnum] != []:
        print("School:", idnum, "Scores:", scores[idnum])
        count += 1
    if count > 10:
        break


# average these scores,
# creating a dict, with school code as key,
# and average Math score as value
avgScores = {}
for idnum in scores.keys():
    results = scores[idnum]
    avgScores[idnum] = sum(results) / len(results) if len(results) > 0 else None

# another quick little sanity check
count = 0
for idnum in avgScores.keys():
    if scores[idnum] != []:
        print("School:", idnum, "Avg Score:", avgScores[idnum])
        count += 1
    if count > 10:
        break


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
