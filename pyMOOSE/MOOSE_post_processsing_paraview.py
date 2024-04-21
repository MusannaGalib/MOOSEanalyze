#!/usr/bin/env pvpython
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import interp1d
from scipy.interpolate import griddata
import numpy as np
import re
import csv
import glob 
from paraview.simple import *
import vtk
from vtkmodules.vtkFiltersCore import vtkCellDataToPointData
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.util import numpy_support
from vtk.util.numpy_support import vtk_to_numpy

'$env:PATH += "D:/Backup_31_July_2022/Research/Research/MOOSE/ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64/ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64/bin/"'


def process_file(input_file, specific_times):
    base_dir = os.path.dirname(input_file)
    folder_name = os.path.basename(base_dir)
    
    # Load the data with IOSSReader
    input_oute = IOSSReader(FileName=[input_file])
    # Important to apply initial update to load metadata including timesteps
    input_oute.UpdatePipelineInformation()

    animationScene = GetAnimationScene()
    # Ensure animation scene is updated to reflect the data's time extent
    animationScene.UpdateAnimationUsingDataTimeSteps()
    
    for time_value in specific_times:
        # Set the desired time for the animation scene
        animationScene.AnimationTime = time_value
        # Force an update of the pipeline to ensure data corresponds to the set time
        input_oute.UpdatePipeline(time_value)

        # Define output file name, including the time to differentiate outputs
        output_file = os.path.join(base_dir, f'{folder_name}_Time_{time_value}.csv')

        # Save the data for the current time
        SaveData(output_file, proxy=input_oute,
                 WriteTimeSteps=0,
                 ChooseArraysToWrite=1,
                 PointDataArrays=['disp', 'eta', 'pot', 'w'],
                 CellDataArrays=['sigma11_aux', 'sigma12_aux', 'sigma22_aux'],
                 FieldDataArrays=['ETA', 'memory', 'num_lin_it', 'num_nonlin_it'],
                 Precision=12, UseScientificNotation=1)

def find_and_process_files(base_directory, filename='input_out.e', specific_times=None):
    for root, dirs, files in os.walk(base_directory):
        if filename in files:
            input_file = os.path.join(root, filename)
            print(f"Processing file: {input_file}")
            process_file(input_file, specific_times=specific_times)



def extract_timestamp(filename):
    """
    Extracts the numerical timestamp from a filename with the pattern 'Bare_Zn_Time_50.0.csv'
    Ensures that '_contour' is not part of the filename.
    """
    # The following regex ends with (?=\.csv$) which asserts that '.csv' is at the end of the string.
    match = re.search(r'Time_(\d+\.?\d*)(?=\.csv$)', filename)
    if match:
        return float(match.group(1))
    return 0  # Default to 0 if no number is found


def plot_variables_across_timesteps(base_directory):
    for root, _, files in os.walk(base_directory):
        
        # Define the pattern to match files like 'Bare_Zn_Time_50.0.csv' but not 'Bare_Zn_Time_50.0_contour.csv'
        pattern = re.compile(r'Bare_Zn_Time_\d+\.\d+\.csv$')

        csv_files = [file for file in files if pattern.search(file)]
        if not csv_files:
            continue  # Skip directories without CSV files

        # Sort files by extracted timestamp to maintain correct time order
        csv_files.sort(key=extract_timestamp)

        variables = ["eta", "pot", "w"]
        data_for_variables = {var: [] for var in variables}

        for csv_file in csv_files:
            csv_path = os.path.join(root, csv_file)
            df = pd.read_csv(csv_path)
            for var in variables:
                if var in df.columns:
                    data_for_variables[var].append((df["Points:0"], df["Points:1"], df[var], os.path.splitext(csv_file)[0]))

        for var, datasets in data_for_variables.items():
            if datasets:
                n = len(datasets)
                fig, axs = plt.subplots(1, n, figsize=(5*n, 4), sharey=True)
                if n == 1:
                    axs = [axs]  # Make axs iterable for a single subplot

                for i, dataset in enumerate(datasets):
                    cmap = plt.get_cmap('coolwarm')
                    x, y, values, label = dataset
                    # Extract just the numerical time part from the label
                    time_match = re.search(r'Time_(\d+\.\d+)', label)
                    if time_match:
                        # If a match is found, use only the time part for the title
                        time_label = f"{time_match.group(1)} sec"
                    else:
                        # If no match is found, use the full label
                        time_label = label
                    axs[i].set_title(time_label)
                    scatter = axs[i].scatter(x, y, c=values, alpha=0.5, cmap=cmap)
                    fig.colorbar(scatter, ax=axs[i], label=var)

                for ax in axs:
                    ax.set_xlabel("x")
                axs[0].set_ylabel("y")
                
                folder_name = os.path.basename(root)
                plt.suptitle(f"{folder_name}")

                output_plot_path = os.path.join(root, f"{var}_{folder_name}.png")
                print(f"Plotting and saving {var} for {folder_name} at {output_plot_path}")
                plt.savefig(output_plot_path)
                plt.close()

                print(f"Saved plot for {var} at: {output_plot_path}")






