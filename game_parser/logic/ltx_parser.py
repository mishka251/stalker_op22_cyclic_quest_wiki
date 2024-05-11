import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

LtxBlockDict = dict[str, str]

LtxBlock = list[str] | LtxBlockDict
LtxParserResults = dict[str, LtxBlock]

MULTILINE_BLOCK_START = "<<END"
MULTILINE_BLOCK_END = "END"

KnownExtendsType = dict[str, LtxBlockDict]


class BaseLtxParser:
    _parsed_blocks: LtxParserResults
    _known_extends: KnownExtendsType

    BLOCK_CAPTION_START = "["
    BLOCK_CAPTION_END = "]"

    def __init__(
        self,
        file_path: Path,
        lines_generator,
        known_extends: KnownExtendsType | None = None,
    ):
        self._path = file_path
        self._known_extends = known_extends or {}
        self._parse(lines_generator)

    def get_parsed_blocks(self) -> LtxParserResults:
        return self._parsed_blocks

    def _parse(  # noqa: C901 PLR0912 PLR0915
        self,
        lines_generator: Iterable[str],
    ) -> None:
        #  pylint: disable=too-many-locals, too-many-branches, too-many-statements
        self._parsed_blocks = {}
        raw_blocks: dict[str, Any] = {}
        blocks_bases: dict[str, tuple[str, ...]] = {}
        current_block_header: str | None = None
        current_multiline_block: str | None = None
        for _line in lines_generator:
            line = self._preprocess_line(_line)
            if current_multiline_block is None:
                if not line:
                    continue
                if self._line_is_include(line):
                    self._parsed_blocks |= self._parse_include(line)
                    continue
                if self._is_block_start_line(line):
                    prev_block_name = current_block_header
                    if prev_block_name is not None:
                        block_code = prev_block_name
                        block_lines = raw_blocks[block_code]
                        block_lines = self._parse_block_lines(block_lines)
                        if isinstance(block_lines, list):
                            self._parsed_blocks[block_code] = block_lines
                        else:
                            current_block: LtxBlockDict = {}
                            current_block |= self._get_bases(
                                blocks_bases[block_code],
                            )
                            current_block |= block_lines
                            self._parsed_blocks[block_code] = current_block
                    current_block_header, bases = self._get_block_caption(line)
                    raw_blocks[current_block_header] = []
                    blocks_bases[current_block_header] = bases
                    continue
            if current_block_header is None:
                raise TypeError
            if line.endswith(MULTILINE_BLOCK_START):
                if current_multiline_block is not None:
                    msg = "Nested multiline block"
                    raise ValueError(msg)
                current_multiline_block = line
                continue
            if current_multiline_block:
                current_multiline_block += "\n" + line
                if line.strip() == MULTILINE_BLOCK_END:
                    key, value = current_multiline_block.split("=", 1)
                    value = value.strip()
                    value = value[len(MULTILINE_BLOCK_START) :]
                    value = value[: -len(MULTILINE_BLOCK_END)]
                    current_multiline_block = f"{key}= {value}"
                    raw_blocks[current_block_header].append(current_multiline_block)
                    current_multiline_block = None

                continue
            raw_blocks[current_block_header].append(line)

        for block_code, _block_lines in raw_blocks.items():
            block_lines = self._parse_block_lines(_block_lines)
            if isinstance(block_lines, list):
                self._parsed_blocks[block_code] = block_lines
            else:
                current_block_: LtxBlockDict = {}
                current_block_ |= self._get_bases(
                    blocks_bases[block_code],
                )
                current_block_ |= block_lines
                self._parsed_blocks[block_code] = current_block_

    def _line_is_include(self, line: str) -> bool:
        return line.startswith("#include")

    def _parse_include(self, line: str) -> LtxParserResults:
        pattern = re.compile(r'#include "(?P<file_path>.*)"')
        if rm := pattern.match(line):
            file_path = rm.groupdict()["file_path"]
        else:
            msg = "incorrect include"
            raise ValueError(msg)
        current_dir = self._path.parent
        file_path = current_dir / file_path

        nested_bases: KnownExtendsType = {
            **self._known_extends,
            **{k: v for k, v in self._parsed_blocks.items() if isinstance(v, dict)},
        }

        nested_parsed = LtxParser(file_path, nested_bases)
        return nested_parsed.get_parsed_blocks()

    def _get_bases(self, bases: tuple[str, ...]) -> LtxBlockDict:
        try:
            return self._get_bases_inner(bases)
        except Exception:
            print(
                f"Error while get_bases  {bases=}, {[self._parsed_blocks[base] for base in bases]=}",
            )
            raise

    def _get_bases_inner(self, bases: tuple[str, ...]) -> LtxBlockDict:
        merged_bases: LtxBlockDict = {}
        for base in bases:
            if isinstance(self._parsed_blocks, dict) and base in self._parsed_blocks:
                maybe_base = self._parsed_blocks[base]
                if isinstance(maybe_base, dict):
                    merged_bases |= maybe_base
                else:
                    msg = f"Base {base} is list"
                    raise ValueError(msg)
            elif base in self._known_extends:
                merged_bases |= self._known_extends[base]
            else:
                msg = f"Unknown {base=} in file={self._path}. {merged_bases=}"
                raise ValueError(
                    msg,
                )

        return merged_bases

    def _preprocess_line(self, line: str) -> str:
        comment_start = ";"
        line = line.split(comment_start)[0]
        comment_start_v2 = r"//"
        line = line.split(comment_start_v2)[0]
        comment_start_v3 = r"--"
        line = line.split(comment_start_v3)[0]
        return line.strip()

    def _is_block_start_line(self, line: str) -> bool:
        return line[0] == self.BLOCK_CAPTION_START and self.BLOCK_CAPTION_END in line

    def _get_block_caption(self, line: str) -> tuple[str, tuple[str, ...]]:
        end_index = line.index(self.BLOCK_CAPTION_END)
        caption = line[1:end_index]
        bases_str = line[end_index + 2 : len(line)] if ":" in line else ""
        bases = () if not bases_str else tuple(s.strip() for s in bases_str.split(","))
        return caption, bases

    def _parse_block_lines(self, lines: list[str]) -> LtxBlock:
        if not lines:
            return {}
        cnt = max(line.count("=") for line in lines)
        if cnt == 0:
            return lines
        d = dict(self._parse_line_key_value(line) for line in lines)
        return {k: v for k, v in d.items() if v is not None}

    def _parse_line_key_value(self, line: str) -> tuple[str, str | None]:
        if "=" in line:
            (key, value) = (s.strip() for s in line.split("=", 1))
        else:
            key = line.strip()
            value = None
        return key, value


class LtxParser(BaseLtxParser):
    _encoding = "cp1251"

    def __init__(self, file_path: Path, known_extends: KnownExtendsType | None = None):
        self._path = file_path

        with self._path.open(encoding=self._encoding) as file:
            lines = file.readlines()
            super().__init__(file_path, lines, known_extends)


class TextLtxParser(BaseLtxParser):
    _encoding = "cp1251"

    def __init__(
        self,
        file_path: Path,
        content: str,
        known_extends: KnownExtendsType | None = None,
    ):
        self._path = file_path

        lines = content.split("\n")
        try:
            super().__init__(file_path, lines, known_extends)
        except Exception:
            print(f"Ошибка парсинга {content}")
            raise
