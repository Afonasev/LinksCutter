import random
import string


def random_str(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
