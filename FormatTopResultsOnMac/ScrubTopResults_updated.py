import os
from file_handlers import ResultsFromTop, ProcessSelector


if __name__ == "__main__":
    # given a parent directory
    parent_directory_on_pc = '/Users/mfuncke/Downloads/'
    test_run_folder = 'ProjectStatusDump'
    full_path_to_test = os.path.join(parent_directory_on_pc, test_run_folder)

    # Get all the folders in the location
    directories = [d for d in os.listdir(full_path_to_test) if os.path.isdir(os.path.join(full_path_to_test, d))]
    directories.sort()

    for directory in directories:
        full_path_to_dir = os.path.join(full_path_to_test, directory)
        files = [os.path.join(full_path_to_dir, f) for f in os.listdir(full_path_to_dir) if f.lower().endswith('.txt')]
        files.sort(key=os.path.getmtime)

        # Get the python processes
        python_processes = ProcessSelector(files[:14:])
        # Get the python process that we were testing
        process_id = python_processes.get_lowest_count_process()

        final_file_full_path = os.path.join(full_path_to_test, 'formatted_results', F'{test_run_folder}_{directory}.csv')
        for i in range(len(files)):
            data = ResultsFromTop(files[i], process_id)

            # Save data to final_file_full_path
            final_headers = data.get_final_headers()
            final_values = data.get_final_values()

            with open(final_file_full_path, 'a') as f:
                if i == 0:
                    f.writelines(','.join(final_headers) + '\n')
                f.writelines(','.join(final_values) + '\n')
