#allow to import all with from fretboardgtr import ScaleGtr for instance
# if no import under this line we have to do from fretboardgtr.fretboardgtr import FretBoardGtr in interpreter
from fretboardgtr.fretboardgtr import FretBoardGtr
from fretboardgtr.scalegtr import ScaleGtr, ChordFromName, ScaleFromName
from fretboardgtr.chordgtr import ChordGtr
from fretboardgtr.constants import Mode