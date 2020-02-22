from subprocess import check_call
import stat
import os


def mk_call(cmd_path):
    if os.lstat(cmd_path).st_mode & stat.S_IEXEC:
        pass
    else:
        os.chmod(cmd_path, stat.S_IEXEC)

    def call(python_pack_name: str, entry: str, ffi_deps_path: str):
        cmd = [
            cmd_path,
            '--out-python',
            python_pack_name,
            '--corefn-entry',
            entry,
            '--out-ffi-dep',
            ffi_deps_path,
        ]
        check_call(cmd)

    return call
