import subprocess
import argparse
import os

copy_cmd = (
    "rsync -rav --progress -e "
    "'ssh -T -c chacha20-poly1305@openssh.com -o Compression=no -x' "
    "{exclude} {remote_host}:{src} {dst}"
)


REMOTE_HOST = os.environ["DEFAULT_REMOTE_HOST"]


def main(src, dst, exclude):
    # Undo tilde conversion
    src = src.replace(os.environ["HOME"], "~")
    dst = dst.replace(os.environ["HOME"], "~")
    if exclude != "":
        exclude = "--exclude=" + exclude.replace(",", " --exclude=")
    cmd = copy_cmd.format(exclude=exclude, remote_host=REMOTE_HOST, src=src, dst=dst)
    print(f"Executing:\n{cmd}")
    subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("dst", nargs="?", default=os.getcwd())
    parser.add_argument("-x", "--exclude", default="")
    args = parser.parse_args()
    main(args.src, args.dst, args.exclude)
