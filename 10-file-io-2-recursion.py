
def big_file_maker(lines_of_text):
    with open("big_file.txt", 'w') as f:
        for i in range(1,lines_of_text+1):
            f.write(str(i) + '\n')
big_file_maker(2000)
# Here are some empty functions that are shown here as examples.  You do NOT have to use these if you don't want to.  You can create your own functions instead. It might be simpler to ignore the examples and to create your own logic rather than trying to use these.

def read_data(filename):
    with open(filename, 'r') as f:
        return f.readlines()

def write_data(new_filename,data):
    with open(new_filename, 'w') as g:
        g.write(data)

def line_glue(source_array, slice_start, slice_stop):
    return ''.join(source_array[slice_start:slice_stop])

def split_file(big_source_array, max_line_number, counter):
    
    
    if len(big_source_array) <= max_line_number:
        # this would be better if write_data could use variable # of arguements
        write_data("new_filename_{0}".format(counter), line_glue(big_source_array, 0, len(big_source_array)))
    else:
        write_data("new_filename_{0}".format(counter), line_glue(big_source_array, 0, max_line_number))
        
        return split_file(big_source_array[max_line_number:], max_line_number, counter+=1)


split_file(read_data('big_file.txt'), 500, 1)