1.  Clone repo 
```
$ git clone git@github.com:nav13n/hrassist.git
```
2. Setup environment
```
$ cd hrassist
$ conda env create -f environment.yaml
$ conda activate hrassist
```
3. Create a data directory and add resumes to it
```
$ mkdir data
```
4. Create a .env file with following variables
```
OPENAI_API_TYPE="azure"
OPENAI_API_BASE="your_openai_api_url"
OPENAI_API_VERSION="your_openai_api_version"
OPENAI_API_KEY="your_openai_api_key"
OPENAI_API_ENGINE="your_openai_api_engine"
```
5. Run the extraction script
```
$ python hrassist/main.py
```