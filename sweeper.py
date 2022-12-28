from QubitPresimulated.librarian import QLibrarian
from QubitPresimulated.sweeper_helperfunctions import extract_QSweep_parameters
from qiskit_metal.analyses.simulation import ScatteringImpedanceSim
from qiskit_metal.analyses.quantization import EPRanalysis
from qiskit_metal.analyses.quantization import LOManalysis
from tqdm import tqdm # creates cute progress bar


class QSweeper:
    '''
    '''

    def __init__(self, analysis):
        self.analysis = analysis
        self.all_simulations = []

    def run_sweep(self, component_name, parameters):
        """
        Runs self.analysis.run_sweep() for all combinations of the options and values in the `parameters` dictionary.

        Parameters:
        - component_name (str): The name of the component to run the sweep on.
        - parameters (dict): A dictionary of options and their corresponding values. The keys are the options (strings), and the values are lists of floats.

        Example:
        If `parameters = {'cross_length': [1, 2] 'cross_gap': [4, 5, 6]}`, then this method will call 
        `self.analysis.()` 6 times with the following arguments:
        1. cross_length: 1 cross_gap: 5
        2. cross_length: 1 cross_gap: 4
        3. cross_length: 1 cross_gap: 6
        4. cross_length: 2 cross_gap: 4
        5. cross_length: 2 cross_gap: 5
        6. cross_length: 2 cross_gap: 6
        """
        # Clear self.all_simulations log
        self.all_simulations = []

        # Define some useful objects
        design = self.analysis.sim.design
        component = self.components[component_name]
        all_combo_parameters = extract_QSweep_parameters(parameters)

        # Select a analysis type
        if (type(self.analysis) == LOManalysis):
            run_analysis = self.run_LOManlaysis
        elif (type(self.analysis) == EPRanalysis):
            run_analysis = self.run_EPRanlaysis
        elif (type(self.analysis) == ScatteringImpedanceSim):
            run_analysis = self.run_ScatteringImpedanceSim
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
            run_analysis(component_name, parameters, kwargs)

            # Autosave data to .csv

            # Append data to QSweeper
            self.all_simulations.append(self.analysis)
            

    def run_LOManlaysis(self, component_name, parameters: dict, **kwargs):
        '''
        
        '''
        pass
    
    def run_EPRanlaysis(self, component_name, parameters: dict, **kwargs):
        pass
    
    def run_ScatteringImpedanceSim(self, component_name, parameters: dict, **kwargs):
        pass



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


    