def setup_plot_over_line(input_oute, time_value):
    """
    Set up and return a configured PlotOverLine filter for given input data and time step,
    along with the start and end points of the line.
    """
    # Define start and end points of the line
    point1 = [0.0, 100.0, 0.0]
    point2 = [199.99999862765003, 100.0, 0.0]

    # Create the PlotOverLine filter with the input data
    plotOverLine = PlotOverLine(Input=input_oute,
                                Point1=point1,
                                Point2=point2)
    
    # Set the animation time to the specified value and update the pipeline
    animationScene = GetAnimationScene()
    animationScene.AnimationTime = time_value
    plotOverLine.UpdatePipeline(time_value)
    
    return plotOverLine, point1, point2



def fetch_plot_data(plotOverLine, var_name):
    """
    Fetch data for the specified variable from the PlotOverLine filter and return the arc length and variable data.
    """
    # Fetch the result of PlotOverLine
    line_data = servermanager.Fetch(plotOverLine)
    
    # Get the arc length (assuming it's stored in a point data array named "arc_length")
    arc_length = np.array(line_data.GetPointData().GetArray("arc_length"))
    
    # Get the data for the specified variable
    var_data = np.array(line_data.GetPointData().GetArray(var_name))
    
    return arc_length, var_data


def plot_variables_over_line_each_timestep_separately(base_directory, specific_times, var_names):
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith("input_out.e"):
                input_file_path = os.path.join(root, file)
                print(f"Processing file: {input_file_path}")

                input_oute = IOSSReader(FileName=[input_file_path])
                input_oute.UpdatePipeline()

                for time_value in specific_times:
                    plotOverLine, point1, point2 = setup_plot_over_line(input_oute, time_value)
                    
                    # Determine layout for subplots
                    num_vars = len(var_names)
                    rows = 2
                    cols = np.ceil(num_vars / rows).astype(int)
                    
                    fig, axs = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
                    axs = axs.flatten()  # Flatten the array to make indexing easier

                    for i, var_name in enumerate(var_names):
                        arc_length, var_data = fetch_plot_data(plotOverLine, var_name)

                        axs[i].plot(arc_length, var_data, label=f'{var_name} at {time_value} sec')
                        axs[i].set_xlabel('Distance along line')
                        axs[i].set_ylabel(var_name)
                        axs[i].legend()
                        #axs[i].set_title(f"{var_name} Across Line")

                    # If there are any leftover axes, disable them
                    for j in range(i + 1, len(axs)):
                        axs[j].axis('off')
                    
                    plt.suptitle(f"Variables Across Line at {time_value} sec from Point1 ({point1[0]}, {point1[1]}) to Point2 ({point2[0]}, {point2[1]})")
                    
                    # Save the plot
                    output_plot_path = os.path.join(root, f"variables_over_line_{time_value}sec.png")
                    plt.savefig(output_plot_path)
                    plt.close()
                    print(f"Saved: {output_plot_path}")
                    

