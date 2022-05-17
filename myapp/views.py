from threading import settrace
from django.conf import Settings, settings
from django.shortcuts import render
from .forms import ResumeForm
from .models import Resume
from django.views import View
import resumeuploader.settings
from resumeuploader.s3 import upload_doc_to_s3_bucket


class HomeView(View):
 def get(self, request):
  form = ResumeForm()
  candidates = Resume.objects.all()
  return render(request, 'myapp/home.html', { 'candidates':candidates, 'form':form})

 def post(self, request):
   form = ResumeForm(request.POST, request.FILES)
   if form.is_valid():
      initial_obj = form.save(commit=False)
      initial_obj.save()
      filepath = initial_obj.my_file.url
      print(filepath)
      filename = filepath.split('/')
      filename = filename[-1]
      print(filename)
      print(resumeuploader.settings.AWS_STORAGE_BUCKET_NAME)
      s3_resume_link = upload_doc_to_s3_bucket(filepath,resumeuploader.settings.AWS_STORAGE_BUCKET_NAME,filename)
      print(s3_resume_link)
      form.save()
   return render(request, 'myapp/home.html', {'form':form})

class CandidateView(View):
 def get(self, request, pk):
  candidate = Resume.objects.get(pk=pk)
  return render(request, 'myapp/candidate.html', {'candidate':candidate})

