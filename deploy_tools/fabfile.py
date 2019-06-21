from fabric.contrib.files import append,exists,sed
from fabric.api import env,local,run
import random

REPO_URL='https://github.com/jingjing0823/superlists.git'

def deploy():
    site_folder=f'/home/{env.user}/sites/{env.host}'
    source_folder=site_folder+"/source"
    _create_directory_if_necessary(site_folder)
    _get_latest_source(source_floder)
    _update_setting(source_floder,env.host)
    _update_virtualenv(source_floder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_if_necessary(site_folder):
    for subfolder in ('database','static','virtualenv','source'):
        run(f'mkdir -p {site_folder}/{subfolder}')
        
def get_latest_source(source_folder):
    if exists(source_folder+"/.git"):
        run(f'cd {souce_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit=local("git log -n 1 --format=%H",capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')
    
def _upate_settings(source_folder,site_name):
    settings_path=source_folder+'/superlists/settings.py'
    sed(settings_path,'DEBUG = True','DEBUG = False')
    sed(settings_path,'ALLOWED_HOSTS =.+$',f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file=source_folder+'superlists/secret_key.py'
    if not exists(secret_key_file):
        chars= 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+{}":'
        key= ''.join(random.SystemRandom().choice(chars) for _ in rang(50))
        append(secret_key_file,f'SECRET_KEY = {key}')
    append(settings_path,'\nfrom .secret_key_file import SECRET_FILE')    
    
def _update_virtualenv(source_folder):
    virtualenv_folder=source_folder+"/../virtualenv"
    if not exists(virtualenv_folder):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')
def _update_static_files(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic')
    
def _update_database(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')    