def plot_variables_over_line_combined(base_directory, specific_times, var_names):
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith("input_out.e"):
                input_file_path = os.path.join(root, file)
                print(f"Processing file: {input_file_path}")

                # Prepare the data structure for holding variable data across all times
                data_across_times = {var_name: [] for var_name in var_names}

                input_oute = IOSSReader(FileName=[input_file_path])
                input_oute.UpdatePipeline()

                # Collect data for each time step
                for time_value in specific_times:
                    plotOverLine, point1, point2 = setup_plot_over_line(input_oute, time_value)
                    for var_name in var_names:
                        arc_length, var_data = fetch_plot_data(plotOverLine, var_name)
                        data_across_times[var_name].append((time_value, arc_length, var_data))

                # Determine layout for subplots
                num_vars = len(var_names)
                rows = 2  # Specify the number of rows you want for subplots
                cols = np.ceil(num_vars / rows).astype(int)  # Calculate the number of columns needed

                fig, axs = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), constrained_layout=True)
                axs = axs.flatten()  # Flatten the array to make indexing easier

                for i, (var_name, time_series) in enumerate(data_across_times.items()):
                    for time_value, arc_length, var_data in time_series:
                        axs[i].plot(arc_length, var_data, label=f'{time_value} sec')
                    axs[i].set_xlabel('Distance along line')
                    axs[i].set_ylabel(var_name)
                    axs[i].legend()
                    axs[i].set_title(f"{var_name} Across Line")

                # If there are any leftover axes, disable them
                for j in range(i + 1, len(axs)):
                    axs[j].axis('off')

                plt.suptitle(f"Variables Across Line from Point1 ({point1[0]}, {point1[1]}) to Point2 ({point2[0]}, {point2[1]})")
                
                # Save the plot
                output_plot_path = os.path.join(root, f"variables_over_line_combined.png")
                plt.savefig(output_plot_path)
                plt.close()
                print(f"Saved: {output_plot_path}")








def generate_and_save_contours(base_directory, specific_times, iso_value=0.5):
    for root, dirs, files in os.walk(base_directory):
        for file_name in files:
            if file_name.lower() == 'input_out.e':
                input_file_path = os.path.join(root, file_name)
                input_oute = OpenDataFile(input_file_path)
                
                for time_value in specific_times:
                    animationScene = GetAnimationScene()
                    animationScene.AnimationTime = time_value
                    animationScene.UpdateAnimationUsingDataTimeSteps()
                    
                    contour = Contour(Input=input_oute)
                    contour.ContourBy = ['POINTS', 'eta']
                    contour.Isosurfaces = [iso_value]
                    contour.UpdatePipeline(time_value)
                    
                    csv_file_name = f"{os.path.basename(root)}_Time_{time_value}_contour.csv"
                    csv_file_path = os.path.join(root, csv_file_name)
                    
                    SaveData(csv_file_path, proxy=contour, PointDataArrays=['eta'], Precision=12)
                    print(f"Saved contour data for time {time_value} to {csv_file_path}")
                    
                    Delete(contour)

def plot_contours_from_csv(base_directory):
    # Walk through all subdirectories of the base directory
    for root, dirs, files in os.walk(base_directory):
        # Check if there are any contour CSV files in this directory
        csv_files = [os.path.join(root, f) for f in files if f.endswith('_contour.csv')]
        
        if not csv_files:
            # Skip directories without any contour CSV files
            continue
        
        # Initialize a figure for this directory
        fig, ax = plt.subplots(figsize=(5, 4))
        
        plot_title = ""
        
        for csv_file in csv_files:
            data = pd.read_csv(csv_file)
            # Attempt to extract the time value safely
            try:
                time_value = os.path.basename(csv_file).split('_Time_')[1].split('_')[0]
                legend_label = f"{time_value} sec"
            except IndexError:
                legend_label = "Invalid Time"
            
            ax.plot(data['Points:0'], data['Points:1'], label=legend_label)
            
            if not plot_title:
                plot_title_parts = os.path.basename(csv_file).split('_Time_')
                if plot_title_parts:
                    plot_title = plot_title_parts[0]
        
        ax.set_title(plot_title)
        ax.set_xlim(0, 200)
        ax.set_ylim(0, 200)
        ax.legend()
        ax.grid(False)
        
        output_filename = os.path.basename(root) + "_combined_contour_plot.png"
        output_filepath = os.path.join(root, output_filename)
        plt.savefig(output_filepath)
        plt.close()
        print(f"Saved combined contour plot to {output_filepath}")



