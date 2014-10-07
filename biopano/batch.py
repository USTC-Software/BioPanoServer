__author__ = 'beibeihome'

import api
from django.shortcuts import HttpResponse


def node_relocate(request):
	if request.method != 'PATCH':
		return HttpResponse('Please relocate node by PATCH request')

	pass

