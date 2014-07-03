from django.shortcuts import render_to_response
from django import forms
import hashlib

# Create your views here.
class login_form(forms.Form):
	username = forms.CharField(max_length = 16)
	password = forms.CharField(max_length = 40, widget = forms.PasswordInput)

def login_view(request):
	success = False
	username = ''
	password = ''
	if request.method == 'POST':
		form = login_form(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = hashlib.sha1(form.cleaned_data['password']).hexdigest()
			success = True
	else:
		form = login_form()
	return render_to_response('login.html', {'success': success, 'username': username, 'password': password})