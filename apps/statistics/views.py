# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


def statisticsView(request):
    currentUrl = request.get_full_path()
    return render(request, 'statistics.html', locals())
