import subprocess

def grep(dir, keyword):
    process = subprocess.Popen(['grep -rni {} {}'.format(keyword, dir)], shell=True, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr is not None:
        print(stderr)
        return None
    else:
        res = stdout.decode('utf-8').strip().split('\n')
        return [r.split(':') for r in res]
