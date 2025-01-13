from django.shortcuts import render, get_object_or_404
from .utils import encrypt_file, generate_key, decrypt_file
from .models import EncryptedFile
from .forms import FileUploadForm
from django.http import HttpResponseRedirect, Http404, FileResponse, HttpResponse
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
        # Decrypt the file to a temporary location
        decrypted_file_path = decrypt_file(file_instance.file.path, file_instance.encryption_key.encode())

        # Serve the decrypted file
        response = FileResponse(open(decrypted_file_path, 'rb'), as_attachment=True, filename=file_instance.filename)

        # Clean up the temporary decrypted file after serving
        os.remove(decrypted_file_path)
        
        return response
    except Exception as e:
        # Ensure cleanup of the temporary file in case of failure
        if os.path.exists(decrypted_file_path):
            os.remove(decrypted_file_path)
        return HttpResponse(f"Error processing file download: {str(e)}", status=500)

def home(request):
    return redirect('upload_file')