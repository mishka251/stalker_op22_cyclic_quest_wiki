import re
from pathlib import Path

from chardet.universaldetector import UniversalDetector
from django.conf import settings

TMP_DIR = Path("tmp")
DEFAULT_ENCODING = "utf-8"


class GSCXmlFixer:
    """
    Правка xml-файлов от GSC, которые не читаются стандартными библиотеками python
    """

    def __init__(
        self,
        encoding: str | None = None,
    ):
        self._encoding = encoding

    def fix(self, source: Path) -> Path:
        self._ensure_tmp_dir()
        header = self._get_file_header(source)
        encoding = self._get_encoding(header, source)
        need_add_root_tag = header is None
        with source.open("r", encoding=encoding) as file:
            content = file.read()
        fixed_content = self._replace_includes(content, encoding)
        fixed_content = self._fix_broken_comments(fixed_content)
        if need_add_root_tag:
            fixed_content = self._add_root_tag(fixed_content, encoding)
        fixed_file_path = self._tml_file_name_for_xml(source)
        with fixed_file_path.open("w", encoding=encoding) as tml_file:
            tml_file.write(fixed_content)
        return fixed_file_path

    def _get_encoding(self, header: str | None, source: Path) -> str:
        encoding = None
        if header:
            encoding = self._get_encoding_from_header(header)
        if encoding is None:
            encoding = self._encoding
        if encoding is None:
            encoding = self._detect_file_encoding_by_content(source)
        return encoding

    def _get_encoding_from_header(self, header: str) -> str | None:
        header_conding_re = re.compile(
            r'<\?xml .*encoding="(?P<encoding>([\w\d\-_]+))".*\?>',
        )
        rm = header_conding_re.match(header)
        if rm:
            return rm.group("encoding")
        return None

    def _get_file_header(self, source: Path) -> str | None:
        with source.open("rb") as file:
            line1 = file.readline()
            line = line1.decode("utf-8-sig")
        if line.startswith("<?xml"):
            return line
        return None

    def _detect_file_encoding_by_content(self, source: Path) -> str:
        detector = UniversalDetector()
        with source.open("rb") as file:
            for line in file:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()
        encoding = detector.result["encoding"]
        if not encoding:
            msg = "Unknown encoding"
            raise ValueError(msg)
        return encoding

    def _ensure_tmp_dir(self) -> None:
        if not TMP_DIR.exists():
            TMP_DIR.mkdir()

    def _tml_file_name_for_xml(self, source_file_path: Path) -> Path:
        return TMP_DIR / source_file_path.name

    def _fix_broken_comments(self, content: str) -> str:
        current_content = ""
        fixed_content = content
        xml_comment_re = re.compile(r"<!--(?P<before>.*?)-{2,}(?P<after>.*)-->")
        while fixed_content != current_content:
            current_content = fixed_content
            fixed_content = re.sub(
                xml_comment_re,
                r"<!--\g<before> \g<after>-->",
                current_content,
            )
        xml_comment2_re = re.compile(r"<!--[\s-]*(?P<comment>.*?)[\s-]*-->")
        return re.sub(xml_comment2_re, r"<!-- \g<comment> -->", fixed_content)

    def _add_root_tag(self, content: str, encoding: str) -> str:
        return f'<?xml version="1.0" encoding="{encoding}"?>\n{content}'

    def _replace_includes(self, content: str, root_encoding: str) -> str:
        import_regex = re.compile(r'#include "(?P<include_path>.*?)"')
        return re.sub(
            import_regex,
            lambda s: self._get_included(s, root_encoding),
            content,
        )

    def _get_included(self, m: re.Match, root_encoding: str) -> str:
        include_path = m.groupdict()["include_path"]
        base_path = settings.OP22_GAME_DATA_PATH / "config"
        target_path = base_path / include_path
        encoding = self._detect_file_encoding_by_content(target_path)
        try:
            with target_path.open("r", encoding=encoding) as file:
                content = file.read()
                fixed_content = self._replace_includes(content, root_encoding)
        except Exception as e:
            msg = f"При парсинге {target_path} {encoding=}"
            raise FixerError(msg) from e
        try:
            tmp_file = Path(f"tmp_{target_path.name}.xml")
            with tmp_file.open("w", encoding=root_encoding) as tml_file:
                tml_file.write(fixed_content)
            tmp_file.unlink()
        except Exception as e:
            msg = f"При парсинге {target_path} {encoding=}"
            raise FixerError(msg) from e
        return f"\n{fixed_content}\n"


class FixerError(Exception):
    pass
