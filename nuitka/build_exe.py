import platform
import subprocess
import sys
import tomllib
from pathlib import Path
import zipfile

project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]
name    = project["name"]
version = project["version"]

arch = platform.machine().lower()
if arch == "amd64": arch = "x86_64"

os = {"win32": "windows", "darwin": "macos"}.get(sys.platform, "linux")

output_file = f"{name}-{version}"

if os == "windows":
    output_file += f"_win_{arch}.exe"

else:
    output_file += f"_{os}.{arch}"

cmd = [
    sys.executable, "-m", "nuitka",
    "--onefile",
    "--output-dir=build",
    f"--output-filename={output_file}",
    f"--product-version={version}",
    f"--onefile-tempdir-spec={{CACHE_DIR}}/{name}/{{VERSION}}",
    "--assume-yes-for-downloads",
    "--deployment",
    "nuitka/hello.py",
]

if os == "windows":
    cmd.append("--windows-console-mode=disable")

subprocess.run(cmd, check=True)

output_path = Path("build") / output_file
zip_path    = output_path.with_name(output_file + ".zip")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(output_path, arcname=output_path.name)