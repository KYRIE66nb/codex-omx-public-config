from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import urllib.parse
import zlib
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


DRAWIO_BASE_URL = "https://app.diagrams.net/"
DEFAULT_BORDER = 10
DEFAULT_VIEWPORT = "1600,1200"
DEFAULT_WAIT_MS = 5000
DEFAULT_TRIM_THRESHOLD = 250
DEFAULT_TRIM_PADDING = 18

SOURCE_FORMAT_ALIASES: dict[str, str] = {
    "dot": "graphviz",
    "drawio": "drawio_xml",
    "drawio_xml": "drawio_xml",
    "graphviz": "graphviz",
    "mermaid": "mermaid",
    "mxfile": "drawio_xml",
    "xml": "drawio_xml",
}

SOURCE_FORMAT_DEFAULTS: dict[str, tuple[str, str, str | None]] = {
    "mermaid": ("drawio", ".mmd", "mermaid"),
    "graphviz": ("graphviz", ".dot", None),
    "drawio_xml": ("drawio", ".drawio", "mxfile"),
}

DIAGRAM_TYPE_DEFAULTS: dict[str, str] = {
    "flowchart": "mermaid",
    "functional_structure": "mermaid",
    "logical_er": "mermaid",
    "conceptual_er": "graphviz",
    "use_case": "graphviz",
    "system_architecture": "graphviz",
}


@dataclass(frozen=True)
class DiagramSpec:
    id: str
    title: str
    type: str
    content: str
    engine: str
    source_format: str
    drawio_content_type: str | None
    label: str
    output_name: str
    source_suffix: str


def encode_uri_component(value: str) -> str:
    return urllib.parse.quote(value, safe="~()*!.'")


def compress_data(value: str) -> str:
    encoded = encode_uri_component(value)
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed = compressor.compress(encoded.encode("utf-8")) + compressor.flush()
    return base64.b64encode(compressed).decode("ascii")


def build_drawio_url(
    content: str,
    *,
    content_type: str = "mermaid",
    lightbox: bool = True,
    border: int = DEFAULT_BORDER,
    dark: bool = False,
    edit: str = "_blank",
) -> str:
    create_obj = {
        "type": content_type,
        "compressed": True,
        "data": compress_data(content),
    }

    params = urllib.parse.urlencode(
        {
            "lightbox": "1" if lightbox else "0",
            "edit": edit,
            "border": str(border),
            **({"dark": "1"} if dark else {}),
        }
    )
    create_hash = urllib.parse.quote(json.dumps(create_obj, ensure_ascii=False, separators=(",", ":")))
    return f"{DRAWIO_BASE_URL}?{params}#create={create_hash}"


def normalize_source_format(source_format: str) -> str:
    normalized = source_format.strip().lower()
    if normalized not in SOURCE_FORMAT_ALIASES:
        raise ValueError(f"Unsupported source format: {source_format}")
    return SOURCE_FORMAT_ALIASES[normalized]


def detect_drawio_source_format(content: str | None) -> str | None:
    if not content:
        return None
    stripped = content.lstrip()
    if stripped.startswith("<mxGraphModel") or stripped.startswith("<mxfile"):
        return "drawio_xml"
    return None


def infer_route(
    diagram_type: str,
    explicit_engine: str | None = None,
    explicit_source_format: str | None = None,
    content: str | None = None,
) -> tuple[str, str, str, str | None]:
    normalized_type = diagram_type.strip().lower()
    if normalized_type not in DIAGRAM_TYPE_DEFAULTS:
        raise ValueError(f"Unsupported diagram type: {diagram_type}")

    default_source_format = DIAGRAM_TYPE_DEFAULTS[normalized_type]

    if explicit_source_format:
        source_format = normalize_source_format(explicit_source_format)
        engine, suffix, drawio_content_type = SOURCE_FORMAT_DEFAULTS[source_format]
        if explicit_engine and explicit_engine.strip().lower() != engine:
            raise ValueError(
                f"Incompatible engine/source_format combination: {explicit_engine} vs {explicit_source_format}"
            )
        return engine, source_format, suffix, drawio_content_type

    if explicit_engine:
        explicit_engine = explicit_engine.strip().lower()
        if explicit_engine not in {"drawio", "graphviz"}:
            raise ValueError(f"Unsupported engine override: {explicit_engine}")
        default_engine = SOURCE_FORMAT_DEFAULTS[default_source_format][0]
        if explicit_engine == "drawio":
            source_format = detect_drawio_source_format(content) or (
                default_source_format if default_engine == "drawio" else "mermaid"
            )
        else:
            source_format = "graphviz"
        engine, suffix, drawio_content_type = SOURCE_FORMAT_DEFAULTS[source_format]
        return engine, source_format, suffix, drawio_content_type

    engine, suffix, drawio_content_type = SOURCE_FORMAT_DEFAULTS[default_source_format]
    return engine, default_source_format, suffix, drawio_content_type


