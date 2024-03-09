import os
import sys

# Import your package functions here, e.g.,
# from your_package_name import generate_and_save_contours, plot_variables_across_timesteps, plot_variables_over_line_combined
from pyMOOSE import (generate_and_save_contours, find_and_process_files,
                     plot_variables_across_timesteps, plot_variables_over_line_combined,
                     plot_variables_over_line_each_timestep_separately,
                     plot_contours_from_csv, plot_variables_over_line_combined_with_contour)

def main():
    # Initial path configuration is moved inside the while loop to allow for repeated adjustments

    # Functions mapping
    operations = {
        "1": {
            "title": "Generate and Save Contours",
            "function": generate_and_save_contours,
            "args": [None, [50.0, 100.0, 150.0]]  # Placeholder for base_directory which will be set later
        },
        "2": {
            "title": "Plot Variables Across Timesteps",
            "function": plot_variables_across_timesteps,
            "args": [None]  # Placeholder for base_directory which will be set later
        },
        "3": {
            "title": "Plot Variables Over Line Combined",
            "function": plot_variables_over_line_combined,
            "args": [None, [50.0, 100.0, 150.0], ['disp', 'eta', 'pot', 'w', 'sigma11_aux', 'sigma22_aux']]  # Placeholder for base_directory which will be set later
        },
        # Add other operations here following the same structure
    }

    while True:
        # Path configuration - moved here to allow user to redefine paths each time the loop starts
        parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        default_script_directory = os.path.join(parent_directory, "Data")
        default_base_directory = os.path.join(parent_directory, "Data")

        user_input = input(f"Press Enter to use the default directory ({default_base_directory}) or enter a new path: ").strip()
        if user_input:
            script_directory = user_input
            base_directory = user_input
            print(f"Using user-specified directory: {user_input}")
        else:
            script_directory = default_script_directory
            base_directory = default_base_directory
            print(f"Using default directory: {base_directory}")

        # Update args in operations with the chosen base_directory
        for operation in operations.values():
            operation['args'][0] = base_directory  # Update the first argument with the current base_directory

        # The rest of your existing code for operations selection
        print("\nSelect the operation you want to perform:")
        for key, operation in operations.items():
            print(f"{key}. {operation['title']}")
        print("0. Exit")

        choice = input("\nEnter your choice: ")
        if choice == "0":
            print("Exiting the program.")
            break

        operation = operations.get(choice)
        if operation:
            # Dynamically call the function based on the user's choice
            operation['function'](*operation['args'])
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
