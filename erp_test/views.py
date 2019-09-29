from django.shortcuts import render,render_to_response
from django.http import JsonResponse
from erp_test.models import UserOrder
import json

# Create your views here.
def call_back(request):
    return render_to_response('call.html',{"info":request.get_raw_uri()})
def syncstatus(request):
    if request.method=='GET':
        user_order=UserOrder()
        user_order.orderno=request.GET.get('orderno')
        user_order.status="-1"
        user_order.save()
        return  JsonResponse({"code":0,"msg":"add ok!"})
    body_info=json.loads(request.body.decode('utf-8'))
    order=UserOrder.objects.filter(body_info.get('orderno'))
    if order.count()>0:
        order.update(status_code=statuscode,status=status)
        return JsonResponse({"status":"OK","errMsg":None})
    else:
        return JsonResponse({"status":"ER","errMsg":""})
