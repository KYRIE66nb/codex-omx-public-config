from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument(
        "--engine",
        default="dot",
        choices=["dot", "neato", "fdp", "sfdp", "twopi", "circo"],
        help="Graphviz layout engine",
    )
    parser.add_argument(
        "--format",
        default=None,
        choices=["png", "svg", "pdf"],
        help="Output format; defaults to output file suffix",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_format = args.format or output_path.suffix.lstrip(".").lower()

    if output_format not in {"png", "svg", "pdf"}:
        print("ERROR\tUnsupported output format. Use png/svg/pdf or set --format.")
        return 2

    dot_path = shutil.which("dot")
    if dot_path is None:
        print("ERROR\tMissing Graphviz 'dot'. Install Graphviz first.")
        return 2

    cmd = [
        dot_path,
        f"-K{args.engine}",
        f"-T{output_format}",
        str(input_path),
        "-o",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR\tGraphviz rendering failed")
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
        return result.returncode

    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
