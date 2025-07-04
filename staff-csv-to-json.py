import json
import csv

def count_csv_rows(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        row_count = sum(1 for row in csv_reader)
    return row_count


# Define the staff CSV filename as a variable
STAFF_CSV_FILENAME = 'new-staff.csv'
# count the number of rows in the staff.csv file as we will need this number later 
# to determine when to add a comma to the end of each json record
row_count = count_csv_rows(STAFF_CSV_FILENAME)


# Define the output JSON filename as a variable
OUTPUT_JSON_FILENAME = 'new-staff-updated.json'
# write the opening bracket and new line to the output JSON file
with open(OUTPUT_JSON_FILENAME, 'a') as json_file: 
        json_file.write('[')
        json_file.write('\n')

# starting at line 2 of the staff.csv file for each line from the staff.csv file, 
# read the quoted string. If the quoted string contains a comma, then split the string into
# two strings, reverse the order of the strings, and then update the the quoted string 
# with the reversed strings. Then store the reversed strings in a variable called updated_name
updated_name = ''
line_count = 0
with open(STAFF_CSV_FILENAME, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader) # skip the first line of the csv file
    for line in csv_reader: 
        name = line[0]
        position = line[2]
        email = line[4]
        if ',' in name:
            updated_name = name.split(',')
            # remove leading and trailing whitespace
            updated_name = [item.strip() for item in updated_name]
            updated_name.reverse()
            updated_name = ' '.join(updated_name)
        else:
            updated_name = name
        # write the updated_name, position, and email to the output JSON file. Each record in the json file will be formatted as:
        # {
        #     "name": "Brad Bigney",
        #     "position": "Elder - Lead Pastor",
        #     "emailAddress": "bradbigney@graceky.org"
        # },
        # {
        #     "name": "Brian Fannin",
        #     "position": "Elder - Florence Campus Pastor",
        #     "emailAddress": "brianfannin@graceky.org"
        # },

        # open the output JSON file in append mode
        with open(OUTPUT_JSON_FILENAME, 'a') as json_file:
            # write the json record to the output JSON file
            json.dump({'name': updated_name, 'position': position, 'emailAddress': email}, json_file)
            # add a comma to the end of each json record, except for the last record
            # line_count < row_count - 2 means we are checking to see if the current line is less 
            # than the total number of lines in the csv file minus 2. If so, then add a comma to the 
            # end of the json record.
            if line_count < row_count - 2:
                 json_file.write(',')
                 json_file.write('\n')
        line_count += 1

# write the closing bracket to the output JSON file
with open(OUTPUT_JSON_FILENAME, 'a') as json_file:
        json_file.write('\n')
        json_file.write(']')
