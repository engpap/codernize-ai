# Documentation Generation Tool
### Set Up
Make sure you set the OPENAI_API_KEY environment variable before running the script. You can do this by running the following command in your terminal:

```bash
export OPENAI_API_KEY=<your_openai_api_key>
```

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