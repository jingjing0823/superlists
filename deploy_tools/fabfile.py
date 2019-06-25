from fabric.contrib.files import append,exists,sed
from fabric.context_managers import settings
from fabric.api import env,local,run,sudo
import random

REPO_URL='https://github.com/jingjing0823/superlists.git'

def deploy():
    site_folder=f'/home/{env.user}/sites/{env.host}'
    source_folder=site_folder+"/source"
    _create_directory_of_site(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder,env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _config_nginx_and_systemd(source_folder,env.host)
    _start_project(site_folder+"/..",env.host)

def _create_directory_of_site(site_folder):
    for subfolder in ('database','static','virtualenv','source'):
        _create_directory_if_necessary(f'{site_folder}/{subfolder}')
        
def _create_directory_if_necessary(path):
    run(f'mkdir -p {path}')
    
def _create_directory_if_necessary_by_root(path):
    run(f'mkdir -p {path}')    
        
def _get_latest_source(source_folder):
    _exist_git_=_command_exist_or_not("git --version")
    if not _exist_git_:
        sudo('yum install git -y')
    if exists(source_folder+"/.git"):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit=local("git log -n 1 --format=%H",capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')
    
def _update_settings(source_folder,site_name):
    settings_path=source_folder+'/superlists/settings.py'
    sed(settings_path,'DEBUG = True','DEBUG = False')
    sed(settings_path,'ALLOWED_HOSTS =.+$',f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file=source_folder+'/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars= 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+{}":'
        key= ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file,f'SECRET_KEY = {key}')
    append(settings_path,'\nfrom .secret_key_file import SECRET_FILE')    
    
def _update_virtualenv(source_folder):
    virtualenv_folder=source_folder+"/../virtualenv"
    if not exists(virtualenv_folder):
        _exist_cc=_command_exist_or_not("gcc --version")
        if not _exist_cc:
            run('sudo yum install gcc -y')
        _exist_p_version=_command_exist_or_not("python3.6 -V|awk '{print $2}'")
        if not _exist_p_version:
            _install_python_env_from_source_code(source_folder+"/../../tools")
    run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')
def _update_static_files(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic -c --noinput')
    
def _update_database(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')
    
def _install_python_env_from_source_code(tools_path):
    run('sudo yum install -y openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel')
    run(f'mkdir -p {tools_path} && cd {tools_path} && wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz')
    sudo(f'cd {tools_path} && tar -xzvf Python-3.6.5.tgz && cd Python-3.6.5 && ./configure --prefix=/usr/local/python3')
    sudo(f'cd {tools_path} && cd Python-3.6.5 && make && make install')
    sudo('ln -f -s /usr/local/python3/bin/python3.6 /usr/bin/python3 && ln -f -s /usr/local/python3/bin/python3.6 /usr/bin/python3.6 &&ln -f -s /usr/local/python3/bin/pip3 /usr/bin/pip3')
    
def _command_exist_or_not(command):
    with settings(warn_only=True):
        result=run(command)
        if result.failed or 'command not found' in result:
            return False
        else:
            return True
def _config_nginx_and_systemd(source_floder,hostname):
    _exist_nginx=_command_exist_or_not('nginx -V')
    if not _exist_nginx:
        sudo('yum install nginx -y')#安装完nginx后需要手动配置一下nginx.conf文件，加入/etc/nginx/sites-enabled/*配置路径，后续优化这一步的手动操作
    for subfolder in ('sites-available','sites-enabled'):
        _create_directory_if_necessary_by_root(f'/etc/nginx/{subfolder}')
    sudo(f'cp {source_floder}/deploy_tools/nginx.template.conf /etc/nginx/sites-available/{hostname}')
    run(f'sudo sed -i "s#SITENAME#{hostname}#g" /etc/nginx/sites-available/{hostname}')
    sudo(f'ln -f -s /etc/nginx/sites-available/{hostname} /etc/nginx/sites-enabled/{hostname}')
    sudo(f'cp {source_floder}/deploy_tools/gunicorn-systemd.template.service /etc/systemd/system/{hostname}.service')
    run(f'sudo sed -i "s#SITENAME#{hostname}#g" /etc/systemd/system/{hostname}.service')
    
def _start_project(tmp_path,hostname):
    #创建存放gunicorn启动时socket文件的临时目录
    _create_directory_if_necessary_by_root(tmp_path)
    #设置nginx和 hostname对应的服务开机自动重启
    sudo('systemctl enable nginx')
    sudo(f'systemctl enable {hostname}')
    
    #重新启动nginx和 hostname对应的服务
    sudo('systemctl restart nginx')
    sudo(f'systemctl restart {hostname}.service')
    
    