from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.checks import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
import hashlib
from django.conf import settings
from Sha2.models import Fichier
import tempfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, generics,mixins,permissions
from .serializer import *
from .permission import IsStaffPermission
"""

import hashlib

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def verify_integrity(file_path, expected_hash):
    calculated_hash = calculate_sha256(file_path)
    if calculated_hash == expected_hash:
        print("L'intégrité du fichier est vérifiée.")
    else:
        print("Erreur : L'intégrité du fichier est compromise.")

# Exemple d'utilisation
file_path = "chemin/vers/mon_fichier.txt"
expected_hash = "9d4b4c8b2b3e0c1dd28e6f745a25e5cfc30a3a1b9f5f3f9d9d8367f1db779c9f"
verify_integrity(file_path, expected_hash)
"""
# Create your views here.
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


class CreateFile(generics.CreateAPIView):
    permission_classes = [IsStaffPermission]
    queryset = Fichier.objects.all()
    serializer_class = FichierSerializers

    def perform_create(self, serializer):
        file=serializer.validated_data.get('path')
        print(file)
    #     # file = request.FILES['pdf']
        nom = str(file).split(".")[0]
    #     # hash = calculate_sha256(file)
        serializer.save(nom=nom, path=file, hash='')
    #
        fichier = serializer.save(nom=nom, path=file, hash='')
        with tempfile.TemporaryFile() as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file.seek(0)

            # fichier = Fichier(nom=nom, hash='')
            serializer.save(nom=nom,hash='')
            # serializer.save(file.name, temp_file,)
            fichier.path.save(file.name, temp_file)
            fichier.save()
    #
            file_path = fichier.path.path
            hash_value = calculate_sha256(file_path)
            serializer.save(hash=hash_value,nom=nom,user=self.request.user)

def send_file(request):
    if request.method == "POST":
        file = request.FILES['pdf']
        nom=str(file).split(".")[0]
        # hash = calculate_sha256(file)
        fichier=Fichier(nom=nom,path=file,hash='')
        with tempfile.TemporaryFile() as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file.seek(0)

            fichier = Fichier(nom=nom, hash='')

            fichier.path.save(file.name, temp_file)
            fichier.save()

            file_path = fichier.path.path
            hash_value = calculate_sha256(file_path)
            fichier.hash = hash_value
            fichier.save()
            fichier.save()

    return render(request,'Sha2/upload.html')

class ListFile(generics.ListAPIView):
    permission_classes = [IsStaffPermission]
    queryset = Fichier.objects.all()
    serializer_class = FichierGetSerializers

def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            file = request.FILES['pdf']
            nom=str(file).split(".")[0]
            # hash = calculate_sha256(file)
            fichier=Fichier(nom=nom,path=file,hash='')
            with tempfile.TemporaryFile() as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file.seek(0)

                fichier = Fichier(nom=nom, hash='')

                fichier.path.save(file.name, temp_file)
                fichier.save()

                file_path = fichier.path.path
                hash_value = calculate_sha256(file_path)
                fichier.hash = hash_value
                fichier.save()
                fichier.save()

            """path = f"{settings.MEDIA_ROOT}/fichiers/{fichier.path}"
            # path=fichier.path
            hash = calculate_sha256(path)
            fichier.hash=hash
            fichier.save()"""
        fichiers=Fichier.objects.all()
        liste=[]
        for files in fichiers:
            with open(files.path.path, 'rb') as file:
                sha256_hash = hashlib.sha256()
                for chunk in iter(lambda: file.read(4096), b""):
                    sha256_hash.update(chunk)

                hash_value = sha256_hash.hexdigest()
                liste.append(hash_value)

        i=0
        for fil in fichiers:
            setattr(fil, 'test', liste[i])
            i+=1

        context={
            "file":fichiers,

        }
        return render(request,'Sha2/index.html',context)
    else:
        return redirect('signin')
def signup(request):
    context = {

    }
    return render(request, 'Sha2/signup.html', context)

def signin(request):
    if request.user.is_authenticated:
        return render(request,'Sha2/index.html')
    else:
        if request.method == "POST":
            username=request.POST['username']
            pwd = request.POST['pwd']
            if User.objects.filter(username=username):

                user = authenticate(username=username, password=pwd)
                my_user = User.objects.get(username=username)
                if user is not None:
                    login(request, user)
                    firstname = user.first_name
                    return redirect('index')


                else:
                    messages.add_message(request, messages.ERROR, "L'authentification à échouer")
                    return render(request, "Sha2/signin.html", {"error": messages.get_messages(request)})
            else:
                messages.add_message(request, messages.ERROR, "Erreur inconnue!!!")
                return render(request, "Sha2/signin.html", {"error": messages.get_messages(request)})

        return render(request, 'Sha2/signin.html')

# ---------------------user-----------------------------
class AddUser(generics.CreateAPIView):
    # permission_classes = [IsStaffPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer