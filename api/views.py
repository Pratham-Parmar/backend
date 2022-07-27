import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import User, Rates, Port
from django.core import serializers
from rest_framework import serializers as restSerializers
# Create your views here.
from django.http import JsonResponse, HttpResponseServerError
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class TokenSerializer(restSerializers.Serializer):
    key = restSerializers.CharField(max_length=60)


@require_http_methods(["POST"])
def login_user(request):
    req = json.loads(request.body)
    user = authenticate(
        request, username=req["username"], password=req["password"])
    if user is not None:
        token = Token.objects.filter(user=user).first()
        token_data = TokenSerializer(token).data
        print('login', token, token_data)

        data = {
            'token': token_data['key'],
            'is_new_user': False,
            'status_code': 200
        }

    else:
        existing_user = User.objects.filter(
            username=req['username']).first()

        if existing_user is not None:
            data = {
                'error': 'Invalid Credentials',
                'status_code': 401
            }

        else:
            new_user = User.objects.create(
                username=req['username'], password=req['password'])
            token = Token.objects.create(user=new_user)
            token_data = TokenSerializer(token).data

            data = {
                'token': token_data['key'],
                'is_new_user': True,
                'status_code': 200
            }

    return JsonResponse(data=data)


def logout_user(request):
    logout(request)
    return JsonResponse({"status": "Success"}, status=200)


@require_http_methods(["POST"])
@login_required
def add(request):
    req = json.loads(request.body)
    source_port = Port.objects.filter(name=req["source"]).first()
    destination_port = Port.objects.filter(name=req["destination"]).first()
    user = User.objects.filter(email=req["email"]).first()
    Rates.objects.create(
        source=source_port,
        destination=destination_port,
        container_size=req["container_size"],
        created_by=user,
        rate=req["rate"]
    )
    return JsonResponse({"status": "success"}, status=200)


@require_http_methods(["GET"])
@login_required
def search(request):
    req = json.loads(request.body)
    query = Rates.objects.raw(
        """
        SELECT * from api_rates 
        GROUP BY source_id,destination_id,line,container_size 
        HAVING MAX(created_at) ORDER BY created_at
        """
    )
    if req["source"] is not None:
        query = query.filter(source=request["source"])

    if req["destination"] is not None:
        query = query.filter(destination=request["destination"])

    if req["line"] is not None:
        query = query.filter(line=request["line"])

    if req["container_size"] is not None:
        query = query.filter(container_size=request["container_size"])

    resp = [x["fields"] for x in serializers.serialize("python", query)]
    return JsonResponse(resp, safe=False, status=200)


@require_http_methods(["GET"])
@login_required
def ports(request):
    query = Port.objects.all()
    resp = [x["fields"] for x in serializers.serialize("python", query)]
    return JsonResponse(resp, safe=False, status=200)
