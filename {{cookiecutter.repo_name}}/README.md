# {{cookiecutter.repo_name}}


## Requirements

```
pyenv virtualenv 3.7.1 env-{{cookiecutter.repo_name}}
pyenv activate env-{{cookiecutter.repo_name}}
pip install poetry
poetry update
```


## Environment Variables

# URL to fetch token
TOKEN_URL=
# Root api url
API_URL=
# API Client ID
CLIENT_ID=
# API Client Secret
CLIENT_SECRET=
# API Audience, may vary (from Auth0)
AUDIENCE=