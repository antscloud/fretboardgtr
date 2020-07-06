import os 
import io
import sys
import unittest
from fretboardgtr.fretboardgtr import FretBoardGtr
from fretboardgtr.scalegtr import ScaleGtr, ChordFromName, ScaleFromName
from fretboardgtr.chordgtr import ChordGtr

path="tests/images/chordgtr/"
class ChordGtrTest(unittest.TestCase):

    """" Test case for fretboardgtr"""

    def test_fingering(self):
        F=ChordGtr()
        F.setfingering(fingering=[0,3,2,0,1,0])
        self.assertEqual(F.fingering,[0,3,2,0,1,0])
    
    def test_backgroundfill(self):
        F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
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
        F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"add_dot.svg")
        F.emptybox()
        F.add_dot()

        """ F.dwg.save() """

        with open(path+'add_dot.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])


    def test_write_lines(self):
        F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"write_lines.svg")
        F.emptybox()
        F.createfretboard()

        """ F.dwg.save() """

        with open(path+'write_lines.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])
    
    def test_write_nut(self):
        F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"nut.svg")
        F.emptybox()
        F.nut()

        """ F.dwg.save() """

        with open(path+'nut.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_show_tuning(self):
        F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"tuning.svg")
        F.emptybox()
        F.show_tuning()

        """ F.dwg.save() """

        with open(path+'tuning.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_fill_fretboard(self):
        F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname(path+"fill_with_chords.svg")
        F.emptybox()
        F.fillfretboard()

        """ F.dwg.save() """

        with open(path+'fill_with_chords.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_draw(self):
        F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
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