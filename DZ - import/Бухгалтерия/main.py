from application.salary import *
from application.db.people import get_employees
import drjson

if __name__ == '__main__':
    print(calculate_salary())
    print(get_employees())
