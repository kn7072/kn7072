# coding="utf-8"

path_temp = r"HTML_REPORT\test_temp.html"
path_index = r"HTML_REPORT\index.html"


def create_index_html(dict_temp):
    """
    :param dict_temp:
    :return:
    """
    with open(path_temp) as f:
        data_temp = f.read().format(**dict_temp)
    with open(path_index, "w") as f:
        f.write(data_temp)
