from django.shortcuts import render, redirect	
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from errand.models import *
import json
from django.core import serializers

# Create your views here.
def home(request):
	if(request.method=="GET"):
		if(not request.user.is_authenticated()):
			return render(request, 'errand/index.html', {})
		user = request.user
		#print(user.myuser.role.role)
		#print(type(user.myuser.role.role))
		if(user.myuser.role.role == "Admin"):
			return redirect('/administrator')
		elif(user.myuser.role.role == "Employee"):
			return redirect('/services')
		elif(user.myuser.role.role == "Errand Boy"):
			return redirect('/jobs')
	elif(request.method=="POST"):
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username = username, password = password)
		if user is not None:
		    login(request, user)
		    return redirect('/')
		else:
			return render(request, 'errand/index.html', {'msg':"Invalid Credentials"})

def services(request):
	if(not request.user.is_authenticated()):
		return redirect('/')
	user = request.user
	if(user.myuser.role.role != "Employee"):
		return redirect('/')
	services = Service.objects.all().order_by('name')
	return render(request, 'errand/service.html', {'services': services})

def jobs(request):
	if(not request.user.is_authenticated()):
		return redirect('/')
	user = request.user
	if(user.myuser.role.role != "Errand Boy"):
		return redirect('/')
	jobs = Job.objects.filter(assigned=user)
	return render(request, 'errand/job.html', {'jobs': jobs})

def jobapi(request):
	if(not request.user.is_authenticated()):
		return HttpResponse("User Unauthenticated")
	user = request.user
	if(user.myuser.role.role != "Errand Boy"):
		return HttpResponse("You do not have Access to Job API")
	jobs = Job.objects.filter(assigned=user, granted=False)
	data = serializers.serialize('json',jobs)
	data = json.loads(data)
	for i in range(0, len(data)):
		data[i]['fields']['service'] = Service.objects.get(id=int(data[i]['fields']['service'])).name
		data[i]['fields']['assigned'] = User.objects.get(id=int(data[i]['fields']['assigned'])).username
		data[i]['fields']['location'] = User.objects.get(id=int(data[i]['fields']['by'])).myuser.location
		data[i]['fields']['by'] = User.objects.get(id=int(data[i]['fields']['by'])).username
	return JsonResponse(data, safe=False)

def serviceapi(request):
	if(not request.user.is_authenticated()):
		return HttpResponse("User Unauthenticated")
	user = request.user
	if(user.myuser.role.role != "Employee"):
		return HttpResponse("You do not have Access to Job API")
	jobs = Job.objects.filter(by=user)
	data = serializers.serialize('json', jobs)
	data = json.loads(data)
	for i in range(0, len(data)):
		data[i]['fields']['service'] = Service.objects.get(id=int(data[i]['fields']['service'])).name
		data[i]['fields']['assigned'] = User.objects.get(id=int(data[i]['fields']['assigned'])).username
		data[i]['fields']['by'] = User.objects.get(id=int(data[i]['fields']['by'])).username
	return JsonResponse(data, safe=False)

def administrator(request):
	if(not request.user.is_authenticated()):
		return redirect('/')
	user = request.user
	if(user.myuser.role.role != "Admin"):
		return redirect('/')
	users = User.objects.all()
	services = Service.objects.all()
	if(request.method=="GET"):
		return render(request, 'errand/admin.html', {'users':users, 'services':services})
	elif(request.method=="POST"):
		print(request.POST)
		if(request.POST.get('type') == 'user'):
			name = request.POST.get('name')
			email = request.POST.get('email')
			rl = request.POST.get('role')
			print(rl)
			role = Role.objects.get(role=rl)
			try:
				fname, lname = name.split()
			except:
				fname = name
				lname = ""
			uname = fname+lname
			pwd = fname+lname
			#try:
			usr = User(email=email, username=uname, password=pwd, first_name=fname, last_name=lname)
			usr.save()
			myusr = MyUser(user=usr,role=role, location="")
			myusr.save()
			#except:
				#return render(request, 'errand/admin.html', {'added': "Error Adding User. Please enter correct details"})
			return render(request, 'errand/admin.html', {'added': "User Added",'users':users, 'services':services})
		else:
			name = request.POST.get('name')
			cost = request.POST.get('cost')
			srv = Service(name=name, cost=int(cost))
			srv.save()
			return render(request, 'errand/admin.html', {'added': "Service Added",'users':users, 'services':services})

