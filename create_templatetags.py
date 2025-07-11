import os

path = "C:/Users/j.sonar/Desktop/django_BOM/bom_project/templatetags"

if not os.path.exists(path):
    os.makedirs(path)

with open(os.path.join(path, "__init__.py"), "w") as f:
    pass
