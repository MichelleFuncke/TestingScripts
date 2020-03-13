import pandas as pd
import os


def convert_mem_column(table):
    table['MEM'].replace('M', '', regex=True, inplace=True)
    table['MEM'] = pd.to_numeric(table['MEM'], errors='coerce')


if __name__ == "__main__":
    # Read data from file
    script = '/Users/mfuncke/Downloads/ProjectStatusDump'
    folder = F'{script}/formatted_results/'
    files = [folder + f for f in os.listdir(folder) if f.lower().endswith('.csv')]
    files.sort(key=os.path.getmtime)

    Results = {}
    column_names = ['file', 'TIME', 'max MEM', 'avg MEM', 'avg cpu']
    result_table = pd.DataFrame(columns=column_names)

    for item in files:
        data_table = pd.read_csv(item)

        # Convert PID and COMMAND columns (might not be important)
        # Convert time column
        data_table['TIME'] = pd.to_datetime(data_table['TIME'], format='%M:%S.%f', errors='coerce')
        # Convert all other columns to numbers
        convert_mem_column(data_table)
        # data_table['MEM'] = pd.to_numeric(data_table['MEM'], errors='coerce')
        # data_table['user%'] = pd.to_numeric(data_table['user%'], errors='coerce')
        # Drop the N/A rows
        data_table.drop(['#MREGS', 'RPRVT', 'VPRVT','VSIZE', 'KPRVT', 'KSHRD'], axis=1, inplace=True)
        data_table.dropna(inplace=True)
        # Get the duration
        duration = data_table['TIME'].max().time()
        # Get the max MEM
        max_memory = data_table['MEM'].max()
        # Get the average user cpu
        average_cpu = data_table['user%'].mean().round(2)
        average_memory = data_table['MEM'].mean().round(1)
        # Store these stats in a table, the file name should be in the table
        series = pd.Series([item, duration, max_memory, average_memory, average_cpu], index=result_table.columns)
        result_table = result_table.append(series, ignore_index=True)

    # Sort
    result_table = result_table.sort_values(by=['file'])

    # Save results to file
    file_name = 'Averages.csv'
    result_table.to_csv(file_name)
