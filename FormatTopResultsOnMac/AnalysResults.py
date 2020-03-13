import pandas as pd
import os


class FileResults(object):
    """The class handles reading data from a file and formatting it"""
    def __init__(self, file_name):
        self.file_name = file_name
        self.data_table = pd.read_csv(file_name)

        self.__convert_time_column()
        self.__convert_mem_column()
        self.__drop_unnecessary_columns()
        # Drop rows that have nans
        self.data_table.dropna(inplace=True)

    def __convert_time_column(self):
        self.data_table['TIME'] = pd.to_datetime(self.data_table['TIME'], format='%M:%S.%f', errors='coerce')

    def __convert_mem_column(self):
        self.data_table['MEM'].replace('M', '', regex=True, inplace=True)
        self.data_table['MEM'] = pd.to_numeric(self.data_table['MEM'], errors='coerce')

    def __drop_unnecessary_columns(self):
        columns = ['#MREGS', 'RPRVT', 'VPRVT', 'VSIZE', 'KPRVT', 'KSHRD']
        self.data_table.drop(columns, axis=1, inplace=True)

    def get_summary_results(self):
        # Get just the file name not the full path
        file_name = os.path.basename(self.file_name)
        # Get the duration
        duration = self.data_table['TIME'].max().time()
        # Get the max MEM
        max_memory = self.data_table['MEM'].max()
        # Get the average user cpu
        average_cpu = self.data_table['user%'].mean().round(2)
        average_memory = self.data_table['MEM'].mean().round(1)
        return [file_name, duration, max_memory, average_memory, average_cpu]


class SummaryResults(object):
    """This class handles storing the overall data from the files"""
    def __init__(self):
        self.column_names = ['file', 'TIME', 'max MEM', 'avg MEM', 'avg cpu']
        self.results = pd.DataFrame(columns=self.column_names)

    def add_row(self, value_list):
        series = pd.Series(value_list, index=self.column_names)
        self.results = self.results.append(series, ignore_index=True)

    def sort_by_file(self):
        return self.results.sort_values(by=['file'])


if __name__ == "__main__":
    # Read data from file
    parent_directory_on_pc = '/Users/mfuncke/Downloads/'
    test_run_folder = 'ProjectStatusDump'
    full_path_to_formatted = os.path.join(parent_directory_on_pc, test_run_folder, 'formatted_results')
    files = [os.path.join(full_path_to_formatted, f) for f in os.listdir(full_path_to_formatted) if f.lower().endswith('.csv')]
    files.sort(key=os.path.getmtime)

    result_table = SummaryResults()

    for item in files:
        file_data = FileResults(item)
        temp = file_data.get_summary_results()
        # Store these stats in a table, the file name should be in the table
        result_table.add_row(temp)

    # Sort
    result_table = result_table.sort_by_file()

    # Save results to file
    averages_file_path = os.path.join(parent_directory_on_pc, 'Averages.csv')
    result_table.to_csv(averages_file_path)
