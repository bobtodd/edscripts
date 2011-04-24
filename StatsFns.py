#!/usr/bin/env python3.1

# preparatory function extract_fields()
# return a list of the entries in each line
def extract_fields(line):
  fields = []
  field = ""
  quote = None
  
  # parse line character by character
  # keeping track of quoted strings
  for c in line:
    if c in "\"'":
      if quote is None: # start of quoted string
        quote = c
      elif quote == c:  # end of quoted string
        quote = None
      else:
        field += c    # other quote inside quoted string
      continue
    
    if quote is None and c == ",": # end of a field
      fields.append(field)
      field = ""
    else:
      field += c        # accumulating a field
  
  if field:
    fields.append(field)  # adding the last field
  
  return fields


import os

def extract_chunk(infilename, outfilename, begin, end, period):
  # open input file
  ifile = open( infilename, 'r')  # open file for reading
  
  # prepare for a sequence of output files
  # remove outfilename extension, insert file iteration number,
  # reattach extension
  iter = 0
  basename, ext  = os.path.splitext(outfilename)
  newoutfilename = "{0}{1:0=3}{2}".format(basename, iter, ext)
  ofile          = open(newoutfilename, 'w')  # open file for writing
  
  # go through lines in ifile
  # write those in desired range to ofile
  # but if you've written "period" lines
  # write to a new ofile
  i     = 0
  count = 0
  last  = None
  for line in ifile:
    if begin <= i <= end:
      data = extract_fields(line)
      if data[0] != last and count >= period:
        ofile.close()
        count = 0
        iter += 1
        newoutfilename = "{0}{1:0=3}{2}".format(basename, iter, ext)
        ofile = open(newoutfilename, 'w')
      ofile.write(line)
      last  = data[0]
    elif end < i:
      break
    i += 1
    count += 1
  
  # close files
  ifile.close(); ofile.close()

import sys, csv

def get_csv_columns(infilename, headfilename=None):
  # open input file & header file (if different)
  ifile           = csv.reader(open(  infilename, 'r'))  # open file for reading
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
        headers += extract_fields(line)
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
  
  data = {}
  for title in headers:
    data[title] = []
  
  # when we use "line" iterator in ifile again,
  # it should be at the point where we left off, i.e.
  # the 1st line if there's a separate header file, or
  # the 2nd line if the header's in the same file
  for line in ifile:                        # should now be first line of data
    values = line
    for i in range(len(headers)):
      data[headers[i]].append(values[i])
  
  # returning both headers (list) and data (dict)
  # allows user to maintain column order using
  # the order of strings in headers list
  return headers, data

def extract_sequential(groupfield, seqfield, infilename, headfilename=None):
  # open input file & prepare output file
  # with same name, plus 'seq' before the extension
  basename, ext  = os.path.splitext(infilename)
  outfilename    = "{0}_{1}{2}".format(basename, 'seq', ext)
  ofile          = csv.writer(open( outfilename, 'w'))  # open file for writing
  
  headers, data = get_csv_columns(infilename, headfilename)
  
  if groupfield not in data.keys():
    print("Error: {0} not in column headers...".format(groupfield))
    print("\tHeaders:{0}".format(headers))
    sys.exit(1)
  elif seqfield not in data.keys():
    print("Error: {0} not in column headers...".format(seqfield))
    print("\tHeaders:{0}".format(headers))
    sys.exit(1)
  else:
    # Now let's remove lines where the "disadv" value changes
    # but the student ID doesn't.
    # We'll remove *all* lines containing that ID.
    i = 1
    removecount = 0
    while i < len(data[groupfield]):                   # iterate down columns
      previousID = data[groupfield][i-1]
      currentID  = data[groupfield][i]
      
      next = i + 1
      
      if currentID != previousID:                      # check for change of student
        start = data[groupfield].index(previousID)     # if so, find first occurrence of previous ID
        end   = i                                      # (this is one *after* last occurrence)
        
        for j in range(start,end):                     # go through all lines with previous ID
          if data[seqfield][j] != data[seqfield][end-1]: # and look for a change in "disadv" value
            for k in list(range(end-1, start-1, -1)):  # if so, go backwards
              for field in data.keys():                # removing all rows with that student ID
                data[field].pop(k)
              removecount += 1
            
            next = start + 1
            break                                      # if change found, no more j iteratation
        
      i = next
  
  print("Total lines removed: {0}".format(str(removecount)))
  
  # Output to file
  # write the headers
  ofile.writerow(headers)
  
  # write data row by row
  for i in range(len(data[groupfield])):
    lineout = [data[title][i] for title in headers]
    ofile.writerow(lineout)


from math import sqrt

# correlation between two lists of data
def corr(x, y):
    assert len(x) == len(y), "lists must have equal length"
    
    xSum = sum(x)
    ySum = sum(y)
    
    xSumSq = sum([item**2 for item in x])
    ySumSq = sum([item**2 for item in y])
    
    iProd = 0.0
    for i in range(len(x)):
      iProd += x[i]*y[i]
    
    n = len(x)
    
    r = n*iProd - xSum*ySum
    r /= sqrt(n*xSumSq - xSum**2) * sqrt(n*ySumSq - ySum**2)
    return r

# correlation between three lists of data
# reduces to corr(x, y) if z == None
# argument "data" is a list of lists
def corr3(data):
    x = data[0]
    y = data[1]
    z = data[2] if len(data) > 2 else None
    
    rxy = corr(x,y)
    rxz = corr(x,z) if z != None else 0
    ryz = corr(y,z) if z != None else 0
    
    # if no z-column, this gives rxy
    rxy_z = rxy - rxz * ryz
    rxy_z /= sqrt(1 - rxz**2) * sqrt(1 - ryz**2)

    # use symmetry of correlation to speed things up
    rzy = ryz
    
    # if no z-column, this gives zero
    rxz_y = rxz - rxy * rzy
    rxz_y /= sqrt(1 - rxy**2) * sqrt(1 - rzy**2)
    
    # speed up using symmetry
    ryx = rxy
    rzx = rxz
    
    # if no z-column, this gives zero
    ryz_x = ryz - ryx * rzx
    ryz_x /= sqrt(1 - ryx**2) * sqrt(1 - rzx**2)
    
    return (rxy_z, rxz_y, ryz_x)


