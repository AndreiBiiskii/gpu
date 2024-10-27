import csv


def data_from_parser(data):
    with open('./data_parser.csv', 'w', encoding='utf-8') as f:
        fieldnames = ['serial_number', 'type', 'model']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for i in data.qs:
            writer.writerow({'serial_number': i.serial_number,
                             'type': i.type.name, 'model': i.model.name})


def parser_data():
    pass