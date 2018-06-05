# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


def employeesView(request):
    currentUrl = request.get_full_path()
    return render(request, 'employees.html', locals())
