from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    #if request.method=='POST':
        #return render(request,'home.html',{'new_item_text':request.POST['item_text']})
    #return render(request,'home.html')
    return render(request,'home.html',{'form':ItemForm()})
def view_list(request,list_id):
    list_=List.objects.get(id=list_id)
    error=None
    if request.method == 'POST':
        try:
            item=Item(text=request.POST.get('item_text',''),list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error="your can't hava an empty list item"
    return render(request,'list.html',{'list':list_,'error':error})    
    	
def new_list(request):
    new_item_text=request.POST.get('item_text','')
    list_=List.objects.create()
    item=Item(text=new_item_text,list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error="your can't hava an empty list item"
        return render(request,'home.html',{'error':error})    
#    return redirect('view_list',list_.id)
    #list_get_absolute_url
    return redirect(list_)
