import csv
import os.path
from typing import Iterator, NamedTuple

from command.command import ArxivBatchCommand
from common import directories
from common.bounding_box import get_symbol_bounding_box
from common.file_utils import (
    clean_directory,
    load_equation_token_locations,
    load_symbols,
)
from common.types import ArxivId, BoundingBox, CharacterLocations, SymbolWithId


class LocationTask(NamedTuple):
    arxiv_id: ArxivId
    character_locations: CharacterLocations
    symbol_with_id: SymbolWithId


class LocateSymbols(ArxivBatchCommand[LocationTask, BoundingBox]):
    @staticmethod
    def get_name() -> str:
        return "locate-symbols"

    @staticmethod
    def get_description() -> str:
        return (
            "Find locations of symbols based on locations of equation tokens. "
            + "Requires 'locate-equation-token-hues' to have been run."
        )

    @staticmethod
    def get_entity_type() -> str:
        return "symbols"

    def get_arxiv_ids_dirkey(self) -> str:
        return "hue-locations-for-equation-tokens"

    def load(self) -> Iterator[LocationTask]:

        for arxiv_id in self.arxiv_ids:

            output_dir = directories.arxiv_subdir("symbol-locations", arxiv_id)
            clean_directory(output_dir)

            token_locations = load_equation_token_locations(arxiv_id)
            if token_locations is None:
                continue

            symbols_with_ids = load_symbols(arxiv_id)
            if symbols_with_ids is None:
                continue

            for symbol_with_id in symbols_with_ids:
                yield LocationTask(
                    arxiv_id=arxiv_id,
                    character_locations=token_locations,
                    symbol_with_id=symbol_with_id,
                )

    def process(self, item: LocationTask) -> Iterator[BoundingBox]:
        symbol = item.symbol_with_id.symbol
        symbol_id = item.symbol_with_id.symbol_id
        box = get_symbol_bounding_box(symbol, symbol_id, item.character_locations)
        if box is not None:
            yield box

    def save(self, item: LocationTask, result: BoundingBox) -> None:
        output_dir = directories.arxiv_subdir("symbol-locations", item.arxiv_id)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        locations_path = os.path.join(output_dir, "symbol_locations.csv")
        symbol_id = item.symbol_with_id.symbol_id
        with open(locations_path, "a") as locations_file:
            writer = csv.writer(locations_file, quoting=csv.QUOTE_ALL)
            writer.writerow(
                [
                    symbol_id.tex_path,
                    symbol_id.equation_index,
                    symbol_id.symbol_index,
                    result.page,
                    result.left,
                    result.top,
                    result.width,
                    result.height,
                ]
            )