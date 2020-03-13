

class ResultsFromTop(object):
    """This class reads and formats individual files that contain results from the top command"""
    def __init__(self, file_name, process_id):
        with open(file_name, 'r') as f:
            contents = f.readlines()

        self.date = ResultsFromTop.__grab_time(contents)
        self.cpu_headers, self.cpu_percentages = ResultsFromTop.__grab_cpu_usage(contents)
        self.process_headers = ResultsFromTop.__grab_headers(contents)
        self.process_values = ResultsFromTop.__grab_process(contents, process_id, len(self.process_headers))

    @staticmethod
    def __grab_time(file_contents):
        return file_contents[1].replace('\n', '')

    @staticmethod
    def __grab_cpu_usage(file_contents):
        for line in file_contents:
            if 'CPU usage:' in line:
                cpu_line = line[line.find(':')+2:len(line)].replace('\n', '')

        return ResultsFromTop.__split_cpu_line(cpu_line)

    @staticmethod
    def __split_cpu_line(line):
        columns = line.split(', ')
        # return a list of the column headers and then values
        headers = []
        values = []
        for item in columns:
            value_split = item.split(' ')
            headers.append(value_split[1] + '%')
            values.append(value_split[0].replace('%', ''))
        return headers, values

    @staticmethod
    def __grab_headers(file_contents):
        index_blank = ResultsFromTop.__index_of_blank_line(file_contents)
        header_line = file_contents[index_blank + 1].replace('\n', '')
        return ResultsFromTop.split_row(header_line)

    @staticmethod
    def split_row(line):
        stripped_line = line
        while ('  ' in stripped_line):
            stripped_line = stripped_line.replace('  ', ' ')

        return stripped_line.split(' ')

    @staticmethod
    def __index_of_blank_line(file_contents):
        for i in range(0, len(file_contents) - 1):
            line = file_contents[i].replace('\n', '')
            if len(line) == 0:
                return i
        raise ValueError

    @staticmethod
    def __grab_process(file_contents, id, num_of_columns):
        process_line = ''.join([',' for i in range(num_of_columns - 1)])
        for line in file_contents:
            if line.find(id) == 0:
                process_line = line.replace('  \n', '')
        return ResultsFromTop.split_row(process_line)

    def get_final_headers(self):
        return ["date"] + self.process_headers + self.cpu_headers

    def get_final_values(self):
        return [self.date] + self.process_values + self.cpu_percentages

    def write_to_csv(self, file_path, include_headers=False):
        with open(file_path, 'a') as f:
            if include_headers:
                headers_line = ','.join(self.get_final_headers())
                f.writelines(headers_line + '\n')

            values_line = ','.join(self.get_final_values())
            f.writelines(values_line + '\n')


class ProcessSelector(object):
    """This class handles selecting the python process that was being tested. Note: the process name can be changed."""
    def __init__(self, file_paths, process_name="python"):
        self.process_dic = {}
        self.process_name = process_name
        for file_location in file_paths:
            self.__grab_process_from_file(file_location)

    def __grab_process_from_file(self, file_name):
        with open(file_name, 'r') as f:
            contents = f.readlines()
        processes = self.__grab_all_python_processes(contents)

        for line in processes:
            if line not in self.process_dic.keys():
                self.process_dic[line] = 1
            else:
                self.process_dic[line] += 1

    def __grab_all_python_processes(self, file_contents):
        process_lines = []
        for line in file_contents:
            if self.process_name in line:
                row_split = ResultsFromTop.split_row(line.replace('  \n', ''))
                process_lines.append(row_split[0])
        return process_lines

    def get_lowest_count_process(self):
        lowest_pid = ''
        lowest_count = 70
        for key in self.process_dic.keys():
            if self.process_dic[key] < lowest_count:
                lowest_pid = key
                lowest_count = self.process_dic[key]
        return lowest_pid
