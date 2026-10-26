import sys
import unittest
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET

BRAND = Path(__file__).parents[1] / "brand"
sys.path.insert(0, str(BRAND))
import gen_logos  # noqa: E402


class FamilyLogoTests(unittest.TestCase):
    def test_plugin_marks_fill_canvas_without_clipping(self):
        import cairosvg
        from PIL import Image

        self.assertEqual(
            {subject.key for subject in gen_logos.PLUGINS},
            {"funchat", "fundoc", "funlink", "funotp", "funcalendar", "funqr", "funcalc"},
        )
        fmt = next(fmt for fmt in gen_logos.FORMATS if fmt.key == "mark")
        for subject in gen_logos.PLUGINS:
            with self.subTest(subject=subject.key):
                png = cairosvg.svg2png(
                    bytestring=gen_logos.render_icon(fmt, subject).encode(),
                    output_width=256, output_height=256,
                )
                alpha = Image.open(BytesIO(png)).getchannel("A")
                left, top, right, bottom = alpha.getbbox()
                self.assertGreaterEqual((bottom - top) / 256, 0.90)
                self.assertLessEqual((bottom - top) / 256, 0.95)
                self.assertGreater(min(left, top, 256 - right, 256 - bottom), 4)

    def test_lockup_uses_containerless_mark(self):
        ns = "{http://www.w3.org/2000/svg}"
        for subject in gen_logos.ORGS:
            for on_dark in (False, True):
                with self.subTest(subject=subject.key, on_dark=on_dark):
                    root = ET.fromstring(gen_logos.render_lockup(subject, on_dark=on_dark))
                    self.assertIsNone(root.find(f".//{ns}rect"))
                    self.assertIsNotNone(root.find(f".//{ns}path"))

    def test_product_variants_keep_smile_and_top_bar_symbol(self):
        ns = "{http://www.w3.org/2000/svg}"
        original = ET.parse(BRAND / "farfarfun-original.svg").getroot()
        eyes = original.find(f"{ns}path[@id='eyes']").get("d")

        for subject in gen_logos.SUBJECTS[1:]:
            for fmt in gen_logos.FORMATS:
                with self.subTest(subject=subject.key, format=fmt.key):
                    root = ET.fromstring(gen_logos.render_icon(fmt, subject))
                    self.assertIn(eyes, [path.get("d") for path in root.iter(f"{ns}path")])
                    self.assertTrue(any(
                        "translate(780,336)" in group.get("transform", "")
                        for group in root.iter(f"{ns}g")
                    ))


if __name__ == "__main__":
    unittest.main()
