from django.shortcuts import render, render_to_response
from django.template import RequestContext
from nations.forms import UserForm, UserProfileForm
from nations.models import UserProfile
from django.http import HttpResponse
import random

# Create your views here.

def index(request):
	template = "nations/home.html"
	context = {}
	return render(request,template,context)

def nation(request, nation_id=0):
	nation = 0
	template = "nations/nation.html"
	if nation_id <= 0:
		try:
			nation = UserProfile.objects.get(user_id=request.user.id)
		except:
			template = "nations/user_not_exist.html"

	else:
		try:
			nation = UserProfile.objects.get(user_id=nation_id)
		except:
			template = "nations/nation_not_exist.html"
	
	context = {'nation': nation}
	return render(request,template,context)

def edit_nation(request):
    context = {}
    if request.POST:
        nation_form = UserProfileForm(data=request.POST)

        if nation_form.is_valid():

            #civ = UserProfile.objects.get(pk=user_id)
            #book_form = UserProfileForm(request.POST, instance = civ)
            #civ.save()    
            return HttpResponse("Hello, world. You're at the polls index.")
        
        else:
            return redirect('/edit_nation')
    else:
        template = "nations/user_not_exist.html"
        try:
            nation = UserProfile.objects.get(user_id=request.user.id)
            template = "nations/edit_nation.html"
            context = {'nation': nation}
        except:
            pass

        return render(request,template,context)


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            resources = random.sample(set(['Aluminium','Cattle','Coal','Fish','Furs','Gold','Gems','Iron','Lead','Lumber','Marble','Oil','Pigs','Rubber','Silver','Spices','Sugar','Uranium','Water','Wheat','Wine']),2)
            profile.resource1 = resources[0]
            profile.resource2 = resources[1]
            profile.government = 'Democracy'
           	

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'registration/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
