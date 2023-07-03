import random
import string


def get_hash(len_hash: int):
    """
    Создаёт хеш-код
    :param len_hash: длинна хеша
    :return: хеш-код
    """
    hash_code = ''

    for i in range(len_hash):
        if random.randint(0, 1):
            hash_code += random.choice(string.ascii_uppercase + string.digits).lower()
        else:
            hash_code += random.choice(string.ascii_uppercase + string.digits).upper()

    return hash_code
