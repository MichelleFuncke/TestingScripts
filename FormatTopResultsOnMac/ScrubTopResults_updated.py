import os


def grab_time(file_contents):
    return file_contents[1].replace('\n', '')


def grab_cpu_usage(file_contents):
    for line in file_contents:
        if 'CPU usage:' in line:
            cpu_line = line[line.find(':')+2:len(line)].replace('\n', '')

    return split_cpu_line(cpu_line)


def split_cpu_line(line):
    columns = line.split(', ')
    # return a list of the column headers and then values
    headers = []
    values = []
    for item in columns:
        value_split = item.split(' ')
        headers.append(value_split[1] + '%')
        values.append(value_split[0].replace('%', ''))
    return headers, values


def grab_headers(file_contents):
    index_blank = index_of_blank_line(file_contents)
    header_line = file_contents[index_blank + 1].replace('\n', '')
    return split_row(header_line)


def index_of_blank_line(file_contents):
    for i in range(0, len(file_contents) - 1):
        line = file_contents[i].replace('\n', '')
        if len(line) == 0:
            return i


def grab_process(file_contents, id, num_of_columns):
    process_line = ''.join([',' for i in range(num_of_columns - 1)])
    for line in file_contents:
        if line.find(id) == 0:
            process_line = line.replace('  \n', '')
    return split_row(process_line)


def split_row(line):
    stripped_line = line
    while ('  ' in stripped_line):
        stripped_line = stripped_line.replace('  ', ' ')

    return stripped_line.split(' ')


def get_process_columns_final(line):
    if len(line) == 0:
        return ['' for i in range(7)]
    columns = line.split(',')
    final_columns = []
    final_columns.append(columns[0])
    final_columns.append(columns[1])
    final_columns.append(columns[2])
    final_columns.append(columns[3])
    final_columns.append(columns[7])
    final_columns.append(columns[14])
    final_columns.append(columns[15])
    return final_columns


def grab_all_python_processes(file_contents):
    python_lines = []
    for line in file_contents:
        if 'python' in line:
            row_split = split_row(line.replace('  \n', ''))
            columns = get_process_columns_final(','.join(row_split))
            python_lines.append(columns[0])
    return python_lines


def grab_python_from_file(process_dic, file_name):
    with open(file_name, 'r') as f:
        contents = f.readlines()
    pythons = grab_all_python_processes(contents)

    for line in pythons:
        if line not in process_dic.keys():
            process_dic[line] = 1
        else:
            process_dic[line] += 1


def get_lowest_count_python(process_dic):
    lowest_pid = ''
    lowest_count = 70
    for key in process_dic.keys():
        if process_dic[key] < lowest_count:
            lowest_pid = key
            lowest_count = process_dic[key]
    return lowest_pid


if __name__ == "__main__":
    # given a parent directory
    parent_directory = '/Users/mfuncke/Downloads/'
    script = 'ProjectStatusDump'
    # loop through the directories inside this directory
    directories = [d for d in os.listdir(parent_directory + script) if os.path.isdir(os.path.join(parent_directory, script, d))]
    directories.sort()
    for directory in directories:
        location = F"{parent_directory}{script}/{directory}"
        files = [location + '/' + f for f in os.listdir(location) if f.lower().endswith('.txt')]
        files.sort(key=os.path.getmtime)

        # Get the python processes
        python_processes = {}
        for file_location in files[:14:]:
            grab_python_from_file(python_processes, file_location)

        # Get the python process that we were testing
        process_id = get_lowest_count_python(python_processes)

        final_file = F'{parent_directory}{script}/formatted_results/{script}_{directory}.csv'
        for i in range(len(files)):
            with open(files[i], 'r') as f:
                contents = f.readlines()

            date = grab_time(contents)
            cpu_headers, cpu_percentages = grab_cpu_usage(contents)
            process_headers = grab_headers(contents)
            process_values = grab_process(contents, process_id, len(process_headers))

            # Save data to final_file
            final_headers = ["date"]
            final_headers += process_headers
            final_headers += cpu_headers

            final_values = [date]
            final_values += process_values
            final_values += cpu_percentages

            with open(final_file, 'a') as f:
                if i == 0:
                    f.writelines(','.join(final_headers) + '\n')
                f.writelines(','.join(final_values) + '\n')
