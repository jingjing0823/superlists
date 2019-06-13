from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    #if request.method=='POST':
        #return render(request,'home.html',{'new_item_text':request.POST['item_text']})
    #return render(request,'home.html')
    if request.method=="POST":
        new_item_text=request.POST.get('item_text','')
        item=Item.objects.create(text=new_item_text)
        return redirect('/')
    items=Item.objects.all()    
    return render(request,'home.html',{'items':items})