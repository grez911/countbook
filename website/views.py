import json
from django.core import serializers
from django.db.models import Count

from .models import Operation, Record

def get(params):
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
