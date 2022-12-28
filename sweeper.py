from QubitPresimulated.librarian import QLibrarian
from itertools import product
# from qiskit_metal.analyses.simulation import ScatteringImpedanceSim
# from qiskit_metal.analyses.quantization import EPRanalysis
# from qiskit_metal.analyses.quantization import LOManalysis


class QSweeper:
    '''
    '''

    def __init__(self, analysis):
        self.analysis = analysis

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

        # Define some useful objects
        design = self.analysis.sim.design
        component = self.components[component_name]
        qoptions = self.component.options

        

        # Get all combinations of the options and values
        
                
                # Update QComponent referenced by 'component_name'
                self.update_qcomponent(qoptions, {option : value})
                self.component.rebuild()

                self.analysis.run()
                print({option: value})








        # if (type(self.analysis) == LOManalysis):
        #     self.run_LOManlaysis(component_name, parameters, kwargs)
        # elif (type(self.analysis) == EPRanalysis):
        #     self.run_EPRanlaysis(component_name, parameters, kwargs)
        # elif (type(self.analysis) == ScatteringImpedanceSim):
        #     self.run_ScatteringImpedanceSim(component_name, parameters, kwargs)
        # else:
        #     raise ValueError('Analysis type is not currently supported.')
        
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


    