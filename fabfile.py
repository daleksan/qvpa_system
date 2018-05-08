# coding: utf-8
import os
from fabric.api import run, env, cd, roles, sudo
from fabric.contrib.project import rsync_project

env.hosts = ['root@195.122.250.15']

project_name = 'qvpa_system'
project_root = 'qvpa'
project_path = '/webapps/{0}/{1}'.format(project_root, project_name)
project_sync_dir = '/webapps/{0}/'.format(project_root)
venv_path = '/webapps/{0}/env_qvpa/bin'.format(project_root)
python = '{0}/python'.format(venv_path)
pip = '{0}/pip'.format(venv_path)

rsync_excludes = ['*.pyc', '*.db', '*~']


def sync():
    rsync_project(project_sync_dir, delete=False, exclude=rsync_excludes)


def install_requirements():
    run('{0} install -r {1}/requirements.txt'.format(pip, project_path))


def db_migrate():
    run('{0} {1}/manage.py migrate --noinput'.format(python, project_path))


def collectstatic():
    run('{0} {1}/manage.py collectstatic --no-input'.format(
        python,
        project_path
    ))


def restart():
    sudo('supervisorctl restart {}'.format(project_root))


def deploy():
    sync()
    install_requirements()
    db_migrate()
    collectstatic()
    restart()
