__author__ = 'beibeihome'

from api.views import *
from django.shortcuts import HttpResponse
import json


def node_batch(request):
	if request.method == 'PATCH':
		#return HttpResponse('Please relocate node by PATCH request')
		try:
			body_list = json.loads(request.body)
		except AttributeError:
			return HttpResponse('json.loads failed')

		for body in body_list:
			sub_request = request
			sub_request.body = body
			id = body['id']

			receiver = get_del_addref_node(sub_request, id)
			if receiver.content != "{'status': 'success}":
				return HttpResponse("{'status': 'error', 'id': " + id + "}")
		return HttpResponse("{'status': 'success}")

	elif request.method == 'POST':
		para_list = request.POST['para_list']
		para_list = json.loads(para_list)
		result_list = []
		for para in para_list:
			sub_request = request
			sub_request.POST = para

			receiver = add_node(sub_request)
			result_list.append(json.loads(receiver.content))
		result_text = json.dumps(result_list)
		return HttpResponse(result_text)

	elif request.method == 'DELETE':
		ref_id_list = json.loads(request.body)

		pass


def link_batch(request):
	if request.method == 'POST':
		#return HttpResponse('{"function": "add_batch", "error": "POST method is requested"}')
		para_list = request.POST['para_list']
		para_list = json.loads(para_list)
		result_list = []
		for para in para_list:
			sub_request = request
			sub_request.POST = para

			receiver = add_link(sub_request)
			result_list.append(json.laads(receiver.content))
		result_text = json.dumps(result_list)
		return HttpResponse(result_text)


def delete(request):
	if request.method != 'DELETE':
		return HttpResponse('{"function": "add_batch", "error": "POST method is requested"}')




