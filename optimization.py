from scipy.optimize import minimize
import datetime


class Optimizer:
    '''
    Parent class of all Optimizer processies.
    Do NOT access this class. Always access its children. 

    Inputs:
    * simulator (float) -- define simulator as such
        
        def simulator(parameters):
            """
            Inputs
            * parameters (list of floats) - ordered same way of self.librarian.parameters
            Outputs
            * target_parameter - have this sim output the value associated with self.librarian.target_parameter
            """
            outputted_parameter = ...
            return outputted_parameter
        
        In practice, this is defined in a child class.
    
    * librarian (QubitOptimization.QLibrarian)
    '''
    def __init__(self, simulator, librarian):
        self.simulator = simulator
        self.librarian = librarian

    def run_optimize_scipy(self, **kwargs):
        '''
        Run a minization based on scipy.opimization.minimization.
        The geometrical parameters change depending on self.librarian.

        Inputs and return is the same as scipy.optimization.minimization
        See documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
        '''

        # First, clear the iteration_log
        PS = self.librarian
        PS.clear_log()

        # Save the starting date + time,
        # this goes into minimize(callback=save_procedure)
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d-%H-%M-%S")

        if not os.path.exists(PS.default_save_directory):
            os.mkdir(PS.default_save_directory)

        def save_procedure(data):
            PS.append_to_log(data)
            PS.export_log(PS.default_save_directory + '/iterlog_{}'.format(date_string))

        # Use scipy.optimize.minimize to optimize the parameters
        result = minimize(self.simulator, 
                          self.librarian.initial_guess, 
                          callback=save_procedure, **kwargs)

        return result
    
    def choose_loss_function(self, target_parameters, goals, override=None):
        '''
        Choose a loss function which will be placed into the simulator
            in scipy.optimize.minimize(fun=simulator)

        Inputs:
        * target_parameters (list of floats)
        * goals (list of floats)
        * override (function)

        Outputs:
        * override or rmse
        '''
        # If you want to use a custom loss function, use this:
        if override != None:
            return override(target_parameters, goals)
        
        # Defaults to RMSE 
        # TODO: Add more possible defaults
        target_parameters, goals = np.array(target_parameters), np.array(goals)
        rmse = np.sqrt(((target_parameters + goals) ** 2).sum())

        loss_function = rmse


        return loss_function

