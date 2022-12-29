from itertools import product

'''
This entire file is just a huge wrapper for 
`extract_QSweep_parameters` which is used in
`QSweeper.run_sweep()`.

When initalizing QSweeper(), there is an input called
`parameters`. It's a nested dict in the structure as
`QComponents.options`, except the values are lists not 
just singular floats.

We use `extract_QSweep_parameters` to preserve the 
structure of this data, but but also create all 
possible combinations of those lists.

Example:
options = {'cross_length': [1, 2], 
             'claw_options':{'claw_a':[3,4]}}

print(extract_QSweep_parameters(options))
# Outputs:
# [{'cross_length': 1, 'claw_options': {'claw_a': 3}},
# {'cross_length': 1, 'claw_options': {'claw_a': 4}},
# {'cross_length': 2, 'claw_options': {'claw_a': 3}},
# {'cross_length': 2, 'claw_options': {'claw_a': 4}}]

TODO: There's definitely a more elegant way of doing this
    I'm just not sure how to do it at the moment.
'''

def extract_QSweep_parameters(parameters: dict):
    '''
    Input:
    * parameters (dict) - nested dictionary with a list
        at the end of the nest
    
    Output:
    * list_of_combos (list of dicts) - same nested structure
        as your input. But you'll have each combination.
    '''
    ext_parameters = extract_parameters(parameters)
    values = extract_values(ext_parameters)
    combo = generate_combinations(values)
    list_of_combos = create_dict_list(ext_parameters, combo)
    return list_of_combos


def extract_parameters(dictionary, keys=None, prefix=''):
        '''
        Extract keys in nested dict, then separates these keys by a `.`
        For our purposes, gets the parameters of interest

        Input:
        * dictionary (dict)

        Output:
        * keys (list of string)
        
        Example:
        my_dict = {'transmon1': {'cross_width': '30um', 
                                 'connection_pads': {'readout': {'pad_width': '200um'}}}}
        print(extract_keys(my_dict))
        # prints: ['transmon1.cross_width', 'transmon1.connection_pads.readout.pad_width']
        '''
        if keys is None:
            keys = []
        for key, value in dictionary.items():
            full_key = f"{prefix}{key}" if prefix else key
            if isinstance(value, dict):
                extract_parameters(value, keys, full_key + '.')
            else:
                keys.append(full_key)
        return keys

def extract_values(dictionary, values=None):
        '''
        Extract values in nested dict
        For our purposes, gets the initial guesses associated w/ self.parameters

        Input:
        * dictionary (dict)

        Output:
        * values (list of ...)

        Example:
        my_dict = {'transmon1': {'cross_width': '30um', 
                                 'connection_pads': {'readout': {'pad_width': '200um'}}}}
        print(extract_values(my_dict))
        # prints: ['30um', '200um']
        '''
        if values is None:
            values = []
        for key, value in dictionary.items():
            if isinstance(value, dict):
                extract_values(value, values)
            else:
                values.append(value)
        return values

def generate_combinations(lists):
    '''
    This function takes in a list of lists and returns a
    list of tuples that contain all possible combinations 
    of the elements in the input lists.

    Input:
    * lists (list) - A list of lists containing elements 
        that we want to generate combinations for.

    Output:
    * combination (list of tuples) - A list of tuples 
        containing all possible combinations of the elements in the input lists.
    '''
    combinations = list(product(*lists))
    return combinations

def create_dict_list(keys, values):
    ''''
    Takes in a list of strings (keys) and a list of values, 
    and returns a list of nested dictionaries where `.`
    in the string references the level of nesting.

    Input: 
    * keys (list of strings) - A list of strings representing 
        the keys for the dictionaries.
    * values (list) - A list of values to be used as the 
        values for the dictionaries

    Output:
    * dict_list (list of nested dictionaries) - A list of 
        nested dictionaries where each dictionary has the 
        keys as its keys and the values as its values.
    '''
    dict_list = []
    for vals in values:
        nested_dict = create_nested_dict(keys)
        d = nested_dict
        for i, key in enumerate(keys):
            parts = key.split('.')
            for part in parts[:-1]:
                d = d[part]
            d[parts[-1]] = vals[i]
        dict_list.append(nested_dict)
    return dict_list