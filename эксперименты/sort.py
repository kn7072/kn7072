sortList = ['a', 'cc', 'bbb']
sortList2 = [[7,'f'],[3,'a'], [2,'cc'], [5,'bbb']]
dict_for_sort = {0: [{'target_branch': 'yyyyyyyyyy', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/31', 'source_branch': 'xxxxxxxxxxx', 'user': 'sg.chernov', 'project_id': 208, 'state': 'closed', 'id_merge_request': 28198, 'num_merge': '31', 'project': 'merge-request-automatization'},
                     {'target_branch': 'master', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/42', 'source_branch': 'xxxxxxxxxxx', 'user': 'sg.chernov', 'project_id': 208, 'state': 'opened', 'id_merge_request': 28220, 'num_merge': '42', 'project': 'merge-request-automatization'},
                     {'target_branch': 'master', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/38', 'source_branch': 'yyyyyyyyyy', 'user': 'sg.chernov', 'project_id': 208, 'state': 'opened', 'id_merge_request': 28216, 'num_merge': '38', 'project': 'merge-request-automatization'},
                     {'target_branch': 'development', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/44', 'source_branch': 'yyyyyyyyyy', 'user': 'sg.chernov', 'project_id': 208, 'state': 'opened', 'id_merge_request': 28222, 'num_merge': '44', 'project': 'merge-request-automatization'}],
                 1: [{'target_branch': 'master', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/42', 'source_branch': 'xxxxxxxxxxx', 'user': 'sg.chernov', 'project_id': 208, 'state': 'opened', 'id_merge_request': 28220, 'num_merge': '42', 'project': 'merge-request-automatization'},
                     {'target_branch': 'development', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/43', 'source_branch': 'xxxxxxxxxxx', 'user': 'sg.chernov', 'project_id': 208, 'state': 'opened', 'id_merge_request': 28221, 'num_merge': '43', 'project': 'merge-request-automatization'}],
                 2: [{'target_branch': 'yyyyyyyyyy', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/31', 'source_branch': 'xxxxxxxxxxx', 'user': 'sg.chernov', 'project_id': 208, 'state': 'closed', 'id_merge_request': 28198, 'num_merge': '31', 'project': 'merge-request-automatization'},
                     {'target_branch': 'new_branch_for_merge_request', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/35', 'source_branch': 'Branch_branch-100500', 'user': 'sg.chernov', 'project_id': 208, 'state': 'closed', 'id_merge_request': 28208, 'num_merge': '35', 'project': 'merge-request-automatization'},
                     {'target_branch': 'master', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/39', 'source_branch': 'xxxxxxxxxxx', 'user': 'sg.chernov', 'project_id': 208, 'state': 'merged', 'id_merge_request': 28217, 'num_merge': '39', 'project': 'merge-request-automatization'},
                     {'target_branch': 'development', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/43', 'source_branch': 'xxxxxxxxxxx', 'user': 'sg.chernov', 'project_id': 208, 'state': 'opened', 'id_merge_request': 28221, 'num_merge': '43', 'project': 'merge-request-automatization'},
                     {'target_branch': 'development', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/41', 'source_branch': 'xxxxxxxxxxx', 'user': 'sg.chernov', 'project_id': 208, 'state': 'merged', 'id_merge_request': 28219, 'num_merge': '41', 'project': 'merge-request-automatization'},
                     {'target_branch': 'development', 'link': 'https://git.sbis.ru/sg.chernov/merge-request-automatization/merge_requests/41', 'source_branch': 'xxxxxxxxxxx', 'user': 'sg.chernov', 'project_id': 208, 'state': 'merged', 'id_merge_request': 28219, 'num_merge': '41', 'project': 'merge-request-automatization'}]}
# Создаем "внешнюю" функцию, которая будет сортировать список в алфавитном порядке:
def sortByAlphabet(inputStr):
        return inputStr[0] # Ключом является первый символ в каждой строке, сортируем по нему

# Вторая функция, сортирующая список по длине строки:
def sortByLength(inputStr):
        return len(inputStr)  # Ключом является длина каждой строки, сортируем по длине

newList = sorted(sortList2, key=sortByAlphabet)
################################################################
import re

data=['test_140815080910_data.p',
'other_test_140815081010_data.p',
'other_test_140815081111_other_data.p']

data.sort(key=lambda L: (re.findall('\d{10}', L), L))
################################################################
def sort_target_branch(var):
        return var['target_branch']

def sort_for_template(list_for_sort):
        template = ['master', 'development', 'rc-3.7.0', 'other']
        temp_sort = []
        for branch in template:
                for i in list_for_sort:
                        if i['target_branch'] == branch:
                                temp_sort.append(i)
                        if branch == 'other' and i['target_branch'] not in template:
                                temp_sort.append(i)
        return temp_sort


for group, list_merge in dict_for_sort.items():
        # newlist = sorted(list_merge, key=sort_target_branch)
        sort_for_template(list_merge)
        for sort_merge in list_merge:
                 print(sort_merge['target_branch'])
        print ("################################")

print()
