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
single = False
year = None
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
dHeaders, dFile = get_headers(datafilename, dheaderfilename)


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


# make a dict to store salaries
salaries = {}                 # dict to hold pairs "schoolID":[array of salaries]
for idnum in schools:         # This is where we'll have to deal with repeats in schools
    salaries[idnum] = []      # For a repeat, we just initialize salaries[idnum] to [] again
                              # ... no big deal

# add data from each file, file by file
for tFilename in tFilenames:
    tHeaders, tFile = get_headers(folder + tFilename, theaderfilename)


    subjectNames = []      # each teacher teaches lots of subjects
    for title in tHeaders: # make a list of columns with subject names
        if "SUBJECT AREA NAME" in title:
            subjectNames.append(title)



    print("Getting Math teachers from", tFilename)

    count = 0
    lineCount = 0
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
        if lineCount % 1000000 == 0:
            print("\t", lineCount, "lines read from", tFilename)
        lineCount += 1

    print("\t Found", count, "Math teachers in file", tFilename, "...")

# so now we have, for each school code,
# an associated list containing all the
# Math teacher salaries for that code

# Single Teachers:
# If we only want data for schools with one Math teacher,
# then we should delete those keys (school IDs) where
# the list of salaries has more than one entry
count = 0
killList = []              # We can't modify the dict as we loop over it
if single:                 # so create a list of schoolIDs to kill
    print("\nRemoving schools with more than one Math teacher...")
    for schoolID in salaries.keys():
        if len(salaries[schoolID]) > 1:
            killList.append(schoolID)
            count += 1
    for idnum in killList:
        salaries.pop(idnum)
    print("\t", count, "schools removed from data...\n")

# Now the rest of the manipulations should work
# whether there's one salary or more for each school

# average those salaries,
# creating a dict, say, with school code as the key,
# and average salary for Math teachers as the value
avgSalaries = {}
for idnum in salaries.keys():
    money = salaries[idnum]
    avgSalaries[idnum] = sum(money) / len(money) if len(money) > 0 else None

# that finishes the salary part of things

# just a quick little sanity check
# count = 0
# for idnum in avgSalaries.keys():
#     print("School:", idnum, "Avg Salary:", avgSalaries[idnum])
#     if count > 10:
#         break
#     count += 1

# now on to the scores

# go through the scores file, e.g. the TAKS data
# for each line, record the school code and the Math score
# stick these in a dict, so that the key is the
# school code, and the value is a list of Math scores
# for all the students in that school
dHeaders, dFile = get_headers(datafilename, dheaderfilename)

scores = {}
for idnum in schools:      # again we'll just live with the repeats
    scores[idnum] = []     # for a repeat, we just re-initialize scores[idnum] to []


print("Getting Math scores:")

count = 0
lineCount = 0
for line in dFile:                                        # go through each line in student data
    thisYear   = line[dHeaders.index("year")].strip()     # get the year for that score
    thisSchool = line[dHeaders.index("campus")].strip()   # get student's school ID
    scoreStr   = line[dHeaders.index("m_raw")].strip()
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
        
# count = 0
# for idnum in scores.keys():
#     if scores[idnum] != []:
#         print("School:", idnum, "Scores:", scores[idnum])
#         count += 1
#     if count > 10:
#         break


# average these scores,
# creating a dict, with school code as key,
# and average Math score as value
avgScores = {}
for idnum in scores.keys():
    results = scores[idnum]
    avgScores[idnum] = sum(results) / len(results) if len(results) > 0 else None

# another quick little sanity check
# count = 0
# for idnum in avgScores.keys():
#     if scores[idnum] != []:
#         print("School:", idnum, "Avg Score:", avgScores[idnum])
#         count += 1
#     if count > 10:
#         break


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

finalSalary = []
finalScore  = []
count = 0
for idnum in avgSalaries.keys():                 # go through each school ID
    if (avgSalaries[idnum] is not None) and \
           (avgScores[idnum] is not None):       # if there's a salary & a score
        finalSalary.append(avgSalaries[idnum])   # then tack them on the lists
        finalScore.append(avgScores[idnum])
    count += 1


# order the lists according to the numeric order
# of the salaries, if need be

# output lists to file, List 1 as 1st column
# List 2 as 2nd column
oFile = open("../tmp/" + outfilename, "w")
try:
    assert len(finalSalary) == len(finalScore)
except:
    print("Uh oh, salary and score lists do not have equal length...")
    sys.exit(1)

for i in range(len(finalSalary)):
    outString = str(finalSalary[i]) + ',' + str(finalScore[i]) + '\n'
    oFile.write(outString)

oFile.close()

# done... use the output for regression, graphing, etc.
