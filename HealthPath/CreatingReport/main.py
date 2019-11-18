import helper
import math
import os
import json


skip_values = []

special_cases = ['KONSIS_Stuhl', 'KONSISFE', 'ENTEROTYPA712', "CALPFE", "BIFIDOH1A712", "BACTERH1A712", "SONSTA712",
                 "BIFIDOH2A712"]


def get_key_value_pair_results(path):
    mini_lab = helper.read_lab_results(path)
    encyclopedia, calprotectin = helper.read_encyclopedia()
    encyclopedia = encyclopedia.dropna(subset=['Code'])
    encyclopedia = encyclopedia.set_index("Code")
    encyclopedia = encyclopedia[['red L', 'orange L', 'yellow L', 'Ok ', 'yellow H', 'orange H', 'red H']]
    analysis_and_result = dict(zip(mini_lab['analysis'], mini_lab['result']))
    analysis_code_and_result = dict(zip(mini_lab['analysis code'], mini_lab['result']))
    analysis_code_and_normal_range = dict(zip(mini_lab['analysis code'], mini_lab['normal range']))
    gender = mini_lab['gender'].values[0]
    date_of_birth = mini_lab['date of birth'].values[0]
    age_days = helper.calculates_age_days(date_of_birth)
    final_result = {}
    ranges_display = {}
    for code, result in analysis_code_and_result.items():
        if code not in skip_values:
            if code in special_cases:
                final_result = helper.if_in_special_cases(code, result, final_result, ranges_display, gender, age_days)
                continue
            try:
                ranges = encyclopedia.loc[code].tolist()
            except:
                final_result[code] = result
                continue

            if type(result) != str:
                if math.isnan(analysis_code_and_normal_range[code]):
                    final_result[code] = result

            if helper.has_numbers(result):
                final_result, lesser_or_bigger_normal_range, normal_range, failed = helper.get_normal_results(
                                            result, analysis_code_and_normal_range[code], final_result, code)
                if failed:
                    final_result[code] = result
                    continue

                final_result, lesser_or_bigger, result, failed2 = helper.get_results(result, final_result, code)
                if failed2:
                    continue

                new_range, sign = helper.convert_scientific_notations_into_numbers_in_list(ranges, final_result, code)
                helper.set_range(new_range, ranges_display, code)
                final_result = helper.three_values(lesser_or_bigger_normal_range, result,
                                                       final_result, code, new_range, sign)

            else:
                final_result = helper.string_values_with_normal_range(result, final_result, code, ranges_display)

    new_display_ranges = helper.group_by_ranges(ranges_display)
    final_r = helper.get_final_data_with_ranges(new_display_ranges, final_result)
    return final_result, final_r


# get_key_value_pair_results("data/Lab_results/11897608.20191112131312.csv")