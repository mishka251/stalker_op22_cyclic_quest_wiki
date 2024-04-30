import re
from pathlib import Path
from typing import Optional, Union

LtxBlock = Union[list[str], dict[str, str]]
LtxParserResults = dict[str, LtxBlock]

MULTILINE_BLOCK_START = "<<END"
MULTILINE_BLOCK_END = "END"


class BaseLtxParser:
    _parsed_blocks: LtxParserResults
    _known_extends: LtxParserResults

    BLOCK_CAPTION_START = "["
    BLOCK_CAPTION_END = "]"

    def __init__(self, file_path: Path, lines_generator,  known_extends: LtxParserResults | None = None):
        self._path = file_path
        self._known_extends = known_extends or {}
        self._parse(lines_generator)

    def get_parsed_blocks(self) -> LtxParserResults:
        return self._parsed_blocks

    def _parse(self, lines_generator):
        self._parsed_blocks = {}
        raw_blocks = {}
        blocks_bases: dict[str, tuple[str, ...]] = {}
        current_block_header = None
        current_multiline_block = None
        for line in lines_generator:
            line = self._preprocess_line(line)
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
                        block_lines = self._parse_block_lines(block_lines, block_code)
                        if isinstance(block_lines, list):
                            self._parsed_blocks[block_code] = block_lines
                        else:
                            self._parsed_blocks[block_code] = {}
                            self._parsed_blocks[block_code] |= self._get_bases(blocks_bases[block_code])
                            self._parsed_blocks[block_code] |= block_lines
                    current_block_header, bases = self._get_block_caption(line)
                    raw_blocks[current_block_header] = []
                    blocks_bases[current_block_header] = bases
                    continue
            if line.endswith(MULTILINE_BLOCK_START):
                if current_multiline_block is not None:
                    raise ValueError("Nested multiline block")
                else:
                    current_multiline_block = line
                    continue
            else:
                if current_multiline_block:
                    current_multiline_block += "\n"+line
                    if line.strip() == MULTILINE_BLOCK_END:
                        key, value = current_multiline_block.split("=", 1)
                        value = value.strip()
                        value = value[len(MULTILINE_BLOCK_START):]
                        value = value[:-len(MULTILINE_BLOCK_END)]
                        current_multiline_block = f"{key}= {value}"
                        raw_blocks[current_block_header].append(current_multiline_block)
                        current_multiline_block = None

                    continue
            raw_blocks[current_block_header].append(line)

        for block_code, block_lines in raw_blocks.items():
            block_lines = self._parse_block_lines(block_lines, block_code)
            if isinstance(block_lines, list):
                self._parsed_blocks[block_code] = block_lines
            else:
                self._parsed_blocks[block_code] = {}
                self._parsed_blocks[block_code] |= self._get_bases(blocks_bases[block_code])
                self._parsed_blocks[block_code] |= block_lines

    def _line_is_include(self, line: str) -> bool:
        return line.startswith("#include")

    def _parse_include(self, line: str) -> LtxParserResults:
        pattern = re.compile(r'#include "(?P<file_path>.*)"')
        if rm:=pattern.match(line):
            file_path = rm.groupdict()["file_path"]
        else:
            raise ValueError("incorrect include")
        current_dir = self._path.parent
        file_path = current_dir / file_path

        nested_bases = {
            **self._known_extends,
            **self._parsed_blocks,
        }

        nested_parsed = LtxParser(file_path, nested_bases)
        return nested_parsed.get_parsed_blocks()

    def _get_bases(self, bases: tuple[str, ...]) -> dict:
        merged_bases : dict= {}
        try:
            for base in bases:
                if base in self._parsed_blocks:
                    merged_bases |= self._parsed_blocks[base]
                elif base in self._known_extends:
                    merged_bases |= self._known_extends[base]
                else:
                    raise ValueError(f"Unknown {base=} in file={self._path}")
        except Exception as e:
            print(f"Error while get_bases {merged_bases=}, {bases=}, {[self._parsed_blocks[base] for base in bases]=}")
            raise e
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
        bases_str = line[end_index + 2:len(line)]
        bases = tuple() if not bases_str else tuple(s.strip() for s in bases_str.split(","))
        return caption, bases

    def _parse_block_lines(self, lines: list[str], name: str) -> LtxBlock:
        if not lines:
            return {}
        cnt = max([line.count("=") for line in lines])
        if cnt == 0:
            return lines
        if cnt >= 1:
            return dict(self._parse_line_key_value(line) for line in lines)

    def _parse_line_key_value(self, line: str) -> tuple[str, str | None]:
        if "=" in line:
            (key, value) = (s.strip() for s in line.split("=", 1))
        else:
            key = line.strip()
            value = None
        return key, value


class LtxParser(BaseLtxParser):
    _encoding = "cp1251"

    def __init__(self, file_path: Path, known_extends: LtxParserResults = None):
        self._path = file_path

        with open(self._path, encoding=self._encoding) as file:
            lines = file.readlines()
            super().__init__(file_path, lines, known_extends)

class TextLtxParser(BaseLtxParser):
    _encoding = "cp1251"

    def __init__(self, file_path: Path, content: str, known_extends: LtxParserResults = None):
        self._path = file_path

        lines = content.split("\n")
        try:
            super().__init__(file_path, lines, known_extends)
        except Exception as ex:
            print(f"Ошибка парсинга {content}")
            raise ex
