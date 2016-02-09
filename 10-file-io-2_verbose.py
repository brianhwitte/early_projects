
'''

Goal: Write a program that splits a large file into two files based on line number. (500 lines per file)
'''

def big_file_maker(lines_of_text):
    with open("big_file.txt", 'w') as f:
        for i in range(1,lines_of_text+1):
            f.write(str(i) + '\n')

big_file_maker(1000)

def read_data(filename):
    with open(filename, 'r') as f:
        return f.readlines()

def write_data(new_filename,data):
    with open(new_filename, 'w') as g:
        g.write(data)

def line_glue(source_array, slice_start, slice_stop):
    return ''.join(source_array[slice_start:slice_stop])

def split_file(source_filename, line_number):
    lines = read_data(source_filename)
    string1 = line_glue(lines, 0, line_number)
    string2 = line_glue(lines, line_number, len(lines))
    write_data('smaller_file_1.txt', string1)
    write_data('smaller_file_2.txt', string2)
    

split_file("big_file.txt", 500)




