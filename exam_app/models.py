from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def validateUser(self, post):
		is_valid = True
		errors = []
		if len(post.get('name')) == 0:
			is_valid = False
			errors.append('Name field cannot be blank.')
		if len(post.get('alias')) == 0:
			is_valid = False
			errors.append('Alias field cannot be blank.')
		if  not re.search(r'\w+\@\w+.\w+', post.get('email')):
			is_valid = False
			errors.append('Email not valid')
		if len(post.get('password')) == 0:
			is_valid =False
			errors.append('Password field cannot be blank.')
		if post.get('password') != post.get('pw_confirm'):
			is_valid = False
			errors.append('Passwords do not match')
		if post.get('birthday') == '':
			is_valid = False
			errors.append('Birthday field cannot be empty')
		return (is_valid, errors)

	def loginUser(self, post):
		user = User.objects.filter(email = post.get('email')).first()
		if user and bcrypt.checkpw(post.get('password').encode(), user.password.encode()):
			return {'status': True, 'user':user}
		else:
			return{'status': False, 'message': 'invalid credentials'}
class User(models.Model):
	name = models.CharField(max_length = 255)
	alias= models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	birthday = models.DateField('birthday')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Friend(models.Model):
	friend = models.ForeignKey(User, related_name = 'Users')
	user = models.ForeignKey(User, related_name = 'Friends')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

# Create your models here.
