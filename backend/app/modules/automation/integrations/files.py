from pathlib import Path


def resolve_workspace_file(path: str, workspace_root: Path) -> Path:
    root = workspace_root.resolve()
    candidate = (root / path).resolve()
    if not candidate.is_relative_to(root):
        raise ValueError("File actions must stay within the configured tenant workspace.")
    return candidate
