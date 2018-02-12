import os
import string
import json
from .data_html import renderjson_js, script_js, style_css, test_temp_html

def generate_html_report(self):
    """Создает html отчет упавших тестов"""

    descriptions_css_elements = {"parent_spoiler": ["spoiler-trigger"],
                                 "child_spoiler": ["spoiler-block-content"],
                                 "simple_elm_json": ["json"],
                                 "simple_elm": [""],
                                 "error_elem": ["error"]}

    parent_spoiler = """
    <div>
        <a href="#" class="spoiler-trigger">
            <span>{name_class}</span>
        </a>
        <div class="spoiler-block" style="display:none;">
            {child_element}
        </div>
    </div>
    """
    child_spoiler = """
    <div class="spoiler-block-content">
        <a href="#{name_test}" name="{name_test}" class="spoiler-trigger">
            <span>{name_test}</span>
        </a>
        <div class="spoiler-block">
            {content}
        </div>
    </div>
    """
    simple_elm_json = """
    <div class="json">{content}</div>
    """
    simple_elm = """
    <div>{content}</div>
    """

    error_elem = """
    <pre class="error">{content}</pre>
    """

    def get_content(list_msg):
        temp_text = ""
        for level, msg, type_msg in list_msg:
            if type_msg == "json":
                msg = simple_elm_json.format(content=msg)
            elif level == "[e]":
                msg = error_elem.format(content=msg)
            else:
                msg = simple_elm.format(content=msg)
            temp_text += msg
        return temp_text

    path_dir = os.path.join(self.config_general.get('LOG_FILE_PATH'), str(self.config_general.get('BUILD', "1")))
    if not os.path.isdir(path_dir):
        os.mkdir(path_dir)
    encoding = "cp1251"
    list_html_suite = []
    for name_file in os.listdir(path_dir):
        if not name_file.endswith(".json"):
            continue
        name_class = name_file.split(".json")[0]
        path = os.path.join(path_dir, name_file)
        with open(path, "r+", encoding=encoding) as f:
            suite_info = json.loads(f.read())
        # анализируем тесты
        list_names_tests = [name_test for name_test in suite_info.keys() if name_test.startswith("test_")]
        list_logs_tests = []
        error_test = False  # если сам тест или teardown завершился ошибкой - считаем тест упавшим
        for test_i in list_names_tests:
            if suite_info[test_i][-1][0] == "[e]":
                # тест завершился ошибкой
                # todo вынести в отдельную функцию
                log_test = get_content(suite_info[test_i])
                html_log = child_spoiler.format(name_test=test_i, content=log_test)
                list_logs_tests.append(html_log)
                error_test = True

            name_teardown = "teardown_" + test_i
            if suite_info.get(name_teardown, None):
                # если teardown есть и в нем ошибка
                if suite_info[name_teardown][-1][0] == "[e]":
                    log_test = get_content(suite_info[name_teardown])
                    html_log = child_spoiler.format(name_test=name_teardown, content=log_test)
                    list_logs_tests.append(html_log)
                    error_test = True

        # Добавляем setup_class - ЕСЛИ ЕСТЬ
        name_setupclass = "setupclass_" + name_class
        if suite_info.get(name_setupclass, None):
            if error_test or suite_info[name_setupclass][-1][0] == "[e]":
                log_test = get_content(suite_info[name_setupclass])
                html_log = child_spoiler.format(name_test=name_setupclass, content=log_test)
                list_logs_tests.append(html_log)

        text_child_element = " ".join(list_logs_tests)
        html_suite = parent_spoiler.format(name_class=name_class, child_element=text_child_element)
        list_html_suite.append(html_suite)

    all_html = "".join(list_html_suite)
    all_html = test_temp_html.format(contents_tests=all_html)

    html = os.path.join(path_dir, "index.html")
    with open(html, "w", encoding="utf-8") as f:
        f.write(all_html)

    path_renderjson_js = os.path.join(path_dir, "renderjson.js")
    with open(path_renderjson_js, "w", encoding="utf-8") as f:
        f.write(renderjson_js)

    path_script_js = os.path.join(path_dir, "script.js")
    with open(path_script_js, "w", encoding="utf-8") as f:
        f.write(script_js)

    path_style_css = os.path.join(path_dir, "style.css")
    with open(path_style_css, "w", encoding="utf-8") as f:
        f.write(style_css)

