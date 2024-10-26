import csv


def data_from_parser(data):
    with open('./data_parser.csv', 'w', encoding='utf-8') as f:
        fieldnames = ['serial_number', 'model', 'name']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for i in data.qs:
            writer.writerow({'serial_number': i.serial_number,
                             'model': i.model.name, 'name': i.name})

def parser_data():
    pass