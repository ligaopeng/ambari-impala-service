ambari集成impala组件
===
## 实现目标
当前最新ambari版本2.6.5.0及HDP3.1.5.0已不再发布维护和更新，由cloudera公司发布的CDP替代，CDP属于收费项目，因此推出基于ambari服务管理平台的impala服务组件。
## 关联项目
* [CDH KUDU on ambari](https://github.com/luckes-yang/ambari-kudu-service)
## 安装前准备
#### 1.配置cdh6镜像源：

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
*无网络环境或网络环境差的情况下，可以将cdh5镜像源制作成本地镜像源进行安装*
## 安装步骤
#### 1.查看当前HDP版本
```shell
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
echo $VERSION
```
#### 2.下载并解压release版本插件包
```shell
git clone https://github.com/luckes-yang/ambari-impala-service.git /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/IMPALA
```
#### 3.重启ambari-server
```shell
ambari-server restart
```
#### 4.修改配置
```shell
mkdir /var/run/hdfs-sockets/
chmod -R 775 /var/run/hdfs-sockets/
```
* hdfs-site.xml
```xml
<property>
    <name>dfs.block.local-path-access.user</name>
    <value>impala</value>
</property>
<property>
    <name>dfs.client.read.shortcircuit</name>
    <value>true</value>
</property>
<property>
    <name>dfs.domain.socket.path</name>
    <value>/var/run/hdfs-sockets/dn_PORT</value>
</property>
<property>
    <name>dfs.client.file-block-storage-locations.timeout.millis</name>
    <value>10000</value>
</property>
<property>
    <name>dfs.datanode.hdfs-blocks-metadata.enabled</name>
    <value>true</value>
</property>
```

* core-site.xml
```xml
<property>
    <name>dfs.client.read.shortcircuit</name>
    <value>true</value>
</property>
<property>
    <name>dfs.client.read.shortcircuit.skip.checksum</name>
    <value>false</value>
</property>
<property>
    <name>dfs.datanode.hdfs-blocks-metadata.enabled</name>
    <value>true</value>
</property>
```

* hive-site.xml
```xml
<property>
    <name>datanucleus.schema.autoCreateAll</name>
    <value>true</value>
</property>
```



chmod -R 775 /var/run/hdfs-sockets/

