# How to put this repository online

Everything below is prepared. The only step nobody but you can do is
authenticate to GitHub, so the push itself is yours to run.

## Pre-flight — three things that were checked

1. **The 842 MB Lean runtime never entered git history.** The original
   `.gitignore` already excluded `work/lean-runtime/`, `work/vendor/` and
   `work/formal-check/`, and the history is only five commits. Had that zip
   been committed, the push would have been rejected outright: GitHub hard-caps
   any single file at 100 MB. The `.gitignore` in this directory supersedes the
   old one and adds LaTeX auxiliaries and the third-party directory.

2. **Third-party code.** `work/sarid-certificate/` holds two files written by
   someone else and is currently tracked. Its upstream licence could not be
   read from here, and code with no licence is "all rights reserved" by
   default. Stop tracking it and fetch it instead — `work-sarid-fetch.sh` does
   that and prints the SHA-256 you should record:

       git rm -r --cached work/sarid-certificate
       git add .gitignore work-sarid-fetch.sh
       git commit -m "Fetch third-party certificate instead of vendoring it"

   The files stay on your disk; they simply stop being redistributed by you.
   They remain in the five old commits. If you want them gone from history too,
   squash before the first push:
   `git checkout --orphan clean && git add -A && git commit && git branch -M main`.
   That discards the agent's commit history, which is itself worth keeping as a
   record — your call.

3. **Authorship.** `outputs/cut-independent.tex` now carries your name and an
   "Acknowledgement of method" section disclosing that AI agents did the
   algebra, certificates, Lean development and literature audit, with you
   responsible for the content. That mirrors what Sarid's claim does and is the
   norm in this venue. To go back to anonymity, restore the author line to
   `Research draft; independent review pending` and delete that section.

## The push

```
cd C:\Users\PcVIP\Documents\Codex\2026-09-08\g

git add -A
git commit -m "Correct attribution, add literature audit, second verifier, 1/25 certificate"

gh repo create erdos-128-sparse-halves --public --source=. --remote=origin --push
```

If you don't use `gh`, create an empty public repo on github.com with that name
and no README, then:

```
git remote add origin https://github.com/<your-user>/erdos-128-sparse-halves.git
git branch -M main
git push -u origin main
```

## After the push, in this order

1. **Say nothing publicly.** No X, no Reddit, no "I improved an Erdős bound".
   The repo is a timestamp, not an announcement. Its own README already states
   that the problem is unsolved and that no priority is claimed.

2. **Send one email.** Bjarne Lidický (Iowa State) is the best first reader: he
   is a co-author of the theorem you depend on, and parts (b) and (c) of that
   same theorem are your route to 0.0248. Thomas Bloom is the alternative — he
   runs erdosproblems.com and has asked publicly for more human scrutiny of AI
   claims. Attach the PDF, link the repo, three short paragraphs, no overselling.

3. **Then do `NEXT.md`** — close the density window — before any arXiv posting
   or proof claim. Publishing 0.02587 now and 0.02481 a fortnight later is
   worse than publishing 0.02481 once.

## Do not

- Do not describe this as solving Erdős 128. It is a partial bound.
- Do not claim the extension of Razborov's Section 4.5 as the contribution;
  `LITERATURE.md` records exactly why that would be wrong.
- Do not submit a proof claim before the bound has been rechecked against the
  literature on the day of submission. The record was 131/5000 in August 2026;
  verify nothing has appeared since.
