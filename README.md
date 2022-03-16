<!--
Copyright 2022 Tony Akocs
SPDX-License-Identifier: MIT
-->
# config-compare
This pre-commit hook prevents commits when the specified JSON files contain different key values.

## Background:
Projects often contain a “config-sample.json file that contains JSON-formatted example 
configurations for the project. When a developer wants to run the project, they just 
copy and change the “config-sample.json file to “config.json. The “config.json file 
is used to build the project which will then contain their own specific configurations. 
The developer's custom “config.json” file is never checked into the repository, but 
the “config-sample.json file is always checked into the repository. When a developer 
makes a change to the “config.json file with a new key value, they often neglect to 
include it in the “config-sample.json file. Following that, they commit all of their 
changes to the repository. Then, when you pull down their changes and build the 
application, you will get an error message that says "unknown property" or 
"property not found". Config-compare is utilized to prevent this situation.

# Description:
This pre-commit hook will compare two JSON configuration files. The comparison takes 
place between the developer’s custom “config.json and the project’s 
“config-sample.json file. If the “config-sample.json file does not contain a key 
value that is in the developer’s config.json file, an error message will be displayed 
to the developer. The comparison is to prevent a developer’s custom config file from 
overwriting the project’s default config file template.

## Parameters
| Command Line    | Input                   | Description                                                    |
| --------------- | ----------------------- | -------------------------------------------------------------- |
| --file1         |  String file name       | The developers custom config file (example: config.json)       |
| --file2         |  String file name       | The project sample config file (example: config-sample.json)   |

## To Run:

```bash
# run in current directory
json-config-compare
# json-config-compare --file1 "cdk.json" --file2 "sample.cdk.json"
```


## pre-commit
If you want to run it from Github use this configuration
```yaml
 -  repo: https://github.com/akocs/json-config-compare
    rev: v0.1.0
    hooks:
      - id: json-config-compare
        always_run: true
        args:
          [
            "--file1=cdk.json",
            "--file2=sample.cdk.json",
          ]
```

