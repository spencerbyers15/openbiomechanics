import ezc3d
import pprint
import numpy as np
import os
import sys
from scipy.interpolate import interp1d
import time
import pandas as pd

# Loop through all the c3d files in a directory

base_path = r'D:\GitHub\openbiomechanics\baseball_pitching\data\c3d'

# Get all the directories in the base path
directories = os.listdir(base_path)

# Loop through all the directories  
for directory in directories:
    # now have to loop through the next subdirectory which is the individual pitcher folders
    pitcher_path = os.path.join(base_path, directory)  

    # Get all the files in the pitcher_path
    files = os.listdir(pitcher_path)
    
    # Loop through all the files in the directory
    for file in files:
        # delete previously made csv files
        if file.endswith('.csv'):
            os.remove(os.path.join(pitcher_path, file))

        # Load the C3D file
        elif file.endswith('.c3d'):

            if 'model' in file:
                continue
            else:
                c3d_path = os.path.join(base_path, directory, file)
                c3d = ezc3d.c3d(c3d_path)
                
                # Get the data points
                data_points_xyz = c3d['data']['points']
                
                # Get the labels for the points
                labels = c3d['parameters']['POINT']['LABELS']['value']

                # print(data_points_xyz.shape)
                # Get the analog signals
                analog_signals = c3d['data']['analogs']
                # print(analog_signals.shape)
           
                analog_labels = c3d['parameters']['ANALOG']['LABELS']['value']
                
                # Get the original time points
                original_time_points = np.arange(data_points_xyz.shape[2])
                
                # Define the new time points for upsampling
                upsample_factor = int(analog_signals.shape[2] / data_points_xyz.shape[2])
                new_time_points = np.linspace(0, data_points_xyz.shape[2] - 1, data_points_xyz.shape[2] * upsample_factor)

                # Upsample the data points using linear interpolation
                upsampled_data_points_xyz = np.zeros((data_points_xyz.shape[0], data_points_xyz.shape[1], len(new_time_points)))
                for i in range(data_points_xyz.shape[0]):
                    for j in range(data_points_xyz.shape[1]):
                        interp_func = interp1d(original_time_points, data_points_xyz[i, j, :], kind='linear')
                        upsampled_data_points_xyz[i, j, :] = interp_func(new_time_points)
              
                # Print the upsampled data shapes
                """
                print(f"Upsampled data points shape for {file}: {upsampled_data_points_xyz.shape}")
                print(f"If 0 there is a match for {file}: {upsampled_data_points_xyz.shape[2] - analog_signals.shape[2]}") 
                """

                # Lets chuck all of this data into a pandas dataframe, with columns being labels from the xyz labels and analog labels and rows being the time points

                # First make a list for the column names

                column_names = []
                for label in labels:
                    # print(label)
                    column_names.append(label+ '_x')
                    column_names.append(label+ '_y')
                    column_names.append(label+ '_z')
                for label in analog_labels:
                    # print(label)
                    column_names.append(label)

                # Now make a list for the rows
                rows = []

                # first row should be the upsampled_data_points_xyz[0 (corresponding to x), 0 (corresponding to first label), : (all time points)]
                # second row should be the upsampled_data_points_xyz[1 (corresponding to y), 0 (corresponding to first label), : (all time points)]
                # third row should be the upsampled_data_points_xyz[2 (corresponding to z), 0 (corresponding to first label), : (all time points)]
                # fourth row should be the upsampled_data_points_xyz[0 (corresponding to x), 1 (corresponding to second label), : (all time points)]

                for i in range(upsampled_data_points_xyz.shape[1]):
                    for j in range(upsampled_data_points_xyz.shape[0]):
                        if j == 3:
                            continue
                        else:
                            data = upsampled_data_points_xyz[j, i, :]
                            # print(data.shape)
                            # time.sleep(0.1)

                            rows.append(data)
                
                for i in range(analog_signals.shape[1]):
                    data = analog_signals[0, i, :]
                    # print(data.shape)
                    # time.sleep(0.1)
                    rows.append(data)

                # make a dataframe with rows and columns
                
                # Ensure all arrays have the same shape
                assert all(arr.shape == rows[0].shape for arr in rows)

                dataframe_arrays = np.vstack(rows).T

                # print(len(rows), len(column_names))
                # drop ".c3d" from the file name
                file_name = file.split('.')[0]
                
                pd.DataFrame(dataframe_arrays, columns=column_names).to_csv(os.path.join(pitcher_path, f'{file_name}.csv'), index=False)
        