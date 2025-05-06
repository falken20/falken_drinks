<div align="center">
  
<!-- Para logo se puede usar https://studio.tailorbrands.com/-->
<img src="./static/images/logo_app.png" alt="drawing" width="400"/>
<a href="https://richionline-portfolio.nw.r.appspot.com"><img src="https://richionline-portfolio.nw.r.appspot.com//static/assets/falken/falken_logo_ia_original.png" width=40 alt="Personal Portfolio web"></a>

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![GitHub language count](https://img.shields.io/github/languages/count/falken20/falken_drinks) ![GitHub Top languaje](https://img.shields.io/github/languages/top/falken20/falken_drinks) ![Test coverage](https://img.shields.io/badge/test%20coverage-0%25-green) ![GitHub License](https://img.shields.io/github/license/falken20/falken_drinks) ![Python used version](https://img.shields.io/static/v1?label=python&message=3.11&color=blue&logo=python&logoColor=white)

  
[![Richi web](https://img.shields.io/badge/web-richionline-blue)](https://richionline-portfolio.nw.r.appspot.com) [![Twitter](https://img.shields.io/twitter/follow/richionline?style=social)](https://twitter.com/richionline)
</div>

---
# falken_drinks
App to manage how much liquid we drink.

##### Deploy
```bash
gcloud app deploy
```

##### Setup
```bash
pip install -r requirements.txt
```

##### Running the app
```bash
flask run
```

##### Running DB utils
```bash
python -m falken_plants.models
```

##### Running the tests with pytest and coverage
```bash
pip install -r requirements-tests.txt
./check_app.sh
```
or
```bash
pip install -r requirements-tests.txt
coverage run -m pytest -v && coverage html --omit=*/venv/*,*/tests/*
```

##### Swagger
```bash
http://127.0.0.1:5000/swagger/
```


##### Environment vars
```bash
LEVEL_LOG                   = "DEBUG, INFO, WARNING, ERROR"

# Configuration mode => development, testing, staging, production
CONFIG_MODE                 = "development" 

# Database URL
DEVELOPMENT_DATABASE_URL    = "sqlite://database.db"
TESTING_DATABASE_URL        = "sqlite:///:memory:"

# Credentials
PRODUCTION_DATABASE_URL     = ""
SECRET_KEY                  = ""
```

##### Configuration file
```bash
.\pyproject.toml
```

---

##### Versions
- 1.0.0 Basic Version


---
##### learning tips
- UV Python package and project manager -> pyproject.toml
