import mne
import json
import os

def convert_edf_to_json(edf_file):
    raw = mne.io.read_raw_edf(edf_file)
    data = raw.to_data_frame()

    # Convert to dictionary
    data_dict = data.to_dict(orient='list')

    # Prepare JSON file name
    json_file = os.path.splitext(edf_file)[0] + '.json'

    # Write data to JSON file
    with open(json_file, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print(f'Converted {edf_file} to {json_file}')

def convert_all_edf_to_json(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.edf'):
            convert_edf_to_json(os.path.join(directory, filename))

if __name__ == '__main__':
    # Replace 'directory_path' with the path to your directory containing EDF files
    directory_path = './'  # Current directory in this example
    convert_all_edf_to_json(directory_path)
