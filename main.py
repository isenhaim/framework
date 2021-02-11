from src.conf import middlewares
from src.core import Application

from src.urls import urlpatterns

application = Application(urlpatterns, middlewares)
