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
    
    
    supported_datatypes = ['qoptions', 'simulations', 'analysis_setup']
    default_save_directory = 'QubitPresimulated/draft_presimulated/'

    def __init__(self):
        self.qoptions = pd.DataFrame()
        self.simulations = pd.DataFrame()
        self.analysis_setup = pd.DataFrame()


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
        for i, row in self.simulations.iterrows():
            error = 0
            for param, target_value in target_parameters.items():
                if param in self.simulations.columns:
                    error += (row[param] - target_value)**2
            if error < min_error:
                min_error = error
                best_match = row['geometry']
        return best_match
    

    #### Section 2: Gathering data 
    # Append qcomponent.options to self.qoptions
    def from_dict(self, dictionary, target_df='qoption'):
        '''
        Get data in the format of QComponent.options
        Append it to a pandas DataFrame
        
        Input: 
        * dictionary
        * target_df (string) - 
            - 'qoption'
            - 'simulation'

        Output:
        Appends dictionary to DataFrame.
        Columns are named after the keys of the dict. For nested dicts, keys are separated by `.`
        Entries below each column are associated w/ the deepest value of the nested dict.
        '''
        keys, values = self.extract_keysvalues(dictionary)
        if (target_df == 'qoption'):
            self.qoptions = self.qoptions.append(dict(zip(keys, values)), ignore_index=True)
        else:
            self.simulations = self.simulations.append(dict(zip(keys, values)), ignore_index=True)
        
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

    # Get row in self.qoptions and export to dict
    def to_qoptions(self, index):
        '''
        Convert a row of self.qoptions to a nested dictionary in the format of QComponent.options
        
        Parameters:
        index (int): The index of the row to convert
        
        Returns:
        dictionary: A nested dictionary in the format of QComponent.options
        '''
        data = {}
        row = self.qoptions.iloc[index]
        for key, value in row.items():
            parts = key.split('.')
            d = data
            for part in parts[:-1]:
                if part not in d:
                    d[part] = {}
                d = d[part]
            d[parts[-1]] = value
        return data

    
    #### Section 3: Import Data
    def read_csv(self, filepath):
        '''
        Read in a .csv and split it into self.qoptions and self.simulations
        '''
        # Read the combined DataFrame from the CSV file
        combined_df = pd.read_csv(filepath)
        
        # Split the combined DataFrame into the two separate DataFrames
        try:
            self.qoptions = combined_df.iloc[:, :combined_df.columns.get_loc('__SPLITTER__')]
            self.simulations = combined_df.iloc[:, combined_df.columns.get_loc('__SPLITTER__')+1:]
        except KeyError:
            print("""ERROR: There are no columns in your `.csv`. This error probably came from using QLibrarian.append_csv() to make a new file.
                     Data won't be formatted properly. """)
        return combined_df


    ### Section 4: Export Data
    def _merge_supported_data(self):
        '''
        Combine all DataFrames specified by self.supported_datatypes

        Return:
        * dataframes_to_merge (List[pd.DataFrame])
        '''
        dataframes_to_merge = []
        for datatype in self.supported_datatypes:
            if hasattr(self, datatype):
                dataframes_to_merge.append(getattr(self, datatype))

        return dataframes_to_merge
    
    def export_csv(self, filepath=None, mode='a', **kwargs):
        '''
        Write self.qoptions and self.simulations to .csv
        Defaults to ./draft_presimulated

        Puts an empty column inbetween the qoptions and simulations

        Inputs:
        * filepath (str)
        * mode (str, optional)
        '''
        insert = '__SPLITTER__'
        merged_data = self._merge_supported_data()

        # Default to date & time name
        if (filepath == None):
            now = datetime.datetime.now()
            date_string = now.strftime("%Y-%m-%d")
    
            filepath = 'testing_{date_string}.csv'
        
        # Combine the two DataFrames and add a splitter column between them
        combined_df = []
        for i, entry in enumerate(merged_data):
            combined_df.append(entry)
            if i != len(merged_data) - 1:
                combined_df.append(insert)
        
        combined_df = pd.concat(combined_df, axis=1)
        
        # Write the combined DataFrame to a CSV file
        combined_df.to_csv(filepath, index=False, mode=mode, **kwargs)

    @staticmethod
    def append_csv(qoption_data, simulation_data, filepath=None):
        '''
        Static verison of `self.write_csv`

        Usage: when you want to append one line of data at a time
            to long term storage (.csv) located at `filepath`
        
        Inputs:
        * qoption_data (pd.DataFrame)
        * simulation_data (pd.DataFrame)
        '''
        # Default to date & time name
        if (filepath == None):
            now = datetime.datetime.now()
            date_string = now.strftime("%Y-%m-%d")
    
            filepath = 'testing_{date_string}.csv'
        
        # Combine the two DataFrames and add an empty column between them
        combined_df = pd.concat([qoption_data, pd.DataFrame(columns=['__SPLITTER__']), simulation_data], axis=1)
        
        # Write the combined DataFrame to a CSV file
        combined_df.to_csv(filepath, index=False, mode='a', header=False)