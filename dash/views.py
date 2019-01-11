from django.shortcuts import render
from django.template import RequestContext
from .bot_pack import instance
import json

from .form import os#,launch

# from django.http import HttpResponse 


credentials_global = ''
account_global = ''

# Create your views here.
def dash_view(request):
    credentials = request.session['cred'][0]
    account = instance(credentials['iam'],credentials['alias'],credentials['passwd'])
    # print(credentials['iam'])
    
    # credentials_global=credentials
    # account_global=account

    if(request.method == 'POST'):
        form = os(request.POST)
        if(form.is_valid()):
            # oos = form.cleaned_data.get("btn")

            if('ubuntu' in request.POST):
                account.create_instance('ubuntu')
            elif('redhat' in request.POST):
                account.create_instance('redhat')
            elif('windows' in request.POST):
                account.create_instance('windows')

            return render(request,'page2.html',{})
        # if(launch.is_valid()):
        #     form = launch()
        # if(form1.is_valid())
    else:
        form = os()

    temp = []
    x=account.list_inst()
    for i in x:
        temp.append(i.id)
    # form1 = launch(HttpResponse(temp))
        
    return render(request,'page2.html',{'os_form':form,'launch_form':temp})
    # return render_to_response('auth.html',RequestContext(request,{}))


# def os():
#     inst = account_global.list_inst()
#     list_avail = launch(inst)