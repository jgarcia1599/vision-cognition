'''

Utility script to create on csv file from a sql dump
Modified from : https://github.com/jamesmishra/mysqldump-to-csv
Usage: 
python3 sqldump-to-csv.py [SQL DUMP FILENAME]

'''

#!/usr/bin/env python
import fileinput
import csv
import sys
import re

# This prevents prematurely closed pipes from raising
# an exception in Python
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

# allow large content in the dump
csv.field_size_limit(sys.maxsize)

def is_insert(line):
    """
    Returns true if the line begins a SQL insert statement.
    """
    return line.startswith('INSERT INTO') or False


def get_values(line):
    """
    Returns the portion of an INSERT statement containing values
    """
    return line.partition('` VALUES ')[2]


def values_sanity_check(values):
    """
    Ensures that values from the INSERT statement meet basic checks.
    """
    assert values
    assert values[0] == '('
    # Assertions have not been raised
    return True


def parse_values(tablename,schema,values, outfile):
    """
    Given a file handle and the raw values from a MySQL INSERT
    statement, write the equivalent CSV to the file
    """
    latest_row = []
    new_csv_filename = tablename + '.csv'

    reader = csv.reader([values], delimiter=',',
                        doublequote=False,
                        escapechar='\\',
                        quotechar="'",
                        strict=True
    )
    with open(new_csv_filename,'w+') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL,quotechar='"')
        
        schema = list(schema.split(','))
        print(schema)
        writer.writerow(schema)
        for reader_row in reader:
            for column in reader_row:
                # If our current string is empty...
                if len(column) == 0 or column == 'NULL':
                    latest_row.append(chr(0))
                    continue
                # If our string starts with an open paren
                if column[0] == "(":
                    # Assume that this column does not begin
                    # a new row.
                    new_row = False
                    # If we've been filling out a row
                    if len(latest_row) > 0:
                        # Check if the previous entry ended in
                        # a close paren. If so, the row we've
                        # been filling out has been COMPLETED
                        # as:
                        #    1) the previous entry ended in a )
                        #    2) the current entry starts with a (
                        if latest_row[-1][-1] == ")":
                            # Remove the close paren.
                            latest_row[-1] = latest_row[-1][:-1]
                            new_row = True
                    # If we've found a new row, write it out
                    # and begin our new one
                    if new_row:
                        writer.writerow(latest_row)
                        latest_row = []
                    # If we're beginning a new row, eliminate the
                    # opening parentheses.
                    if len(latest_row) == 0:
                        column = column[1:]
                # Add our column to the row we're working on.
                latest_row.append(column)
            # At the end of an INSERT statement, we'll
            # have the semicolon.
            # Make sure to remove the semicolon and
            # the close paren.
            if latest_row[-1][-2:] == ");":
                latest_row[-1] = latest_row[-1][:-2]
                writer.writerow(latest_row)

SCHEMAS = {}


def is_create_statement(line):
    return line.startswith('CREATE TABLE')


def is_field_definition(line):
    return line.strip().startswith('`')


def is_insert_statement(line):
    return line.startswith('INSERT INTO')


def get_mysql_name_value(line):
    value = None
    result = re.search(r'\`([^\`]*)\`', line)
    if result:
        value = result.groups()[0]
    return value


def get_value_tuples(line):
    values = line.partition(' VALUES ')[-1].strip().replace('NULL', "''")
    if values[-1] == ';':
        values = values[:-1]

    return ast.literal_eval(values)

def write_file(output_directory, table_name, schema, values):
    file_name = os.path.join(output_directory, '%s.csv' % (table_name,))
    with open(file_name, 'w') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=schema)
        writer.writeheader()
        for value in values:
            writer.writerow(dict(zip(schema, value)))


TABLE_NAMES = {}
def main():
    """
    Parse arguments and start the program
    """
    # Iterate over all lines in all files
    # listed in sys.argv[1:]
    # or stdin if no args given.
    current_table_name = None
    try:
        for line in fileinput.input():

            # Look for an INSERT statement and parse it.
            if is_create_statement(line):
                current_table_name = get_mysql_name_value(line)
                SCHEMAS[current_table_name] = []
            elif current_table_name and is_field_definition(line):
                field_name = get_mysql_name_value(line)
                SCHEMAS[current_table_name].append(field_name)
            if is_insert(line):
                current_table_name = get_mysql_name_value(line)
                if current_table_name not in TABLE_NAMES:
                    TABLE_NAMES[current_table_name] = 0
                    updated_table_name = current_table_name + '_' + str(TABLE_NAMES[current_table_name])
                else:
                    TABLE_NAMES[current_table_name] +=1
                    updated_table_name = current_table_name + '_' + str(TABLE_NAMES[current_table_name])
                current_schema = SCHEMAS[current_table_name]
                schema_string = ','.join(current_schema)
                values = get_values(line)
                if values_sanity_check(values):
                    # print(sys.stdout)
                    print('\n')
                    print(current_table_name)
                    parse_values(updated_table_name,schema_string,values, sys.stdout)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()