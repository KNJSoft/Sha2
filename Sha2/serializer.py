from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Fichier

import hashlib



class FichierSerializers(serializers.ModelSerializer):
    # url=serializers.SerializerMethodField(read_only=True)
    # username=serializers.CharField(source='user',read_only=True)

    # validation personnalisée
    # nom=serializers.CharField()
    # hash=serializers.CharField()


    class Meta:
        model=Fichier
        fields=('path',)

    # def validate_nom(self,value):
    #
    #         return value

class FichierGetSerializers(serializers.ModelSerializer):
    hash_verify = serializers.SerializerMethodField(read_only=True)
    username = serializers.CharField(source='user', read_only=True)

    class Meta:
        model=Fichier
        fields=('nom','path','hash','username','hash_verify')

    def get_hash_verify(self,obj):
        with open(obj.path.path, 'rb') as file:
            sha256_hash = hashlib.sha256()
            for chunk in iter(lambda: file.read(4096), b""):
                sha256_hash.update(chunk)

            hash_value = sha256_hash.hexdigest()
        return hash_value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model=User
        fields=("username","password")

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError(f"le nom d'utilisateur doit avoir au moins 4 caracteres")
        elif User.objects.all().filter(username=value):
            raise serializers.ValidationError(f"ce nom d'utilisateur existe déjà")
        else:
            return value

    def validate_password(self, value):
        if len(value) < 12:
            raise serializers.ValidationError(f"le mot de passe doit avoir au moins 12 caracteres")

        else:
            return value