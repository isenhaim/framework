import sqlite3
from models import Student

connection = sqlite3.connect('db.sqlite')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DatabaseCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Database commit error: {message}')


class DatabaseUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Database update error: {message}')


class DatabaseDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Database delete error: {message}')


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table = 'student'

    def all(self):
        statement = f'SELECT * from {self.table}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.table} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseDeleteException(e.args)


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
