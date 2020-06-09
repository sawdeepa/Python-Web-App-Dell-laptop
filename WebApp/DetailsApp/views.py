from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from .models import Master,Category,Rule
from django.views.generic import View,TemplateView,ListView,DetailView
#from tabination.views import TabView
import numpy as np
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import csv
import pyodbc
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os, tempfile, zipfile
from wsgiref.util import FileWrapper
import xlwt
import mimetypes
from django.conf import settings
from django.http import JsonResponse
from django.db import connection, transaction
#from rest_framework import viewsets
def send_file(request,id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Table.csv"'
    c = get_data(id)
    writer = csv.writer(response)
    for i in c:
        writer.writerow(i)
    return response
def error(request):
    ListA={}
    return render(request,'DetailsApp/error.html',context=ListA)
class MasterListView(ListView):

    model=models.Master
    context_object_name='masterr_list'
    template_name='base.html'

'''class IndexView(TemplateView):
    template_name='base.html'

class MasterListView(ListView):
    context_object_name='master_list'
    model=models.Master

class MasterDetailView(DetailView):
    context_object_name='master_detail'
    model=models.Master
    template_name='DetailsApp/WebApp.html'
    '''


# Create your views here.
def index(request):
    master_list=Master.objects.order_by('id')
    Qry22 = Master.objects.values('id')
    Qry2 = Rule.objects.values('id')
    List=[]
    for ids in Qry22:
        List.append(ids['id'])
    ListC={}
    for l in List:
        ListC['count'+str(l)] = Rule.objects.filter(DomainID=l).count()
    ListC['master_list'] = master_list
    return render(request,'DetailsApp/WebApp.html',context=ListC)

def tilesid(request,id):
    Qry21 = Master.objects.filter(pk=id).values('Domain')
    for data in Qry21:
        Q1 = data['Domain']
    T_list = Category.objects.order_by('IDCat')
    Qry22 = Category.objects.values('id')
    List=[]
    for ids in Qry22:
        List.append(ids['id'])
    ListM={}
    for l in List:
        ListM['access'+str(l)]=Rule.objects.filter(DomainID=id,CategoryID=l)
    R_list = Rule.objects.filter(DomainID=id)
    ListM['access_records']=T_list
    ListM['access_recordsd']=T_list
    #ListM['access_records1']=R_list
    ListM['Domain']=Q1
    ListM['RuleID']=id
    ListM['DomainID']=id
    #T_dict = {'access_records': T_list,'access_recordsd': T_list,'access_records1': R_list,'Domain':Q1,'RuleID': id}
    return render(request, 'DetailsApp/WebApp0.html', context=ListM)


def get_data(id):
    try:
        Qry21 = Rule.objects.filter(pk=id).values('Query')
        for data in Qry21:
            Q1 = data['Query']
        Qry22 = Q1
        print(Qry22)
        conn = pyodbc.connect("Driver={SQL Server};"
                              "Server=10.118.23.78;"
                              "Database=D-DASH_Phase0_DQ;"
                              "UID=dsuser;"
                              "PWD=Password.1;"
                              # "Trusted_Connection=yes;"
                              )
        cursor = conn.cursor()
        Qry1111 = []

        cursor.execute(Qry22)

        names = list(map(lambda x: x[0], cursor.description))
        Qry1111.append(names)
        a = 1
        for row in cursor.fetchall():
            l = []

            for i in range(0, len(row)):
                l.append(row[i])
            a = a + 1
            Qry1111.append(l)
        print(a)

        Rule.objects.filter(pk=id).update(Recordcount=a-1)
        Rule.objects.filter(pk=id).update(LastRefreshedOn=date.today())
        L_list = Rule.objects.filter(pk=id).values('Recordcount')
        conn.close()
        return(Qry1111)

    except Exception as err:
        print(type(err),err)
        message="Could not connect to SQL server.Try Connecting to Deloitte Net"
        print(message)
        T_dict = {'message':message,'error':err}
        return render(request,'DetailsApp/error.html',context=T_dict)




def details(request,id):
    try:
        Qry21 = Rule.objects.filter(pk=id).values('Query')
        for data in Qry21:
            Q1 = data['Query']
        Qry22 = Q1
        print(Qry22)
        conn = pyodbc.connect("Driver={SQL Server};"
                              "Server=10.118.23.78;"
                              "Database=D-DASH_Phase0_DQ;"
                              "UID=dsuser;"
                              "PWD=Password.1;"
                              # "Trusted_Connection=yes;"
                              )
        cursor = conn.cursor()
        Qry1111 = []

        cursor.execute(Qry22)

        names = list(map(lambda x: x[0], cursor.description))
        Qry1111.append(names)
        a = 1
        for row in cursor.fetchall():
            l = []

            for i in range(0, len(row)):
                l.append(row[i])
            a = a + 1
            Qry1111.append(l)
        print(a)

        Rule.objects.filter(pk=id).update(Recordcount=a-1)
        Rule.objects.filter(pk=id).update(LastRefreshedOn=date.today())
        L_list = Rule.objects.filter(pk=id).values('Recordcount')
        conn.close()
        #pagination
        user_list = Qry1111
        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        ''' Graphs '''
        QryTableM = Rule.objects.filter(pk=id).values('VQuery')
        for data in QryTableM:
            Q1 = data['VQuery']
        QryTableM = Rule.objects.filter(pk=id).values('Insight')
        for data in QryTableM:
            QInsight = data['Insight']
        QryTableM = Rule.objects.filter(pk=id).values('GraphValue')
        for data in QryTableM:
            QGraphValue = data['GraphValue']
        QryTableM = Rule.objects.filter(pk=id).values('Xaxis')
        for data in QryTableM:
            XXaxis = data['Xaxis']
        QryTableM = Rule.objects.filter(pk=id).values('Yaxis')
        for data in QryTableM:
            YYaxis = data['Yaxis']
        QryTableM = Rule.objects.filter(pk=id).values('Subtitle')
        for data in QryTableM:
            SSubtitle = data['Subtitle']

        GraphID=QGraphValue
        Insight=QInsight
        Qry22aa = Q1

        conn = pyodbc.connect("Driver={SQL Server};"
                                  "Server=10.118.23.78;"
                                  "Database=D-DASH_Phase0_DQ;"
                                  "UID=dsuser;"
                                  "PWD=Password.1;"
                                  # "Trusted_Connection=yes;"
                                  )
        cursor = conn.cursor()
        Qryaa = []

        cursor.execute(Qry22aa)
        names = list(map(lambda x: x[0], cursor.description))
        Qryaa.append(names)

        for row in cursor.fetchall():
            laa = []
            for i in range(0, len(row)):
                laa.append(row[i])
            Qryaa.append(laa)
        Qryaa=json.dumps(Qryaa,cls=DjangoJSONEncoder)

        conn.close()
        a ='GraphA'+str(GraphID)+'.html';
        R_list = Rule.objects.filter(pk=id)

        TT_dict={ 'users': users ,'Query1': Qry1111,'ID':id,'GraphID':GraphID,'access_records': R_list,'Query': Qryaa,'Insight':Insight,'XXaxis':XXaxis,'YYaxis':YYaxis,'SSubtitle':SSubtitle}
        return render(request,'DetailsApp/'+a,context=TT_dict)
    except Exception as err:
        print(type(err),err)
        message="Could not connect to SQL server.Try Connecting to Deloitte Net"
        print(message)
        T_dict = {'message':message,'error':err}
        return render(request,'DetailsApp/error.html',context=T_dict)


def refresh(request,DomainID,id):

    Qry21 = Rule.objects.filter(pk=id).values('Query')
    for data in Qry21:
        Q1 = data['Query']
    Qry22 = Q1
    try:
        conn = pyodbc.connect("Driver={SQL Server};"
                              "Server=10.118.23.78;"
                              "Database=D-DASH_Phase0_DQ;"
                              "UID=dsuser;"
                              "PWD=Password.1;"
                              # "Trusted_Connection=yes;"
                              )
        cursor = conn.cursor()
        Qry1111 = []

        cursor.execute(Qry22)

        names = list(map(lambda x: x[0], cursor.description))
        Qry1111.append(names)
        a = 1
        for row in cursor.fetchall():
            l = []

            for i in range(0, len(row)):
                l.append(row[i])
            a = a + 1
            Qry1111.append(l)
        Rule.objects.filter(pk=id).update(Recordcount=a-1)
        Rule.objects.filter(pk=id).update(LastRefreshedOn=date.today())
        L_list = Rule.objects.filter(pk=id).values('Recordcount')
        T_list=Rule.objects.order_by('id')
        T_dict = {'access_records': T_list}
        b = '/' + str(DomainID)
        return redirect(b)
    except Exception as err:
        print(type(err),err)
        message="Could not connect to SQL server.Try Connecting to Deloitte Net"
        print(message)
        T_dict = {'message':message,'error':err}
        return render(request,'DetailsApp/error.html',context=T_dict)
        '''print(type(err),err)
        message="Could not connect to SQL server.Try Connecting to Deloitte Net"
        print(message)
        T_dict = {'message':message}
        b = '/' + str(DomainID)
        return redirect(b,context=T_dict)'''
