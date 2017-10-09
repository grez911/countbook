import json
import datetime
from django.core import serializers
from django.db.models import Count

from .models import Operation, Record

def get_today():
    """
    Returns list of list [id, name, show, today_count]
    for every operation in Operation model
    """
    today_records = Record.objects.all()\
        .filter(date=datetime.datetime.now())\
        .values('operation')\
        .order_by()\
        .annotate(count=Count('operation'))
    today_records = {rec['operation']: {'count': rec['count']}
        for rec in today_records}
    operations = {op.id: {'name': op.name, 'show': op.show}
        for op in Operation.objects.all()}
    result = ["get_today"]
    for opkey, opvalue in operations.items():
        try:
            result.append([opkey, opvalue['name'], opvalue['show'],
                today_records[opkey]['count']])
        except:
            result.append([opkey, opvalue['name'], opvalue['show'], 0])
    result = json.dumps(result)
    return result

def get_month(params):
    all_records = Record.objects.all()\
        .filter(date__range=('2017-10-08', '2017-10-08'))\
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