def infer_engine(diagram_type: str, explicit_engine: str | None = None) -> tuple[str, str]:
    engine, _, suffix, _ = infer_route(diagram_type, explicit_engine=explicit_engine)
    return engine, suffix


def load_manifest(path: Path) -> list[DiagramSpec]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_diagrams = payload.get("diagrams")
    if not isinstance(raw_diagrams, list) or not raw_diagrams:
        raise ValueError("Manifest must contain a non-empty 'diagrams' list.")

    seen_ids: set[str] = set()
    diagrams: list[DiagramSpec] = []
    for item in raw_diagrams:
        diagram_id = str(item["id"]).strip()
        if not diagram_id:
            raise ValueError("Diagram id cannot be empty.")
        if diagram_id in seen_ids:
            raise ValueError(f"Duplicate diagram id: {diagram_id}")
        seen_ids.add(diagram_id)

        diagram_type = str(item["type"]).strip().lower()
        content = str(item["content"]).strip()
        if not content:
            raise ValueError(f"Diagram {diagram_id} content cannot be empty.")

        engine, source_format, suffix, drawio_content_type = infer_route(
            diagram_type,
            explicit_engine=item.get("engine"),
            explicit_source_format=item.get("source_format"),
            content=content,
        )
        diagrams.append(
            DiagramSpec(
                id=diagram_id,
                title=str(item.get("title", diagram_id)).strip() or diagram_id,
                type=diagram_type,
                content=content,
                engine=engine,
                source_format=source_format,
                drawio_content_type=drawio_content_type,
                label=str(item.get("label", diagram_id)).strip() or diagram_id,
                output_name=str(item.get("output", f"{diagram_id}.png")).strip() or f"{diagram_id}.png",
                source_suffix=suffix,
            )
        )
    return diagrams


def trim_white_margins(
    source_path: Path,
    output_path: Path,
    *,
    background_threshold: int = DEFAULT_TRIM_THRESHOLD,
    padding: int = DEFAULT_TRIM_PADDING,
) -> Path:
    image = Image.open(source_path).convert("RGB")
    grayscale = image.convert("L")
    mask = grayscale.point(lambda value: 255 if value < background_threshold else 0)
    bbox = mask.getbbox()

    if bbox is None:
        image.save(output_path)
        return output_path

    left = max(bbox[0] - padding, 0)
    top = max(bbox[1] - padding, 0)
    right = min(bbox[2] + padding, image.width)
    bottom = min(bbox[3] + padding, image.height)
    image.crop((left, top, right, bottom)).save(output_path)
    return output_path


