import os
import ScrubTopResults_updated
import AnalysResults


if __name__ == "__main__":
    # Specify the location of the top results
    parent_directory_on_pc = '/Users/mfuncke/Downloads/'
    test_run_folder = 'ProjectStatusDump'
    full_path_to_test = os.path.join(parent_directory_on_pc, test_run_folder)
    # Specify where to put the formatted results
    full_path_to_formatted = os.path.join(full_path_to_test, 'formatted_results')
    # Specify where to put the averages.csv
    averages_file_path = os.path.join(parent_directory_on_pc, 'Averages.csv')

    # Perform the actions to create the formatted results
    ScrubTopResults_updated.format_top_result_in_multiple_directories(full_path_to_test, test_run_folder)
    # Perform the actions to create averages.csv
    AnalysResults.calculate_averages(full_path_to_formatted, averages_file_path)