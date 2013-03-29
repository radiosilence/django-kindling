import os
import sys
from jinja2 import Environment, PackageLoader
from subprocess import Popen
env = Environment(loader=PackageLoader('kindling', 'templates'))

FILES = (
    ('.gitignore', False),
    ('config.rb', False),
    ('requirements.txt', False),
    ('fabfile.py', False),
    ('settings/__init__.py', True),
    ('settings/base.py', True),
    ('settings/development.py', True),
    ('settings/local.py', True),
    ('settings/production.py', True),
    ('settings/celery_development.py', True),
    ('settings/celery_local.py', True),
    ('settings/celery_production.py', True),
)

def generate(app, path, in_app=False):
    print(u'Generating {}'.format(path))
    template = env.get_template(path)
    data = template.render(app=app)
    path = [app, path]
    if in_app:
        path.insert(0, app)
    with open(os.path.join(*path), 'w') as f:
        f.write(data)

def new(app):
    os.unsetenv('DJANGO_SETTINGS_MODULE')
    if not app:
        print('App must be set.')
        sys.exit()
    
    p = Popen(['pip', 'install', 'django'])
    p.wait()

    
    p = Popen(['django-admin.py', 'startproject', app])
    p.wait()

    p =Popen(['git', 'init', app])
    p.wait()
    
    os.mkdir(os.path.join(app, app, 'settings'))
    os.remove(os.path.join(app, app, 'settings.py'))
    for args in FILES:
        generate(app, *args)

    virtual_env = os.environ.get('VIRTUAL_ENV', None)
    if virtual_env:
        with open(os.path.join(virtual_env, 'bin', 'postactivate'), 'w') as f:
            f.write('#!/bin/zsh\nexport DJANGO_SETTINGS_MODULE={app}.settings.local'.format(app=app))

if __name__ == '__main__':
    new(sys.argv[1])
