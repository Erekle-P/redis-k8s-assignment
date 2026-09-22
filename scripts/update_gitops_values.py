from pathlib import Path
import sys


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: update_gitops_values.py <values-file> <repository> <tag>"
        )

    path = Path(sys.argv[1])
    repository = sys.argv[2]
    tag = sys.argv[3]

    lines = path.read_text().splitlines()
    result = []

    inside_image = False
    repository_written = False
    tag_written = False

    for line in lines:
        if line == "image:":
            inside_image = True
            result.append(line)
            continue

        if inside_image and line and not line.startswith("  "):
            if not repository_written:
                result.append(f"  repository: {repository}")
                repository_written = True
            if not tag_written:
                result.append(f"  tag: {tag}")
                tag_written = True
            inside_image = False

        if inside_image and line.startswith("  repository:"):
            result.append(f"  repository: {repository}")
            repository_written = True
        elif inside_image and line.startswith("  tag:"):
            result.append(f"  tag: {tag}")
            tag_written = True
        else:
            result.append(line)

    if inside_image:
        if not repository_written:
            result.append(f"  repository: {repository}")
        if not tag_written:
            result.append(f"  tag: {tag}")

    path.write_text("\n".join(result) + "\n")


if __name__ == "__main__":
    main()
