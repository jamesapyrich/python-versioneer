#!/usr/bin/python

try:
    import argparse
except ImportError:
    # pre Python 2.7 compatibility
    import optparse

def unquote(s):
    return s.replace("%", "%%")
def ver(s):
    return s.replace("@VERSIONEER@", "0.7+")

def create_script(vcs):
    if vcs not in ("git", "hg",):
        raise ValueError("Unhandled revision-control system '%s'" % vcs)
    f = open("versioneer.py", "w")
    def get(fn):
        with open(fn, "r") as f_:
            return f_.read()
    f.write(ver(get("src/header.py")))
    f.write('VCS = "%s"\n' % vcs)
    f.write("IN_LONG_VERSION_PY = False\n")
    f.write("\n\n")
    for line in open("src/%s/long-version.py" % vcs, "r").readlines():
        if line.startswith("#### START"):
            f.write("LONG_VERSION_PY = '''\n")
            f.write("IN_LONG_VERSION_PY = True\n")
        elif line.startswith("#### SUBPROCESS_HELPER"):
            f.write(unquote(get("src/subprocess_helper.py")))
        elif line.startswith("#### MIDDLE"):
            f.write(unquote(get("src/%s/middle.py" % vcs)))
        elif line.startswith("#### PARENTDIR"):
            f.write(unquote(get("src/parentdir.py")))
        elif line.startswith("#### END"):
            f.write("'''\n")
        else:
            f.write(ver(line))
    f.write(get("src/subprocess_helper.py"))
    f.write(get("src/%s/middle.py" % vcs))
    f.write(get("src/parentdir.py"))
    f.write(get("src/%s/install.py" % vcs))
    f.write(ver(get("src/trailer.py")))
    f.close()

if __name__ == '__main__':
    vcs_desc = "Make versioneer.py for your project"
    vcs_args = ['-V', '--vcs']
    vcs_kwargs = {
            'dest': 'vcs',
            'default': 'git',
            'help': "The VCS to use. Options: git (default), hg",
    }
    try:
        argparse
        parser = argparse.ArgumentParser(description=vcs_desc)
        parser.add_argument(*vcs_args, **vcs_kwargs)
        options = parser.parse_args()
    except NameError:
        parser = optparse.OptionParser(description=vcs_desc, usage="make-versioneer.py [-h] [-V VCS]")
        parser.add_option(*vcs_args, **vcs_kwargs)
        (options, args) = parser.parse_args()

    vcs = options.vcs
    create_script(vcs)
