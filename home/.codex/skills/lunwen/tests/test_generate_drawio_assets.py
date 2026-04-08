from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "generate_drawio_assets.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "drawio-assets" / "manifest.json"


def load_module():
    spec = importlib.util.spec_from_file_location("generate_drawio_assets", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class GenerateDrawioAssetsTests(unittest.TestCase):
    def test_load_manifest_routes_supported_diagrams(self) -> None:
        module = load_module()
        diagrams = module.load_manifest(FIXTURE_PATH)

        self.assertEqual(
            [item.id for item in diagrams],
            ["flow-01", "logical-er-01", "conceptual-er-01", "use-case-01", "system-architecture-01"],
        )
        self.assertEqual([item.engine for item in diagrams], ["drawio", "drawio", "graphviz", "graphviz", "graphviz"])
        self.assertEqual(
            [item.source_format for item in diagrams],
            ["mermaid", "mermaid", "graphviz", "graphviz", "graphviz"],
        )
        self.assertEqual(diagrams[0].source_suffix, ".mmd")
        self.assertEqual(diagrams[2].source_suffix, ".dot")
        self.assertEqual(diagrams[3].source_suffix, ".dot")
        self.assertEqual(diagrams[4].source_suffix, ".dot")

    def test_build_drawio_url_uses_lightbox_hash_payload(self) -> None:
        module = load_module()
        url = module.build_drawio_url("flowchart TD\nA-->B")

        self.assertIn("https://app.diagrams.net/?", url)
        self.assertIn("lightbox=1", url)
        self.assertIn("#create=", url)

    def test_trim_white_margins_crops_image(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source.png"
            output = Path(tmpdir) / "trimmed.png"

            image = Image.new("RGB", (200, 200), "white")
            for x in range(70, 131):
                for y in range(80, 121):
                    image.putpixel((x, y), (0, 0, 0))
            image.save(source)

            module.trim_white_margins(source, output, background_threshold=250, padding=8)

            with Image.open(output) as trimmed:
                self.assertLess(trimmed.size[0], 200)
                self.assertLess(trimmed.size[1], 200)
                self.assertGreater(trimmed.size[0], 50)
                self.assertGreater(trimmed.size[1], 30)

    def test_write_sources_creates_expected_sidecars(self) -> None:
        module = load_module()
        diagrams = module.load_manifest(FIXTURE_PATH)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            paths = module.write_source_sidecars(diagrams, output_dir)

            self.assertTrue((output_dir / "flow-01.mmd").exists())
            self.assertTrue((output_dir / "logical-er-01.mmd").exists())
            self.assertTrue((output_dir / "conceptual-er-01.dot").exists())
            self.assertTrue((output_dir / "use-case-01.dot").exists())
            self.assertTrue((output_dir / "system-architecture-01.dot").exists())
            self.assertEqual(paths["flow-01"].suffix, ".mmd")

    def test_result_manifest_preserves_generated_png_paths(self) -> None:
        module = load_module()
        payload = {
            "flow-01": Path("/tmp/flow-01.png"),
            "logical-er-01": Path("/tmp/logical-er-01.png"),
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "result.json"
            module.write_result_manifest(payload, output_path)

            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(data["flow-01"], "/tmp/flow-01.png")
            self.assertEqual(data["logical-er-01"], "/tmp/logical-er-01.png")

    def test_load_manifest_accepts_drawio_xml_source_format(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "diagrams": [
                            {
                                "id": "system-architecture-drawio",
                                "type": "system_architecture",
                                "engine": "drawio",
                                "source_format": "drawio_xml",
                                "content": "<mxGraphModel><root><mxCell id=\"0\"/><mxCell id=\"1\" parent=\"0\"/></root></mxGraphModel>",
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            diagrams = module.load_manifest(manifest_path)

        self.assertEqual(diagrams[0].engine, "drawio")
        self.assertEqual(diagrams[0].source_format, "drawio_xml")
        self.assertEqual(diagrams[0].source_suffix, ".drawio")
        self.assertEqual(diagrams[0].drawio_content_type, "mxfile")

    def test_load_manifest_infers_drawio_xml_from_drawio_engine_and_xml_content(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "diagrams": [
                            {
                                "id": "system-architecture-drawio-auto",
                                "type": "system_architecture",
                                "engine": "drawio",
                                "content": "<mxfile host=\"app.diagrams.net\"><diagram id=\"1\"><mxGraphModel><root><mxCell id=\"0\"/><mxCell id=\"1\" parent=\"0\"/></root></mxGraphModel></diagram></mxfile>",
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            diagrams = module.load_manifest(manifest_path)

        self.assertEqual(diagrams[0].engine, "drawio")
        self.assertEqual(diagrams[0].source_format, "drawio_xml")
        self.assertEqual(diagrams[0].source_suffix, ".drawio")


if __name__ == "__main__":
    unittest.main()
