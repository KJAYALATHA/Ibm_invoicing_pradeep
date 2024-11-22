import re
import string


def format_amount(amount):
    """
    method to format the amount value without commas
    :param amount: string amount
    :return: amount without commas
    """
    return re.sub("[^\d\.\"]", "", amount)


# print(format_amount("2,880,485,898,999.55"))


def compare(s1, s2):
    """
    method to compare strings and ignore white space and special characters
    :param s1:
    :param s2:
    :return:
    """
    remove = string.punctuation + string.whitespace
    mapping = {ord(c): None for c in remove}
    return s1.translate(mapping) == s2.translate(mapping)

# print(compare("TAMILNADU", "TAMIL NADU"))
