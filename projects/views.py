__author__ = 'feiyicheng'

from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import json
from .models import Project
from decorators import logged_in


def search(request, *args, **kwargs):
    """
    search for projects by name or author(support fuzzy search)
    :param request: request object
    :param args: do not matter in this method
    :param kwargs: keyword arguments
    :return: results or error information in JSON format
    """

    if request.method == 'POST':
        try:
            para = request.POST['query']
        except KeyError:
            return HttpResponse("{'status':'error', 'reason':'your POST paras should have a field named query'}")

        try:
            para = json.loads(para)
        except:
            return HttpResponse("{'status':'error', 'reason':'requet string not conform to json format'}")

        try:
            author_name = para['author']
        except KeyError:
            author_name = None
        try:
            prj_name = para['name']
        except KeyError:
            prj_name = None

        if not author_name and not prj_name:
            return HttpResponse("{'status':'error', 'reason':'your query contains neither author nor name'}")

        if author_name:
            if prj_name:
                results = Project.objects.filter(name__icontains=prj_name, author__icontains=author_name)
            else:
                results = Project.objects.filter(author__icontains=author_name)
        else:
            results = Project.objects.filter(name__icontains=prj_name)

        clean_results = []
        for result in results:
            clean_result = {
                'author': result.author.username,
                'id': result.id,
                'name': result.name,
            }
            clean_results.append(clean_result)

        data_dict = {'status': 'success', 'results': clean_results}
        return HttpResponse(json.dumps(data_dict))


@logged_in
def create_project(request, *args, **kwargs):
    """
    create a totally new project
    :param request: request object
    :param args: nonsense
    :param kwargs: kwargs['prj_name']
    :return:
    """
    user = request.user
    prj_name = kwargs['prj_name']

    if user.is_authenticated():
        new_prj = Project(name=prj_name, author=user, is_active=True)
        new_prj.save()
        return HttpResponse("{'status':'success','id':'%d'}" % (new_prj.pk, ))


@logged_in
def delete_project(request, *args, **kwargs):
    """
    delete a porject of the user's own
    :param request: request object
    :param args: nonsense
    :param kwargs: kwargs['prj_id']
    :return:
    """
    user = request.user
    prj_id = _get_prj_id_int(kwargs['prj_id'])
    if not prj_id:
        return HttpResponse("{'status':'error', 'reason':'prj_id should be a integer'}")

    if user.is_authenticated():
        if _is_author(prj_id, user):
            # the user operating is the author of the project, he/she has the power to delete id
            Project.objects.get(id=prj_id).delete()
            return HttpResponse("{'status':'success'}")

        else:
            return HttpResponse("{'status':'error', 'reason':'No access! Only the author of the project \
            has the right to delete it'}")
    else:
        return HttpResponse("{'status':'error', 'reason':'user not logged in'}")


@logged_in
def add_collaborator(request, *args, **kwargs):
    """
    add a collaborator to the user's own project
    :param request:
    :param args:
    :param kwargs: kwargs['username'] kwargs['prj_id]
    :return:

    """
    user = request.user
    username = kwargs['username']
    prj_id = _get_prj_id_int(kwargs['prj_id'])
    if not prj_id:
        return HttpResponse("{'status':'error', 'reason':'prj_id should be a integer'}")

    if not _is_author(prj_id, user):
        # the user is not the author of the project
        return HttpResponse("{'status':'error', 'reason':'No access! Only the author of the project \
            has the right to delete it'}")

    if user.is_authenticated():

        prj = Project.objects.get(id=prj_id)
        try:
            collaborator = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse("{'status':'error', 'reason':'cannot find a user matching the input username'}")
        prj.collaborators.add(collaborator)
        return HttpResponse("{'status':'success', 'id':'%s', 'username':'%s'}" % (prj_id, username))
    else:
        return HttpResponse("{'status':'error', 'reason':'user not logged in'}")


@logged_in
def get_my_projects(request, *args, **kwargs):
    user = request.user
    clean_results = []

    results_author = user.projects_authored.all()
    for result in results_author:
        clean_result = {
            'author': result.author,
            'id': result.id,
            'name': result.name,
        }
        clean_results.append(clean_result)
    results_collaborated = user.projects_collaborated.all()
    for result in results_collaborated:
        clean_result = {
            'author': result.author.username,
            'id': result.id,
            'name': result.name,
        }
        clean_results.append(clean_result)

    data_dict = {'status': 'success', 'results': clean_results}
    return HttpResponse(json.dumps(data_dict))


'''
def switch_project(request, *args, **kwargs):
    user = request.user
    prj = _get_prj_id_int(kwargs['prj_id'])
    if not _has_access(prj, user):
        return HttpResponse("{'status':'error', 'reason':'You dont have access to do this'}")
    else:
        user.userprofile.currentProject = prj
        return HttpResponse("{'status':'success', 'id':'%d'}" % (prj.id, ))
'''



def _get_prj_id_int(prj_id_str):
    """
    convert a string to in else return None
    :param prj_id_str: a number in string format
    :return:
    """
    try:
        prj_id = int(prj_id_str)
    except ValueError:
        return None
    else:
        return prj_id


def _is_author(prj_id, user):
    """

    :param prj_id: the project id (integer)
    :param user:  the user object
    :return: True if the user is the author of the project else False
    """
    prj = Project.objects.get(id=prj_id)
    if user == prj.author:
        return True
    else:
        return False


def _has_access(prj, user):
    if prj in user.projects_authored.all() or prj in user.projects_collaborated.all():
        return True
    else:
        return False
