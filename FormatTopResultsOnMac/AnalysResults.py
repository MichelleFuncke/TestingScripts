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

    def __add_row(self, value_list):
        series = pd.Series(value_list, index=self.column_names)
        self.results = self.results.append(series, ignore_index=True)

    def sort_by_file(self):
        self.results = self.results.sort_values(by=['file'])

    def __add_item(self, file_name):
        file_data = FileResults(file_name)
        self.__add_row(file_data.get_summary_results())

    def add_items(self, files):
        for item in files:
            self.__add_item(item)

    def to_csv(self, file_name):
        self.results.to_csv(file_name)


def calculate_averages(dir_path, results_path):
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.lower().endswith('.csv')]
    files.sort(key=os.path.getmtime)

    result_table = SummaryResults()
    result_table.add_items(files)
    result_table.sort_by_file()

    # Save results to file
    result_table.to_csv(results_path)


if __name__ == "__main__":
    # Read data from file
    parent_directory_on_pc = '/Users/mfuncke/Downloads/'
    test_run_folder = 'ProjectStatusDump'
    full_path_to_formatted = os.path.join(parent_directory_on_pc, test_run_folder, 'formatted_results')
    averages_file_path = os.path.join(parent_directory_on_pc, 'Averages.csv')

    calculate_averages(full_path_to_formatted, averages_file_path)
