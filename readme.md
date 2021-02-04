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
*无网络环境或网络环境差的情况下，可以将cdh6镜像源制作成本地镜像源进行安装*

使用httpd

```shell
vim /etc/yum.repos.d/cdh6.repo

#VERSION_NUMBER=2.7.4.0-118
[cdh6-3.2.0]
name=cdh6 Version - cdh6-3.2.0
baseurl=http://jq1:8099/cdh6/yum/
gpgcheck=1
gpgkey=http://jq1:8099/cdh6/yum/RPM-GPG-KEY-cloudera
enabled=1
priority=1
autorefresh=0
```
本地源所需rpm文件,下载地址为https://archive.cloudera.com/cdh6/6.3.2/redhat7/yum/

```shell
└── yum
    ├── repodata
    │   ├── 3224703272392229e02b46c2ef95286e92cce148a07c04752bcfe98870bfd675-primary.sqlite.bz2
    │   ├── 4526a7a317692d4c0de084f217193070a78b6b6e0013044b66dca3f5911a7053-filelists.xml.gz
    │   ├── 4f1d5a908a6b4fd79988109121695168a65ef0846f178bbf32dc99f92c7cef36-filelists.sqlite.bz2
    │   ├── 60fad47e7a1f5dc0769fa02df8a8bbb3703afbfd8748ada66a4eb27ff77572f8-other.sqlite.bz2
    │   ├── 9554b60409a425c25954a95755e77747be8299d113940fbf0712a31579f79146-other.xml.gz
    │   ├── cb6c5f61bfc4d0dca26d9ed6758b93802404ce4e0e5daaeaa98346bb6864b312-primary.xml.gz
    │   ├── repomd.xml
    │   ├── repomd.xml.asc
    │   ├── repomd.xml.key
    │   └── RPMS
    │       └── x86_64
    ├── RPM-GPG-KEY-cloudera
    └── RPMS
        ├── noarch
        │   ├── avro-doc-1.8.2+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── avro-libs-1.8.2+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── avro-tools-1.8.2+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── bigtop-utils-0.7.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── hbase-solr-1.5+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── hbase-solr-doc-1.5+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── hbase-solr-indexer-1.5+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── parquet-1.9.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── parquet-format-2.4.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── sentry-2.1.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── sentry-hdfs-plugin-2.1.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── sentry-store-2.1.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── solr-7.4.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── solr-crunch-1.0.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── solr-doc-7.4.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── solr-mapreduce-1.0.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   ├── solr-server-7.4.0+cdh6.3.2-1605554.el7.noarch.rpm
        │   └── wget-log
        └── x86_64
            ├── hbase-2.1.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── impala-3.2.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── impala-catalog-3.2.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── impala-debuginfo-3.2.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── impala-server-3.2.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── impala-shell-3.2.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── impala-state-store-3.2.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── impala-udf-devel-3.2.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── kudu-1.10.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── kudu-client0-1.10.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── kudu-client-devel-1.10.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── kudu-debuginfo-1.10.0+cdh6.3.2-1605554.el7.x86_64.rpm
            ├── kudu-master-1.10.0+cdh6.3.2-1605554.el7.x86_64.rpm
            └── kudu-tserver-1.10.0+cdh6.3.2-1605554.el7.x86_64.rpm

```

## 安装步骤

#### 1.查看当前HDP版本（ambari-server节点）
```shell
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
echo $VERSION
```
#### 2.下载并解压release版本插件包（ambari-server节点）
```shell
git clone git@github.com:ligaopeng/ambari-impala-service.git /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/IMPALA
```
#### 3.重启ambari-server
```shell
ambari-server restart
```
#### 4.修改配置'

在所有节点上执行

```shell
mkdir /var/run/hdfs-sockets/
chmod -R 775 /var/run/hdfs-sockets/
```
在ambari管理界面上设置

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
    <name>dfs.client.read.shortcircuit.skip.checksum</name>
    <value>false</value>
</property>

```

* hive-site.xml
```xml
<property>
    <name>datanucleus.schema.autoCreateAll</name>
    <value>true</value>
</property>
```




