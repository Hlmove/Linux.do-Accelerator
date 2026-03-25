#!/usr/bin/env python3
import os
import pathlib
import re
import sys


def replace_once(path: pathlib.Path, pattern: str, replacement: str) -> None:
    content = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, content, count=1, flags=re.MULTILINE | re.DOTALL)
    if count != 1:
        raise SystemExit(f"failed to update {path}")
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    raw_tag = (
        os.environ.get("LINUXDO_RELEASE_TAG")
        or os.environ.get("RELEASE_TAG")
        or os.environ.get("GITHUB_REF_NAME")
        or ""
    ).strip()
    if not raw_tag:
        raise SystemExit("missing release tag; set RELEASE_TAG or run this workflow from a tag ref")
    if not raw_tag.startswith("v"):
        raise SystemExit(f"release tag must start with 'v': {raw_tag}")

    package_version = raw_tag[1:]
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?", package_version)
    if not match:
        raise SystemExit(f"unsupported release tag format: {raw_tag}")

    major, minor, patch = (int(part) for part in match.groups())
    android_version_code = (major * 1_000_000) + (minor * 1_000) + patch

    repo_root = pathlib.Path(
        os.environ.get("REPO_ROOT", pathlib.Path(__file__).resolve().parents[1])
    )

    replace_once(
        repo_root / "Cargo.toml",
        r'(^\[package\]\n.*?^version = ")[^"]+(")',
        rf'\g<1>{package_version}\2',
    )
    replace_once(
        repo_root / "Cargo.lock",
        r'(^\[\[package\]\]\nname = "linuxdo-accelerator"\nversion = ")[^"]+(")',
        rf'\g<1>{package_version}\2',
    )
    replace_once(
        repo_root / "android/app/build.gradle.kts",
        r'^(\s*versionCode\s*=\s*)\d+$',
        rf"\g<1>{android_version_code}",
    )
    replace_once(
        repo_root / "android/app/build.gradle.kts",
        r'^(\s*versionName\s*=\s*")[^"]+(")$',
        rf'\g<1>{package_version}\2',
    )

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as handle:
            handle.write(f"release_tag={raw_tag}\n")
            handle.write(f"package_version={package_version}\n")
            handle.write(f"android_version_code={android_version_code}\n")

    print(f"release tag: {raw_tag}")
    print(f"package version: {package_version}")
    print(f"android versionCode: {android_version_code}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
