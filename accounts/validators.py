from django.contrib.auth.hashers import check_password
from django.forms import ValidationError

from collections import namedtuple
import re

PasswordStrengthCondition = namedtuple('Condition', ['result', 'message'])


def check_empty(something):
    if something:
        raise ValidationError(
            message="Something went wrong, "
            "this page is not for automated machines",
            code="Tarpit"
        )


def password_checker(pword, userObj=None, oldPword=None):
    errors = []
    password = pword.strip()
    length = PasswordStrengthCondition(
        len(password) >= 14,
        'Must be 14 characters or longer'
    )
    special_character = PasswordStrengthCondition(
        re.search(r'\W+', password) is not None,
        'Must contain a special character'
    )
    lower = PasswordStrengthCondition(
        re.search(r'[a-z]+', password) is not None,
        'Must contain at least one lower case letter',
    )
    upper = PasswordStrengthCondition(
        re.search(r'[A-Z]+', password) is not None,
        'Must contain at least one upper case letter'
    )
    digit = PasswordStrengthCondition(
        re.search(r'\d+', password) is not None,
        'Must contain at least one digit'
    )
    u_name = PasswordStrengthCondition(
        not(userObj.username.lower() in password.lower()),
        'Cannot contain your username'
    )
    f_name = PasswordStrengthCondition(
        not(userObj.first_name.lower() in password.lower()),
        'Cannot contain your first name'
    )
    l_name = PasswordStrengthCondition(
        not(userObj.last_name.lower() in password.lower()),
        'cannot contain your last name'
    )
    for check in [length, special_character, lower, upper, digit, u_name, f_name, l_name]:
        if not check.result:
            errors.append(check.message)
    if oldPword:
        new_is_old = PasswordStrengthCondition(
            (check_password(password, oldPword)),
                 'Must be different from your current password'
                 )
        if new_is_old.result:
            errors.append(new_is_old.message)
    if errors:
        return errors
    else:
        return None