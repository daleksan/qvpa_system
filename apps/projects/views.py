# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings

from jira import JIRA

# Create your views here.


def projectsView(request):
    currentUrl = request.get_full_path()
    jira = JIRA(basic_auth=(settings.JIRA_USERNAME, settings.JIRA_PASSWORD),
                options={'server': settings.JIRA_SERVER})
    projects = jira.projects()
    project_info = {}
    for p in projects:
        search_string = 'is assignee of "{}"'.format(p.key)
        users = jira.search_users(search_string)
        print p, users, search_string
        project_info[p.name] = len(users)
    print project_info
    return render(request, 'projects.html', locals())
