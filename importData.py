import csv
with open('leftGlove.csv', 'r') as read_obj: # read csv file as a list of lists
  csv_reader = csv.reader(read_obj) # pass the file object to reader() to get the reader object
  leftGloveData = list(csv_reader) # Pass reader object to list() to get a list of lists

with open('rightGlove.csv', 'r') as read_obj: # read csv file as a list of lists
  csv_reader = csv.reader(read_obj) # pass the file object to reader() to get the reader object
  rightGloveData = list(csv_reader) # Pass reader object to list() to get a list of lists