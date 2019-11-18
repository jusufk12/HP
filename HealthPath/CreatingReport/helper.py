import pandas as pd
import numpy as np
import re
from datetime import date
from dateutil import parser


def read_lab_results(path):
    """

    :return:
    """
    lab = pd.read_csv(path, delimiter=";")
    return lab


def read_encyclopedia():
    encyclopedia = pd.read_excel("Matrix.xlsx", sheet_name="Sheet1")
    Calprotectin = pd.read_excel("Matrix.xlsx", sheet_name="Calprotectin")
    return encyclopedia, Calprotectin


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
    if ":" in result:
        result = result.split(":")
        _, r1 = convert_scientific_notation_to_number(result[0])
        _, r2 = convert_scientific_notation_to_number(result[1])
        r = [r1, r2]
        return _, r
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


def get_position(new_range, lab_result):
    for pos in range(len(new_range)):
        if type(new_range[pos]) == list:
            if (lab_result >= new_range[pos][0]) and (lab_result <= new_range[pos][1]):
                 new_range.insert(pos+1, lab_result)
                 break
            elif lab_result < new_range[pos][0]:
                new_range.insert(pos, lab_result)
                break
            elif new_range.count(np.nan) == 6:
                if lab_result > new_range[pos][1]:
                    new_range.insert(pos+2, lab_result)
                    break

        elif not np.isnan(new_range[pos]):
                             
            if lab_result > new_range[pos]:

                if len(new_range)-1 != pos:
                    if lab_result > new_range[pos] and np.isnan(new_range[pos+1]).any():
                        new_range.insert(pos+1, lab_result)
                        break
                else:
                    if lab_result > new_range[pos]:
                        new_range.insert(pos+1, lab_result)
                        break

            else:
                new_range.insert(pos, lab_result)
                break


def three_values(lesser_or_bigger_normal_range, result, final_result, code, new_range, sign):
    if check_if_list_is_in_list(new_range):
        pass
    if len(result) == 1:
        lab_result = float(result[0])
    elif len(result) == 3:
        lab_result = float(result[0]) * float(result[1]) ** float(result[2])
    try:
        get_position(new_range, lab_result)
    except:
        pass

    position = new_range.index(lab_result)
    if new_range.count(lab_result) == 1:
        if lesser_or_bigger_normal_range == "<" and position == 3:
                final_result[code] = 0
        elif lesser_or_bigger_normal_range == "<" and position == 4:
            final_result[code] = 1
        elif lesser_or_bigger_normal_range == "<" and position == 5:
            final_result[code] = position - 3
        elif lesser_or_bigger_normal_range == "<" and position == 6:
            final_result[code] = position - 2

        elif lesser_or_bigger_normal_range == ">" and position == 4:
            final_result[code] = 0
        elif lesser_or_bigger_normal_range == ">" and position == 3:
            final_result[code] = position - 4
        elif lesser_or_bigger_normal_range == ">" and position == 2:
            final_result[code] = position - 4
        elif lesser_or_bigger_normal_range == ">" and position == 1:
            final_result[code] = -3

        elif lesser_or_bigger_normal_range == None and position == 4:
            if type(new_range[new_range.index(lab_result) - 1]) == list:
                if new_range[new_range.index(lab_result) - 1][1] > lab_result:
                    final_result[code] = 0
                else:
                    final_result[code] = 1
            else:
                final_result[code] = position - 4
        else:
            final_result[code] = position-4
    elif new_range.count(lab_result) == 2:
        tmp_index = new_range.index(lab_result)
        if new_range[tmp_index] == new_range[tmp_index+1]:
            temp_value = 1
        else:
            temp_value = 0
        if lesser_or_bigger_normal_range == "<" and position == 3:
            final_result[code] = 0
        elif lesser_or_bigger_normal_range == ">" and position == 4:
            final_result[code] = 0 - temp_value
        elif lesser_or_bigger_normal_range == ">" and position == 3:
            final_result[code] = 0 - temp_value
        else:
            final_result[code] = position-3
    elif new_range.count(lab_result) == 3:
        if sign == "<":
            final_result[code] = new_range.index(lab_result)-2
        else:
            final_result[code] = new_range.index(lab_result)-3

        pass
    normalized_value = final_result[code]
    final_result[code] = [normalized_value, round(lab_result, 2)]
    return final_result


def check_if_list_is_in_list(new_range):
    for l in new_range:
        if type(l) == list:
            return True
    return False


def two_values(final_result, result, normal_range, code, new_range):

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


def one_value(lesser_or_bigger_normal_range, normal_range, result, final_result, code, new_range):
    normal_range_value = float(normal_range[0])
    if len(result) == 3:
        lab_result = float(result[0]) * float(result[1]) ** float(result[2])
    elif len(result) == 1:
        lab_result = result[0]

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


def string_values_with_normal_range(result, final_result, code, ranges_display):
    if result == "positiv" or result == "positive":
        final_result[code] = 2
    elif result == 'negativ' or result == "negative":
        final_result[code] = 0
    elif result == "p":
        final_result[code] = 0
    elif result == "n":
        final_result[code] = 2
    elif result == "borderline" or result == "Borderline":
        final_result[code] = 1
    else:
        final_result[code] = result
        ranges_display[code] = 'no_value'
        return final_result
    ranges_display[code] = 'n/p'
    return final_result


