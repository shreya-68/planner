from Django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from login.models import *

def signup(request):
    """Create new user"""
    UserFormset = inlineformset_factory(User, UserProfile, exclude = ("roomno","sleephours","lunchtime","dinnertime","ususalwakingtime","hobbies","cpi","cursem","Year","studentid"))
    if request.method == 'POST':
    	formset = UserFormset(request.POST)
        if form.is_valid():
        	user = formset.save(commit = False)
        	user.roomno = 12345
        	user.sleephours = None
        	user.lunchtime = None
        	user.dinnertime = None
        	user.usualwakingtime = None
        	user.hobbies = None
        	user.cpi = 5
        	user.cursem = 6
        	user.Year = 2009
        	user.studentid = 200901090
            usser.save()
            
