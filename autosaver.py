import subprocess
import os

def acp(target_file: str, message: str = None, directory: str = None):
    '''
    Add, commit, and push a target file to your Git respository

    Inputs:
    * target_file (str) 
    * message (str, optional) - inputs into -m 'message'
        Correct usage (include inner quotations)
        message = '"Updated file."'
    '''
    # Add the .csv file to the staging area
    subprocess.run(['git', 'add', target_file])

    # Commit the changes
    if (message == None):
        message = f'"Updated {target_file}"'
    subprocess.run(['git', 'commit', '-m', message])

    # Push the changes to the remote repository
    if (directory == None):
        directory = 'master'
    subprocess.run(['git', 'push', 'origin', directory])