def convert_scientific_notations_into_numbers_in_list(ranges, final_result, code):
    new_range = []
    first = True
    for r in ranges:
        if type(r) == str:
            if first:
                if "<" in r:
                    sign = "<"
                elif ">" in r:
                    sign = ">"
                else:
                    sign = None
                first = False
        try:
            if np.isnan(r):
                new_range.append(r)
            else:
                 new_range.append(float(r))
        except:
            final_result, lesser_or_bigger, result, failed2 = get_results(r, final_result, code)
            if len(result) == 2:
                temp = []
                for n in result:
                    if len(n) == 1:
                        temp.append(float(n[0]))
                    elif len(n) == 2:
                        temp.append(float(n[0]) ** float(n[1]))
                    elif len(n) == 3:
                        temp.append(float(n[0]) * float(n[1]) ** float(n[2]))
                new_range.append(temp)
            else:
                if len(result) == 1:
                    result = float(result[0])
                else:
                    result = float(result[0]) * float(result[1]) ** float(result[2])
                new_range.append(result)
    return new_range, sign


def if_in_special_cases(code, result, final_result, ranges_display, gender, age_days):

    if (code == "KONSIS_Stuhl") or (code == "KONSISFE"):
        if result == "firm" or result == "fest":
            final_result[code] = 1
        elif result == "tough pasty" or result == "zähbreiig":
            final_result[code] = 2
        elif result == "mushy" or result == "breiig":
            final_result[code] = 3
        elif result == "thin mushy" or result == "zähbreiig":
            final_result[code] = 4
        elif result == "liquid" or result == "flüssig":
            final_result[code] = 5
        else:
            final_result[code] = ""
        ranges_display[code] = 'no_value'
    elif code == "BACTERH1A712":
        final_result[code] = result
        ranges_display[code] = 'no_value'
    elif code == "BIFIDOH1A712":
        final_result[code] = result
        ranges_display[code] = 'no_value'
    elif code == 'ENTEROTYPA712':
        if type(result) == str:
            final_result[code] = 1
        else:
            final_result[code] = int(result)
        ranges_display[code] = 'no_value'
    elif code == "BIFIDOH2A712":
        final_result[code] = result
        ranges_display[code] = 'no_value'
    elif code == 'PHFE':
        try:
            final_result[code] = int(result)
        except:
            result = re.findall(r'\d+', result)
            result = int(result[0])
            final_result[code] = result
        ranges_display[code] = '-3/3'
    elif code == "SONSTA712":
        try:
            final_result[code] = float(result)
        except:
            result = re.findall(r'\d+', result)
            result = float(result[0])
            final_result[code] = result

    elif code == "CALPFE":
        def check_value(real, normal):
            if real < normal:
                return 0
            else:
                return 1

        real_val = float(".".join(re.findall('\d+', result)))
        if gender == "M":
            if age_days <= 180:
                normal_value = 280

            elif age_days <= 365:
                normal_value = 180

            elif age_days <= 1460:
                normal_value = 75

            elif age_days <= 65535:
                normal_value = 50

            elif age_days <= 4383:
                normal_value = 50
            normalized_value = check_value(real_val, normal_value)

        elif gender == "W":
            if age_days <= 180:
                normal_value = 280

            elif age_days <= 365:
                normal_value = 180

            elif age_days <= 1460:
                normal_value = 75

            elif age_days <= 65535:
                normal_value = 50

            elif age_days <= 4383:
                normal_value = 50

            normalized_value = check_value(real_val, normal_value)

        elif gender == "U":
            if age_days <= 180:
                normal_value = 280

            elif age_days <= 365:
                normal_value = 180

            elif age_days <= 1460:
                normal_value = 75

            elif age_days <= 65535:
                normal_value = 50

            elif age_days <= 4383:
                normal_value = 50

            normalized_value = check_value(real_val, normal_value)
        ranges_display[code] = '0/1'
        final_result[code] = [normalized_value, real_val]
    return final_result


def set_range(new_range, ranges_display, code):
    l_new = ['missing' if x is np.nan else x for x in new_range]
    res = [i for i, val in enumerate(l_new) if val != 'missing']
    range_to_display = list(map(lambda x: x - 3, res))
    if len(range_to_display) == 1:
        ranges_display[code] = str(range_to_display[0])
    else:
        ranges_display[code] = str(range_to_display[0])+"/"+str(range_to_display[-1])


def group_by_ranges(ranges):
    new_dict = {}
    for pair in ranges.items():
        if pair[1] not in new_dict.keys():
            new_dict[pair[1]] = []

        new_dict[pair[1]].append(pair[0])
    return new_dict


def get_final_data_with_ranges(new_display_ranges, final_result):
    final_r = {}
    for index, values in new_display_ranges.items():
        temp_dict = {}
        for val in values:
            temp_dict[val] = final_result[val]
        final_r[index] = temp_dict

    return final_r


def calculates_age_days(birth_date):
    today = date.today()
    today = parser.parse(str(today))
    birth_date = parser.parse(birth_date)
    delta = today - birth_date
    num_days = delta.days
    return num_days