from src import views

urlpatterns = {
    '/': views.main,
    '/about/': views.about,
    '/contact/': views.contact,
}
