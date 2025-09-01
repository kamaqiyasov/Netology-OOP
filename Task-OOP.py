class BasePerson:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
    
    def get_average_grade(self):
        if not hasattr(self, 'grades'):
            return None

        avg_grades = list(map(lambda grade: round(sum(grade) / len(grade), 2), self.grades.values()))
        average_grade = sum(avg_grades) / len(avg_grades) if avg_grades else "Нет оценок"
        return average_grade

    def get_base_info(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def __eq__(self, other):
        # Операция равенства (==).
        if self.get_average_grade() is not None or other.get_average_grade() is not None:
            return self.get_average_grade() == other.get_average_grade()

        return id(self) == id(other)
    
    def __ne__(self, other):
        # Операция неравенства (!=).
        return not self.__eq__(other)
    
    def __lt__(self, other):
        # Операция "меньше" (<).
        if self.get_average_grade() is not None or other.get_average_grade() is not None:
            return self.get_average_grade() < other.get_average_grade()

        return id(self) < id(other)
    
    def __le__(self, other):
        # Операция "меньше или равно" (<=)
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other):
        # Операция "больше" (>)
        return not self.__le__(other)
    
    def __ge__(self, other):
        # Операция "больше или равно" (>=)
        return not self.__lt__(other)

class Student(BasePerson):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname)
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
    
    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        courses_in_progress = ", ".join(self.courses_in_progress) if self.courses_in_progress else "Нет курсов"
        finished_courses = ", ".join(self.finished_courses) if self.finished_courses else "Нет курсов"
        return (
            f'{super().get_base_info()}\n'
            f'Средняя оценка за домашние задания: {super().get_average_grade()}\n'
            f'Курсы в процессе изучения: {courses_in_progress}\n'
            f'Завершенные курсы: {finished_courses}'
        )

class Mentor(BasePerson):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return (
            f'{super().get_base_info()}\n'
            f'Средняя оценка за лекции: {super().get_average_grade()}'
        )

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return super().get_base_info()

def avg_students_course(students, course):
    """
    Функция для подсчета среднего значения оценок по определенному курсу
    Args:
        students (list): Список объектов Student
        course (str): Название курса
    Returns:
        float: Средняя оценка
    """
    
    avg = list(map(lambda x: sum(x.grades[course]) / len(x.grades[course]), filter(lambda s: course in s.grades, students)))
    return round(sum(avg) / len(avg), 2) if avg else 'Такого курса нет'

def avg_lectors_course(lectors, course):
    """
    Функция ля подсчета средней оценки за лекции всех лекторов в рамках курса
    Args:
        students (list): Список объектов Student
        course (str): Название курса
    Returns:
        float: Средняя оценка
    """
    avg = list(map(lambda x: sum(x.grades[course]) / len(x.grades[course]), filter(lambda s: course in s.grades, lectors)))
    return round(sum(avg) / len(avg), 2) if avg else 'Такого курса нет'


lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Олег', 'Олегов')
reviewer1 = Reviewer('Пётр', 'Петров')
reviewer2 = Reviewer('Петя', 'Перово')
student1 = Student('Ольга', 'Алёхина', 'Ж')
student2 = Student('Алена', 'Петрова', 'Ж')

student1.courses_in_progress += ['Python', 'C++']
student2.courses_in_progress += ['Java', 'C++', 'Python']
lecturer1.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Python', 'Java']
reviewer1.courses_attached += ['Python', 'C++']
reviewer2.courses_attached += ['C++', 'Java']

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer2.rate_hw(student2, 'Java', 5)
reviewer2.rate_hw(student2, 'Java', 6)
reviewer2.rate_hw(student2, 'Java', 4)
reviewer2.rate_hw(student2, 'C++', 10)
reviewer2.rate_hw(student2, 'C++', 9)
reviewer2.rate_hw(student2, 'C++', 10)
reviewer1.rate_hw(student1, 'Python', 10)
reviewer2.rate_hw(student1, 'C++', 8)
reviewer2.rate_hw(student1, 'C++', 4)
reviewer2.rate_hw(student1, 'C++', 6)
student1.rate_lecture(lecturer1, 'Python', 7)
student2.rate_lecture(lecturer1, 'Python', 8)
student1.rate_lecture(lecturer1, 'Python', 9)
student1.rate_lecture(lecturer1, 'C++', 9)
student1.rate_lecture(lecturer1, 'C++', 10)
student1.rate_lecture(lecturer2, 'Python', 7)
student1.rate_lecture(lecturer2, 'Python', 1)
student1.rate_lecture(lecturer2, 'Python', 5)
student2.rate_lecture(lecturer2, 'Java', 5)
student2.rate_lecture(lecturer2, 'Java', 3)

print(isinstance(lecturer1, Mentor))
print(isinstance(reviewer1, Mentor))
print(lecturer1.courses_attached)
print(reviewer1.courses_attached)

print(student1)
print(lecturer1)
print(reviewer1)

print(student1 > student2)
print(student1 == student2)

print(lecturer1 > student2)
print(lecturer1 == student2)

print(avg_students_course([student1, student2], 'Python'))
print(avg_lectors_course([lecturer1, lecturer2], 'Python'))