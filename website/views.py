from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Operation, Record

class IndexView(generic.ListView):
    template_name = 'website/index.html'
    context_object_name = 'operation_list'

    def get_queryset(self):
        return Operation.objects.all()

def append_operation(request):
    op = Operation(operation_name=request.POST['operation_name'], show=True)
    op.save()
    return HttpResponseRedirect(reverse('website:index'))
