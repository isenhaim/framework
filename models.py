import jsonpickle

from patterns.observer import Observer, Subject
from patterns.prototype import PrototypeMixin
from src.unitofwork import DomainObject


class BaseSerializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


class User:
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    types = {"student": Student, "teacher": Teacher}

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class Category:
    id = 0

    def __init__(self, name, category):
        self.id = Category.id
        Category.id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Course(PrototypeMixin, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class SmsNotifier(Observer):
    def update(self, subject: Course):
        print("SMS->", "к нам присоединился", subject.students[-1].name)


class EmailNotifier(Observer):
    def update(self, subject: Course):
        print(("EMAIL->", "к нам присоединился", subject.students[-1].name))


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {"interactive": InteractiveCourse, "record": RecordCourse}

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class TrainingSite:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print("item", item.id)
            if item.id == id:
                return item
            else:
                return item
        raise Exception(f"Нет категории с id = {id}")

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item
