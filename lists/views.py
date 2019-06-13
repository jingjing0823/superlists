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
        return redirect('/lists/the_only_list_in_the_world/')
    return render(request,'home.html')
def view_list(request):
    items=Item.objects.all()    
    return render(request,'list.html',{'items':items})