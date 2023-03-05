import os
import re
import shutil
import string
import sys
import time
from contextlib import contextmanager

import requests

TARGET_PAGES = "docs"
READ_SPEND = 400

Authorization = os.getenv("TOKEN")


@contextmanager
def to_folder(path):
    oldpath = os.getcwd()
    try:
        os.chdir(path)
        yield oldpath
    finally:
        os.chdir(oldpath)


def get_base_path():
    return os.path.dirname(os.path.abspath(__file__))


def mkdirs(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except Exception as e:
        print(e.args)


def walk(path=".", exclude=None):
    if exclude is None:
        exclude = []

    global_folders = []

    def __func(path):
        dirpath = os.getcwd()
        folders = []
        filenames = []

        to_path = os.path.join(dirpath, path)
        with to_folder(to_path):
            dirpath = os.getcwd()
            for folder_or_file in os.listdir(path):
                if folder_or_file in exclude:
                    continue
                if os.path.isdir(os.path.join(to_path, folder_or_file)):
                    folders.append(folder_or_file)
                    global_folders.append(os.path.join(to_path,
                                                       folder_or_file))
                else:
                    filenames.append(folder_or_file)
            return dirpath, folders, filenames

    yield __func(path)

    for folder in global_folders:
        yield __func(folder)


def get_type_file(workspace, file_type):
    exclude = ['.git', ".env", TARGET_PAGES]
    path_list = []
    for dirpath, _, filenames in walk(workspace, exclude):
        for filename in filenames:
            if filename.endswith(file_type):
                path = os.path.join(dirpath, filename)
                path_list.append(path)
    return path_list


def get_md(workspace):
    if os.path.isfile(workspace):
        return [workspace]

    return get_type_file(workspace, (".md", ".MD"))


def convert_link_md_to_html(path):
    with open(path, "r", encoding="utf-8") as md_file:
        md_file_content_s = md_file.readlines()

    ole_strs = ""
    new_strs = ""
    for md_file_content in md_file_content_s:
        c = re.sub("\.md", ".html", md_file_content)
        ole_strs += md_file_content
        new_strs += c
    return ole_strs == new_strs, new_strs


def make_folder(path):
    path = path[len(get_base_path()):]
    if path.startswith("\\"):
        return path[1:]
    return path


def get_article_length(content):
    # 获取文章字数
    other = string.ascii_letters+string.digits+string.punctuation+" "
    size = 0
    for _char in content:
        if _char not in other:
            size += 1
    return size


def get_article_read_spend(size):
    spend = size // READ_SPEND
    if spend <= 1:
        return "1"
    return str(int(spend))


def do_mdcat(md_file_path, title_list):
    md_file_dir, md_file_name = os.path.split(md_file_path)

    with open(md_file_path, "r", encoding="utf-8") as md_file:
        md_file_content = md_file.read()
        status, c = convert_link_md_to_html(md_file_path)
        if not status:
            md_file_content = c

    url = "https://api.github.com/markdown"

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
    }

    if Authorization:
        headers["Authorization"] = "Bearer %s" % Authorization

    payload = {"text": md_file_content}
    response = requests.request("POST", url, headers=headers,
                                json=payload, verify=False)

    if response.status_code == 200:
        with open(".static/template.tml", "r", encoding="utf-8") as template_file:
            template_content = template_file.read()

        title_strs = ""
        for title in title_list:
            _str = "<li><a href=\"#%s\">%s</a></li>" % (title, title)
            title_strs += _str

        content = response.text
        content_len = get_article_length(content)
        html_content = template_content.replace("$MD_TITLE", md_file_name).\
            replace("$MD_HTML", content).\
            replace("$MD_LINK", title_strs).\
            replace("$MD_SIZE", str(content_len)).\
            replace("$MD_TIME", get_article_read_spend(content_len))

        md_file_dir = make_folder(md_file_dir)
        target_path = os.path.join(TARGET_PAGES, md_file_dir)
        mkdirs(target_path)

        new_filename = md_file_name.strip(".md") + ".html"
        if new_filename == "README.html":
            new_filename = "index.html"
        path = os.path.join(target_path, new_filename)
        with open(path, "w", encoding="utf-8") as export_file:
            export_file.write(html_content)
    else:
        print("ERROR:", response.json()["message"])


def match_value(c, symbol):
    rex = re.match(symbol, c)
    if not rex:
        return ""
    return c.lstrip("#").lstrip()


def scan_article_title(path):

    with open(path, "r", encoding="utf-8") as md_file:
        content = md_file.readlines()

    titles = []
    for symbol in ("## ", "### ", "\d+\."):
        status = False
        for x in content:
            x = x.rstrip()
            rex = match_value(x, symbol)
            if not rex:
                continue
            titles.append(rex)
            status = True
        if status:
            break
    return titles


def get_static_file(workspace):
    if os.path.isfile(workspace):
        _workspace, _ = os.path.split(workspace)
        workspace = os.path.join(get_base_path(), _workspace)
    
    file_type = (".png", ".PNG", ".jpg", ".JPG",
                 ".jpeg", ".gif", ".JPEG", ".GIF")
    return get_type_file(workspace, file_type)


def do_static_file(workspace):
    paths = get_static_file(workspace)
    for _path in paths:
        path = make_folder(_path)
        target_path = os.path.join(TARGET_PAGES, path)
        folder_path, _ = os.path.split(target_path)
        mkdirs(folder_path)
        shutil.copy(_path, target_path)


def main(workspace):
    path_list = get_md(workspace)
    for path in path_list:
        print("do:", path)
        titles = scan_article_title(path)
        # print(titles)
        do_mdcat(path, titles)
        time.sleep(1)
    # 收集静态文件
    do_static_file(workspace)


if __name__ == "__main__":
    try:
        argv = sys.argv[1]
    except IndexError:
        argv = "."
    main(argv)
