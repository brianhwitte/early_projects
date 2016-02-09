'''To print out a list of all variables operating at a particular point in your code, copy these functions into the top of your script.  Type "print_table(dir())" at the point in your  script where you want to observe active variables.  

    Magic variables will no be shown, but functions will be part of the table.

'''
'''Week 5 refactor:'''

def detect_variables(all_var):
    '''prints a tab-separated table of variables and values.  To use, put a statement of <variable_list> = dir() or <variable_list> = locals() at the point in the script where needed.  Call 'detect_variables' with <variable_list> as the argument. 
        Doesn't work weel for user-created objects.
    '''

    mundane_var = [var for var in all_var if '__' not in var]

    print "name\ttype\tvalue"

    for entry in mundane_var:

        print "{}\t{}\t{}".format(entry, type(entry), eval(entry))

'''Original week 1 version'''

def working_var(all_var, unwanted_var):
    ''' working_var takes a parameter 'all_var' which is a list of all variables operating in the environment where the print_table function is called.  The parameter 'unwanted_var' is a list of variable names to be removed from the list of all variables.  This is currently set to remove all 'magic' variables with __ in the name"
    '''
    for x in unwanted_var:
        if x in all_var:
            all_var.remove(x)
    return all_var



def make_new_entry(eval_var):
    '''This function returns a dictionary of the type and value for each variable.
    '''
    return {
            'type': type(eval_var),
            'value': eval_var
        }

def make_table(clean_list):
    '''Returns a dictionary of each variable in the environment at which the make_table function is called, along with the type and value of each variable.
    '''
    table = {}

    for x in clean_list:
         table[x] = make_new_entry(eval(x))

    return table

def print_table(vars):
    '''Returns a tab separated table of the names, types and values of each variable operating in the environment where it is called.  Note that these variables include the functions above.
    '''
    remove = ['__builtins__', '__doc__', '__name__', '__package__', '__file__',]
    clean_list = working_var(vars, remove)
    col_values = make_table(clean_list)

    col_titles = ["name space", "type", "value"]
    print "\t".join(col_titles)
    for i in col_values:
        print "{0}\t{1}\t{2}".format(i, str(col_values[i]["type"]),str(col_values[i]["value"]))

