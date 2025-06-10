import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

# Non-recursive flattening function to handle nested JSON structures. The flattening logic within the loop for layers 
# doesn't have explicit handling for lists within the details. If details is a list, it will directly assign the list 
# to the flat_item with the layer as the key
def flatten_json(json_list):
    """Flattens a list of nested JSON objects, avoiding redundant layer names."""
    flattened_data = []
    for item in json_list:
        flat_item = {}
        source = item.get('_source', {})
        layers = source.get('layers', {})
        for layer, details in layers.items():
            if isinstance(details, dict):
                for key, value in details.items():
                    if layer == key:
                        flat_item[f"{layer}"] = value # Use just the layer name if keys are the same
                    else:
                        flat_item[f"{layer}.{key}"] = value
            else:
                flat_item[layer] = details
        # Include top-level keys if needed
        flat_item['_index'] = item.get('_index')
        flat_item['_type'] = item.get('_type')
        flat_item['_score'] = item.get('_score')
        flattened_data.append(flat_item)
    return flattened_data

# Preprocess the DataFrame to ensure consistent types
# This function will convert any dictionary or list columns to JSON strings
# to avoid issues with mixed types in the DataFrame   
def preprocess_dataframe(df):
    """Ensures all columns in the DataFrame have consistent types."""
    for column in df.columns:
        if df[column].apply(lambda x: isinstance(x, dict)).any():
            # Convert dictionaries to JSON strings
            df[column] = df[column].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)
        elif df[column].apply(lambda x: isinstance(x, list)).any():
            # Convert lists to JSON strings
            df[column] = df[column].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
    return df

def json_to_parquet(json_file_path, parquet_file_path):
    """Reads a JSON file, flattens it, preprocesses the data, and writes to a Parquet file."""
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}")
        return

    flattened_data = flatten_json(data)
    df = pd.DataFrame(flattened_data)

    # Preprocess the DataFrame to handle mixed types
    df = preprocess_dataframe(df)

    try:
        table = pa.Table.from_pandas(df)
        pq.write_table(table, parquet_file_path)
        print(f"Successfully flattened and saved to {parquet_file_path}")
    except Exception as e:
        print(f"Error writing to Parquet: {e}")

def view_parquet_columns(parquet_file_path):
    """Prints the column names of a Parquet file."""
    try:
        table = pq.read_table(parquet_file_path)
        print("Columns in the Parquet file:")
        print(table.schema.names)
    except FileNotFoundError:
        print(f"Error: Parquet file not found at {parquet_file_path}")
    except Exception as e:
        print(f"Error reading Parquet file: {e}")

def process_directory(input_dir, output_dir):
    """Processes all JSON files in the input directory and saves Parquet files in the output directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            json_file_path = os.path.join(input_dir, filename)
            parquet_file_path = os.path.join(output_dir, filename.replace('.json', '.parquet'))
            print(f"Processing {json_file_path}...")
            json_to_parquet(json_file_path, parquet_file_path)

# Example usage:
input_directory = '/home/LQL3227/phd/json/'  # Replace with the path to your input directory
output_directory = '/home/LQL3227/phd/parquet/'  # Replace with the path to your output directory

process_directory(input_directory, output_directory)