# madsuite.org

## Installation
To install the dependency, run:
```bash
git clone git@github.com:MadNLP/madsuite.org.git
cd madsuite.org
pip install .
```

## Usage
To build the website, run:
```bash
python -m madsuiteorg build
```

To serve the website locally, run:
```bash
python -m madsuiteorg serve
```
To deploy the website, push commits to the `main` branch of this repository, which will trigger the auto deployment process. Direct deployment to `gh-pages` is disabled by the repository rule
