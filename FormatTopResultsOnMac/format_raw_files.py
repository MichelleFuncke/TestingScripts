import os
from file_handlers import ResultsFromTop, ProcessSelector


def __get_all_directories(path_to_parent):
    directories = [d for d in os.listdir(path_to_parent) if os.path.isdir(os.path.join(path_to_parent, d))]
    directories.sort()
    return directories


def __get_all_files_in_dir(path_to_dir):
    files = [os.path.join(path_to_dir, f) for f in os.listdir(path_to_dir) if f.lower().endswith('.txt')]
    files.sort(key=os.path.getmtime)
    return files


def __extract_top_results_and_save_to_file(file_list, final_file_full_path):
    # Get the python processes
    python_processes = ProcessSelector(file_list[:14:])
    # Get the python process that we were testing
    process_id = python_processes.get_lowest_count_process()

    headers_flag = True
    for file_name in file_list:
        data = ResultsFromTop(file_name, process_id)

        # Save data to final_file_full_path
        data.write_to_csv(final_file_full_path, include_headers=headers_flag)
        headers_flag = False


def top_results_in_multidirs(full_path_to_parent_dir, test_script_name, full_path_to_final_results):
    # Get all the folders in the location
    directories = __get_all_directories(full_path_to_parent_dir)
    for directory in directories:
        full_path_to_dir = os.path.join(full_path_to_parent_dir, directory)
        files = __get_all_files_in_dir(full_path_to_dir)

        final_file_full_path = os.path.join(full_path_to_final_results, F'{test_script_name}_{directory}.csv')
        __extract_top_results_and_save_to_file(files, final_file_full_path)


if __name__ == "__main__":
    # given a parent directory
    parent_directory_on_pc = '/Users/mfuncke/Downloads/'
    test_run_folder = 'ProjectStatusDump'
    full_path_to_test = os.path.join(parent_directory_on_pc, test_run_folder)
    full_path_to_formatted = os.path.join(full_path_to_test, 'formatted_results')

    top_results_in_multidirs(full_path_to_test, test_run_folder, full_path_to_formatted)
