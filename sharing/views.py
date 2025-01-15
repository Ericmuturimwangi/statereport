from django.shortcuts import render, get_object_or_404, redirect
from .utils import encrypt_file, generate_key, decrypt_file
from .models import EncryptedFile, Profile
from .forms import FileUploadForm
from django.http import HttpResponseRedirect, Http404, FileResponse, HttpResponse
import os
from django.shortcuts import redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings

@login_required
def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.encryption_key = generate_key().decode()  # Generate the encryption key
            instance.filename = request.FILES['file'].name  # Save the original file name
            instance.save()

            # Encrypt the file to ensure no easy access
            file_path = instance.file.path
            encrypt_file(file_path, instance.encryption_key)  # Use the string as-is

            return render(request, 'sharing/success.html', {'file': instance})  # Pass the instance to the template

    else:
        form = FileUploadForm()
    return render(request, 'sharing/upload.html', {'form': form})

@login_required
def download_file(request, pk):
    try:
        file_instance = get_object_or_404(EncryptedFile, pk=pk) 

        # Decrypt the file before serving it
        decrypt_file(file_instance.file.path, file_instance.encryption_key.encode())

        # Serve the file
        response = FileResponse(open(file_instance.file.path, 'rb'),
                                as_attachment=True,
                                filename=file_instance.file.name)

    # re-encrypt the file after serving
        decrypt_file(file_instance.file.path, file_instance.encryption_key.encode())
        return response

    except Exception as e:
        return HttpResponse(f"Error processing file download: {str(e)}", status=500)


def home(request):
    return redirect('upload_file')

# register user
def register_sender(request):
    print(os.path.exists(settings.BASE_DIR / "templates/register/sender.html"))  # Check file existence
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role='sender')
            return redirect ('login')
    else:
        form = UserCreationForm()
    return render(request, 'register/receiver.html', {'form': form})

def register_receiver(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role='receiver')
            return redirect ('login')
    else:
        form = UserCreationForm()
    return render(request, 'register/sender.html', {'form': form})   