def plot_contours_from_csv_for_combined_plot(root, ax):
    csv_files = [os.path.join(root, f) for f in os.listdir(root) if f.endswith('_contour.csv')]
    for csv_file in csv_files:
        data = pd.read_csv(csv_file)
        time_value = os.path.basename(csv_file).split('_Time_')[1].split('_')[0]
        ax.plot(data['Points:0'], data['Points:1'], label=f"{time_value} sec")
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 200)
    ax.legend()
    ax.set_title('Contour Plot')
    ax.grid(False)

def plot_variables_over_line_combined_with_contour(base_directory, specific_times, var_names):
    for root, dirs, files in os.walk(base_directory):
        if "input_out.e" in files:
            input_file_path = os.path.join(root, "input_out.e")
            print(f"Processing file: {input_file_path}")

            # Prepare the data structure for holding variable data across all times
            data_across_times = {var_name: [] for var_name in var_names}

            # Initialize the figure with one additional subplot for the contour
            total_plots = len(var_names) + 1
            cols = 3  # Set this to the number of columns you want
            rows = (total_plots + cols - 1) // cols  # Calculate the number of rows needed
            fig, axs = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), constrained_layout=True)
            axs = axs.flatten()  # Flatten the array to make indexing easier

            # Generate the contour plot
            contour_ax = axs[0]
            plot_contours_from_csv_for_combined_plot(root, contour_ax)

            # Now plot the variables over line
            input_oute = IOSSReader(FileName=[input_file_path])
            input_oute.UpdatePipeline()

            # Collect data for each time step and plot
            for time_value in specific_times:
                plotOverLine, point1, point2 = setup_plot_over_line(input_oute, time_value)
                for var_name in var_names:
                    arc_length, var_data = fetch_plot_data(plotOverLine, var_name)
                    data_across_times[var_name].append((time_value, arc_length, var_data))

            for i, var_name in enumerate(var_names, start=1):
                for time_value, arc_length, var_data in data_across_times[var_name]:
                    axs[i].plot(arc_length, var_data, label=f'{time_value} sec')
                axs[i].set_xlabel('Distance along line')
                axs[i].set_ylabel(var_name)
                axs[i].legend()
                axs[i].set_title(f"{var_name} Across Line")

            # Turn off any unused axes
            for j in range(len(var_names) + 1, len(axs)):
                axs[j].axis('off')

            plt.suptitle(f"Analysis for {root}")
            output_plot_path = os.path.join(root, "analysis_combined_with_contour.png")
            plt.savefig(output_plot_path)
            plt.close()
            print(f"Saved: {output_plot_path}")



def auto_detect_folders(base_directory):
    """Automatically detect and return a list of folders within the given base directory."""
    return [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]

