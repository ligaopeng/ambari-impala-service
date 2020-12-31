ambari集成impala组件
===
## 实现目标
当前最新ambari版本2.6.5.0及HDP3.1.5.0已不再发布维护和更新，由cloudera公司发布的CDP替代，CDP属于收费项目，因此推出基于ambari服务管理平台的impala服务组件。
## 关联项目
* [CDH KUDU on ambari](https://github.com/luckes-yang/ambari-kudu-service)
## 安装前准备
#### 1.配置cdh5或cdh6镜像源：
CDH5镜像源：
```shell
# cdh5适配impala版本为cdh-impala2.12.0
wget -P /etc/yum.repos.d/ https://archive.cloudera.com/cdh5/redhat/7/x86_64/cdh/cloudera-cdh5.repo
```
CDH6镜像源：
```shell
# cdh6适配kudu版本为cdh-impala3.2.0
echo "[cloudera-cdh6.3.2]
# Packages for Cloudera's Distribution for Hadoop, Version 6.3.2, on RedHat or CentOS 7 x86_64
name=Cloudera's Distribution for Hadoop, Version 5
baseurl=https://archive.cloudera.com/cdh6/6.3.2/redhat7/yum/
gpgkey =https://archive.cloudera.com/cdh6/6.3.2/redhat7/yum/RPM-GPG-KEY-cloudera    
gpgcheck = 1" > /etc/yum.repos.d/cloudera-cdh6.3.2.repo
```
#### 2.配置cdh5镜像源：

*无网络环境或网络环境差的情况下，可以将cdh5镜像源制作成本地镜像源进行安装*