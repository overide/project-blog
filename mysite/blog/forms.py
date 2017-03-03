from django import forms
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)

    def send_email(self,post,post_url):
    	sent = False
    	subject = "{} ({}) suggests you reading {}".format(
    		self.cleaned_data['name'],
    		self.cleaned_data['email'],
    		post.title)
    	message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
    		post.title,
    		post_url,
    		self.cleaned_data['name'],
    		self.cleaned_data['comments'])
    	recipient = self.cleaned_data['to']
    	try:
    		send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
    		sent = True
    	except Exception:
    		sent = False

    	return sent

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name','email','body')