def write_source_sidecars(diagrams: list[DiagramSpec], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    result: dict[str, Path] = {}
    for diagram in diagrams:
        path = output_dir / f"{diagram.id}{diagram.source_suffix}"
        path.write_text(diagram.content + "\n", encoding="utf-8")
        result[diagram.id] = path
    return result


def write_result_manifest(payload: dict[str, Path], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({key: str(value) for key, value in payload.items()}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def render_drawio_png(
    spec: DiagramSpec,
    output_path: Path,
    *,
    viewport_size: str = DEFAULT_VIEWPORT,
    wait_ms: int = DEFAULT_WAIT_MS,
    browser_channel: str = "chrome",
    trim_threshold: int = DEFAULT_TRIM_THRESHOLD,
    trim_padding: int = DEFAULT_TRIM_PADDING,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(".raw.png")
    url = build_drawio_url(spec.content, content_type=spec.drawio_content_type or "mermaid")

    command = [
        "npx",
        "playwright",
        "screenshot",
        f"--channel={browser_channel}",
        f"--viewport-size={viewport_size}",
        f"--wait-for-timeout={wait_ms}",
        url,
        str(temp_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Draw.io rendering failed for {spec.id}.\n"
            f"STDOUT:\n{result.stdout.strip()}\nSTDERR:\n{result.stderr.strip()}".strip()
        )

    trim_white_margins(
        temp_path,
        output_path,
        background_threshold=trim_threshold,
        padding=trim_padding,
    )
    temp_path.unlink(missing_ok=True)
    return output_path


def render_graphviz_png(spec: DiagramSpec, source_path: Path, output_path: Path) -> Path:
    if source_path.suffix != ".dot":
        raise ValueError(f"Graphviz rendering requires a .dot source. Got: {source_path.name}")

    render_script = Path(__file__).resolve().with_name("render_graphviz.py")
    command = [sys.executable, str(render_script), str(source_path), str(output_path)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Graphviz rendering failed for {spec.id}.\n"
            f"STDOUT:\n{result.stdout.strip()}\nSTDERR:\n{result.stderr.strip()}".strip()
        )
    return output_path


def render_assets(
    diagrams: list[DiagramSpec],
    source_paths: dict[str, Path],
    output_dir: Path,
    *,
    viewport_size: str = DEFAULT_VIEWPORT,
    wait_ms: int = DEFAULT_WAIT_MS,
    browser_channel: str = "chrome",
    trim_threshold: int = DEFAULT_TRIM_THRESHOLD,
    trim_padding: int = DEFAULT_TRIM_PADDING,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rendered: dict[str, Path] = {}

    for spec in diagrams:
        output_path = output_dir / spec.output_name
        if spec.engine == "drawio":
            render_drawio_png(
                spec,
                output_path,
                viewport_size=viewport_size,
                wait_ms=wait_ms,
                browser_channel=browser_channel,
                trim_threshold=trim_threshold,
                trim_padding=trim_padding,
            )
        elif spec.engine == "graphviz":
            render_graphviz_png(spec, source_paths[spec.id], output_path)
        else:
            raise ValueError(f"Unsupported engine: {spec.engine}")

        rendered[spec.label] = output_path

    return rendered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="Path to a diagram manifest JSON file.")
    parser.add_argument("output_dir", help="Directory for source sidecars and PNG assets.")
    parser.add_argument(
        "--result-manifest",
        default=None,
        help="Optional JSON output that maps diagram labels to generated PNG paths.",
    )
    parser.add_argument(
        "--sources-only",
        action="store_true",
        help="Write sidecar source files only and skip PNG rendering.",
    )
    parser.add_argument("--viewport-size", default=DEFAULT_VIEWPORT, help='Playwright viewport, e.g. "1600,1200".')
    parser.add_argument("--wait-ms", type=int, default=DEFAULT_WAIT_MS, help="Wait time before screenshot capture.")
    parser.add_argument("--browser-channel", default="chrome", help="Chromium channel for Playwright.")
    parser.add_argument("--trim-threshold", type=int, default=DEFAULT_TRIM_THRESHOLD, help="White trim threshold.")
    parser.add_argument("--trim-padding", type=int, default=DEFAULT_TRIM_PADDING, help="Trim padding in pixels.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    output_dir = Path(args.output_dir)
    result_manifest_path = Path(args.result_manifest) if args.result_manifest else output_dir / "result-manifest.json"

    diagrams = load_manifest(manifest_path)
    source_paths = write_source_sidecars(diagrams, output_dir)

    if args.sources_only:
        write_result_manifest({}, result_manifest_path)
        print(str(result_manifest_path))
        return 0

    rendered = render_assets(
        diagrams,
        source_paths,
        output_dir,
        viewport_size=args.viewport_size,
        wait_ms=args.wait_ms,
        browser_channel=args.browser_channel,
        trim_threshold=args.trim_threshold,
        trim_padding=args.trim_padding,
    )
    write_result_manifest(rendered, result_manifest_path)
    print(str(result_manifest_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
