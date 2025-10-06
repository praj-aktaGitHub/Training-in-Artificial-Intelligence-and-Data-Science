import logging

class InvalidMarksError(Exception):
    pass
def check_marks(marks):
    if marks == None:
        raise InvalidMarksError('Please enter marks')
    if marks < 0 or marks > 100:
        raise InvalidMarksError('Marks must be between 0 and 100')

try:
    check_marks(int(input('Enter marks:')))
except InvalidMarksError as e:
    logging.error(e)
