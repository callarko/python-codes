# main.py
from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment
import logging

# Load the workspace from the config file
ws = Workspace.from_config()

# Create an environment (you can also use an existing one)
env = Environment.from_conda_specification(
    name='my-environment',
    file_path='./MLfolder/environment.yml'
)

# Define the ScriptRunConfig
script_config = ScriptRunConfig(
    source_directory='MLfolder',  # This should be the relative path to your source directory
    script='training_script.py',  # This should be the script name inside the source directory
    arguments=['--data-path', 'data/train-data.csv'],  # Specify any arguments your script needs
    environment=env
)

# Create and submit the experiment
experiment = Experiment(workspace=ws, name='MLscript')
run = experiment.submit(config=script_config)

# Monitor the run
logging.info("Run ID: {}".format(run.id))
logging.info("Experiment Name: {}".format(run.experiment.name))

run.wait_for_completion(show_output=True)
