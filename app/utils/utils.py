from passlib.context import CryptContext
import re


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class Validator:
    @staticmethod
    def only_number(value):
        return re.sub('\D', '', value.replace('.', '').replace('-', ''))

    @staticmethod
    def validateCPF(cpf) -> bool:
        cpf = re.sub('\D', '', cpf.replace('.', '').replace('-', ''))

        if not cpf:
            return False

        if len(cpf) != 11:
            return False

        if cpf == (cpf[0] * len(cpf)):
            return False

        # Variables
        sum_values_1 = 0
        digit_one = 0

        sum_values_2 = 0
        digit_two = 0

        # CALC FOR FIRST DIGIT
        for key, multiply in enumerate(range(len(cpf)-1, 1, -1)):
            sum_values_1 += int(cpf[key]) * multiply

        digit_one = 11 - (sum_values_1 % 11)
        digit_one = digit_one if digit_one <= 9 else 0

        # CALC FOR SECOND DIGIT
        for key, multiply in enumerate(range(len(cpf), 1, -1)):
            sum_values_2 += int(cpf[key]) * multiply

        digit_two = (sum_values_2 * 10) % 11

        if digit_one != int(cpf[9]) or digit_two != int(cpf[10]):
            return False

        return True

    @staticmethod
    def validatePIS(pis) -> bool:
        pis = re.sub('\D', '', pis.replace('.', '').replace('-', ''))

        if not pis:
            return False

        if len(pis) != 11:
            return False

        if pis == (pis[0] * len(pis)):
            return False

        # Variables
        sum_values_1 = 0
        digit_one = 0

        # CALC FOR FIRST DIGIT
        pis_weight = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for key, multiply in enumerate(pis_weight):
            sum_values_1 += int(pis[key]) * multiply

        digit_one = 11 - (sum_values_1 % 11)
        digit_one = digit_one if digit_one <= 9 else 0

        if digit_one != int(pis[10]):
            return False

        return True

    @staticmethod
    def validateEMAIL(email) -> bool:
        email = email.lower()
        # ^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$
        if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
            return True
        else:
            return False
