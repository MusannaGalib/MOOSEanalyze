#!/usr/bin/env pvpython
import os
import pandas as pd
import matplotlib.pyplot as plt
from paraview.simple import *

'$env:PATH += "D:/Backup_31_July_2022/Research/Research/MOOSE/ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64/ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64/bin/"'


def process_file(input_file):
    base_dir = os.path.dirname(input_file)
    folder_name = os.path.basename(base_dir)
    output_file = os.path.join(base_dir, f'{folder_name}.csv')

    # create a new 'IOSS Reader'
    input_oute = IOSSReader(registrationName='input_out.e', FileName=[input_file])
    input_oute.ElementBlocks = ['block_0']
    input_oute.NodeBlockFields = ['disp', 'eta', 'pot', 'w']
    input_oute.ElementBlockFields = ['G', 'c', 'dG/deta', 'dG/dpot', 'dG/dw', 'extra_stress_00', 'extra_stress_01', 'extra_stress_02', 'extra_stress_10', 'extra_stress_11', 'extra_stress_12', 'extra_stress_20', 'extra_stress_21', 'extra_stress_22', 'sigma11_aux', 'sigma12_aux', 'sigma22_aux']
    input_oute.NodeSets = []
    input_oute.SideSets = []

    # Assume rest of the processing here...

    # Save data to the same directory as input file
    SaveData(output_file, proxy=input_oute, 
             WriteTimeSteps=1,
             WriteTimeStepsSeparately=1,
             ChooseArraysToWrite=1,
             PointDataArrays=['disp', 'eta', 'pot', 'w'],
             CellDataArrays=[ 'sigma11_aux', 'sigma12_aux', 'sigma22_aux'],
             FieldDataArrays=['ETA', 'memory', 'num_lin_it', 'num_nonlin_it'],
             Precision=12, UseScientificNotation=1,AddTimeStep=1,AddTime=1)

def find_and_process_files(base_directory, filename='input_out.e'):
    for root, dirs, files in os.walk(base_directory):
        if filename in files:
            input_file = os.path.join(root, filename)
            print(f"Processing file: {input_file}")
            process_file(input_file)



def plot_data_from_csv(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Check if required columns exist in the DataFrame
    required_columns = ["Points:0", "Points:1", "eta", "pot", "w"]
    if not all(column in df.columns for column in required_columns):
        print(f"Missing required columns in {csv_file}. Skipping plot.")
        return

    # Plot settings
    plt.figure(figsize=(10, 6))

    # Plotting eta, pot, and w against Points:0 (x-axis) and Points:1 (y-axis)
    for column in ["eta", "pot", "w"]:
        plt.scatter(df["Points:0"], df["Points:1"], c=df[column], label=column, alpha=0.5)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(f"Plot of {column} against x and y")
        plt.colorbar(label=column)
        plt.legend()
        plt.grid(True)

        # Save the plot to the same directory as the CSV file
        output_plot_path = os.path.join(os.path.dirname(csv_file), f"{column}_plot.png")
        plt.savefig(output_plot_path)
        plt.clf()  # Clear the figure for the next plot

def find_and_plot_files(base_directory):
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".csv"):
                csv_file_path = os.path.join(root, file)
                print(f"Creating plot for: {csv_file_path}")
                plot_data_from_csv(csv_file_path)     

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.realpath(__file__))
    find_and_process_files(script_directory)
    find_and_plot_files(script_directory)

#cd D:/Backup_31_July_2022/Research/Research/MOOSE/ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64/ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64/bin/
#./PvPython C:/Users/galibubc/Downloads/MOOSE/MOOSE_post_processsing_paraview.py