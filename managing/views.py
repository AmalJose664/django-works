from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import random
from .models import *
from .forms import MovieForm
from pymongo import MongoClient
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse("<a href='create/'>Go to pages</a>")

def create(request):
	
	frm = MovieForm()
	frm.fields.pop('movie_rate')
	if request.POST:
		
		data_from_user=request.POST.copy()
		data_from_user['movie_rate'] = random.randint(1,100) 
		
		form = MovieForm(data_from_user)
			
		if form.is_valid():
			form.save()
			
			return JsonResponse({'success':True,})
		else:
			
			return JsonResponse({
				'error':True,
				'message':"some eroor",
				'reason':form.errors
			})
		
	else:
		return render(request,'create.html',{'frm':frm})
	





@login_required(login_url='/login/')
def edit(request):
	if not request.GET.get('id'):
		return JsonResponse({'error':True,'reason':'No data recived'})
	id=request.GET.get('id')
	
	movie_instance = Movie.objects.get(id=id)
	frm = MovieForm(instance=movie_instance)
	frm.fields.pop('movie_rate')

	movie_instance_for_update= movie_instance
	if request.POST:
		data_from_user=request.POST.copy()
		data_from_user['movie_rate'] = random.randint(1,100) 
		
		
		form = MovieForm(data_from_user,instance=movie_instance_for_update)
			
		if form.is_valid():
			form.save()
			
			return JsonResponse({'success':True,})
		else:
			
			return JsonResponse({
				'error':True,
				'message':"some eroor",
				'reason':form.errors
			})
	recent_visits = request.session.get('recent_visits',[])
	recent_visits.insert(0,id)
	request.session['recent_visits'] = recent_visits

	return render(request,'edit.html',{'frm':frm})





@login_required(login_url='/login/')
def list(request):


	recent_visits = request.session.get('recent_visits',[])

	recent_movie_set = Movie.objects.filter(id__in=recent_visits)

	
	count = request.session.get('count',0)
	
	visits = int(count)+1
	request.session['count'] = visits

	
	
	movie_list = Movie.objects.all() #exclude(movie_year=2001).order_by('movie_rate').filter(movie_name__startswith='Movie')
	

	#get_documents('users','_id') this is to see old way of mongo db

	response = render (request,'list.html',{'movies':movie_list,'visits':visits,'recent_movies':recent_movie_set})
	response.set_cookie('visits',visits)
	#return JsonResponse({'list':'dffsfs'})
	return response




def get_documents(collection,field):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['shopping']
    collection = db[collection]

    documents = collection.find()
	
    

    ids = [str(doc[field]) for doc in documents]
    print(ids)
  
