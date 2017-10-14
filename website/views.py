import json
import datetime
import calendar
from django.db.models import Count

from .models import Operation, Record

def get_day(year=None, month=None, day=None):
    '''
    Returns day statistics
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

    result = {'type': 'get_day', 'data': []}

    for opkey, opvalue in operations.items():
        try:
            result['data'].append({
                'id': opkey,
                'name': opvalue['name'],
                'show': opvalue['show'],
                'count': day_records[opkey]['count']
            })
        except:
            result['data'].append({
                'id': opkey,
                'name': opvalue['name'],
                'show': opvalue['show'],
                'count': 0
            })

    result['data'] = sorted(result['data'], key=lambda k: k['name'])
    result = json.dumps(result)
    return result

def append_record(id):
    '''
    Appends a record to the database
    '''
    record = Record(operation=Operation.objects.get(id=id))
    record.save()

def append_operation(name):
    '''
    Appends an operation to the database
    '''
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

def del_operation(id):
    '''
    Deletes an operation with all associated recors
    '''
    op = Operation.objects.get(id=id)
    op.delete()
