# Codernize AI

## Overview

This project contains two tools for modernizing Java projects:

- DocGen: Generates documentation for a project.
- ModGen: Generates a modernization report for a project.

## Design Document
You can find the design document [here](./design-doc.pdf).
### Set Up
Make sure you set the OPENAI_API_KEY environment variable before running the script. You can do this by running the following command in your terminal:

```bash
export OPENAI_API_KEY=<your_openai_api_key>
```

## DocGen

### Usage
To run the documentation generation script, use the following command:

```bash
python3 doc-gen.py /path/to/project -o out_docs -doc documentation.md -d
```
Where:
- `/path/to/project` is the path to the project you want to document.
- `-o out_docs` specifies the output directory for the generated documentation.
- `-doc documentation.md` specifies the name of the documentation file to be generated.
- `-d` enables debug mode, which provides additional output for troubleshooting.

Example:
```bash
python3 doc-gen.py /Users/dre/dev/jboss-eap-quickstarts/kitchensink -o out_docs -doc documentation.md -d
```


## ModGen
### Usage
To generate a modernization report, use the following command:

```bash
python3 mod-gen.py /path/to/docs.md /path/to/java/repo -o out_docs -report modernization-report.md -d
```
Where:
- `/path/to/docs.md` is the path of the generated documentation by the modernization tool for better understanding of the project.
- `/path/to/java/repo` is the path to the java repository to be modernized.
- `-o out_docs` specifies the output directory for the generated documentation.
- `-report modernization-report.md` specifies the name of the modernization report file to be generated.
- `-d` enables debug mode, which provides additional output for troubleshooting.

Example:
```bash
python3 mod-gen.py /Users/dre/dev/interview/codernize-ai/docs/output.md /Users/dre/dev/jboss-eap-quickstarts/kitchensink -o out_docs -report modernization-report.md -d
```