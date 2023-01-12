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
        
    def run_sweep(self, component_name: str, parameters: dict, custom_analysis = None, save_path = None, **kwargs):
        """
        Runs self.analysis.run_sweep() for all combinations of the options and values in the `parameters` dictionary.

        Inputs:
        * component_name (str) - The name of the component to run the sweep on.
        * parameters (dict) - A dictionary of options and their corresponding values. 
            The keys are the options (strings), and the values are lists of floats.
        * custom_analysis (func (QAnalysis) -> dict, optional) - Create a custom analyzer to
            parse data! See self.run_EPRanalysis, self.run_LOManalysis, self.runScatteringImpedanceSim
            for examples.
        * kwargs - parameters associated w/ QAnalysis.run()
        
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

        # Clear simulations library
        self.librarian = QLibrarian()

        # Define some useful objects
        design = self.analysis.sim.design
        component = design.components[component_name]
        all_combo_parameters = extract_QSweep_parameters(parameters)

        # Select a simulator type
        if custom_analysis != None:
            run_analysis = custom_analysis
        else:
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
            design.rebuild()

            # Run the analysis, extract important data
            data = run_analysis(**kwargs)

            # Log QComponent.options and data from analysis
            self.librarian.from_dict(component.options, 'qoption')
            self.librarian.from_dict(data, 'simulation')

            # Save this data to a csv
            newest_qoption = self.librarian.qoptions.tail(n=1)
            newest_simulation = self.librarian.simulations.tail(n=1)
            
            QLibrarian.append_csv(newest_qoption, newest_simulation, filepath = save_path)

            # Tell me this iteration is finished
            print('Simulated and logged configuration: {}'.format(combo_parameter))

            # Append full result to QSweeper.full_simulations
            full_QAnalysis = self.analysis
            self.full_simulations.append(full_QAnalysis)

        return self.librarian
            
    def run_LOManlaysis(self, data_name, **kwargs):
        all_data = self.analysis.get_data(data_name)
        return all_data
    
    def run_EPRanlaysis(self, data_name, **kwargs):
        try:
            self.analysis.sim.run(**kwargs)
            self.analysis.run_epr()
        except:
            pass
        
        results = self.analysis.sim.renderer.epr_quantum_analysis.results['0']
    
        return results
    
    def run_ScatteringImpedanceSim(self, data_name, **kwargs):
        all_data = self.analysis.get_data(data_name)
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


    