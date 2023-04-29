import random


def generate_number_for_card():
    number = [str(random.randint(0, 9)) for _ in range(15)]
    return "4"+"".join(number)


def generate_cvv_fo_card():
    cvv = [str(random.randint(0, 9)) for _ in range(3)]
    return "".join(cvv)