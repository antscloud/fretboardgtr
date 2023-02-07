import os
import io
import sys
import unittest
from fretboardgtr.fretboardgtr import FretBoardGtr
from fretboardgtr.scalegtr import ScaleGtr, ChordFromName, ScaleFromName
from fretboardgtr.chordgtr import ChordGtr
from fretboardgtr.constants import Mode, Chord

path="tests/images/scalegtr/"
class ScaleGtrTest(unittest.TestCase):

    """" Test case for fretboardgtr"""

    def test_scalefromname_findscale(self):
        self.assertEqual(ScaleFromName().results,{'root': 'C', 'scale': ['C', 'D', 'E', 'F', 'G', 'A', 'B']})
        self.assertEqual(ScaleFromName(root='D#',mode='Aeolian').results,{'root': 'D#', 'scale': ['D#', 'F', 'F#', 'G#', 'A#', 'B', 'C#']})
        self.assertEqual(ScaleFromName(root='D#',mode=Mode.AEOLIAN).results,{'root': 'D#', 'scale': ['D#', 'F', 'F#', 'G#', 'A#', 'B', 'C#']})
        self.assertEqual(ScaleFromName(root='A#',mode='Dominantbebop').results,{'root': 'A#', 'scale': ['A#', 'C', 'D', 'D#', 'F', 'G', 'G#', 'A']})
        self.assertEqual(ScaleFromName(root='A#',mode=Mode.DOMINANT_BEBOP).results,{'root': 'A#', 'scale': ['A#', 'C', 'D', 'D#', 'F', 'G', 'G#', 'A']})


    def test_chordfromname_findscale(self):
        self.assertEqual(ChordFromName().results,{'root': 'C', 'scale': ['C', 'E', 'G']})
        self.assertEqual(ChordFromName(root='D#',quality='M').results,{'root': 'D#', 'scale': ['D#', 'G', 'A#']})
        self.assertEqual(ChordFromName(root='D#',quality=Chord.MAJOR).results,{'root': 'D#', 'scale': ['D#', 'G', 'A#']})
        self.assertEqual(ChordFromName(root='D',quality=Chord.MINOR).results,{'root': 'D', 'scale': ['D', 'F', 'A']})
        self.assertEqual(ChordFromName(root='C',quality=Chord.DOMINANT_SEVENTH).results,{'root': 'C', 'scale': ['C', 'E', 'G', 'A#']})
        self.assertEqual(ChordFromName(root='C',quality=Chord.MAJOR_SEVENTH).results,{'root': 'C', 'scale': ['C', 'E', 'G', 'B']})
        self.assertEqual(ChordFromName(root='C',quality=Chord.AUGMENTED).results,{'root': 'C', 'scale': ['C', 'E', 'G#']})
        self.assertEqual(ChordFromName(root='C',quality=Chord.POWER).results,{'root': 'C', 'scale': ['C', 'G']})
        self.assertEqual(ChordFromName(root='C',quality=Chord.SUSPENDED_FOURTH).results,{'root': 'C', 'scale': ['C', 'F', 'G']})
        self.assertEqual(ChordFromName(root='E',quality='dim(maj11)').results,{'root': 'E', 'scale': ['E', 'G', 'A', 'A#', 'D#']})


    def test_emptybox(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"emptybox.svg")
        F.emptybox()

        """ F.dwg.save() """

        with open(path+'emptybox.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])
    
    def test_backgroundfill(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.background_color='rgb(0,0,0)'
        F.pathname(path+"background.svg")
        F.emptybox()
        F.background_fill()

        """ F.dwg.save() """

        with open(path+'background.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_add_dot(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"add_dot.svg")
        F.emptybox()
        F.add_dot()

        """ F.dwg.save() """

        with open(path+'add_dot.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_add_dot_24(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.last_fret=24
        F.pathname(path+"add_dot_24.svg")
        F.emptybox()
        F.add_dot()

        """ F.dwg.save() """

        with open(path+'add_dot_24.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_write_lines(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"write_lines.svg")
        F.emptybox()
        F.createfretboard()

        """ F.dwg.save() """

        with open(path+'write_lines.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])
    
    def test_write_nut(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"nut.svg")
        F.emptybox()
        F.nut()

        """ F.dwg.save() """

        with open(path+'nut.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_show_fret(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"show_fret.svg")
        F.emptybox()
        F.show_fret()

        """ F.dwg.save() """

        with open(path+'show_fret.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_show_tuning(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"tuning.svg")
        F.emptybox()
        F.show_tuning()

        """ F.dwg.save() """

        with open(path+'tuning.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_fill_with_chords(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"fill_with_chords.svg")
        F.emptybox()
        F.fill_with_chords()

        """ F.dwg.save() """

        with open(path+'fill_with_chords.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_fill_with_scale(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"fill_with_scale.svg")
        F.emptybox()
        F.fill_with_scale()

        """ F.dwg.save() """

        with open(path+'fill_with_scale.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_draw(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.theme(show_note_name=True)
        F.theme(open_color_scale=True,string_size=3,default_theme=True)
        F.pathname(path+"draw.svg")
        F.draw()
        """ F.dwg.save() """

        with open(path+'draw.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

if __name__ == "__main__" :
    unittest.main()