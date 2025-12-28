from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'  # ✅ Importante ser o caminho completo
    verbose_name = 'Usuários'