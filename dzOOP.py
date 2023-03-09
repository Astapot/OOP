class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def estimate_lec(self, lecturer, cours, grade):
        if isinstance(lecturer, Lecturer) and cours in self.courses_in_progress and cours in lecturer.courses_attached:
            if cours in lecturer.grades:
                lecturer.grades[cours] += [grade]
            else:
                lecturer.grades[cours] = [grade]
        else:
            return 'Ошибка'

    def average(self):
        if len(self.grades) > 0:
            sum1 = 0
            length = 0
            for i in self.grades.values():
                length += len(i)
                sum1 += sum(i)
            self.average_grade = sum1 / length
        else:
            self.average_grade = 0
        return self.average_grade

    def __str__(self):
        Student.average(self)
        print(f'Имя: {self.name}', f'Фамилия: {self.surname}', sep='\n')
        print(f'Средняя оценка за домашние задания: {self.average_grade}')
        print(f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}')
        return f'Завершенные курсы: {", ".join(self.finished_courses)}'

    def __gt__(self, other):
        Student.average(self)
        Student.average(other)
        return self.average_grade > other.average_grade

    # Не понял зачем тут селф ставить, это нелогично, поэтому поставил другое значение
    def average_grade_course(students, course):
        sum1 = 0
        len1 = 0
        for student in students:
            if isinstance(student, Student) and course in student.courses_in_progress:
                sum1 += sum(student.grades[course])
                len1 += len(student.grades[course])
        return sum1 / len1


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average(self):
        if len(self.grades) > 0:
            sum1 = 0
            length = 0
            for i in self.grades.values():
                length += len(i)
                sum1 += sum(i)
            self.average_grade = sum1 / length
        else:
            self.average_grade = 0
        return self.average_grade

    def __str__(self):
        Lecturer.average(self)
        print(f'Имя: {self.name}', f'Фамилия: {self.surname}', sep='\n')
        return f'Средняя оценка за лекции: {self.average_grade}'

    def __gt__(self, other):
        Lecturer.average(self)
        Lecturer.average(other)
        return self.average_grade > other.average_grade

    # Аналогично неясно, зачем тут селф, поэтому список лекторов
    def average_grade_course(lecturers, course):
        sum1 = 0
        len1 = 0
        for lector in lecturers:
            if isinstance(lector, Lecturer) and course in lector.courses_attached:
                sum1 += sum(lector.grades[course])
                len1 += len(lector.grades[course])
        return sum1 / len1


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        print(f'Имя: {self.name}')
        return f'Фамилия: {self.surname}'


Oleg = Reviewer('oleg', 'myagkov')
Pelmen = Reviewer('Very', 'Hot')


ARTEM = Lecturer('artem', 'korolev')
CAT = Lecturer('Ms', 'Myaw')


sTUDENT = Student('sdt', 'sdfsdf', 'm')

DOG = Student('Mr', 'Waff', 'm')

Pelmen.courses_attached = ['Python']
DOG.courses_in_progress = ['Python']
CAT.courses_attached = ['Python']
Student.estimate_lec(DOG, CAT, 'Python', 1)
Student.estimate_lec(DOG, CAT, 'Python', 2)
# print(CAT.grades)
# print(CAT)

Reviewer.rate_hw(Pelmen, DOG, 'Python', 10)
Reviewer.rate_hw(Pelmen, DOG, 'Python', 7)
# print(DOG)

# print(Lecturer.__gt__(CAT, ARTEM))
# print(Student.__gt__(sTUDENT, DOG))
# print(Student.__gt__(DOG, sTUDENT))
# print(CAT)
# print(DOG)
Oleg.courses_attached = ['Python']
Reviewer.rate_hw(Oleg, DOG, 'Python', 3)
Reviewer.rate_hw(Pelmen, DOG, 'Python', 10)
sTUDENT.courses_in_progress = ['Python']
Reviewer.rate_hw(Pelmen, sTUDENT, 'Python', 5)
# print(sTUDENT)
# print(DOG.grades)
# print(sTUDENT.grades)
# print(Student.average_grade_course([DOG, sTUDENT], 'Python'))
print(CAT.grades)
print(ARTEM.grades)
print(Lecturer.average_grade_course([CAT, ARTEM], 'Python'))