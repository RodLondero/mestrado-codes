import pandas as pd
import math
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

results_directory = base_dir + "\\resultados\\"


def get_data_from_file(file_name: str):
    """Get the data from a file

    Parameters:
        file_name (str): Name of the file that will be read

    Returns:
        DataFrame: returns a dataframe with the file data
    """
    columns, data = read_file(results_directory + file_name)
    return pd.DataFrame(data, columns=columns)


def read_file(file_name: str):
    """This function is used to read a file

    Parameters:
        file_name (str): Name of the file that will be read

    Returns:
        content[0]:  return a list with the file columns
        content[1:]: return all values after column line
    """
    with open(file_name, 'r') as f:
        content = f.read().splitlines()
        content = get_columns(content)
        content = convert_to_float(content)
    return content[0], content[1:]


def get_columns(content_file: list):
    """Extract the column list of a file

    Parameters:
        content_file (list): Content file read

    Returns:
        content_file: return the content file with columns formated
    """
    # Clear first and second lines
    content_file.pop(0)
    content_file.pop(0)

    # Split the new first line that contains columns names
    content_file[0] = content_file[0].strip("()\n").split('"')

    # Remove elements equals to ''
    for i, val in enumerate(content_file[0]):
        if val.strip() == '':
            content_file[0].pop(i)

    return content_file


def convert_to_float(content_file: list):
    """Convert the file content to float

    Args:
        content_file (list): Content file read

    Returns:
        content_file: return the content file with float numbers
    """
    # Loop for all elements after column names (index 0)
    for i in range(0, len(content_file[1:])):
        line = content_file[1:][i].strip('\n').split(' ')
        # float_numbers = list()
        line = [float(item) for item in line]

        content_file[i + 1] = line

    return content_file


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