def log_out(request):
	logout(request)
	return redirect('/')

def hasAccess(user, access):
	total = user.myuser.role.access.all()
	if(access in total):
		return True
	else:
		return False

def getErrandBoy():
	ebs = User.objects.filter(myuser__role__role = 'Errand Boy')
	if(len(ebs) == 0):
		return HttpResponse("No available Errand Boys")
	mi = ebs[0].id
	no = len(ebs[0].assigned_to.all())
	for i in range(0, len(ebs)):
		if(len(ebs[i].assigned_to.all()) < no):
			no = len(ebs[i].assigned_to.all())
			mi = ebs[i].id
	return mi

@csrf_exempt
def addservice(request):
	if(not request.user.is_authenticated()):
		return HttpResponse("User Unauthenticated")
	user = request.user
	access = Access.objects.filter(name='req_service')[0]
	if(hasAccess(user, access)):
		minid = getErrandBoy()
		eboy = User.objects.get(id=minid)
		sid = request.POST.get('sid')
		print(sid)
		service = Service.objects.get(id=int(sid))
		job = Job(by=user, assigned=eboy, service=service)
		job.save()
		return HttpResponse("Job Added")
	else:
		return HttpResponse("Unauthourized access")

def pending(request):
	if(not request.user.is_authenticated()):
		return redirect('/')
	user = request.user
	if(user.myuser.role.role != "Employee"):
		return redirect('/')
	pending = Job.objects.filter(by=user)
	return render(request, 'errand/pending.html', {'pending':pending})

@csrf_exempt
def grantjobapi(request):
	if(not request.user.is_authenticated()):
		return HttpResponse("User Unauthenticated")
	user = request.user
	if(user.myuser.role.role != "Errand Boy"):
		return HttpResponse("You do not have access to Grant a job")
	jobid = request.POST.get('jobid')
	response_data = {'res': 'true'}
	try:
		job = Job.objects.get(id=int(jobid))	
		job.granted = True
		job.save()
	except:
		response_data['res'] = 'false'
	return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def acceptjobapi(request):
	if(not request.user.is_authenticated()):
		return HttpResponse("User Unauthenticated")
	user = request.user
	if(user.myuser.role.role != "Employee"):
		return HttpResponse("You do not have access to Accept a job")
	jobid = request.POST.get('jobid')
	print(request.POST)
	response_data = {'res': 'true'}
	try:
		job = Job.objects.get(id=int(jobid))	
		job.delete()
	except:
		response_data['res'] = 'false'
	return HttpResponse(json.dumps(response_data), content_type="application/json")

def profile(request):
	if(request.method=="GET"):
		if(not request.user.is_authenticated()):
			return redirect('/')		
		return render(request, 'errand/profile.html', {})
	elif(request.method=="POST"):
		username = request.user.username
		currentPassword = request.POST.get('cu_pwd')
		print currentPassword
		user = authenticate(username = username, password = currentPassword)
		if user is not None:
		    password = request.POST.get('pwd')
		    print password
		    confirmPassword = request.POST.get('cpwd')
		    print confirmPassword
		    if(password == confirmPassword):
		    	print "in if"
		    	user = request.user
		    	print user
		    	user.set_password(password)
		    	user.save()
		    	return render(request, 'errand/profile.html', {'msg':'Password Changed'})
		    else:
		    	print "new passwords dont match"
		    	return render(request, 'errand/profile.html', {'msg':'Passwords do not matched'})
		else:
			print "current password dont match"
		    	return render(request, 'errand/profile.html', {'msg':'Invalid Current Password'})
					

