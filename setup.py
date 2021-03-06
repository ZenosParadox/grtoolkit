import setuptools, os, sys, re
from grtoolkit.Storage import search, File
from os.path import dirname

def gen_manifestation():
    manifestation = File(dirname(__file__) + "\\MANIFEST.in")
    _, files = search(dirname(__file__),viewPrint=False, rootInclude=True,abs=True)

    exts = [".jpg", "png", ".docx", ".pdf", ".accdb", ".exe", ".csv", ".zip"]
    protect_files = list()

    for file in files:
        for ext in exts:
            if file[(len(file)-len(ext)):] == ext:
                protect_files.append(file)

    for i in range(len(protect_files)):
        manifestation.write_and_append("include " + protect_files[i].replace('\\', '/'))

with open("README.md", "r") as fh:
    long_description = fh.read()

def delDotPrefix(string):
    '''Delete dot prefix to file extension if present'''
    return string[1:] if string.find(".") == 0 else string

def filesInFolder(folder, fileType):  # Returns list of files of specified file type
    fileType = delDotPrefix(fileType)
    file_regex = re.compile(
        r".*\." + fileType, re.IGNORECASE
    )  # Regular Expression; dot star means find everything
    file_list = []
    for _, _, filenames in os.walk(folder):  # folders, subfolders, filenames
        for singlefile in filenames:
            file_search = file_regex.findall(singlefile)
            if file_search:  # if file_search is not empty
                file_list.append(singlefile)
    return file_list

# NOTE: PATHS CALCULATED IN SETUP.PY NEED UNIX STYLE PATH REFERENCES WITH DIFFERENT SLASHES

gen_manifestation() #Update Manifestation File

setuptools.setup(
    name="grtoolkit",
    version="20.11.4",
    author="Gabriel Rosales",
    author_email="gabriel.alejandro.rosales@gmail.com",
    description="Common functions for quick python development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZenosParadox/grtoolkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=[f'cmdline\\{file}' for file in filesInFolder('cmdline/',"*")],
    include_package_data=True, #To use MANIFEST.in to include non-code files
    install_requires=['PyPDF2', 'requests', 'twine', 'wheel', 'pipenv', 'sympy', 'pyautogui', 'numpy', 'pandas', 'matplotlib', 'bs4', 'pyodbc', 'scipy']
)