def compare_folders_at_time(base_directory, specific_times, var_names, folder_names=None):
    # If folder_names is not provided or is an empty list, auto-detect all folders in the base directory
    if folder_names is None:
        folder_names = auto_detect_folders(base_directory)
    
    # Process each folder
    for folder_name in folder_names:
        folder_path = os.path.join(base_directory, folder_name)
        # Verify that the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder does not exist: {folder_path}. Skipping...")
            continue
        print(f"Processing folder: {folder_name}")
        
        for time_value in specific_times:
            print(f"Comparing at {time_value} seconds...")

            # Initialize the figure with one additional subplot for the contour
            total_plots = len(var_names) + len(folder_names)  # One plot for each variable per folder + contour per folder
            cols = 3  # Adjust the number of columns as needed
            rows = (total_plots + cols - 1) // cols  # Calculate the number of rows needed
            fig, axs = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), constrained_layout=True)
            axs = axs.flatten()  # Flatten the array to make indexing easier

            # Data structure for holding variable data from different folders
            data_from_folders = {folder_name: {var_name: [] for var_name in var_names} for folder_name in folder_names}

            plot_index = 0  # To manage subplot indices

            for folder_name in folder_names:
                folder_path = os.path.join(base_directory, folder_name)
                input_file_path = os.path.join(folder_path, "input_out.e")
                print(f"Processing file: {input_file_path} for folder: {folder_name}")

                # Generate the contour plot for each folder
                contour_ax = axs[plot_index]
                plot_contours_from_csv_for_combined_plot(folder_path, contour_ax)
                contour_ax.set_title(f"Contour: {folder_name}")
                plot_index += 1

                # Load the data for the specified time step
                input_oute = IOSSReader(FileName=[input_file_path])
                input_oute.UpdatePipeline()

                plotOverLine, point1, point2 = setup_plot_over_line(input_oute, time_value)
                for var_name in var_names:
                    arc_length, var_data = fetch_plot_data(plotOverLine, var_name)
                    data_from_folders[folder_name][var_name] = (arc_length, var_data)

            # Now plot the variables for each folder
            for var_name in var_names:
                for folder_name in folder_names:
                    arc_length, var_data = data_from_folders[folder_name][var_name]
                    axs[plot_index].plot(arc_length, var_data, label=f'{folder_name}')
                axs[plot_index].set_xlabel('Distance along line')
                axs[plot_index].set_ylabel(var_name)
                axs[plot_index].legend()
                axs[plot_index].set_title(f"{var_name} Comparison at {time_value} sec")
                plot_index += 1

            # Turn off any unused axes
            for j in range(plot_index, len(axs)):
                axs[j].axis('off')

            plt.suptitle("Variable Comparison Across Different Folders with Contours")
            output_plot_path = os.path.join(base_directory, f"variable_contour_comparison_at_{time_value}_sec.png")
            plt.savefig(output_plot_path)
            plt.close()
            print(f"Saved: {output_plot_path}")









def plot_contours_from_csv_rotated(root, ax):
    csv_files = [os.path.join(root, f) for f in os.listdir(root) if f.endswith('_contour.csv')]
    for csv_file in csv_files:
        data = pd.read_csv(csv_file)
        time_value = os.path.basename(csv_file).split('_Time_')[1].split('_')[0]
        ax.plot(data['Points:1'], data['Points:0'], label=f"{time_value} sec")
    ax.set_ylim(0, 200)
    ax.legend(loc='upper right', fontsize=12)
    ax.set_xlabel('um', fontsize=14)
    #ax.set_ylabel('Distance along line', fontsize=14)
    ax.grid(False)
    # Increase the font size for the tick labels
    ax.tick_params(labelsize=12)

def compare_two_contour_plots(base_directory, specific_time, folder_names):
    if len(folder_names) < 2:
        print("Need at least two folder names to compare.")
        return
    
    # Create a figure
    fig = plt.figure(figsize=(6, 4), constrained_layout=False)

    # Manually set the positions of the subplots
    ax1 = fig.add_axes([0, 0, 0.5, 1])  # Left plot from 0% to 50% of the figure width
    ax2 = fig.add_axes([0.5, 0, 0.5, 1], sharey=ax1)  # Right plot from 50% to 100% of the figure width

    # Turn off the y-ticks for the second plot
    ax2.tick_params(left=False, labelleft=False)

    # Plot the contours for the first two folders
    for i, folder_name in enumerate(folder_names[:2]):
        folder_path = os.path.join(base_directory, folder_name)
        
        if not os.path.exists(folder_path):
            print(f"Folder does not exist: {folder_path}. Skipping...")
            continue
        
        print(f"Processing folder: {folder_name}")
        plot_contours_from_csv_rotated(folder_path, (ax1 if i == 0 else ax2))
        (ax1 if i == 0 else ax2).set_title(f"Contour: {folder_name}")

    # Set labels for the first plot
    ax1.set_ylabel('Distance along line')
    ax1.set_xlabel('Variable of interest')

    # If desired, rotate the x-axis labels for better readability
    for ax in [ax1, ax2]:
        plt.setp(ax.get_xticklabels(), rotation=45)

    # Add a figure title
    #fig.suptitle(f"Contour Comparison at {specific_time} sec")

    # Save the figure
    output_plot_path = os.path.join(base_directory, f"combined_contour_comparison_at_{specific_time}_sec.png")
    fig.savefig(output_plot_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {output_plot_path}")

















def plot_sigma22_aux_over_line_combined(base_directory, specific_times, folder_names, output_directory=None):
    if len(folder_names) < 2:
        print("Need at least two folder names to compare.")
        return
    
    if output_directory is None:
        output_directory = base_directory
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 6), sharex=True)

    for i, folder_name in enumerate(folder_names[:2]):
        folder_path = os.path.join(base_directory, folder_name)
        
        if not os.path.exists(folder_path):
            print(f"Folder does not exist: {folder_path}. Skipping...")
            continue
        
        print(f"Processing folder: {folder_name}")
        plot_sigma22_aux_from_folder(folder_path, specific_times, (ax1 if i == 0 else ax2), (i == 0), ax2)

    ax2.set_xlabel('Distance along line', fontsize=16)  # Increase font size

    plt.tight_layout(pad=0)
    
    # Save the figure as PNG with increased quality and folder names in the file name
    output_plot_path = os.path.join(output_directory, f"sigma22_aux_comparison_{folder_names[0]}_{folder_names[1]}.png")
    plt.savefig(output_plot_path, format='png', bbox_inches='tight', dpi=600)
    plt.close(fig)
    print(f"Saved: {output_plot_path}")


