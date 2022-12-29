from QubitPresimulated.librarian import QLibrarian
from QubitPresimulated.sweeper_helperfunctions import extract_QSweep_parameters
from qiskit_metal.analyses.simulation import ScatteringImpedanceSim
from qiskit_metal.analyses.quantization import EPRanalysis
from qiskit_metal.analyses.quantization import LOManalysis
from tqdm import tqdm # creates cute progress bar


class QSweeper:
    '''
    '''

    def __init__(self, analysis,):
        self.analysis = analysis
        self.full_simulations = []
        
    def run_sweep(self, component_name: str, parameters: dict, data_name: str = None, save_path = None):
        """
        Runs self.analysis.run_sweep() for all combinations of the options and values in the `parameters` dictionary.

        Inputs:
        * component_name (str) - The name of the component to run the sweep on.
        * parameters (dict) - A dictionary of options and their corresponding values. 
            The keys are the options (strings), and the values are lists of floats.
        * data_name (str, optional) - Label to query for data. If not specified, the entire
            dictionary is returned. Defaults to None.
        *
        
        Output:
        * Librarian (QLibrarian)- 

        Example:
        If `parameters = {'cross_length': [1, 2], 'cross_gap': [4, 5, 6]}`, then this method will call 
        `self.analysis.()` 6 times with the following arguments:
        1. cross_length: 1 cross_gap: 5
        2. cross_length: 1 cross_gap: 4
        3. cross_length: 1 cross_gap: 6
        4. cross_length: 2 cross_gap: 4
        5. cross_length: 2 cross_gap: 5
        6. cross_length: 2 cross_gap: 6
        """
        # Clear self.full_simulations log
        self.full_simulations = []

        # Initalize QLibrarian for output
        Librarian = QLibrarian()

        # Define some useful objects
        design = self.analysis.sim.design
        component = design.components[component_name]
        all_combo_parameters = extract_QSweep_parameters(parameters)

        # Select a analysis type
        if (type(self.analysis) == LOManalysis):
            get_data = self.run_LOManlaysis
        elif (type(self.analysis) == EPRanalysis):
            get_data = self.run_EPRanlaysis
        elif (type(self.analysis) == ScatteringImpedanceSim):
            get_data = self.run_ScatteringImpedanceSim
        else:
            raise ValueError('Analysis type is not currently supported.')
        

        # Get all combinations of the options and values, w/ `tqdm` progress bar
        for combo_parameter in tqdm(all_combo_parameters):
            # Update QComponent referenced by 'component_name'
            component.options = self.update_qcomponent(component.options, combo_parameter)
            component.rebuild()

            # Run the analysis
            self.analysis.run()

            # Parse through data from the analysis
            data = get_data(data_name)

            # Log QComponent.options and data from analysis
            Librarian.from_dict(component.options, Librarian.qoptions_data)
            Librarian.from_dict(data, Librarian.simulation_data)

            # Save this data to a csv
            Librarian.write_csv(filepath = save_path, mode='a')

            # Tell me what you finished
            print('Simulated and logged configuration: {}'.format(combo_parameter))

            # Append full result to QSweeper.full_simulations
            self.full_simulations.append(self.analysis)
        
        
        self.simulation_Librarian = Librarian

        return Librarian
            

    # TODO: Might be able to get rid of these, but not sure yet...
    def run_LOManlaysis(self, data_name):
        all_data = self.analysis.get_data()
        return all_data
    
    def run_EPRanlaysis(self, data_name):
        all_data = self.analysis.get_data()
        return all_data
    
    def run_ScatteringImpedanceSim(self, data_name):
        all_data = self.analysis.get_data()
        return all_data

    def update_qcomponent(self, qcomponent_options: dict, dictionary):
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
    
        return qcomponent_options


    