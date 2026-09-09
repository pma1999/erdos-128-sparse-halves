"""Install the pinned portable Windows Lean runtime inside this workspace."""
from pathlib import Path
import hashlib
import shutil
import urllib.request
import zipfile

root=Path(__file__).resolve().parents[1]/'work/lean-runtime'
root.mkdir(parents=True,exist_ok=True)
name='lean-4.33.1-windows.zip'
url='https://github.com/leanprover/lean4/releases/download/v4.33.1/'+name
expected='c39360867edfff6b090f20c16e18581c969ce839b71e813d76022ec04ec73e4d'
archive=root/name
assert shutil.disk_usage(root).free>5*1024**3,'At least 5 GiB free required.'
if not archive.exists():
 temporary=root/(name+'.partial')
 with urllib.request.urlopen(url) as src,temporary.open('wb') as dst:
  shutil.copyfileobj(src,dst)
 with temporary.open('rb') as src:
  downloaded=hashlib.file_digest(src,'sha256').hexdigest()
 assert downloaded==expected,'Downloaded archive checksum mismatch.'
 temporary.replace(archive)
with archive.open('rb') as src:
 actual=hashlib.file_digest(src,'sha256').hexdigest()
assert actual==expected,'Archive checksum mismatch; nothing extracted.'
with zipfile.ZipFile(archive) as z:
 for entry in z.infolist():
  assert (root/entry.filename).resolve().is_relative_to(root.resolve())
 z.extractall(root)
print('Lean 4.33.1 installed locally; SHA-256 verified.')
