import pandas as pd


input_csv = "data/1_ground_truth/20241104_cafe/2024-11-04__10-51-25_Cafe.csv"
output_csv = f"{input_csv[:-4]}-new.csv"
column = "Seconds"
new_column_name = "Seconds-from-start"


def add_subtracted_column(input_csv, output_csv, column, new_column_name):
    df = pd.read_csv(input_csv)
    if column not in df.columns:
        print(f"Error: Column '{column}' not found in the input CSV.")
        return
    df[new_column_name] = round(df[column] - df[column][0], 2)

    # Move the new column to the second-to-last position
    cols = list(df.columns)
    cols.remove(new_column_name)
    cols.insert(-1, new_column_name)
    df = df[cols]

    df.to_csv(output_csv, index=False)
    print(f"Modified CSV saved as '{output_csv}'.")

add_subtracted_column(input_csv, output_csv, column, new_column_name)
