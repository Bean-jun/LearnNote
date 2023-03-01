import os
import re
import sys
import time
from contextlib import contextmanager
from os.path import split

import requests

TARGET_PAGES = "docs"


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


def get_md(workspace):
    if os.path.isfile(workspace):
        return [workspace]

    exclude = ['.git', ".env", TARGET_PAGES]
    path_list = []
    for dirpath, _, filenames in walk(workspace, exclude):
        for filename in filenames:
            if filename.endswith((".md", ".MD")):
                path = os.path.join(dirpath, filename)
                path_list.append(path)
    return path_list


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


def do_mdcat(md_file_path):
    md_file_dir, md_file_name = split(md_file_path)

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
        html_content = template_content.replace("$MD_TITLE", md_file_name).\
            replace("$MD_HTML", response.text)

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


def do_mdcat2(md_file_path):
    md_file_dir, md_file_name = split(md_file_path)

    with open(md_file_path, "r", encoding="utf-8") as md_file:
        md_file_content = md_file.read()
        status, c = convert_link_md_to_html(md_file_path)
        if not status:
            md_file_content = c

    with open(".static/template.tml", "r", encoding="utf-8") as template_file:
        template_content = template_file.read()
    html_content = template_content.replace("$MD_TITLE", md_file_name).\
        replace("$MD_HTML", md_file_content)

    md_file_dir = make_folder(md_file_dir)
    target_path = os.path.join(TARGET_PAGES, md_file_dir)
    mkdirs(target_path)

    new_filename = md_file_name.rstrip(".md") + ".html"
    if new_filename == "README.html":
        new_filename = "index.html"
    path = os.path.join(target_path, new_filename)
    with open(path, "w", encoding="utf-8") as export_file:
        export_file.write(html_content)


def main(workspace):
    path_list = get_md(workspace)
    for path in path_list:
        print("do:", path)
        do_mdcat(path)
        time.sleep(1)


if __name__ == "__main__":
    try:
        argv = sys.argv[1]
    except IndexError:
        argv = "."
    main(argv)
