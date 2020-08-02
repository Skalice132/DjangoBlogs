from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Приложение "Пользователи"'

    def ready(self):
        import users.signals
