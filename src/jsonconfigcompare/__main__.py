import argparse
from typing import Sequence
import json
import os

"""
This file will compare two JSON files, where --file1 is the developers configuration
file that does not get checked into GIT. The other JSON file, --file2, will be
the sample configuration file that does get checked into GIT. There is also a directory
parameter, --dir, that is also passed just in-case your config files are in a directory.
If your config files are at the top of the directory structure just pass in blank

- repo: https://github.com/akocs/json-config-compare
    rev: main
    hooks:
      - id: json-config-compare
        name: json-config-compare
        description: Compare the projects sample config keys to developers config file
        language: python
        language_version: 3.8.6
        args:
          [
            "--file1=cdk.json",
            "--file2=sample.cdk.json",
          ]

or to run it locally from the .git/hooks directory

 - repo: local
    hooks:
      - id: json-config-compare
        name: json-config-compare
        description: Compare the projects sample config keys to developers config file
        language: python
        language_version: 3.8.6
        entry: python .git/hooks/jsonconfigcompare.py
        args:
          [
            "--file1=cdk.json",
            "--file2=sample.cdk.json",
          ]

"""

def __loadConfigFile(fileName: str) -> list:
    # Get current working directory
    cwd = os.getcwd()
    keys = []
    localFileName = cwd + "/" + fileName
    with open(localFileName, "r", encoding='utf-8') as stream:
        try:
            data = json.load(stream)
            __get_keys(data, keys)
        except Exception as e:
            print(f"Error: {e}")
    return keys

def __get_keys(data, keys_list):
    if isinstance(data, dict):
        for k, v in iter(sorted(data.items())):
            if isinstance(v, list):
                __get_keys(v, keys_list)
            elif isinstance(v, dict):
                __get_keys(v, keys_list)
            keys_list.append(k)   #  Altered line
    elif isinstance(data, list):
        for i in data:
            if isinstance(i, list):
                __get_keys(i, keys_list)
            elif isinstance(i, dict):
                __get_keys(i, keys_list)
    else:
        print("** Skipping item of type: {}").format(type(data))
    return keys_list

def __checkIfEqual(l1: list, l2: list) -> bool:
    l1.sort()
    l2.sort()
    if (l1 == l2):     
        return True
    else:
        return False        
  
def __parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dir', type=str, default='',
        help='directory where the config files are located',
    )
    parser.add_argument(
        '--file1', type=str, default='config.yaml',
        help='Developers config YAML file',
    )
    parser.add_argument(
        '--file2', type=str, default='config-sample.yaml',
        help='Sample config YAML file',
    )
    parser.set_defaults(verbose=False)
    parser.add_argument('files', nargs=argparse.REMAINDER)
    return parser.parse_args()

def main(argv: Sequence[str] = None) -> int:
    args = __parse_arguments()
    configFile = args.file1
    configSampleFile = args.file2
    configKeys = __loadConfigFile(configFile)
    configSampleKeys = __loadConfigFile(configSampleFile)
    
    # remove duplicates
    configKeys = list( set( configKeys ) )
    configSampleKeys = list( set( configSampleKeys ) )

    isEqual = __checkIfEqual(configKeys, configSampleKeys)
    if (isEqual):
        print("Config files are same")
    else:
        list_difference = []
        for element in configSampleKeys:
            if element not in configKeys:
                list_difference.append(element)
        print(f"Missing values in {configSampleFile}: {list_difference}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
