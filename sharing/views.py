from django.shortcuts import render, get_object_or_404
from .utils import encrypt_file, generate_key, decrypt_file
from .models import EncryptedFile
from .forms import FileUploadForm
from django.http import HttpResponseRedirect, Http404, FileResponse
import os
from django.shortcuts import redirect

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

def download_file(request, pk):
    file_instance = get_object_or_404(EncryptedFile, pk=pk)
    try:
        decrypt_file(file_instance.file.path, file_instance.encryption_key.encode())
        response = FileResponse(open(file_instance.file.path, 'rb'))

        encrypt_file(file_instance.file.path, file_instance.encryption_key.encode())
        return response
    except Exception as e:
        raise Http404(f"Error: {str(e)}")

def home(request):
    return redirect('upload_file')