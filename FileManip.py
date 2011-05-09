#!/usr/bin/env python3.1
# FileManip.py
# A pared-down module containing some functions commonly used
# to manipulate files containing education data.

def extract_fields(line):
  """Return a list of the entries in each line.

  WARNING: this function is elegant, but doesn't deal well
  with field entries that themselves include commas, e.g.
  'Washington, D.C.' will cause this function to split into
  'Washington' and 'D.C.'.
  """
  
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

def extract_chunk(infilename, outfilename, begin, end, period = None):
  """Extract a group of lines from input file and write to output file.

  Extract a contiguous sequence of lines, starting with
  line number "begin" and ending with line number "end".
  If this will produce an inordinately large output file,
  the user can break it into sections of length "period".
  """

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
      if data[0] != last and (period != None and count >= period):
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
    
    return headers, ifile



def get_csv_columns(infilename, headfilename=None):
  """Take data from CSV file and read into a dict of columns.

  Column headers become the dictionary keys and are read
  from the first line of the input file, unless a header
  file is specified, in which case the column names are
  read from the header.
  """
  
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
  """From a CSV file, extract rows sequentially that share a common property.

  The usage of this function is best illustrated by an
  example:

  Suppose several rows of data correspond to one value of
  a particular property.  For example, the data for one
  student is spread over several rows.  These rows all
  share a "groupfield", here Student ID.  Suppose also
  that each student has another property, e.g. the value
  of a variable DISADV, and we only
  want to keep in our output file those students who
  maintain a constant value of DISADV.  That is, if
  a given student's DISADV value changes, we remove *all*
  data regarding that student from the output.  The
  property name "DISADV" is the "seqfield" we would
  input to the function.
  """
  
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

