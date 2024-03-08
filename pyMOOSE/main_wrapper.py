import os
import sys

def main():
    # Path configuration
    script_directory = os.path.dirname(os.path.realpath(__file__))
    base_directory = script_directory  # Assuming the data is processed in the script's directory

    # Functions mapping
    operations = {
        "1": {
            "title": "Generate and Save Contours",
            "function": "generate_and_save_contours",
            "args": [base_directory, [50.0, 100.0, 150.0]]
        },
        "2": {
            "title": "Plot Variables Across Timesteps",
            "function": "plot_variables_across_timesteps",
            "args": [base_directory]
        },
        "3": {
            "title": "Plot Variables Over Line Combined",
            "function": "plot_variables_over_line_combined",
            "args": [base_directory, [50.0, 100.0, 150.0], ['disp', 'eta', 'pot', 'w', 'sigma11_aux', 'sigma22_aux']]
        },
        # Add other operations here following the same structure
    }

    while True:
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
            globals()[operation['function']](*operation['args'])
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
