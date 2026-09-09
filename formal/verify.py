"""Compile Scalar.lean, audit axioms, and replay its declarations in Lean's kernel.

This verifies a conditional scalar result, not the graph theorem or Erdos 128.
The replay uses Lean's own kernel; it is not an external proof assistant.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

root=Path(__file__).resolve().parents[1]
runtime=root/'work/lean-runtime/lean-4.33.1-windows'
lean=runtime/'bin/lean.exe';checker=runtime/'bin/leanchecker.exe'
source=root/'formal/Scalar.lean'
output=root/'outputs/lean-scalar-verification.json'
report={'status':'running','scope':'Conditional scalar bound only; graph construction not formalized.'}
output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
try:
 assert lean.is_file(),'Run python formal/setup.py first.'
 text=source.read_text(encoding='utf-8')
 assert not re.search(r'^\s*(axiom|constant)\b',text,re.M)
 assert not re.search(r'\b(sorry|admit|native_decide)\b',text)
 expected={'SparseHalf.'+n for n in re.findall(r'^theorem (\w+)',text,re.M)}
 build=root/'work/formal-check';build.mkdir(parents=True,exist_ok=True)
 version=subprocess.check_output([str(lean),'--version'],text=True,encoding='utf-8').strip()
 assert 'version 4.33.1,' in version
 run=subprocess.run([str(lean),'-o',str(build/'Scalar.olean'),'Scalar.lean'],
     cwd=root/'formal',text=True,encoding='utf-8',capture_output=True,timeout=60)
 log=run.stdout+run.stderr
 (root/'outputs/lean-scalar-compilation.txt').write_text(log,encoding='utf-8')
 assert run.returncode==0,log
 assert 'sorryAx' not in log and 'error:' not in log
 audit={name:set(x.strip() for x in axioms.split(',') if x.strip())
   for name,axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log)}
 assert set(audit)==expected,(set(audit),expected)
 allowed={'propext','Classical.choice','Quot.sound'}
 assert all(v<=allowed for v in audit.values()),audit
 print('Compiled and audited',len(audit),'theorems.',flush=True)
 env=os.environ.copy();env['LEAN_PATH']=str(build)
 replay=subprocess.run([str(checker),'-v','Scalar'],cwd=root/'formal',env=env,
     text=True,encoding='utf-8',capture_output=True,timeout=120)
 replay_log=replay.stdout+replay.stderr
 (root/'outputs/lean-scalar-replay.txt').write_text(replay_log,encoding='utf-8')
 assert replay.returncode==0,replay_log
 assert 'replaying Scalar' in replay_log,replay_log
 report.update(status='passed',lean_version=version,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
   checked_theorems=len(audit),axioms={k:sorted(v) for k,v in audit.items()},
   replay='passed, target module Scalar only; imported standard library trusted',
   no_added_axioms=True,no_sorry=True,
   limitations=['No formal graph construction or rounding theorem yet.','No formal proof of the external BCL max-cut theorem.','No theorem at 1/50 and no counterexample.'])
except Exception as err:
 report.update(status='failed',error=str(err))
 raise
finally:
 output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
