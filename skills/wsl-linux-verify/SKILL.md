---
name: wsl-linux-verify
description: Verify Linux-targeted code from this Windows box using WSL Ubuntu. Use when a project targets Linux (Omarchy plugins, shell scripts, systemd services, POSIX file-permission / symlink / file-descriptor / O_NOFOLLOW logic) but the dev machine is Windows; when tests fail spuriously on Windows for POSIX reasons (st_mode bits, WinError 10054 socket resets, missing O_NOFOLLOW/getuid); or when you need real Linux evidence before claiming a fix works. Covers the drvfs caveat (copy out of /mnt/c), stripping CRLF, running suites in WSL, and baselining pre-existing failures with a git worktree so you don't mistake them for regressions.
---

# wsl-linux-verify

This box is Windows 11; a lot of the work (Omarchy plugins, shell helpers,
anything touching POSIX permissions/symlinks/fds) **targets Linux**. A fix is
not "verified" until it passes on Linux — Windows-green is necessary but not
sufficient. WSL Ubuntu is installed and is the fast local way to get that
evidence (no SSH to a Linux host needed for a quick check).

## Calling WSL from the pi bash tool

The pi `bash` tool is **git-bash (POSIX)**, not PowerShell. Invoke WSL through
`wsl.exe` and strip the UTF-16 nulls it emits:

```bash
wsl.exe -e bash -lc 'cd ~/proj && python3 --version && uname -a' 2>&1 | tr -d '\0'
```

Available in WSL: `python3` (3.14), `node`. **Not** installed: `omarchy` CLI,
`qmllint` (so `tests/run` can't fully run there — invoke the Python/Node
suites directly; the marketplace bot runs `omarchy plugin validate` on the
pushed commit anyway).

## The drvfs caveat (the whole point)

The repo lives on `/mnt/c/...` (Windows filesystem mounted as drvfs). **drvfs
does not honor POSIX semantics**: `chmod` is largely ignored (files report
`0777`/`0666`), `O_NOFOLLOW`/symlink behavior is unreliable, and ownership is
faked. Any test that asserts on permission bits, symlinks, or no-follow
descriptor opens will misbehave there.

So **copy the tree into the WSL native filesystem first** and run there:

```bash
wsl.exe -e bash -lc '
  set -e
  rm -rf ~/verify && mkdir -p ~/verify
  cp -r /mnt/c/Users/darry/path/to/repo/. ~/verify/
  cd ~/verify
  sed -i "s/\r$//" bin/* tests/*.py tests/run 2>/dev/null || true   # strip CRLF
  for t in tests/*_test.py; do python3 "$t" >/tmp/$(basename "$t").log 2>&1 \
    && echo "PASS $t" || { echo "FAIL $t"; tail -n 8 /tmp/$(basename "$t").log; }; done
' 2>&1 | tr -d '\0'
```

The `sed -i 's/\r$//'` matters: a Windows checkout (core.autocrlf=true) can
leave CRLF in the working copy, and a **CRLF shebang breaks a Linux
executable**. Git stores LF, so a fresh clone is fine — but the copied
working tree may not be. Strip it before running.

## Windows-spurious failures — recognize, don't chase

When a suite fails on the **Windows** side but the code is Linux-targeted,
these are environment artifacts, not bugs (confirmed by baselining, below):

- `st_mode & 0o077 == 0` / "file is not readable by others" → Windows reports
  `0o100666`; POSIX permission bits don't exist there.
- oversized-read tests → `WinError 10054` ("existing connection forcibly
  closed"): Windows RSTs when a server writes a large body and the client
  closes early; timing-dependent and flaky.
- `O_NOFOLLOW`, `O_DIRECTORY`, `os.getuid` absent → guard with
  `getattr(os, "O_NOFOLLOW", 0)` / `hasattr(os, "getuid")` and **skip** the
  POSIX-only assertion on Windows rather than failing it.
- `open(path)` without `encoding=` → `UnicodeDecodeError` under cp1252. Run
  with `PYTHONUTF8=1` on the Windows side, or just run in WSL (UTF-8 default).

Write platform-aware tests: `POSIX = hasattr(os, "getuid")`, then
`if POSIX: check(...) else: skip(...)`. That keeps the suite green on Windows
while still proving the security-critical paths on Linux.

## Baseline before claiming a regression

If a test fails after your change, prove whether it's pre-existing:

```bash
git worktree add /tmp/base origin/main      # clean checkout of the base
# run the SAME test in /tmp/base (in WSL if it's Linux-targeted)
git worktree remove /tmp/base --force
```

Identical failure on the base = pre-existing artifact, not your regression.
This is the evidence discipline that stops you "fixing" a Windows quirk or
mis-attributing it to your diff.

## When to escalate beyond WSL

WSL covers pure userspace Linux (Python/Node/shell, POSIX file semantics on
native fs). It does **not** cover: real systemd services, GPU/kernel modules,
the actual Omarchy/Hyprland shell, or D-Bus/MPRIS against a running desktop.
For those, test on a real Linux host.
