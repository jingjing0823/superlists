配置新网站
=================

##需要的包

*nginx
*Python 3.6
*virtualenv + pip
*Git

以centos为例:

yum install python3 nginx pip git -y

##nginx 虚拟主机
参考nginx.template.conf
把SITENAME替换成所需的域名，例如tb-bm-staging.club

##systemd服务
参考unicorn-upstart.template.conf
把SITENAME替换成所需的域名，例如tb-bm-staging.club

文件夹结构

#文件夹结构

/home/username
|__sites
		|——database
		|——source
		|——static
		|——virtualenv