# -*- coding: utf8 -*-
"""
unpack ipynb
Tested 2015 March
"""
import os
from pprint import pprint
import re


def dont_do_anything(fw, cell_dict):
    print "won't do anything about", cell_dict["cell_type"]
    print cell_dict


def handle_heading(fw, cell_dict):

    output = convert_heading(cell_dict)

    fw.write(output)
    return output


def convert_heading(cell_dict):
    """
    string to be written to file

    :param cell_dict:
    :return:

    >>> cd = {'source': ["Fraud detection with Benford's law"], 'cell_type': 'heading', 'level': 1, 'metadata': {}}
    >>> convert_heading(cd)
############################################################
# Fraud detection with Benford's law
############################################################
"""

    '''
    sample heading cell
    {'cell_type': 'heading',
     'level': 1,
     'metadata': {},
     'source': ['HYPOTHESIS TESTING EXERCISES - SOLUTION']}
    '''

    # decoration for heading
    output = ('#' * 60 + '\n')
    # print lines in 'source' field
    for line in cell_dict['source']:
        output += '# ' + line + '\n'
    # decoration for heading
    output += '#'.ljust(60, '#') + '\n'
    return output


def handle_markdown(fw, cell_dict):
    """"""
    '''
    {'cell_type': 'markdown',
     'metadata': {},
     'source': ["Verify the validity of Benford's law when applied to 1)
                the population of a country; 2) the number of breast cancer
                cases in each country.\n",
      '\n',
      '1. Collect a count of the first digits of all the numbers in the data sets\n',
      "2. Use a statistical tests to compare the observed count to the one
      expected by Benford's law"]}
    '''
    code_list = cell_dict['source']

    fw.write('"""\n')
    for code in code_list:
        fw.write(code)
    fw.write('\n"""\n')


def handle_code(fw, cell_dict):
    """"""
    '''
    {'cell_type': 'code',
     'collapsed': False,
     'input': ['%matplotlib inline\n',
      '\n',
      'import numpy as np\n',
      'import pandas as pd\n',
      'import matplotlib.pyplot as plt\n',
      'import statsmodels.api as sm\n',
      'from scipy import stats'],
     'language': 'python',
     'metadata': {},
     'outputs': [],
     'prompt_number': 1}
    '''

    '''handle input cell'''
    process_input_source(cell_dict, fw, "input")

    '''handle source cell'''
    process_input_source(cell_dict, fw, "source")

    '''handle output cell'''
    output = cell_dict.get("output", [])
    for code in output:
        fw.write('## ')
        fw.write(code)

    fw.write('\n')
    fw.write('#'.ljust(20, '#'))
    fw.write('\n\n')


def process_input_source(cell_dict, fw, marker):
    for code in cell_dict.get(marker, []):
        if code:
            '''magic command'''
            py_name = find_py_name_from_run_magic_cmd(code)
            if py_name:
                fw.write('from %.124s import *\n' % py_name)
            else:
                if '%' == code[0]:
                    fw.write('#')
                code_strip = code.strip()
                if code_strip and ('?' == code_strip[-1]) and ('#' != code_strip[0]):
                    fw.write('help(')
                    fw.write(code.strip()[:-1])
                    fw.write(')\n')
                else:
                    fw.write(code)


def find_py_name_from_run_magic_cmd(code):
    """
    find ??? of magic command '%run ???.py'
    :param code:
    :return:
    >>> find_py_name_from_run_magic_cmd('%run phugoid.py')
    'phugoid'
    """
    result = re.findall(r'%run\s(.*).py', code)
    if result:
        result = result[0]
    return result


# lookup table of cell handlers
handler = {'heading': handle_heading,
           'code': handle_code,
           'markdown': handle_markdown,
           'raw': handle_markdown,
           }


def unpack(filename, b_verbose=False):
    """

    :param filename:
    :param b_verbose: if True print more detailed information
    :return:
    """

    split_ext = os.path.splitext(filename)

    if ".ipynb" != split_ext[1]:
        filename = split_ext[0] + ".ipynb"
    py_name = split_ext[0] + ".py"

    if not os.path.exists(py_name):

        fw = open(py_name, 'w')

        ''' read file '''
        if os.path.exists(filename):
            f = open(filename, 'r')
            txt = f.read()
            f.close()

            ''' replace all triple double quotes to triple qutes to avoid
            possible confusion '''
            txt = txt.replace('"""', "'''")

            ''' decompose '''
            false = False
            true = True
            null = None
            d = eval(txt)

            try:
                worksheets = d.get('worksheets', [])
                if worksheets:
                    for worksheet in worksheets:
                        cells = worksheet.get('cells', [])
                        process_cells(cells, fw, b_verbose)
                else:
                    cells = d.get('cells', [])
                    process_cells(cells, fw, b_verbose)
                    if b_verbose and not cells:
                        print("No worksheet to process")
            except:
                print filename
                raise

        fw.close()


def process_cells(cells, fw, b_verbose=False):
    if cells:
        fw.write("# -*- coding: utf8 -*-\nfrom pylab import *\n")
        for cell in cells:
            # process cell, or don't do anything
            process_one_cell(fw, cell)
        # to present the result at least at the end
        fw.write('print (" The presented result might be overlapping. ".center(60, "*"))')
        fw.write("\nshow()\n")
    else:
        if b_verbose:
            print("No cell to process")


def process_one_cell(fw, cell):
    call_this = handler.get(cell['cell_type'],
                            dont_do_anything)
    call_this(fw, cell)


def convert_tree(full_path=os.path.abspath(os.curdir)):
    for dir_path, dir_names, file_names in os.walk(full_path):
        for filename in file_names:
            if filename.endswith(".ipynb"):
                full_path = os.path.join(dir_path, filename)
                unpack(full_path)


if "__main__" == __name__:
    import sys
    if 2 <= len(sys.argv):
        unpack(sys.argv[1])
    else:
        convert_tree(os.path.abspath(os.curdir))
