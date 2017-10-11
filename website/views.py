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

def get_year(year, month):
    '''
    Returns month statistics
    '''
    last_month_day = calendar.monthrange(year, month)[1]
    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month, last_month_day)
    all_records = Record.objects.all()\
        .filter(date__range=(start_date, end_date))\
        .values('operation')\
        .order_by()\
        .annotate(count=Count('operation'))
    operation_ids = [record['operation'] for record in all_records]
    corresponding_operations = Operation.objects.filter(id__in=operation_ids)
    operation_id_to_name = {op.id: op.name for op in corresponding_operations}
    result = []
    for record in all_records:
        result.append({
            "id": record['operation'],
            "name": operation_id_to_name[record['operation']],
            "count": record['count']
        })
    list = json.dumps(result)
    return list

def get_year(year, month):
    '''
    (Not implemented yet!) Returns year statistics
    '''
    last_month_day = calendar.monthrange(year, month)[1]
    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month, last_month_day)
    all_records = Record.objects.all()\
        .filter(date__range=(start_date, end_date))\
        .values('operation')\
        .order_by()\
        .annotate(count=Count('operation'))
    operation_ids = [record['operation'] for record in all_records]
    corresponding_operations = Operation.objects.filter(id__in=operation_ids)
    operation_id_to_name = {op.id: op.name for op in corresponding_operations}
    result = []
    for record in all_records:
        result.append({
            "id": record['operation'],
            "name": operation_id_to_name[record['operation']],
            "count": record['count']
        })
    list = json.dumps(result)
    return list
