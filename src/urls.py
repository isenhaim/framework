from src import views

urlpatterns = {
    '/': views.main,
    '/about/': views.about,
    '/contact/': views.contact,
    '/create-category/': views.create_category,
    '/create-course/': views.create_course,
    '/category-list/': views.category_list,
    '/courses-list/': views.courses_list,
    '/copy-course/': views.copy_course,
}
