from django.contrib.auth import authenticate

def autenticar_usuario(username, password):
    user = authenticate(username=username, password=password)
    return user
