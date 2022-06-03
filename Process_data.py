import collections
import operator
import csv


class MyProject:
    def __init__(self):
        self.header = []
        self.body = []

    def __readfile__(self, filepath) -> list:
        """Private function - returns content of a file"""
        content = []
        try:
            with open(filepath, 'r', encoding='Latin-1') as f:
                for line in f:
                    content.append(line)
                f.close()
        except FileNotFoundError as e:
            print(f'{filepath} - not found')
            print(e)

        return content

    def load_content(self, filepath: str, has_label: bool = True, sep: str = ','):
        """Loads content"""
        content = self.__readfile__(filepath)
        if len(content) > 0:
            try:
                if has_label:
                    self.header = content[0].strip().split(sep)
                    for line in content[1:-1]:
                        self.body.append([v.strip() for v in line.split(sep)])
                    return self.header, self.body
            except TypeError:
                print('Missing content')

    def disp_header(self):
        """Returns header of the dataset"""
        if len(self.header) > 0:
            return self.header
        else:
            return f'Column names do not exist'

    def disp_body(self, start: int = 0, end: int = -1):
        """Returns body of the dataset"""
        return self.body[start:end]

    def dataset_split(self, training=0.7, validate=0.1):
        """Method that splits dataset into 3 subsets returns tuple (train, val, test)"""
        train_size = int(round(len(self.body) * training, 0))
        val_size = int(round(len(self.body) * validate, 0))
        dataset_train = self.body[:train_size]
        dataset_val = self.body[train_size:train_size+val_size]
        dataset_test = self.body[train_size+val_size:]
        return dataset_train, dataset_val, dataset_test

    @staticmethod
    def class_countability(data, decision_class_index: int = 0):
        result = [(k, v) for k, v in collections.Counter(map(operator.itemgetter(decision_class_index),
                                                         data.disp_body())).items()]
        return result

    @staticmethod
    def disp_data_decision_class(data, decision_class: int = 1):
        return [item[0:] for item in data.disp_body() if item[0] == str(decision_class)]

    @staticmethod
    def save_to_file(main_dataset, subset, file_name):
        with open(file_name, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(main_dataset.disp_header())
            csvwriter.writerows(subset)
        csvfile.close()


if __name__ == '__main__':
    dataset = MyProject()
    dataset.load_content('input/wine.csv')
    print('Header of the dataset')
    print(dataset.disp_header())
    print('Body of the dataset')
    print(dataset.disp_body())

    # split dataset into 3 subsets
    train, val, test = dataset.dataset_split()
    print(len(dataset.disp_body()))

    # return decision classes with their count from selected
    print('Decision class countability')
    print(dataset.class_countability(dataset, decision_class_index=0))

    # return dataset based filter by decision class
    print('Dataset based on decision class chosen')
    print(dataset.disp_data_decision_class(dataset, decision_class=3))
    dec3 = dataset.disp_data_decision_class(dataset, decision_class=3)

    # save dataset to csv
    dataset.save_to_file(dataset, dec3, 'output/dec3.csv')
