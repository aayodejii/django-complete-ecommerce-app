from django.apps import AppConfig


class ThemallConfig(AppConfig):
    name = 'themall'

    
    def ready(self):
    	import themall.signals

