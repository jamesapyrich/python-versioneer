
import sys

def do_vcs_install(versionfile_source, ipy):
    HG = "hg"
    if sys.platform == "win32":
        HG = "hg.py"
    run_command([HG, "add", "versioneer.py"])
    run_command([HG, "add", versionfile_source])
    run_command([HG, "add", ipy])
