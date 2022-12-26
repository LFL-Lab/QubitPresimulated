import pandas as pd

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
        self.data = pd.DataFrame()
    

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
        for i, row in self.data.iterrows():
            error = 0
            for param, target_value in target_parameters.items():
                if param in self.data.columns:
                    error += (row[param] - target_value)**2
            if error < min_error:
                min_error = error
                best_match = row['geometry']
        return best_match
    
    def update_qcomponent(qcomponent_options: dict, dictionary):
        '''
        Given a qcomponent.options dictionary,
        Update it based on an input dictionary
        '''
        for key, value in dictionary.items():
            if key in qcomponent_options:
                if type(value) == dict:
                    self.update_qcomponent(qcomponent_options[key], value)
                else:
                    qcomponent_options[key] = value
            else:
                qcomponent_options[key] = value
    

    #### Section 2: Gathering data 
    # TODO: Create add_data

    def from_qoptions(self, dictionary):
        '''
        Turns a nested dictionary w/ values and 
        appends it to self.data. 

        Use it to quickly get qcomponent.options 
        I.e. dicionary = qcomponent.options

        Input:
        * dictionary (dict) - qcomponent.options dictionary

        Output:
        * df (pd.DataFrame) - updated self.data
        '''
        df = self.data
        for key, value in dictionary.items():
            if isinstance(value, dict):
                nested_df = self.from_qoptions(value)
                df = nested_df
            else:
                df[key] = [value]
        return df   


    #### Section 3: Remembering data
    def read_csv(self, filepath):
        self.data = pd.read_csv(filepath)
    
    def write_csv(self, filepath=None):
        '''
        Write self.data to .csv
        Defaults to ./draft_presimulated
        '''
        # Default to date & time name
        if (file_path == None):
            now = datetime.datetime.now()
            date_string = now.strftime("%Y-%m-%d-%H-%M-%S")

            # and it will go into self.default_save_directory
            if not os.path.exists(self.default_save_directory):
                os.mkdir(self.default_save_directory)
    
            file_path = self.default_save_directory + 'QubitPresimulated/draft_presimulated/draft_{date_string}.csv'
            
        self.data.to_csv(file_path, index=False)