def plot_sigma22_aux_from_folder(folder_path, specific_times, ax, is_top_plot, ax2):
    var_name = 'sigma22_aux'
    for file in os.listdir(folder_path):
        if file.endswith("input_out.e"):
            input_file_path = os.path.join(folder_path, file)
            input_oute = IOSSReader(FileName=[input_file_path])
            input_oute.UpdatePipeline()

            # Collect data for each time step
            for time_value in specific_times:
                plotOverLine, _, _ = setup_plot_over_line(input_oute, time_value)
                arc_length, var_data = fetch_plot_data(plotOverLine, var_name)
                ax.plot(arc_length, var_data, label=f"{time_value} sec")

    ax.set_ylabel(var_name, fontsize=16)  # Increase font size
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))  # Set significant decimal digits
    ax.grid(False)
    ax.tick_params(labelsize=14)
      
    if is_top_plot:
        ax.legend(loc='upper right', fontsize=11)
    else:
        ax.legend(loc='lower right', fontsize=11)
      
    if ax is not ax2:
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)  # Remove ticks and labels on the x-axis









if __name__ == "__main__":
    # Get the directory of the currently executing script and then move up one level
    parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # Point both variables to the "Data" folder inside the parent directory
    script_directory = os.path.join(parent_directory, "Data")
    base_directory = os.path.join(parent_directory, "Data")

    # Get the directory of the currently executing script and run on the folders availabe in the script folder
    #script_directory = os.path.dirname(os.path.realpath(__file__))
    #base_directory = os.path.dirname(os.path.realpath(__file__))

  
    
    # Define specific times of interest
    specific_times = [50.0, 100.0, 150.0]  # Adjust to match exact times in your dataset
    find_and_process_files(script_directory, specific_times=specific_times)
    plot_variables_across_timesteps(script_directory)

    var_names = ['disp', 'eta', 'pot', 'w', 'sigma11_aux', 'sigma22_aux']  # Define the variable names to plot

    plot_variables_over_line_combined(base_directory, specific_times, var_names)
    plot_variables_over_line_each_timestep_separately(base_directory, specific_times, var_names)
    generate_and_save_contours(base_directory, specific_times)
    plot_contours_from_csv(base_directory)
    plot_variables_over_line_combined_with_contour(base_directory, specific_times, var_names)

    # Specify folder names to process only those folders
    folder_names = ['Bare_Zn','MLD_Alucone_eigen_0.5']
    for specific_time in specific_times:
        compare_folders_at_time(base_directory, specific_times, var_names, folder_names)
        compare_two_contour_plots(base_directory, specific_time, folder_names)

    # Or, call without specifying folder_names to auto-detect and process all folders
    # compare_folders_at_time(base_directory, specific_times, var_names)