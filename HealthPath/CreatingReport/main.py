import helper
import math


def get_key_value_pair_results(path):
    mini_lab = helper.read_lab_results(path)
    analysis_code_and_result = dict(zip(mini_lab['analysis code'], mini_lab['result']))
    analysis_code_and_normal_range = dict(zip(mini_lab['analysis code'], mini_lab['normal range']))
    final_result = {}
    for code, result in analysis_code_and_result.items():
        if type(result) != str:
            if math.isnan(analysis_code_and_normal_range[code]):
                final_result[code] = result
        if helper.has_numbers(result):
            final_result, lesser_or_bigger_normal_range, normal_range, failed = helper.get_normal_results(
                                        result, analysis_code_and_normal_range[code], final_result, code)
            if failed:
                continue
            final_result, lesser_or_bigger, result, failed2 = helper.get_results(result, final_result, code)
            if failed2:
                continue
            if len(normal_range) == 3:
                final_result = helper.three_values(lesser_or_bigger_normal_range, result, normal_range, final_result, code)

            elif len(normal_range) == 2:
                final_result = helper.two_values(final_result, result, normal_range, code)
            elif len(normal_range) == 1:
                final_result = helper.one_value(lesser_or_bigger_normal_range, normal_range, result, final_result, code)

        else:
            final_result = helper.string_values_with_normal_range(result, final_result, code)

    return final_result


get_key_value_pair_results("data/Lab_results/A712C-Maxi-Muster.csv")