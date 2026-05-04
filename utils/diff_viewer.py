import difflib

class DiffViewer:
    @staticmethod
    def generate_diff(old_text, new_text, filename="policy_diff.html"):
        """Generate an HTML diff between two policy versions."""
        old_lines = old_text.splitlines(keepends=True)
        new_lines = new_text.splitlines(keepends=True)

        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile='Original Policy',
            tofile='Revised Policy',
            lineterm=''
        )

        html_diff = difflib.HtmlDiff().make_file(
            old_lines,
            new_lines,
            fromdesc='Original Policy',
            todesc='Revised Policy'
        )

        return '\n'.join(diff), html_diff

    @staticmethod
    def print_diff(old_text, new_text):
        """Print a simple diff to console."""
        old_lines = old_text.splitlines(keepends=True)
        new_lines = new_text.splitlines(keepends=True)

        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile='Original',
            tofile='Revised',
            lineterm=''
        )

        return ''.join(diff)
