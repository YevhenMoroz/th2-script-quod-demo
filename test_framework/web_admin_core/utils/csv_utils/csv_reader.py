import csv


class CsvReader:
    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file
        self.csv_content = list()

    def read_csv_content(self):
        if self.csv_content:
            self.csv_content = list()

        with open(self.path_to_file, 'r') as file:
            csv_file = csv.DictReader(file)

            for row in csv_file:
                self.csv_content.append(row)

        return self.csv_content
