from heapq import nlargest
from operator import itemgetter

from django import template

register = template.Library()


@register.filter
def get_col(value, col):
    for i, k in enumerate(value):
        value[i]['result'] = k[col]
    return nlargest(10, value, key=itemgetter(col))


@register.filter
def get_col_perc(value, args):
    if args is None:
        return []
    arg_list = [arg.strip() for arg in args.split(',')]
    if len(arg_list) != 2:
        return []
    for i, k in enumerate(value):
        value[i]['result'] = (k[arg_list[0]] / k[arg_list[1]]
                              ) if k[arg_list[1]] != 0 else 0

    return nlargest(10, value, key=itemgetter('result'))


@register.filter
def get_col_sum(value, args):
    if args is None:
        return []
    arg_list = [arg.strip() for arg in args.split(',')]
    if len(arg_list) != 2:
        return []
    for i, k in enumerate(value):
        value[i]['result'] = 0
        for sum_idx in arg_list:
            value[i]['result'] += k[sum_idx]
    return nlargest(10, value, key=itemgetter('result'))
