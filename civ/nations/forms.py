from nations.models import Nation
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    nation_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']

class NationForm(forms.ModelForm):
	governments = [('Democratic','Democracy'),('Capitalist','Capitalism'),('Communist','Communism'),('Monarchical','Monarchy'),('Federal','Federalism'),('Dictorial','Dictatorship')]
	resources = [('Aluminium', 'Aluminium'),('Cattle','Cattle'),('Coal','Coal'),('Fish','Fish'),('Furs','Furs'),('Gold','Gold'),('Gems','Gems'),('Iron','Iron'),('Lead','Lead'),('Lumber','Lumber'),('Marble','Marble'),('Oil','Oil'),('Pigs','Pigs'),('Rubber','Rubber'),('Silver','Silver'),('Spices','Spices'),('Sugar','Sugar'),('Uranium','Uranium'),('Water','Water'),('Wheat','Wheat'),('Wine','Wine')]
	religions = [('None','None'),('Mixed','Mixed'),('Christianity','Christian'),('Islam','Islamic'),('Jewish','Judaism'),('Buddhism','Buddist'),('Hinduism','Hindu'),('Sikhism','Sikh')]
	tax_brackets = [('28','28%'),('27','27%'),('26','26%'),('25','25%'),('24','24%'),('23','23%'),('22','22%'),('21','21%'),('20','20%'),('19','19%'),('18','18%'),]

	resource1 = forms.ChoiceField(choices=resources)
	resource2 = forms.ChoiceField(choices=resources)

	government = forms.ChoiceField(choices=governments)
	religion = forms.ChoiceField(choices=religions)
	tax_rate = forms.ChoiceField(choices=tax_brackets)
	
	class Meta:
		model = Nation
		exclude = ['user','nation_name','funds','infrastructure','technology','land','soldiers','tanks','collect_taxes','paid_bills','citizens']
    	
class extendForm(forms.ModelForm):
   	class Meta:
		model = Nation
		fields = ['infrastructure','technology','land']
    	