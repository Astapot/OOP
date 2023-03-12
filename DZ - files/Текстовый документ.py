from pprint import pprint
# # Задание 1
# with open('rec.txt', encoding='utf-8') as file:
#     cook_book = {}
#     for line in file:
#         ingredients = []
#         ingredient = {}
#         meal = line.strip()
#         ing_count = int(file.readline())
#         for i in range(ing_count):
#             ingredient = {}
#             line_ = file.readline()
#             ingredient['ingredient_name'] = line_.split(' | ')[0]
#             ingredient['quantity'] = line_.split(' | ')[1]
#             ingredient['measure'] = line_.split('| ')[2].strip()
#             ingredients.append(ingredient)
#         cook_book[meal] = ingredients
#         file.readline()
#     # pprint(cook_book, sort_dicts=False)
#








# # Задание 2
#
# def get_shop_list_by_dishes(dishes, person_count):
#     result = {}
#     for dish in dishes:
#         for meal in cook_book:
#             if dish == meal:
#                 for ingredients in cook_book[meal]:
#                     ingredient = {}
#                     ingredient['measure'] = ingredients['measure']
#                     ingredient['quantity'] = int(ingredients['quantity']) * person_count
#                     if ingredients['ingredient_name'] not in result:
#                         result[ingredients['ingredient_name']] = ingredient
#                     else:
#                         result[ingredients['ingredient_name']]['quantity'] += ingredient['quantity']
#     return result
#
# pprint(get_shop_list_by_dishes(['Омлет','Утка по-пекински','Фахитос'], 3), sort_dicts=False)



# Задание 3


#
# import os
# a = os.getcwd()
# b = 'py-homework-basic-files'
# c = '2.4.files'
# d = 'sorted'
# e = '1.txt'
# g = '2.txt'
# f = '3.txt'
# path1 = os.path.join(a,b,c,d,e)
# path2 = os.path.join(a,b,c,d,g)
# path3 = os.path.join(a,b,c,d,f)
# new_dict = {}
# with open(path1, encoding='utf-8') as file1:
#     len1 = len(file1.readlines())
#     new_dict[e] = len1
# with open(path2, encoding='utf-8') as file2:
#     len2 = len(file2.readlines())
#     new_dict[g] = len2
# with open(path3, encoding='utf-8') as file3:
#     len3 = len(file3.readlines())
#     new_dict[f] = len3
# with open('result', 'w', encoding='utf-8') as result:
#     for i in sorted(new_dict.values()):
#         for n in new_dict:
#             if new_dict[n] == i:
#                 result.writelines([n,'\n'])
#                 result.writelines([str(i), '\n'])
#                 a1 = os.getcwd()
#                 b1 = 'py-homework-basic-files'
#                 c1 = '2.4.files'
#                 d1 = 'sorted'
#                 e1 = n
#                 path = os.path.join(a1,b1,c1,d1,e1)
#                 with open(path, encoding='utf-8') as f1:
#                     result.write(f1.read())



