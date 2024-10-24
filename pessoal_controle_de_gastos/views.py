from django.shortcuts import render   # Added for this step
from django.http import HttpResponse
from django import forms
from django import utils
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone, timedelta

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('', scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_key('')
worksheet = wks.get_worksheet(0)

def index(request):

    inputdescricao = forms.TextInput()
    inputvalor = forms.NumberInput()
    descricao = ''
    agora = datetime.now()
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    agora = agora.astimezone(fuso_horario)
    horaatual = agora.strftime("%d/%m/%Y %H:%M:%S")
    retorno = ''

    def next_available_row(worksheet):

        str_list = list(filter(None, worksheet.col_values(1)))
        return str(len(str_list)+1)

    next_row = next_available_row(worksheet)

    if request.method=='POST':
        descricao = request.POST['input1']
        valor = request.POST['input2']

        worksheet.update_cell(next_row, 1, valor)
        worksheet.update_cell(next_row, 2, descricao)
        worksheet.update_cell(next_row, 4, horaatual)

        retorno = 'Registro efetuado com sucesso.'

    return render(
        request,
        "pessoal_controle_de_gastos/index.html",  # Relative path from the 'templates' folder to the template file
        # "index.html", # Use this code for VS 2017 15.7 and earlier
        {
            'title' : "Controle de gastos",
            'message1' : "Insira a descrição do gasto",
            'input1': inputdescricao,
            'message2' : "Insira o valor",
            'input2': inputvalor,
            'retorno': retorno
        }
    ) 
