"""Starter usability checks; numerical checks are added with each implementation."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


class StarterChecks(unittest.TestCase):
    def test_installed_entry_point_outside_project(self):
        # An editable install must not rely on the terminal's working directory.
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, '-m', 'econlab'], cwd=folder,
                                    capture_output=True, text=True, check=True)
        self.assertIn('Student starter', result.stdout)
        self.assertIn('README.md', result.stdout)

    def test_documentation_links_resolve(self):
        documents = list(ROOT.glob('*.md'))
        for folder in ('notes', 'prompts', 'docs'):
            documents.extend((ROOT / folder).rglob('*.md'))
        for path in documents:
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                target = unquote(target.split('#')[0])
                with self.subTest(document=path.relative_to(ROOT), target=target):
                    self.assertTrue((path.parent / target).exists())


if __name__ == '__main__':
    unittest.main()
