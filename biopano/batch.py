__author__ = 'beibeihome'

import api
from django.shortcuts import HttpResponse
import json


def node_relocate(request):
	if request.method != 'PATCH':
		return HttpResponse('Please relocate node by PATCH request')
	try:
		body_list = json.loads(request.body)
	except AttributeError:
		return HttpResponse('json.loads failed')

	for body in body_list:
		sub_request = request
		sub_request.body = body
		id = body['id']

		receiver = api.views.get_del_addref_node(sub_request, id)
		if receiver.content != "{'status': 'success}":
			return HttpResponse("{'status': 'error', 'id': " + id + "}")
	return HttpResponse("{'status': 'success}")


def node_add(request):
	if request.method != 'POST':
		return HttpResponse('{"function": "node_add_batch", "error": "POST method is requested"}')
	para_list = request.POST['para_list']
	para_list = json.loads(para_list)



