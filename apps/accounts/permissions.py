def es_superadmin(user):
    return user.perfil.rol == "SUPERADMIN"
