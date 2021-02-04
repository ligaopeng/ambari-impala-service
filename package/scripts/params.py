#!/usr/bin/env python
import socket
import os

from resource_management import *
from resource_management.libraries.script.script import Script

script_dir = os.path.dirname(os.path.realpath(__file__))

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()
stack_name = default("/hostLevelParams/stack_name", None)
stack_version_buildnum = default("/commandParams/version", None)

impala_env = config['configurations']['impala-env']
impala_log_dir = impala_env['impala_log_dir']
impala_scratch_dir = impala_env['impala_scratch_dir']
impala_log_file = os.path.join(impala_log_dir, 'impala-setup.log')
impala_catalog_host = config['clusterHostInfo']['impala_catalog_service_hosts'][0]
impala_state_store_host = config['clusterHostInfo']['impala_state_store_hosts'][0]
enable_ranger = impala_env['enable_ranger']

current_host_name = socket.getfqdn()
security_enabled = config['configurations']['cluster-env']['security_enabled']

hdfs_host = default("/clusterHostInfo/namenode_hosts", [''])[0]
if not hdfs_host:
    hdfs_host = default("/clusterHostInfo/namenode_host", [''])[0]
hive_host = default("/clusterHostInfo/hive_metastore_host", [''])[0]
kudu_master_hosts = ",".join(config['clusterHostInfo']['kudu_master_hosts'])
kudu_master_host_num = len(config['clusterHostInfo']['kudu_master_hosts'])

scp_conf_dir = "/etc/impala/conf"
scp_conf_from = {
    "hive": {
        "host": hive_host,
        "files": ["/etc/hive/conf/hive-site.xml"]},
    "hdfs": {
        "host": hdfs_host,
        "files": [
            "/etc/hadoop/conf/core-site.xml",
            "/etc/hadoop/conf/hdfs-site.xml"]}
}
