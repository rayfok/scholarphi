from typing import Any, List, NamedTuple, Optional

ArxivId = str
S2Id = str
S2AuthorId = str

Path = str
AbsolutePath = str
RelativePath = str


class Author(NamedTuple):
    id: Optional[S2AuthorId]
    name: str


class Reference(NamedTuple):
    s2Id: S2Id
    arxivId: Optional[ArxivId]
    doi: Optional[str]
    title: str
    authors: List[Author]
    venue: Optional[str]
    year: Optional[int]


class S2Metadata(NamedTuple):
    s2id: S2Id
    references: List[Reference]


class Bibitem(NamedTuple):
    key: str
    """
    Plaintext extracted for bibitem.
    """
    text: str


EquationIndex = int
CharacterIndex = int


class Symbol(NamedTuple):
    characters: List[CharacterIndex]
    mathml: str
    """
    List of child symbols. Should be of type 'Symbol'. 'children' is a bit of misnomer. These is
    actually a list of all other symbols for which this is the closest ancestor.
    """
    children: List[Any]


class Character(NamedTuple):
    text: str
    i: CharacterIndex
    start: int
    end: int


class FileContents(NamedTuple):
    arxiv_id: ArxivId
    """
    Absolute path to the TeX file.
    """
    path: str
    contents: str


class ColorizedCitation(NamedTuple):
    hue: float
    keys: List[str]


class ColorizedEquation(NamedTuple):
    hue: float
    tex: str
    i: EquationIndex


class SymbolId(NamedTuple):
    tex_path: str
    equation_index: int
    symbol_index: int


class CompilationResult(NamedTuple):
    success: bool
    compiled_pdfs: Optional[List[str]]
    stdout: bytes
    stderr: bytes


class Point(NamedTuple):
    """
    Location of a pixel within an image.
    """

    x: int
    y: int


class Rectangle(NamedTuple):
    """
    Rectangle within an image. Left and top refer to positions of pixels.
    """

    left: int
    top: int
    width: int
    height: int


class PdfBoundingBox(NamedTuple):
    """
    Bounding box in PDF coordinates.
    """

    left: float
    top: float
    width: float
    height: float
    page: int


class PdfBoundingBoxAndHue(NamedTuple):
    hue: float
    box: PdfBoundingBox


class RasterBoundingBox(NamedTuple):
    """
    Bounding box of pixel locations in an image.
    """

    left: int
    top: int
    width: int
    height: int
    page: int


class BoundingBoxInfo(NamedTuple):
    pdf_box: PdfBoundingBox
    raster_box: RasterBoundingBox
