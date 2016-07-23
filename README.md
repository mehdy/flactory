# Flactory
When you're creating **small applications** using flask everything's **great**!  
but as you're trying to create more and more **large applications** with same structure you always want it will be kind of bothering to copy your last project, remove unwanted parts and change some parts and then start developing your application. It has too much trouble.

so I developed a little handy tool to have some project **template structure** and it will create your project base code using templates.

# Installation
---

as any other python package just:
```
$ pip install flactory
```

# Getting started
---

when you installed flactory you can pull an application template from a git repository:
```
$ flactory pull https://github.com/mehdy/my-flask-app-template.git
```

this will clone the project inside the `.flactory/templates` and you can only use it inside that directory.  
if you want it to be cloned **globally** just pass the `-g` or `--global` option when you want to pull a template
```
$ flactory pull -g https://github.com/mehdy/my-flask-app-template.git
```
now it will clone the project inside the `$HOME/.flactory/templates`. and it's accessible from anywhere by the user whom `$HOME` belongs to.
