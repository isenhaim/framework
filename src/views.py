import datetime

from logger import Logger, debug
from models import BaseSerializer, EmailNotifier, SmsNotifier, TrainingSite
from src.cbv import CreateView, ListView
from src.conf import code_success, middlewares
from src.core import Application, DebugApplication, FakeApplication
from src.render import render

# from src.urls import urlpatterns

site = TrainingSite()
logger = Logger("views")
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


# application = DebugApplication(urlpatterns, middlewares)
# application = FakeApplication(urlpatterns, middlewares)


class StudentCreateView(CreateView):
    template = "create_student.html"

    def create_object(self, data: dict):
        name = data["name"]
        name = name.replace("+", " ")
        new_object = site.create_user("student", name)
        site.students.append(new_object)


class StudentListView(ListView):
    queryset = site.students
    template = "list_students.html"


class CategoryCreateView(CreateView):
    template = "create_category.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["categories"] = site.categories
        return context

    def create_object(self, data: dict):
        name = data["name"]
        category_id = data.get("category_id")

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)


class CategoryListView(ListView):
    queryset = site.categories
    template = "list_category.html"


class AddStudentByCourseCreateView(CreateView):
    template = "add_student.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["courses"] = site.courses
        context["students"] = site.students
        return context

    def create_object(self, data: dict):
        course_name = data["course_name"]

        course = site.get_course(course_name)
        student_name = data["student_name"]

        student = site.get_student(student_name)
        course.add_student(student)


urlpatterns = {
    "/create-student/": StudentCreateView(),
    "/student-list/": StudentListView(),
    "/category-list/": CategoryListView(),
    "/create-category/": CategoryCreateView(),
    "/add-student/": AddStudentByCourseCreateView(),
}

application = Application(urlpatterns, middlewares)


@application.route("/")
@debug
def main(request):
    static = request.get("static", None)
    return code_success, render("index.html", static=static)


@application.route("/courses-list/")
@debug
def courses_list(request):
    logger.log("Список курсов")
    return code_success, render("list_courses.html", objects_list=site.courses)


@application.route("/copy-course/")
@debug
def copy_course(request):
    request_params = request["request_params"]
    name = request_params["name"]
    old_course = site.get_course(name)
    if old_course:
        new_name = f"copy_{name}"
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return code_success, render("list_courses.html", objects_list=site.courses)


@application.route("/create-course/")
@debug
def create_course(request):
    if request["method"] == "POST":
        data = request["data"]
        name = data["name"]
        category_id = data.get("category_id")

        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course("record", name, category)
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
            site.courses.append(course)
        return code_success, render("create_course.html", categories=site.categories)
    else:
        return code_success, render(
            "create_course.html", categories=site.categories, course=site.courses
        )


@application.route("/about/")
@debug
def about(request):
    static = request.get("static", None)
    return code_success, render("about.html", static=static)


@application.route("/contact/")
@debug
def contact(request):
    if request["method"] == "POST":
        data = request["data"]
        theme = data["theme"]
        email = data["email"]
        text = data["text"]

        msg = (
            f"\nPOST-форма\n"
            f'Дата: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}\n'
            f"E-mail: {email}\n"
            f"Тема: {theme}\n"
            f"Сообщение: {text}\n"
        )

        with open("email/emails.txt", "a+") as f:
            f.write(msg)

    return code_success, render("contacts.html")


@application.route("/api/")
def course_api(request):
    return code_success, BaseSerializer(site.courses).save()
