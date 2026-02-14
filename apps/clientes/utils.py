from .models import Cliente

def clientes_visibles_para(user):

    if user.perfil.es_superadmin():
        return Cliente.objects.all()

    return Cliente.objects.filter(usuario=user)
