from django.shortcuts import render
from nch_brasil.settings import BASE_DIR
import os
import investpy as inv
import pandas as pd
from .models import  Funds, HistoricalData
import json
from django.http import JsonResponse
import datetime


def getFund(funds):
    nch_fund_seach = inv.search_funds(by='name', value=funds)
    # nch_fund_info = inv.get_fund_information(fund=funds, as_json=True, country='brazil')
    nch_historical_data = inv.get_fund_historical_data(funds, country='brazil', from_date='10/01/2020', to_date='01/01/2021', as_json=True)

    historical = json.loads(nch_historical_data)

    json_load_info = nch_fund_seach.to_json(orient="split")
    info_funds = json.loads(json_load_info)
    # print ('json_r', json_load_historical)

    return (info_funds, historical)

def populateDB(json_r, flag):

    if flag == "Information Fund":
        list_data = json_r['data'][0]
        p = Funds(
            name = list_data[1],
            symbol = list_data[2],
            country = list_data[0],
            isin = list_data[4],
            issuer = list_data[3]
        )
        p.save()

    else:
        name = json_r['name']
        id_fund = Funds.objects.get(name=name)
        for r in json_r['historical']:
            
            p = HistoricalData(
                funds_id = id_fund,
                date = datetime.datetime.strptime(r['date'], "%d/%m/%Y").date(),
                close = r['close'] 
            )
            p.save()
            # print ('json_r', r)


import random
from datetime import date, timedelta

def pushFinance(fund_name):
    # info_funds, historical = getFund(fund_name)
    # print ('-----------', historical)
    name = 'IBX100'
    id_fund = Funds.objects.get(symbol=name)
    start_date = date(2020, 1, 1)
    end_date = date(2021, 1, 1)
    delta = timedelta(days=3)
    while start_date <= end_date:
        print(start_date.strftime("%Y-%m-%d"))
        start_date += delta
        p = HistoricalData(
            funds_id = id_fund,
            date = start_date,
            close = random.randint(144,201)
        )
        p.save()
    # populateDB(info_funds, "Information Fund")
    # populateDB(historical, "Historical Fund")


def index(request):
    teste = {
        "Cota NCH Maracanã FIA": "225,15",
        "PL Junho 2021": "R$ 114,55 MI",
        "Rentabilidade Mês": "-4,56%",
        "Rentabilidade Ano": "15,27%",
        "Rentabilidade ITD": "139,67%",
     }
    context = {'teste': teste}
    return render(request, 'index.html', context)

def funds_nch(request):
    nch = Funds.objects.get(isin='BRNCH1CTF006')
    datanch = nch.funds_id.all().values('date', 'close', 'funds_id').order_by('date')
    return JsonResponse(list(datanch), safe=False)

def funds_ibx(request):
    ibx = Funds.objects.get(isin='IBX100')
    dataibx = ibx.funds_id.all().order_by('date').values('date', 'close', 'funds_id')
    return JsonResponse(list(dataibx), safe=False)
