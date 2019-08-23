import pandas as pd


def read_lab_results(path):
    """

    :return:
    """
    lab = pd.read_csv(path, delimiter=";")
    return lab


def has_numbers(inputString):
    if type(inputString) == str:
        return any(char.isdigit() for char in inputString)


def has_lesser_or_bigger(result):
    lesser_or_bigger = None
    if "<" in result:
        lesser_or_bigger = "<"
    elif ">" in result:
        lesser_or_bigger = ">"
    return lesser_or_bigger


def convert_scientific_notation_to_number(result):

    if "-" in result:
        if "^" not in result:
            lesser_or_bigger = has_lesser_or_bigger(result)
            result = result.lower()
            result = result.replace(",", ".")
            result = result.split("-")
            result1 = float(result[0])
            result2 = float(result[1])
            return lesser_or_bigger, [result1, result2]
        else:
            lesser_or_bigger = has_lesser_or_bigger(result)
            result = result.lower()
            result = result.replace("^", "*")
            result = result.replace(",", ".")
            result = result.split("-")
            result1 = result[0].split("*")
            result2 = result[1].split("*")
            result1 = float(result1[0]) ** float(result1[1])
            result2 = float(result2[0]) ** float(result2[1])
            return lesser_or_bigger, [result1, result2]
    else:
        lesser_or_bigger = has_lesser_or_bigger(result)
        try:
            result = float(result)
            return lesser_or_bigger, [result]
        except:
            result = result.lower()
            result = result.replace("<", "")
            result = result.replace(">", "")
            result = result.replace("^", "*")
            result = result.replace("x", "*")
            result = result.replace(",", ".")
            result = str.strip(result)
            result = result.split("*")
            return lesser_or_bigger, result


def three_values(lesser_or_bigger_normal_range, result, normal_range, final_result, code):
    lab_result = float(result[0]) * float(result[1]) ** float(result[2])
    normal_range_value = float(normal_range[0]) * float(normal_range[1]) ** float(normal_range[2])
    if lesser_or_bigger_normal_range == ">":
        if lab_result >= normal_range_value:
            final_result[code] = "positive"
        elif lab_result < normal_range_value:
            final_result[code] = "negative"

    elif lesser_or_bigger_normal_range == "<":
        if lab_result <= normal_range_value:
            final_result[code] = "positive"
        elif lab_result > normal_range_value:
            final_result[code] = "negative"

    return final_result


def two_values(final_result, result, normal_range, code):
    if len(result) == 3:
        lab_result = float(result[0]) * float(result[1]) ** float(result[2])
    elif len(result) == 1:
        lab_result = result[0]
    if (lab_result >= normal_range[0]) and (lab_result < normal_range[1]):
        final_result[code] = "in_range"
    elif lab_result < normal_range[0]:
        final_result[code] = "below"
    elif lab_result > normal_range[1]:
        final_result[code] = "above"
    return final_result


def one_value(lesser_or_bigger_normal_range, normal_range, result, final_result, code):
    normal_range_value = float(normal_range[0])
    if len(result) == 3:
        lab_result = float(result[0]) * float(result[1]) ** float(result[2])
    elif len(result) == 1:
        lab_result = result[0]
    else:
        print(result)
    if lesser_or_bigger_normal_range == ">":
        if lab_result >= normal_range_value:
            final_result[code] = "positive"
        elif lab_result < normal_range_value:
            final_result[code] = "negative"

    elif lesser_or_bigger_normal_range == "<":
        if lab_result <= normal_range_value:
            final_result[code] = "positive"
        elif lab_result > normal_range_value:
            final_result[code] = "negative"

    return final_result


def get_normal_results(result, normal_value, final_result, code):
    failed = False
    try:
        lesser_or_bigger_normal_range, normal_range = convert_scientific_notation_to_number(normal_value)
    except:
        final_result[code] = result[0]
        failed = True
        lesser_or_bigger_normal_range = None
        normal_range = None

    return final_result, lesser_or_bigger_normal_range, normal_range, failed


def get_results(result, final_result, code):
    failed = False
    try:
        lesser_or_bigger, result = convert_scientific_notation_to_number(result)
        if len(result) == 1:
            try:
                float(result[0])
            except:
                final_result[code] = result[0]
                failed = True
                lesser_or_bigger = None
                result = None
    except:
        final_result[code] = result
        failed = True
        lesser_or_bigger = None
        result = None

    return final_result, lesser_or_bigger, result, failed


def string_values_with_normal_range(result, final_result, code):
    if result == "positiv":
        final_result[code] = "positive"
    elif result == 'negativ':
        final_result[code] = "negative"
    else:
        final_result[code] = result

    return final_result