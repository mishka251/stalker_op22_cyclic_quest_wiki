import re
from pathlib import Path

from django.conf import settings

TMP_DIR = Path('tmp')
DEFAULT_ENCODING = "windows-1251"


class GSCXmlFixer:
    """
    Правка xml-файлов от GSC, которые не читаются стандартными библиотеками python
    """

    def __init__(self, source_path: Path):
        self._source = source_path

    def fix(self, add_root_tag: bool=False) -> Path:
        if not TMP_DIR.exists():
            TMP_DIR.mkdir()

        with open(self._source, 'r', encoding=DEFAULT_ENCODING) as file:
            content = file.read()
        fixed_content = self._fix_broken_comments(content)
        if add_root_tag:
            fixed_content = self._add_root_tag(fixed_content)
        fixed_file_path = self._tml_file_name_for_xml(self._source)
        with open(fixed_file_path, 'w', encoding=DEFAULT_ENCODING) as tml_file:
            tml_file.write(fixed_content)
        return fixed_file_path

    def _tml_file_name_for_xml(self, source_file_path: Path) -> Path:
        return TMP_DIR / source_file_path.name

    def _fix_broken_comments(self, content: str) -> str:
        current_content = ''
        fixed_content = content
        xml_comment_re = re.compile(r'<!--(?P<before>.*?)-{2,}(?P<after>.*)-->')
        while fixed_content != current_content:
            current_content = fixed_content
            fixed_content = re.sub(xml_comment_re, r'<!--\g<before> \g<after>-->', current_content)
        xml_comment2_re = re.compile(r'<!--[\s-]*(?P<comment>.*?)[\s-]*-->')
        fixed_content = re.sub(xml_comment2_re, r'<!-- \g<comment> -->', fixed_content)
        return fixed_content

    def _add_root_tag(self, content: str) -> str:
        return f'<xml>{content}</xml>'

    def _replace_includes(self, content: str) -> str:
        import_regex = re.compile(r'#include "(?P<include_path>.*?)"')
        return re.sub(import_regex, self._get_included, content)

    def _get_included(self, m: re.Match) -> str:
        include_path = m.groupdict()['include_path']
        base_path = settings.OP22_GAME_DATA_PATH / 'config'
        target_path = base_path / include_path
        with open(target_path, 'r') as file:
            return file.read()