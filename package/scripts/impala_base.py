from resource_management import *
import os


class ImpalaBase(Script):
    impala_packages = [
        'impala-server',
        'impala-catalog',
        'impala-state-store',
        'impala-shell']

    def install_impala(self, env):
        self.install_packages(env)
        if self.impala_packages is not None and len(self.impala_packages):
            for pack in self.impala_packages:
                Package(pack)
        import params
        env.set_params(params)

        script_dir = params.files_dir
        datalake_jar = None
        for dir in os.listdir(script_dir):
            if dir.startswith('hadoop-azure-datalake') and dir.endswith(".jar"):
                datalake_jar = dir
        if datalake_jar is None:
            raise Exception("Couldn't find hadoop-azure-datalake-*.jar in " + script_dir)
        File(
            "/usr/lib/impala/lib/"+datalake_jar,
            content=StaticFile(os.path.join(script_dir, datalake_jar)), mode=0o644)
        File(format("{tmp_dir}/impala_init_lib.sh"),
             content=Template('init_lib.sh.j2', datalakeJar=datalake_jar), mode=0o700)
        Execute(format("bash {tmp_dir}/impala_init_lib.sh"))

    def configure_impala(self, env):
        import params
        env.set_params(params)
        realm_name = os.popen(
            'grep "default_realm" /etc/krb5.conf ').read().strip(os.linesep).split(' ')[-1]
        File("/etc/default/impala",
             content=Template("impala.j2", realm_name=realm_name),
             mode=0o644
             )
        Directory(format('{impala_scratch_dir}'), mode=0o777)
        self.configure_hdfs()

    @staticmethod
    def configure_hdfs():
        import params
        for service_name in params.scp_conf_from.keys():
            if params.scp_conf_from[service_name]["host"]:
                for fndir in params.scp_conf_from[service_name]["files"]:
                    Execute(format("ln -s %s /etc/impala/conf/" % fndir), ignore_failures=True)
