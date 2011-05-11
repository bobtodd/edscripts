#!/usr/bin/env python3.1

# salary.py
# A script to arrange data in the form teacher-salary vs. student-grades
# or the form teacher-experience vs. student-grades

import sys, os, csv
import FileManip as fm

# open files
# default columns to be processed
options = []
single = False
year = None
tColumn = "BASE PAY"
dColumn = 'm_raw'
folder = None
folderList = None
dheaderfilename = None
theaderfilename = None
outfilename = 'output.txt'
error = "Use --help option for assistance"

# check for options
if len(sys.argv) > 1:
    if sys.argv[1] in ('-h', '-help', '--help'):
        print("Usage: ", sys.argv[0], " [OPTIONS] teacherfile datafile")
        print("""
  teacherfile: The file from which you get the teacher data.
  datafile:    The file containing the student scores.

  Valid OPTIONS:
    -h, -help, --help:
              Evidently you've already discovered this one.

    -hd, -hdata, --headerdata:
              Follow this option with the name of the file
              containing the column titles for TAKS data,
              if located in a separate file.

    -ht, -hteach, --headerteacher:
              Follow this option with the name of the file
              containing the column titles for TEA data,
              if located in a separate file.

    -t, -tcol, --tcolumn:
              Follow this option with the name of the
              column in the TEA files from which you wish
              to extract data.

              Default: "BASE PAY"

    -c, -col, --column:
              Follow this option with the name of the
              column in the TAKS file from which you wish
              to extract data.

              Default: "m_raw"

    -y, -yr, --year:
              Follow this option with the year containing
              the data which you would like to extract
              from the TAKS file.

    -s, -sing, --single:
              Use this option if you wish the program to
              extract only data for those schools where
              there is a single Math teacher.  You do
              not need to follow this parameter with
              anything.

    -f, -fold, --folder:
              Follow this option with the name of the
              folder containing the TEA files from which
              you wish to extract data.

              NOTE: The files should have roughly the
              same form, differing by index.  For example:
              TCHM01.csv, TCHM02.csv, etc.  In this case,
              when you pass the TEA filename as a (non-
              optional) parameter to the program, you
              should replace the varying elements by '*',
              as in TCHM*.csv.  Make sure you enclose
              this expression in quotes: 'TCHM*.csv'

    Example usage (all one line):

    ./teachers.py -s -y 2007 -col m_ssc -hd headers.csv -f ../data/ 'TCHM*.csv' TAKS.csv

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
    elif option in ('-t', '-tcol', '--tcolumn'):
        tColumn = sys.argv[1]
        del sys.argv[1]
    elif option in ('-c', '-col', '--column'):
        dColumn = sys.argv[1]
        del sys.argv[1]
    elif option in ('-y', '-yr', '--year'):
        year = sys.argv[1]
        del sys.argv[1]
    elif option in ('-f', '-fold', '--folder'):
        folder = sys.argv[1]
        del sys.argv[1]
    elif option in ('-s', '-sing', '--single'):
        single = True
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

if folder is not None:
    folderList = os.listdir(folder)

# open input file with student data
dHeaders, dFile = fm.get_headers(datafilename, dheaderfilename)


# get school codes, throw them all into a list or dict
# perhaps best to just iterate through the teacher file
# and just pluck out the schools codes.  simple as that.
print("Getting school IDs:")

schools = []
colnum = dHeaders.index('campus')
lineCount = 0
for line in dFile:
    idnum = line[colnum]
    # ideally we should only append idnum
    # if it's not already in schools
    # but that implies a search through the array
    # for every ID we add: very inefficient!  And worse as the array grows!
    # So we'll just have to live with repeats
    schools.append(idnum)
    if lineCount % 1000000 == 0:
        print("\t", lineCount, "lines read from", datafilename)
    lineCount += 1

# with the school codes in hand, now choose a subject
# let's say Math

# open the teacher file(s)
# go through each teacher,
# see if he teaches Math, and if so,
# add his salary to a list associated with the school code
# and add his experience to another list for that code

# first make a list of all the teacher files
# we want to parse
tFilenames = []
if folder is not None:
    print("Getting filenames for teacher data from", folder)
    teacherBasename, teacherExt = os.path.splitext(teacherfilename)
    tPattern = teacherBasename.strip('*').lstrip(folder)
    for tFilename in folderList:
        tBasename, tExt = os.path.splitext(tFilename)
        if tPattern in tBasename:
            tFilenames.append(tFilename)
            print("\t", tFilename, "added to list...")
else:
    tFilenames.append(teacherfilename)
    print("Single file for teacher data:", teacherfilename)


# make a dict of dicts to store salaries and more
# dict to hold groups "schoolID":[array of salaries], [array of yrs experience]
teachers = {}
for idnum in schools:         # This is where we'll have to deal with repeats in schools
    teachers[idnum] = {}               # For a repeat, re-initialize salaries[idnum] to {}
    teachers[idnum]['salaries'] = []   # as well as teachers[]['salaries']
    teachers[idnum]['experience'] = [] # etc.

# add data from each file, file by file
for tFilename in tFilenames:
    tHeaders, tFile = fm.get_headers(folder + tFilename, theaderfilename)


    subjectNames = []                    # each teacher teaches lots of subjects
    for title in tHeaders:               # make a list of columns with subject names
        if "SUBJECT AREA NAME" in title:
            subjectNames.append(title)



    print("Getting Math teachers from", tFilename)

    count = 0
    lineCount = 0
    for line in tFile:                 # look at each row in this teacher file
        teachesMath = False
        for subject in subjectNames:   # check the columns that contain the subjects taught
            if "math" in line[tHeaders.index(subject)].lower(): # if even one says "Math"
                teachesMath = True                              # take note
                count += 1
                break
        if teachesMath:
            thisSchool     = line[tHeaders.index("CAMPUS NUMBER")].strip()
            thisSalary     = float(line[tHeaders.index("BASE PAY")].strip())
            thisExperience = float(line[tHeaders.index("EXPERIENCE")].strip())
            if thisSchool not in teachers.keys():
                schools.append(thisSchool)
                teachers[thisSchool] = {}
                teachers[thisSchool]['salaries'] = []
                teachers[thisSchool]['experience'] = []
            teachers[thisSchool]['salaries'].append(thisSalary)
            teachers[thisSchool]['experience'].append(thisExperience)
        if lineCount % 1000000 == 0:
            print("\t", lineCount, "lines read from", tFilename)
        lineCount += 1

    print("\t Found", count, "Math teachers in file", tFilename, "...")

# so now we have, for each school code,
# an associated list containing all the
# Math teacher salaries for that code
# and all the years of experience for
# Math teachers for the same code

# Single Teachers:
# If we only want data for schools with one Math teacher,
# then we should delete those keys (school IDs) where
# the list of salaries has more than one entry
count = 0
killList = []              # We can't modify the dict as we loop over it
if single:                 # so create a list of schoolIDs to kill
    print("\nRemoving schools with more than one Math teacher...")
    for schoolID in teachers.keys():
        if len(teachers[schoolID]['salaries']) > 1:
            killList.append(schoolID)
            count += 1
    for idnum in killList:
        teachers.pop(idnum)
    print("\t", count, "schools removed from data...\n")

# Now the rest of the manipulations should work
# whether there's one salary or more for each school

# average those salaries and years of experience,
# creating a dict, say, with school code as the key,
# and average salary for Math teachers as one value
# and the average experience as the other
avgTeachers = {}
countDeadbeats = 0
for idnum in teachers.keys():
    money      = teachers[idnum]['salaries']
    experience = teachers[idnum]['experience']

    avgTeachers[idnum] = {}
    avgTeachers[idnum]['salaries'] = sum(money) / len(money) if len(money) > 0 else None
    avgTeachers[idnum]['experience'] = sum(experience) / len(experience) if len(experience) > 0 else None
    if len(money) == 0:
        countDeadbeats += 1

# Recall that the dict 'teachers' was initialized
# with all the schoolIDs from the TAKS data.
# If the files used for the TEA data don't include
# all schools, then many 'teacher' keys will be eliminated
print(countDeadbeats, "schools omitted for lack of salary...\n")

# that finishes the salary and experience part of things

# now on to the scores

# go through the scores file, e.g. the TAKS data
# for each line, record the school code and the Math score
# stick these in a dict, so that the key is the
# school code, and the value is a list of Math scores
# for all the students in that school
dHeaders, dFile = fm.get_headers(datafilename, dheaderfilename)

scores = {}
for idnum in schools:      # again we'll just live with the repeats
    scores[idnum] = []     # for a repeat, we just re-initialize scores[idnum] to []


print("Getting", dColumn, "scores:")

count = 0
lineCount = 0
for line in dFile:                                        # go through each line in student data
    thisYear   = line[dHeaders.index("year")].strip()     # get the year for that score
    thisSchool = line[dHeaders.index("campus")].strip()   # get student's school ID
    scoreStr   = line[dHeaders.index(dColumn)].strip()
    thisScore  = float(scoreStr) if scoreStr != '' else None # get student's Math score
    if (thisYear == year or year is None) and (thisScore is not None):
        # If it's the year we want (or all years)
        # and there's a score
        if thisSchool not in scores.keys():               # make sure that school's on the list, and
            schools.append(thisSchool)
            scores[thisSchool] = []
        scores[thisSchool].append(thisScore)              # add the score to the list for that school
    if lineCount % 1000000 == 0:
        print("\t", lineCount, "lines read from", datafilename)
    lineCount += 1
    count += 1

# average these scores,
# creating a dict, with school code as key,
# and average Math score as value
avgScores = {}
for idnum in scores.keys():
    results = scores[idnum]
    avgScores[idnum] = sum(results) / len(results) if len(results) > 0 else None

# the UPSHOT:
# we have some dicts, whose key:value pairs look roughly
# schoolID:avgMathTeacherSalary,
# schoolID:avgMathTeacherExperience,
# and
# schoolID:avgTAKSscoreForMath

# create three lists, one of average salaries, another of
# average experience, and the last of associated
# average Math scores, linking via
# schoolID:
#             List 1                   List 2                       List 3
# Element 0   salary0 -> (schoolID) -> experience0 -> (schoolID) -> score0
# Element 1   salary1 -> (schoolID) -> experience1 -> (schoolID) -> score1
# etc.

# actually, we should pack them into a dict
# together with the schoolID as key, so that we
# don't lose that information

finalOutput = {}
count       = 0
countSalary = 0
countScore  = 0
countBoth   = 0
for idnum in avgTeachers.keys():                 # go through each school ID
    theSalary     = avgTeachers[idnum]['salaries']
    theExperience = avgTeachers[idnum]['experience']
    theScore      = avgScores[idnum]
    if theSalary is None:
        countSalary += 1
    if theScore is None:
        countScore += 1
    if theSalary is None and theScore is None:
        countBoth += 1
    if (theSalary is not None) and (theScore is not None):
        # if there's a salary and a score
        # tack them on
        finalOutput[idnum] = {
            'avgSalary': theSalary,
            'avgExperience': theExperience,
            'avgScore': theScore
        }
        count += 1

print(count, "school IDs added for output...")
print("\t", countSalary, "schools omitted for lack of salary data...")
print("\t", countScore, "schools omitted for lack of score data...")
print("\t", countBoth, "schools omitted for lack of salary and score data...")


# output to file
# 1st column: School IDs
# 2nd column: avgSalary
# 3rd column: avgExperience
# 4th column: avgScore
oFile = open("../tmp/" + outfilename, "w")

for idnum in finalOutput.keys():
    outString  = idnum
    outString += ','
    outString += str(finalOutput[idnum]['avgSalary'])
    outString += ','
    outString += str(finalOutput[idnum]['avgExperience'])
    outString += ','
    outString += str(finalOutput[idnum]['avgScore'])
    outString += '\n'
    oFile.write(outString)

oFile.close()

# done... use the output for regression, graphing, etc.
