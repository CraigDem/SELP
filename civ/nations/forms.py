from nations.models import Nation
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    nation_name = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

class NationForm(forms.ModelForm):

	governments = [('Democratic','Democracy'),('Capitalist','Capitalism'),('Communist','Communism'),('Monarchical','Monarchy'),('Federal','Federalism'),('Dictorial','Dictatorship')]
	resources = [('Aluminium', 'Aluminium'),('Cattle','Cattle'),('Coal','Coal'),('Fish','Fish'),('Furs','Furs'),('Gold','Gold'),('Gems','Gems'),('Iron','Iron'),('Lead','Lead'),('Lumber','Lumber'),('Marble','Marble'),('Oil','Oil'),('Pigs','Pigs'),('Rubber','Rubber'),('Silver','Silver'),('Spices','Spices'),('Sugar','Sugar'),('Uranium','Uranium'),('Water','Water'),('Wheat','Wheat'),('Wine','Wine')]
	religions = [('None','None'),('Mixed','Mixed'),('Christianity','Christian'),('Islam','Islamic'),('Jewish','Judaism'),('Buddhism','Buddist'),('Hinduism','Hindu'),('Sikhism','Sikh')]

	resource1 = forms.ChoiceField(required=False,choices=resources)
	resource2 = forms.ChoiceField(required=False,choices=resources)

	government = forms.ChoiceField(required=False,choices=governments)
	religion = forms.ChoiceField(required=False,choices=religions)
    
	class Meta:
		model = Nation
    	fields = ('government','religion','resource1','resource2')
    