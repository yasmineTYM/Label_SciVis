## How to install the interface for the first time
1. pull the repo using
```
git pull https://github.com/yasmineTYM/Label_SciVis.git
```
*
2. set up the backend 
* you can activate your own virtual environment, or open the environment in this system by:
```
cd gui/
source /env/bin/activate
```
* install the required package in the virtual environment:
```
pip install Flask==1.0.2 Flask-Cors==3.0.7
```

3. set up the front end 
```
* cd frontend/
* rm -f node_modules
* rm package-lock.json
* npm cache clean --force
* npm install 
```

## How to run the interface?
1. run backend 
* open your own virtual environment or 
```
cd gui/
source /env/bin/activate
```
* cd gui/server/
* python app.py 

2. run frontend 
* cd gui/frontend/
* npm run dev 


## the normal workflow using the git for code management
1. before you trying to update, retrieve the most updated version from the git 
```
git pull
```
2. after you edit the code, check the status
```
git status
```
3. add the changed files to your local repo 
```
git add file_name
git add -A
```

4. commit(save) the changes
```
git commit -m 'add your own comments'
```

5. push your changes to the main branch
```
git push
```



