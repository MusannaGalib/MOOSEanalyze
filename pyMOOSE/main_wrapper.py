import os
import sys



#sys.path.append('D:\\Backup_31_July_2022\\Research\\Research\\pyMOOSE')



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
                         plot_variables_over_line_combined_with_contour,)
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

    # Executing all functions in sequence
    print("Executing all operations...")
    find_and_process_files(base_directory, specific_times=specific_times)
    plot_variables_across_timesteps(base_directory)
    plot_variables_over_line_combined(base_directory, specific_times, var_names)
    plot_variables_over_line_each_timestep_separately(base_directory, specific_times, var_names)
    generate_and_save_contours(base_directory, specific_times)
    plot_contours_from_csv(base_directory)
    plot_variables_over_line_combined_with_contour(base_directory, specific_times, var_names)

    print("All operations completed successfully.")

if __name__ == "__main__":
    main()
