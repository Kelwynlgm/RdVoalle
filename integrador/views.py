import requests
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Clientes
from .serializers import ClienteSerializer


class ClientesApiView(APIView):
    def get(self, request):
        clientes = Clientes.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

    def post(self, request):
        retorno = request.data['leads'][0]
        status_lead = request.data['leads'][0]['custom_fields']['Você já é nosso cliente?']
        origem_lead = request.data['leads'][0]['first_conversion']['conversion_origin']['source']
        if status_lead == "Ainda não sou cliente":
            telefone = request.data['leads'][0]['mobile_phone']
            cidade = request.data['leads'][0]['city']
            if telefone is None:
                telefone = request.data['leads'][0]['personal_phone']
            if "+55" in telefone:
                novo_telefone = (telefone.replace("+55", ""))
            if cidade is None:
                cidade = "Cidade não informada"
            if origem_lead == "linklist.bio":
                dados_lead2 = {
                    "nome": retorno['name'].upper(),
                    "email": retorno['email'],
                    "cidade": cidade,
                    "telefone": novo_telefone,
                    "origem": 1.13
                }
            elif origem_lead == "infolinktelecom.com":
                dados_lead2 = {
                    "nome": retorno['name'].upper(),
                    "email": retorno['email'],
                    "cidade": cidade,
                    "telefone": novo_telefone,
                    "origem": 1.12
                }
            elif origem_lead == "Facebook":
                dados_lead2 = {
                    "nome": retorno['name'].upper(),
                    "email": retorno['email'],
                    "cidade": cidade,
                    "telefone": novo_telefone,
                    "origem": 1.14
                }
            elif origem_lead == "Google":
                dados_lead2 = {
                    "nome": retorno['name'].upper(),
                    "email": retorno['email'],
                    "cidade": cidade,
                    "telefone": novo_telefone,
                    "origem": 1.11
                }
            else:
                dados_lead2 = {
                    "nome": retorno['name'].upper(),
                    "email": retorno['email'],
                    "cidade": cidade,
                    "telefone": novo_telefone,
                    "origem": 1.03
                }
            url = "https://erp.infolinktelecom.com/api/api/events/new_suspect"
            headers = {
                'Authorization-Token': '488aec95-0bd0-11ea-956c-5e2f033a4602'
            }
            serializer = serializar_cliente(dados_lead2)
            response = requests.request("POST", url, headers=headers, data=dados_lead2)
            print(response.text.encode('utf8'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return HttpResponse("Já é cliente. Lead não contabilizada", status=status.HTTP_200_OK)


def get_response(request):
    return HttpResponse("OK")


def serializar_cliente(dados_lead):
    serializer = ClienteSerializer(data=dados_lead)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer

def index(request):
    return render(request, 'index.html')