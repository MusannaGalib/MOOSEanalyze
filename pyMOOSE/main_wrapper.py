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
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.util import numpy_support
from vtk.util.numpy_support import vtk_to_numpy



#sys.path.append('D:\\Backup_31_July_2022\\Research\\Research\\pyMOOSE')

#$Env:PATH += ";D:\Backup_31_July_2022\Research\Research\MOOSE\ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64\ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64\bin"


# Assuming main_wrapper.py is in the pyMOOSE\pyMOOSE directory
# and you want to import modules from pyMOOSE (one level up)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now try to import your modules
try:
    from pyMOOSE import (find_and_process_files,
                         plot_variables_across_timesteps,
                         plot_variables_over_line_combined,
                         plot_variables_over_line_each_timestep_separately,
                         generate_and_save_contours,
                         plot_contours_from_csv,
                         plot_variables_over_line_combined_with_contour,
                         compare_folders_at_time,
                         compare_two_contour_plots,
                         plot_sigma22_aux_over_line_combined_top_bottom,
                         plot_sigma22_aux_over_line_combined_left_right,
                         calculate_eta_distance_with_time,
                         plot_points_vs_time)

except ModuleNotFoundError:
    print("Failed to import pyMOOSE. Ensure the package is correctly placed within the project.")
    sys.exit(1)


    


def main():
    # Initial path configuration
    parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    default_base_directory = os.path.join(parent_directory, "Data")

    # Ask the user for a directory path or use the default
    user_input = input(f"Press Input to use the default directory ({default_base_directory}) or enter a new path: ").strip()
    base_directory = user_input if user_input else default_base_directory
    print(f"Using directory: {base_directory}")


    # Specific times and variables might need to be adjusted based on your requirements
    specific_times = [50.0, 100.0, 150.0]
    var_names = ['disp', 'eta', 'pot', 'w', 'sigma11_aux', 'sigma22_aux']

    # Default specific times and variable names
    #default_specific_times = "50.0, 100.0, 150.0"
    #default_var_names = "disp, eta, pot, w, sigma11_aux, sigma22_aux"

    # Ask the user for custom specific times or use the default
    #specific_times_input = input(f"Enter specific times separated by commas [{default_specific_times}] (press enter to use default): ").strip()
    #specific_times = [float(time.strip()) for time in specific_times_input.split(",")] if specific_times_input else [float(time.strip()) for time in default_specific_times.split(",")]

    # Ask the user for custom variable names or use the default
    #var_names_input = input(f"Enter variable names separated by commas [{default_var_names}] (press enter to use default): ").strip()
    #var_names = [name.strip() for name in var_names_input.split(",")] if var_names_input else [name.strip() for name in default_var_names.split(",")]


    # Executing all functions in sequence
    #print("Executing all operations...")
    #find_and_process_files(base_directory, specific_times=specific_times)
    #plot_variables_across_timesteps(base_directory)
    #plot_variables_over_line_combined(base_directory, specific_times, var_names)
    #plot_variables_over_line_each_timestep_separately(base_directory, specific_times, var_names)
    #generate_and_save_contours(base_directory, specific_times)
    #plot_contours_from_csv(base_directory)
    #plot_variables_over_line_combined_with_contour(base_directory, specific_times, var_names)
    #plot_sigma22_aux_over_line_combined_top_bottom(base_directory, specific_times, folder_names)
    #calculate_eta_distance_with_time(base_directory, folder_names=None)
    #plot_points_vs_time(base_directory, folder_names=None)


    folder_names = ['Bare_Zn', 'Bare_Zn_i_5.0_3', 'MLD_Alucone_eigen_0.5_i_5']
    for specific_time in specific_times:
        compare_folders_at_time(base_directory, specific_times, var_names, folder_names)
        compare_two_contour_plots(base_directory, specific_time, folder_names)
        plot_sigma22_aux_over_line_combined_top_bottom(base_directory, specific_times, folder_names)
        plot_sigma22_aux_over_line_combined_left_right(base_directory, specific_times, folder_names)
        calculate_eta_distance_with_time(base_directory, folder_names)
        plot_points_vs_time(base_directory, folder_names)

    # Or, call without specifying folder_names to auto-detect and process all folders
    #compare_folders_at_time(base_directory, specific_times, var_names)    

    print("All operations completed successfully.")

if __name__ == "__main__":
    main()
