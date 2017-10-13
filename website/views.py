import json
import datetime
import calendar
from django.core import serializers
from django.db.models import Count

from .models import Operation, Record

def get_day(year=None, month=None, day=None):
    '''
    Returns list of list [id, name, show, day_count]
    for every operation in Operation model
    '''
    if year == None and month == None and day == None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime(year, month, day)

    day_records = Record.objects.all()\
        .filter(date=date)\
        .values('operation')\
        .order_by()\
        .annotate(count=Count('operation'))

    day_records = {rec['operation']: {'count': rec['count']}
        for rec in day_records}

    operations = {op.id: {'name': op.name, 'show': op.show}
        for op in Operation.objects.all()}

    result = ["get_day"]

    for opkey, opvalue in operations.items():
        try:
            result.append([opkey, opvalue['name'], opvalue['show'],
                day_records[opkey]['count']])
        except:
            result.append([opkey, opvalue['name'], opvalue['show'], 0])

    result = json.dumps(result)
    return result

def append_record(id):
    record = Record(operation=Operation.objects.get(id=id))
    record.save()

def append_operation(name):
    record = Operation(show=True, name=name)
    record.save()

def get_month(year, month):
    '''
    Returns month statistics per each day
    '''
    start_day = 1
    end_day = calendar.monthrange(year, month)[1]

    all_operations = Operation.objects.all()
    all_records = Record.objects.all()\
        .filter(date__year=year, date__month=month)

    stats = []

    for op in all_operations:
        day_records = all_records\
            .filter(operation_id=op.id)\
            .values('date')\
            .order_by()\
            .annotate(count=Count('date'))
        if day_records:
            # Skip operation if it has not had records in this month
            cur_op = dict()
            cur_op = {
                'name': op.name,
                'stats': {
                    rec['date'].day: rec['count']
                    for rec in day_records
                },
                'id': op.id
            }
            for day in range(start_day, end_day + 1):
                # Append days with zero operation count
                if not day in cur_op['stats']:
                    cur_op['stats'][day] = 0
            stats.append(cur_op)

    result = {'type': 'get_month', 'data': stats}
    return json.dumps(result)
