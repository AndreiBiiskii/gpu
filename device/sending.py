import csv
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from device.models import Equipment, Si


def sending(request, title):
    sm = EmailMessage
    subject = 'sample'
    body = 'sample'
    from_email = 'freemail_2019@mail.ru'
    to_email = request.user.email
    msg = sm(subject, body, from_email, [to_email])
    msg.attach_file(f'./{title}.csv')
    # msg.send()
    with open('./1.csv', 'r', encoding='utf-8') as f:
        fieldnames = ['serial_number', 'comment']
        writer = csv.DictReader(f, fieldnames=fieldnames, delimiter=';')
        for row in writer:
            try:
                # if Equipment.objects.filter(
                #                 Q(serial_number=self.cleaned_data['serial_number']) & Q(model__name=self.cleaned_data['model'])):
                eq = Equipment.objects.get(Q(serial_number=row['serial_number']) & Q(si_or = True))
                eq.comment = row['comment']
                eq.save()
            except:
                with open('./bag.csv', 'a') as f1:
                    f1.write(f'{row["serial_number"]};{row["comment"]}\n')

    with open(f'./{title}.csv', 'w', encoding='utf-8'):
        pass
    return redirect(reverse_lazy('search'))


# sample_send

def sample_send(request, data):
        # fieldnames = ['№', 'position', 'location', 'teg', 'serial_number', 'type', 'model', 'name', 'reg_number',
        #               'min_scale', 'max_scale', 'unit', 'comment', 'interval', 'previous_verification',
        #               'next_verification', 'result', ]  #
        # writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        # writer.writeheader()
        # for i, eq in enumerate(data):
        #     if eq.si_or:
        #         try:
        #             from_si = Si.objects.get(equipment=eq)
        #         except:
        #             continue
        #         writer.writerow({
        #             '№': i + 1,
        #             'position': eq.positions.last().name,
        #             'location': eq.locations.last().name,
        #             'teg': eq.tags.last().name,
        #             'type': eq.type.name,
        #             'model': eq.model.name,
        #             'name': eq.name.name,
        #             'serial_number': eq.serial_number,
        #             'reg_number': from_si.reg_number,
        #             'min_scale': from_si.scale.min_scale,
        #             'max_scale': from_si.scale.max_scale,
        #             'unit': from_si.unit,
        #             'comment': from_si.com,
        #             'interval': from_si.interval,
        #             'previous_verification': from_si.previous_verification,
        #             'next_verification': from_si.next_verification,
        #             'result': from_si.result
        #         }
        #         )
        #     if not eq.si_or:
        #         writer.writerow({
        #             '№': i + 1,
        #             'position': eq.positions.last().name,
        #             'location': eq.locations.last().name,
        #             'teg': eq.tags.last().name,
        #             'type': eq.type.name,
        #             'model': eq.model.name,
        #             'name': eq.name.name,
        #             'serial_number': eq.serial_number,
        #         }
        #         )
    return redirect(reverse_lazy('search'))


def send_all(request, start, end):
    if start == 0:
        with open('./all_data.csv', 'w', encoding='utf-8'):
            pass
    if not request.user.is_staff:
        redirect('login')
    last = Equipment.objects.all().count()
    get_all = Equipment.objects.filter(si_or=True)[start:end]
    with open('./all_data.csv', 'a', encoding='utf-8') as f:
        fieldnames = ['№', 'position', 'location', 'teg', 'type', 'model', 'name', 'reg_number', 'serial_number',
                      'min_scale', 'max_scale', 'unit', 'comment', 'interval', 'previous_verification',
                      'next_verification', 'result', ]  #
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for i, eq in enumerate(get_all):
            try:
                from_si = Si.objects.get(equipment=eq)
            except:
                continue
            writer.writerow({
                '№': i + start,
                'position': eq.positions.last().name,
                'location': eq.locations.last().name,
                'teg': eq.tags.last().name,
                'type': eq.type.name,
                'model': eq.model.name,
                'name': eq.name.name,
                'reg_number': from_si.reg_number,
                'serial_number': eq.serial_number,
                'min_scale': from_si.scale.min_scale,
                'max_scale': from_si.scale.max_scale,
                'unit': from_si.unit,
                'comment': from_si.com,
                'interval': from_si.interval,
                'previous_verification': from_si.previous_verification,
                'next_verification': from_si.next_verification,
                'result': from_si.result,
            }
            )
    if end < last:
        start = end
        end += 1000
        return redirect(reverse_lazy('send_all', kwargs={'start': start, 'end': end}))
    sending(request, 'all_data')
    return redirect(reverse_lazy('search'))
