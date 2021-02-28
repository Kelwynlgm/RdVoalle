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
        retorno = request.data['leads'][0]['last_conversion']['content']
        status_lead = request.data['leads'][0]['custom_fields']['Você já é nosso cliente?']
        if status_lead != "Já sou cliente Infolink":
            telefone = request.data['leads'][0]['mobile_phone']
            cidade = request.data['leads'][0]['city']
            if telefone is None:
                telefone = request.data['leads'][0]['personal_phone']
            if cidade is None:
                cidade = "Cidade não informada"
            dados_lead2 = {
                "nome": retorno['Nome'],
                "email": retorno['email_lead'],
                "cidade": cidade,
                "telefone": telefone,
                "origem": 1.03
            }
            url = "https://erp.infolinktelecom.com/api/api/events/new_suspect"
            headers = {
                'Authorization-Token': '488aec95-0bd0-11ea-956c-5e2f033a4602'
            }
            response = requests.request("POST", url, headers=headers, data=dados_lead2)
            print(response.text.encode('utf8'))
            serializer = serializar_cliente(dados_lead2)
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