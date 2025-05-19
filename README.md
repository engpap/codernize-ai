# Codernize AI

## Overview

This project contains three tools for generating documentation, modernization reports, and system diagrams for Java projects:

- DocGen: Generates documentation for a project.
- ModGen: Generates a modernization report for a project.
- DiagGen: Generates a system diagram for a project.

## Design Document
You can find the design document [here](./design-doc.pdf).

## Use of GenAI
GenAI was used in multiple ways throughout this project:
- As a coding assistant, to generate boilerplate code and help bootstrap the initial setup of the project.
- Through the OpenAI API, which is integrated directly into the tools themselves (DocGen, ModGen, and DiagGen) to generate documentation, modernization reports, and system diagrams.
- For prompt engineering, to refine and improve the quality of the prompts used by the tools via the APIs.

### Set Up
Make sure you set the OPENAI_API_KEY environment variable before running the scripts. You can do this by running the following command in your terminal:

```bash
export OPENAI_API_KEY=<your_openai_api_key>
```

## DocGen

### Usage
To run the documentation generation script, use the following command:

```bash
python3 doc-gen.py /path/to/project -o docs -doc documentation.md -d
```
Where:
- `/path/to/project` is the path to the project you want to document.
- `-o docs` specifies the output directory for the generated documentation.
- `-doc documentation.md` specifies the name of the documentation file to be generated.
- `-d` enables debug mode, which provides additional output for troubleshooting.

Example:
```bash
python3 doc-gen.py /Users/dre/dev/jboss-eap-quickstarts/kitchensink -o docs -doc documentation.md -d
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
- `-o docs` specifies the output directory for the generated documentation.
- `-report modernization-report.md` specifies the name of the modernization report file to be generated.
- `-d` enables debug mode, which provides additional output for troubleshooting.

Example:
```bash
python3 mod-gen.py /Users/dre/dev/codernize-ai/docs/output.md /Users/dre/dev/jboss-eap-quickstarts/kitchensink -o docs -report modernization-report.md -d
```

## DiagGen
### Usage
To generate system diagrams, use the following command:

```bash
python3 diag-gen.py /path/to/project -o docs -diagram system-diagram.mermaid -d
```
Where:
- `/path/to/project` is the path to the repository you want to analyze.
- `-o docs` specifies the output directory for the generated diagrams.
- `-diagram system-diagram.mermaid` specifies the name of the system diagram file to be generated.
- `-d` enables debug mode, which provides additional output for troubleshooting.

Example:
```bash
python3 diag-gen.py /Users/dre/dev/jboss-eap-quickstarts/kitchensink -o docs -diagram sys-diagram.mermaid
```