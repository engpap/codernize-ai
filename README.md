### Set Up
Make sure you set the OPENAI_API_KEY environment variable before running the script. You can do this by running the following command in your terminal:

```bash
export OPENAI_API_KEY=<your_openai_api_key>
```

# Documentation Generation Tool

### Usage
To run the documentation generation script, use the following command:

```bash
python3 gen_docs.py /path/to/project -o out_docs -doc documentation.md -d
```
Where:
- `/path/to/project` is the path to the project you want to document.
- `-o out_docs` specifies the output directory for the generated documentation.
- `-doc documentation.md` specifies the name of the documentation file to be generated.
- `-d` enables debug mode, which provides additional output for troubleshooting.

Example:
```bash
python3 gen_docs.py /Users/dre/dev/jboss-eap-quickstarts/kitchensink -o out_docs -doc documentation.md -d
```

# Modernization Report

To generate a modernization report, use the following command:

```bash
python3 modernize.py /path/to/docs.md /path/to/java/repo -o out_docs -report modernization-report.md -d
```
Where:
- `/path/to/docs.md` is the path to the documentation file to be generated.
- `/path/to/java/repo` is the path to the java repository to be modernized.
- `-o out_docs` specifies the output directory for the generated documentation.
- `-report modernization-report.md` specifies the name of the modernization report file to be generated.
- `-d` enables debug mode, which provides additional output for troubleshooting.

Example:
```bash
python3 modernize.py /Users/dre/dev/interview/codernize-ai/docs/output.md /Users/dre/dev/jboss-eap-quickstarts/kitchensink -o out_docs -report modernization-report.md -d
```