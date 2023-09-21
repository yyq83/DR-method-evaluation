import argparse
import pandas as pd
import numpy as np

# Function to generate the final CSV file from origin and pre CSV files
def generate_final_csv(file_path):
    # Create an empty DataFrame with columns for 'origin', 'pre', and 'file_name'
    final_data = pd.DataFrame(columns=['origin', 'pre', 'file_name'])

    # Loop through each of the 10 folds
    for i in range(1, 11):
        # Read the 'origin' data from origin{i}.csv file
        with open(f'{file_path}/origin{i}.csv', 'r') as f:
            csv = pd.read_csv(f, header=None)
            origin_data = csv.values

        # Read the 'pre' data from pre{i}.csv file
        with open(f'{file_path}/pre{i}.csv', 'r') as f:
            csv = pd.read_csv(f, header=None)
            pre_data = csv.values

        origin = []
        pre = []

        # Flatten the data from 2D arrays to 1D lists
        for line in origin_data:
            for item in line:
                origin.append(item)

        for line in pre_data:
            for item in line:
                pre.append(item)

        # Convert lists to NumPy arrays
        origin_array = np.array(origin)
        pre_array = np.array(pre)

        # Create a 'file_name' feature with the name 'origin{i}' for each fold
        file_name = [f'origin{i}'] * len(origin_array)

        # Create a DataFrame with 'origin', 'pre', and 'file_name' columns for the current fold
        df = pd.DataFrame({'origin': origin_array, 'pre': pre_array, 'file_name': file_name})

        # Concatenate the current fold's DataFrame to the final_data
        final_data = pd.concat([final_data, df], ignore_index=True)

    # Save all the data as 'final_CV_folds.csv'
    final_data.to_csv(f'{file_path}/final_CV_folds.csv', index=False, header=True)

if __name__ == "__main__":
    # Initialize argparse to accept a file path argument
    parser = argparse.ArgumentParser(description='Generate final.csv from origin and pre CSV files.')
    parser.add_argument('--file_path', type=str, help='Path to the directory containing origin and pre CSV files')
    args = parser.parse_args()

    # Call the generate_final_csv function with the provided file path
    generate_final_csv(args.file_path)
