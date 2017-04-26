from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
	return render(request, 'index.html')

def createUser(request):
	if request.method != 'POST':
		return redirect('/')
	else:
		check = User.objects.validateUser(request.POST)
		if check[0] == False:
			for error in check[1]:
				messages.error(request, error)
			return redirect('/')
		else:
			hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
			user = User.objects.create(
				name = request.POST.get('name'),
				alias = request.POST.get('alias'),
				email = request.POST.get('email'),
				password = hashed_pw,
				birthday = request.POST.get('birthday')
				)
			request.session['user_id'] = user.id
			return redirect ('/success')

def login(request):
	if request.method != 'POST':
		return redirect('/')
	else:
		check = User.objects.loginUser(request.POST)
		if check['status'] == False:
			messages.error(request, check['message'])
			return redirect('/')
		else:
			request.session['user_id'] = check['user'].id
			return redirect('/success')

def currentUser(request):
	#Check to see if user is already in session.
	return User.objects.get(id=request.session['user_id'])

def success(request):
	users = User.objects.all()
	friends =Friend.objects.all().filter(user = currentUser(request))
	other_users =[]
	if friends:
		for friend in friends:
			friend = friend
		for user in users:
			if user !=friend.friend and user!= currentUser(request):
				other_users.append(user)
	else:
		for user in users:
			if user != currentUser(request):
				other_users.append(user)
	context = {
	'currentUser' : currentUser(request),
	'users' : other_users,
	'friends': friends,
	}
	return render(request, 'success.html', context)

def logout(request):
	request.session.clear()
	return redirect ('/')

def add_friend(request, id):
	user = User.objects.filter(id = id).first()
	friends = Friend.objects.create(friend=user, user = currentUser(request))
	return redirect('/success')

def show_profile(request, id):
	context ={
	'user':User.objects.filter(id =id).first()
	}
	return render(request, 'profile.html', context)

def delete_friend(request, id):
	friend = Friend.objects.filter(id = id)
	if friend:
		friend.delete()
	return redirect('/success')
