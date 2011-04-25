#!/usr/bin/env python3.1

# salary.py
# A script to arrange data in the form teacher-salary vs. student-grades

# open files

# get school codes, throw them all into a list or dict
# perhaps best to just iterate through the teacher file
# and just pluck out the schools codes.  simple as that.

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
