from pathlib import Path
from typing import Union

LtxBlock = Union[list[str], dict[str, str]]
LtxParserResults = dict[str, LtxBlock]


class LtxParser:
    _encoding = 'cp1251'
    _parsed_blocks: LtxParserResults = None

    def __init__(self, file_path: Path):
        self._path = file_path
        self._parse()

    def get_parsed_blocks(self) -> LtxParserResults:
        return self._parsed_blocks

    def _parse(self):
        self._parsed_blocks = {}
        raw_blocks = {}
        current_block_header = None
        with open(self._path, 'r', encoding=self._encoding) as file:
            for line in file.readlines():
                line = self._preprocess_line(line)
                if not line:
                    continue
                if self._is_block_start_line(line):
                    current_block_header = self._get_block_caption(line)
                    raw_blocks[current_block_header] = []
                    continue
                raw_blocks[current_block_header].append(line)

        for block_code, block_lines in raw_blocks.items():
            self._parsed_blocks[block_code] = self._parse_block_lines(block_lines)

    def _preprocess_line(self, line: str) -> str:
        comment_start = ';'
        line = line.split(comment_start)[0]
        return line.strip()

    def _is_block_start_line(self, line: str) -> bool:
        BLOCK_CAPTION_START = '['
        BLOCK_CAPTION_END = ']'
        return line[0] == BLOCK_CAPTION_START and line[-1] == BLOCK_CAPTION_END

    def _get_block_caption(self, line: str) -> str:
        return line[1:len(line) - 1]

    def _parse_block_lines(self, lines: list[str]) -> LtxBlock:
        if len(lines) == 0:
            raise ValueError("empty block")
        cnt = lines[0].count('=')
        if any([l.count('=') != cnt for l in lines[1:]]):
            raise ValueError('Кол-во знаков = отличается в блоке')
        if cnt == 0:
            return lines
        elif cnt == 1:
            return dict(self._parse_line_key_value(l) for l in lines)
        raise ValueError('Не должно быть больше 1 =')

    def _parse_line_key_value(self, line: str) -> tuple[str, str]:
        (key, value) = line.split('=')
        return key.strip(), value.strip()
