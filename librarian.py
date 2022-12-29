import pandas as pd
import datetime
import os

class QLibrarian:
    '''
    This class is split into 3 sections
    1. Using presimulated data to make stuff.
        - find_best_match
        - export those options into a format compatiable w/ qcomponent.options
    2. Gathering data
        - Adding data from a sweep
    3. Remembering data
        - Reading and writing to permanent .csv
    '''
    def __init__(self):
        self.qoptions_data = pd.DataFrame()
        self.simulation_data = pd.DataFrame()
        self.default_save_directory = 'QubitPresimulated/draft_presimulated/'
    

    #### Section 1: Using your data to do things!
    def find_best_match(self, target_parameters: dict):
        """
        TODO:
        Fix row['geometry'], I want it to give me all the qcomponent.options

        Finds the geometry that best matches the target parameters.

        Input:
        * target_parameters (dict) - which maps parameter names (str) to target values (float).
        
        """
        best_match = None
        min_error = float('inf')
        for i, row in self.simulation_data.iterrows():
            error = 0
            for param, target_value in target_parameters.items():
                if param in self.simulation_data.columns:
                    error += (row[param] - target_value)**2
            if error < min_error:
                min_error = error
                best_match = row['geometry']
        return best_match
    

    #### Section 2: Gathering data 

    # Append qcomponent.options to self.qoptions_data
    def from_dict(self, dictionary, df):
        '''
        Get data in the format of QComponent.options
        Append it to a pandas DataFrame
        
        Input: 
        * dictionary

        Output:
        Appends dictionary to DataFrame.
        Columns are named after the keys of the dict. For nested dicts, keys are separated by `.`
        Entries below each column are associated w/ the deepest value of the nested dict.
        '''
        keys, values = self.extract_keysvalues(dictionary)
        df = df.append(dict(zip(keys, values)), ignore_index=True)

    def extract_keysvalues(self, dictionary, parent_key=''):
        '''
        Helper method for self.from_dict
        Not used for front end.

        Inputs:
        * dictionary (dict)

        Output:
        * keys (list of strings) - names which will be assigned to pd.DataFrame
            columns. For every level into the nested list, names will be separated by a `.`
        * values (list of strings) - entries associated w/ each key in keys
        '''
        keys = []
        values = []
        for key, value in dictionary.items():
            new_key = parent_key + '.' + key if parent_key else key
            if isinstance(value, dict):
                nested_keys, nested_values = self.extract_keysvalues(value, new_key)
                keys.extend(nested_keys)
                values.extend(nested_values)
            else:
                keys.append(new_key)
                values.append(value)
        return keys, values

    # Get row in self.qoptions_data and export to dict
    def to_qoptions(self, index):
        '''
        Convert a row of self.qoptions_data to a nested dictionary in the format of QComponent.options
        
        Parameters:
        index (int): The index of the row to convert
        
        Returns:
        dictionary: A nested dictionary in the format of QComponent.options
        '''
        data = {}
        row = self.qoptions_data.iloc[index]
        for key, value in row.items():
            parts = key.split('.')
            d = data
            for part in parts[:-1]:
                if part not in d:
                    d[part] = {}
                d = d[part]
            d[parts[-1]] = value
        return data

    
    # TODO: Build method to modulary import data from the simulation


    # 
    


    #### Section 3: Remembering data
    def read_csv(self, filepath):
        '''
        Read in a .csv and split it into self.qoptions_data and self.simulation_data
        '''
        # Read the combined DataFrame from the CSV file
        combined_df = pd.read_csv(filepath)
        
        # Split the combined DataFrame into the two separate DataFrames
        self.qoptions_data = combined_df.iloc[:, :combined_df.columns.get_loc(' ')]
        self.simulation_data = combined_df.iloc[:, combined_df.columns.get_loc(' ')+1:]
    
    def write_csv(self, file_path=None, mode='a', **kwargs):
        '''
        Write self.qoptions_data and self.simulation_data to .csv
        Defaults to ./draft_presimulated

        Puts an empty column inbetween the qoptions_data and simulation_data

        Inputs:
        * filepath (str)
        * mode (str, optional)
        '''
        # Default to date & time name
        if (file_path == None):
            now = datetime.datetime.now()
            date_string = now.strftime("%Y-%m-%d")
    
            file_path = 'testing_{date_string}.csv'
        
        # Combine the two DataFrames and add an empty column between them
        combined_df = pd.concat([self.qoptions_data, pd.DataFrame(columns=[' ']), self.simulation_data], axis=1)
        
        # Write the combined DataFrame to a CSV file
        combined_df.to_csv(file_path, index=False, mode=mode, **kwargs)