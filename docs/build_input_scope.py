"""Tracked working-file inputs for the two traceability generators.

Not a sandbox, snapshot lock, output-path guard or script-execution policy.
Licensed under AGPLv3; see LICENSE/LICENSE_INDEX.md.
"""
from __future__ import annotations

import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
from typing import Callable


class InputScopeError(RuntimeError):
    """Input discovery was unavailable or a selected input was unsafe to read."""


def configure_utf8_output() -> None:
    """CLI output contract; imported parser helpers do not change streams."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="strict")


def _plain_path(path: Path, *, directory: bool) -> None:
    info = path.lstat()  # Never resolve away a link before inspecting it.
    if stat.S_ISLNK(info.st_mode) or (
        getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    ):
        raise InputScopeError(f"linked/reparse input refused: {path}")
    expected = stat.S_ISDIR if directory else stat.S_ISREG
    if not expected(info.st_mode):
        raise InputScopeError(f"non-regular input refused: {path}")


def _long_path_spelling(path: Path) -> str:
    """Expand Windows 8.3 names for comparison, without resolving path aliases."""
    name = str(path)
    if os.name != "nt":
        return name

    import ctypes
    from ctypes import wintypes

    get_long_path = ctypes.WinDLL("kernel32", use_last_error=True).GetLongPathNameW
    get_long_path.argtypes = (wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD)
    get_long_path.restype = wintypes.DWORD
    required = get_long_path(name, None, 0)
    if not required:
        raise ctypes.WinError(ctypes.get_last_error())
    buffer = ctypes.create_unicode_buffer(required)
    length = get_long_path(name, buffer, len(buffer))
    if not length:
        raise ctypes.WinError(ctypes.get_last_error())
    if length >= len(buffer):
        raise OSError("Windows long-path spelling changed during comparison")
    return buffer.value


def tracked_inputs(
    repo_root: Path, include: Callable[[PurePosixPath], bool]
) -> list[Path]:
    """Select index membership, validate paths, then let callers read live bytes.

    Staged additions and unstaged edits are eligible; untracked/ignored scratch
    is not. Tracked files remain eligible if an ignore rule later matches them.
    Staged deletion removes membership; unstaged deletion fails. No Git-less
    fallback. The validation/read interval is not protected against a writer.
    """
    root = Path(os.path.abspath(repo_root))
    # Repository selection must not inherit a different index/worktree from the
    # caller. Git may still read host global/system and repository configuration;
    # disable fsmonitor so enumeration does not invoke a configured monitor command.
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"

    def git(*args: str) -> bytes:
        result = subprocess.run(
            ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", *args],
            cwd=root, env=env, capture_output=True, check=True,
        )
        return result.stdout

    try:
        # Inspect the supplied root and its ancestors, not only child files.
        for parent in reversed((root, *root.parents)):
            _plain_path(parent, directory=True)
        top = Path(os.fsdecode(git("rev-parse", "--show-toplevel").rstrip(b"\r\n")))
        if os.path.normcase(os.path.abspath(top)) != os.path.normcase(_long_path_spelling(root)):
            raise InputScopeError("requested root is not the Git worktree top level")
        records = git("ls-files", "--stage", "--full-name", "-z").split(b"\0")
        selected: list[Path] = []
        for record in records:
            if not record:
                continue
            metadata, raw_name = record.split(b"\t", 1)
            mode, _object_id, stage = metadata.split()
            name = raw_name.decode("utf-8", errors="strict")
            relative = PurePosixPath(name)
            if (relative.is_absolute() or relative.as_posix() != name
                    or any(part in ("", ".", "..") for part in name.split("/"))
                    or "\\" in name or ":" in name):
                raise InputScopeError("non-relative Git input path refused")
            if not include(relative):
                continue
            if stage != b"0" or mode not in (b"100644", b"100755"):
                raise InputScopeError(f"unmerged or non-file index input refused: {name}")
            path = root
            for index, part in enumerate(relative.parts):
                path /= part
                _plain_path(path, directory=index < len(relative.parts) - 1)
            selected.append(path)
        return sorted(selected)
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as exc:
        raise InputScopeError(f"tracked input discovery failed: {exc}") from exc
