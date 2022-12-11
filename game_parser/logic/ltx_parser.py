import re
from pathlib import Path
from typing import Union

LtxBlock = Union[list[str], dict[str, str]]
LtxParserResults = dict[str, LtxBlock]


class LtxParser:
    _encoding = 'cp1251'
    _parsed_blocks: LtxParserResults = None
    _known_extends: LtxParserResults = None

    BLOCK_CAPTION_START = '['
    BLOCK_CAPTION_END = ']'

    def __init__(self, file_path: Path, known_extends: LtxParserResults = None):
        self._path = file_path
        self._known_extends = known_extends or {}
        self._parse()

    def get_parsed_blocks(self) -> LtxParserResults:
        return self._parsed_blocks

    def _parse(self):
        self._parsed_blocks = {}
        raw_blocks = {}
        blocks_bases: dict[str, tuple[str, ...]] = {}
        current_block_header = None
        with open(self._path, 'r', encoding=self._encoding) as file:
            for line in file.readlines():
                line = self._preprocess_line(line)
                if not line:
                    continue
                if self._line_is_include(line):
                    self._parsed_blocks |= self._parse_include(line)
                    continue
                if self._is_block_start_line(line):
                    current_block_header, bases = self._get_block_caption(line)
                    raw_blocks[current_block_header] = []
                    blocks_bases[current_block_header] = bases
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
            if not self._parsed_blocks[block_code]:
                raise ValueError(f"empty block {block_code=}")

    def _line_is_include(self, line: str) -> bool:
        return line.startswith('#include')

    def _parse_include(self, line: str) -> LtxParserResults:
        pattern = re.compile(r'#include "(?P<file_path>.*)"')
        file_path = pattern.match(line).groupdict()['file_path']
        current_dir = self._path.parent
        file_path = current_dir / file_path

        nested_bases = {
            **self._known_extends,
            **self._parsed_blocks
        }
        # print(f'Parse nested {file_path=}')
        nested_parsed = LtxParser(file_path, nested_bases)
        return nested_parsed.get_parsed_blocks()

    def _get_bases(self, bases: tuple[str, ...]) -> dict:
        merged_bases = dict()
        for base in bases:
            if base in self._parsed_blocks:
                merged_bases |= self._parsed_blocks[base]
            elif base in self._known_extends:
                merged_bases |= self._known_extends[base]
            else:
                raise ValueError(f'Unknown {base=}')
        return merged_bases

    def _preprocess_line(self, line: str) -> str:
        comment_start = ';'
        line = line.split(comment_start)[0]
        comment_start_v2 = r'//'
        line = line.split(comment_start_v2)[0]
        return line.strip()

    def _is_block_start_line(self, line: str) -> bool:
        return line[0] == self.BLOCK_CAPTION_START and self.BLOCK_CAPTION_END in line

    def _get_block_caption(self, line: str) -> tuple[str, tuple[str, ...]]:
        end_index = line.index(self.BLOCK_CAPTION_END)
        caption = line[1:end_index]
        bases_str = line[end_index + 2:len(line)]
        if not bases_str:
            bases = tuple()
        else:
            bases = tuple(map(lambda s: s.strip(), bases_str.split(',')))
        return caption, bases

    def _parse_block_lines(self, lines: list[str], name: str) -> LtxBlock:
        if not lines:
            return {}
        cnt = lines[0].count('=')
        if any([l.count('=') != cnt for l in lines[1:]]):
            raise ValueError(f'Кол-во знаков "=" отличается в блоке {name=}')
        if cnt == 0:
            return lines
        elif cnt == 1:
            return dict(self._parse_line_key_value(l) for l in lines)
        raise ValueError(f'Не должно быть больше 1 =, {name=}')

    def _parse_line_key_value(self, line: str) -> tuple[str, str]:
        (key, value) = line.split('=')
        return key.strip(), value.strip()
