import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

BRAND = Path(__file__).parents[1] / "brand"
sys.path.insert(0, str(BRAND))
import gen_logos  # noqa: E402


class FamilyLogoTests(unittest.TestCase):
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
