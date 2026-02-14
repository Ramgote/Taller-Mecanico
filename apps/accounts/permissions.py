def es_superadmin(user):
    return user.perfil.rol == "SUPERADMIN"

def es_responsable(user):
    return user.perfil.rol == "RESPONSABLE"
