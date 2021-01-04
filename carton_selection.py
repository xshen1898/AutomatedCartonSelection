# -*- coding: utf-8 -*-
# Author: shen.charles@hotmail.com 

import sys
import argparse
from itertools import permutations, product
from functools import reduce

# 箱子类型列表
BOX_LIST = [
    {'name': 'TM1513', 'length': 140, 'width': 100, 'height': 80},
    {'name': 'TM1512', 'length': 200, 'width': 100, 'height': 80},
    {'name': 'TM1509', 'length': 240, 'width': 110, 'height': 100},
    {'name': 'TM1511', 'length': 220, 'width': 140, 'height': 125},
    {'name': 'TM1507', 'length': 280, 'width': 160, 'height': 100},
    {'name': 'TM1510', 'length': 230, 'width': 200, 'height': 120},
    {'name': 'TM1508', 'length': 270, 'width': 180, 'height': 160},
    {'name': 'TM1505', 'length': 330, 'width': 210, 'height': 160},
    {'name': 'TM1506', 'length': 300, 'width': 240, 'height': 220},
    {'name': 'TM1503', 'length': 420, 'width': 270, 'height': 160},
    {'name': 'TM1502', 'length': 420, 'width': 290, 'height': 240},
    {'name': 'TM1504', 'length': 400, 'width': 330, 'height': 270},
    {'name': 'TM1501', 'length': 480, 'width': 340, 'height': 280},
]

# 获取输入参数
def get_args():
    parser = argparse.ArgumentParser(prog='box_selection.py', description='Box Selection.')
    parser.add_argument(
        '--items',
        '-i',
        action='append',
        required=True,
        help='Specify the dimension(length,width,height) of items'
    )
    args = parser.parse_args()
    return args

# 从输入参数获取商品长宽高列表
def get_items(items):
    result = []
    for item in items:
        result.append(list(map(lambda x: int(x), item.split(','))))
    return result
    

# 获取所有的排列集合
def get_permutations(arrs):
    result = []
    for arr in arrs:
        arr_len = len(arr)
        arr_permutation = permutations(arr, arr_len)
        result.append(list(arr_permutation))
    return result

# 获取所有组合的笛卡尔积(Cartesian product)
def get_product(arrs):
    result = list(product(*arrs))
    return result

# 获取一种组合的所有长宽高
def get_items_laying_combination_dimensions(x, y):
    if isinstance(x[0], int) and isinstance(x[1], int) and isinstance(x[2], int):
        combination_dimension1 = (x[0] + y[0], max(x[1], y[1]), max(x[2], y[2]))
        combination_dimension2 = (max(x[0], y[0]), x[1] + y[1], max(x[2], y[2]))
        combination_dimension3 = (max(x[0], y[0]), max(x[1], y[1]), x[2] + y[2])
        return (combination_dimension1, combination_dimension2, combination_dimension3)
    else:
        combination_dimensions = []
        for x_x in x:
            combination_dimension = get_items_laying_combination_dimensions(x_x, y)
            combination_dimensions.extend(combination_dimension)
        return combination_dimensions

def main():
    # 获取商品长宽高列表
    args = get_args()
    items = get_items(args.items)
    # 将所有箱子按体积大小进行排序
    boxes = sorted(BOX_LIST, key=lambda x: x['length'] * x['width'] * x['height'])
    # 获取商品的所有摆放的排列组合
    items_laying_permutations = get_permutations(items)
    # 获取所有商品摆放的排列组合的所有组合(笛卡尔积)
    items_laying_combinations = get_product(items_laying_permutations)
    # 获取所有商品摆放的所有组合的排列组合
    items_laying_combinations_permutations = get_permutations(items_laying_combinations)
    # 获取所有组合的所有长宽高
    results = []
    for items_laying_combinations_permutation in items_laying_combinations_permutations:
        for items_laying_combination in items_laying_combinations_permutation:
            items_laying_combination_dimensions = reduce(
                get_items_laying_combination_dimensions,
                items_laying_combination
            )
            results.append(
                {
                    'combination': items_laying_combination,
                    'dimensions': items_laying_combination_dimensions
                }
            )

    # 从最小的箱子开始，依次遍历所有箱子
    for box in boxes:
        # 依次遍历所有的长宽高
        for result in results:
            for dimension in result['dimensions']:
                if all([dimension[0] <= box['length'], dimension[1] <= box['width'], dimension[2] <= box['height']]):
                    output = '推荐箱型：{}\n组合方式：{}\n组合尺寸：{}'.format(
                        box,
                        result['combination'],
                        dimension
                    )
                    print(output)
                    sys.exit()

    print('未匹配到合适的箱型')

if __name__ == '__main__':
    main()
