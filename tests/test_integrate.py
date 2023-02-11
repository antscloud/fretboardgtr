import unittest
from fretboardgtr.scalegtr import ScaleGtr, ChordFromName, ScaleFromName
from fretboardgtr.chordgtr import ChordGtr
from fretboardgtr.constants import Mode, Chord
import tempfile
from pathlib import Path

path = Path("tests/images/integrate/")


class IntegrateTest(unittest.TestCase):

    def test_scale_degree_name(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname('img/scale_degree_name.svg')
        F.draw()

        with open(path / 'scale_degree_name.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_scale_no_color(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.theme(show_note_name=True,color_scale=False)
        F.pathname('img/scale_no_color.svg')
        F.draw()

        with open(path / 'scale_no_color.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_scale_note_name(self):
        F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
        F.customtuning(['E','A','D','G','B','E'])
        F.theme(show_note_name=True)
        F.theme(open_color_scale=True,string_size=3,default_theme=True)
        F.pathname('img/scale_note_name.svg')
        F.draw()

        with open(path / 'scale_note_name.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_TestScaleName(self):
        F=ScaleGtr(ScaleFromName(root='F#',mode=Mode.IONIAN))
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname('img/TestScaleName.svg')
        F.theme(show_note_name=True)
        F.draw()

        with open(path / 'TestScaleName.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_TestScaleNameEnhar(self):
        F=ScaleGtr(scale=['D#','F','G','G#','A#','C','D'], root='D#',enharmonic=True)
        F.customtuning(['D','A','D','G','B','E'])
        F.pathname('img/TestScaleNameEnhar.svg')
        F.theme(show_note_name=True)
        F.draw()

        with open(path / 'TestScaleNameEnhar.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_TestScaleNameEnhar24(self):
        F=ScaleGtr(scale=['D#','F','G','G#','A#','C','D'], root='D#',enharmonic=True)
        F.customtuning(['D','A','D','G','B','E'])
        F.theme(last_fret=24)
        F.pathname('img/TestScaleNameEnhar24.svg')
        F.theme(show_note_name=True)
        F.draw()

        with open(path / 'TestScaleNameEnhar24.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_chord_degree_name(self):
        F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
        F.customtuning(['E','A','D','G','B','E'])
        F.pathname('img/chord_degree_name.svg')
        F.set_color(perfectfourth='rgb(0, 0, 0)',root='rgb(0, 0, 0)')
        F.draw()

        with open(path / 'chord_degree_name.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_TestChordName(self):
        F=ScaleGtr(ChordFromName(root='C',quality=Chord.MAJOR))
        F.customtuning(['D','A','D','G','A','D'])
        F.pathname('img/TestChordName.svg')
        F.draw()

        with open(path / 'TestChordName.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_lefthandchord(self):
        F=ChordGtr(fingering=[3,3,2,0,1,0],root="C",lefthand=True)
        F.customtuning(['F','A','D','G','B','E'])
        F.pathname('img/lefthandchord.svg')
        F.draw()

        with open(path / 'lefthandchord.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_chord_name_long(self):
        F=ChordGtr(fingering=[0,18,2,0,2,0],root="C")
        F.customtuning(['F','A','D','G','B','E'])
        F.pathname('img/chord_name_long.svg')
        F.theme(show_note_name=True)
        F.draw()

        with open(path / 'chord_name_long.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])

    def test_chord_name_background(self):
        F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
        F.customtuning(['F','A','D','G','B','E'])
        F.pathname('img/chord_name_background.svg')
        F.theme(show_note_name=True,background_color='rgb(70,70,70)')
        F.draw()

        with open(path / 'chord_name_background.svg','r') as f:
            file=f.read()
            self.assertEqual(F.dwg.tostring(),file.split('<?xml version="1.0" encoding="utf-8" ?>\n')[1])


    def test_save_diagram_in_different_formats(self):
        extensions = ['png', 'pdf', 'bmp', 'gif', 'svg'] # NOTE: SVG should be the last one
        F=ScaleGtr(root='A')
        with tempfile.TemporaryDirectory() as tmpdirname:
            for ext in extensions:
                with self.subTest(ext=ext):
                    out = Path(tmpdirname) / f'some_file.{ext}'
                    F.pathname(out)
                    self.assertFalse(out.exists(),
                                     f"{out} should not have been created yet")
                    F.save() # NOTE: Extension has been specified in pathname
                    self.assertTrue(out.exists(),
                                    f"{out} should have been written.")
                    if ext != 'svg':
                        self.assertFalse(out.with_suffix('.svg').exists(),
                                         f"SVG version should not have been saved next to {out}")

                    out2 = Path(tmpdirname) / 'another_file'
                    F.pathname(out2)  # NOTE: Without extension
                    out2 = out2.with_suffix('.' + ext)
                    self.assertFalse(out2.exists(),
                                     f"{out2} should not have been created yet")
                    F.save(extension=ext)
                    self.assertTrue(out2.exists(),
                                    f"{out2} should have been written.")
                    self.assertTrue(out2.stat().st_size > 1_000,
                                    f"{out2} should not be empty.")


if __name__ == "__main__" :
    unittest.main()