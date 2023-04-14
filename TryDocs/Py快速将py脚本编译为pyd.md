# Py快速将py脚本编译为pyd

1. 环境安装

    Ubuntu环境安装
    ```shell
    sudo apt install gcc
    sudo apt install python3-dev

    pip install cython
    ```
    windows环境安装
    ```shell
    visual stdio 17(19)(22) 安装一下吧

    pip install cython
    ```


2. 编译脚本

    ```python
    # setup.py
    import os
    from distutils.core import setup

    from Cython.Build import cythonize

    # 不需要编译为pyd的文件
    exclude_filelist = ["__init__.py", "main.py", "config.py", "setup.py"]

    build_file_list = []
    for dirpath, _, filenames in os.walk("."):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if not filename.endswith(".py") or filename in exclude_filelist:
                continue
            build_file_list.append(path)

    setup(ext_modules=cythonize(build_file_list,
                                language_level=3))

    # 编译完成之后，删除原始py文件和编译过程中的c文件
    # 注意：酌情删除
    for py_file in build_file_list:
        c_file = py_file.replace(".py", ".c")
        os.remove(py_file)
        os.remove(c_file)
    ```


3. 开始编译

    ```shell
    python setup.py build_ext --inplace
    ```