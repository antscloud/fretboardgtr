import os 
import io
import sys
import unittest
from fretboardgtr.fretboardgtr import FretBoardGtr
from fretboardgtr.scalegtr import ScaleGtr, ChordFromName, ScaleFromName
from fretboardgtr.chordgtr import ChordGtr


class FretBoardGtrTest(unittest.TestCase):

    """" Test case for fretboardgtr"""

    def test_createobjectattributs(self):
        F=FretBoardGtr()

        self.assertEqual(F.tuning,['E','A','D','G','B','E'])
        self.assertEqual(F.fingering,[0,3,2,0,1,0])
        self.assertEqual(F._ol,10)
        self.assertEqual(F.gap,3)
        self.assertEqual(F.dic_color,{
            "1":'rgb(231, 0, 0)',
            "b2":'rgb(249, 229, 0)',
            "2":'rgb(249, 165, 0)',
            "b3":'rgb(0, 94, 0)',
            "3":'rgb(0, 108, 0)',
            "4":'rgb(0, 154, 0)',
            "b5":'rgb(0, 15, 65)',
            "5":'rgb(0, 73, 151)',
            "b6":'rgb(168, 107, 98)',
            "6":'rgb(222, 81, 108)',
            "b7":'rgb(120, 37, 134)',
            "7":'rgb(120, 25, 98)'
        })
        self.assertEqual(F.path,"default.svg")
        self.assertEqual(F.attribute_dic,{
        'wf':50, #width of fret
        'hf':70, # height of fret
        'R':20, # radius of circle
        'background_color':'rgb(255,255,255)',
        'fretcolor':'rgb(150,150,150)',
        'strings_color':'rgb(0,0,0)',
        'nut_color':'rgb(0,0,0)',
        'fretsize':3,
        'string_same_size':False,
        'string_size':3,
        'dot_color':'rgb(200,200,200)',
        'dot_color_stroke':'rgb(0,0,0)',
        'dot_width_stroke':2,
        'dot_radius':7,
        'fontsize_bottom_tuning':15,
        'fontsize_text':20,
        'fontsize_fret':20,
        'open_circle_color':'rgb(255,255,255)',
        'open_circle_stroke_color':'rgb(0,0,0)',
        'open_circle_stroke_width':3,
        'open_text_color':'rgb(0,0,0)',
        'cross_color':'rgb(0,0,0)',
        'fretted_circle_color':'rgb(0,0,0)',
        'fretted_circle_stroke_color':'rgb(0,0,0)',
        'fretted_circle_stroke_width':3,
        'fretted_text_color':'rgb(255,255,255)',
        'fontsize_cross':20,
        'nut_height':7,
        'show_nut':True,
        'first_fret':0,
        'last_fret':12,
        'show_tun':True,
        'show_ft':True,
        'color_scale':True,
        'open_color_scale':False,
        'show_note_name':False,
        'show_degree_name':True,
        'color_chord':True,
        'open_color_chord':True
        })
    
    def test_pathname(self):
        F=FretBoardGtr()
        F.pathname("/chords/chordsimage")
        self.assertEqual(str(F.path),"/chords/chordsimage")

    def test_customtuning(self):
        F=FretBoardGtr()
        F.customtuning(['D','A','D','G','A','D'])
        self.assertEqual(F.tuning,['D','A','D','G','A','D'])

    def test_setcolor(self):
        F=FretBoardGtr()
        F.set_color(root='rgb(0, 0, 0)')
        self.assertEqual(F.dic_color,{
            "1":'rgb(0, 0, 0)',
            "b2":'rgb(249, 229, 0)',
            "2":'rgb(249, 165, 0)',
            "b3":'rgb(0, 94, 0)',
            "3":'rgb(0, 108, 0)',
            "4":'rgb(0, 154, 0)',
            "b5":'rgb(0, 15, 65)',
            "5":'rgb(0, 73, 151)',
            "b6":'rgb(168, 107, 98)',
            "6":'rgb(222, 81, 108)',
            "b7":'rgb(120, 37, 134)',
            "7":'rgb(120, 25, 98)'
        })
        
        F=FretBoardGtr()
        F.set_color(perfectfourth='rgb(0, 0, 0)')
        self.assertEqual(F.dic_color,{
            "1":'rgb(231, 0, 0)',
            "b2":'rgb(249, 229, 0)',
            "2":'rgb(249, 165, 0)',
            "b3":'rgb(0, 94, 0)',
            "3":'rgb(0, 108, 0)',
            "4":'rgb(0, 0, 0)',
            "b5":'rgb(0, 15, 65)',
            "5":'rgb(0, 73, 151)',
            "b6":'rgb(168, 107, 98)',
            "6":'rgb(222, 81, 108)',
            "b7":'rgb(120, 37, 134)',
            "7":'rgb(120, 25, 98)'
        })


        F=FretBoardGtr()
        F.set_color(perfectfourth='rgb(0, 0, 0)',root='rgb(0, 0, 0)')

        self.assertEqual(F.dic_color,{
            "1":'rgb(0, 0, 0)',
            "b2":'rgb(249, 229, 0)',
            "2":'rgb(249, 165, 0)',
            "b3":'rgb(0, 94, 0)',
            "3":'rgb(0, 108, 0)',
            "4":'rgb(0, 0, 0)',
            "b5":'rgb(0, 15, 65)',
            "5":'rgb(0, 73, 151)',
            "b6":'rgb(168, 107, 98)',
            "6":'rgb(222, 81, 108)',
            "b7":'rgb(120, 37, 134)',
            "7":'rgb(120, 25, 98)'
        })

        F=FretBoardGtr()
        F.set_color(perfectfourth='rgb(0, 0, 0)',root='rgb(0, 0, 0)', default_theme=True)
        self.assertEqual(F.dic_color,{
            "1":'rgb(231, 0, 0)',
            "b2":'rgb(249, 229, 0)',
            "2":'rgb(249, 165, 0)',
            "b3":'rgb(0, 94, 0)',
            "3":'rgb(0, 108, 0)',
            "4":'rgb(0, 154, 0)',
            "b5":'rgb(0, 15, 65)',
            "5":'rgb(0, 73, 151)',
            "b6":'rgb(168, 107, 98)',
            "6":'rgb(222, 81, 108)',
            "b7":'rgb(120, 37, 134)',
            "7":'rgb(120, 25, 98)'
        })

        F=FretBoardGtr()
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        F.set_color(perfectourth='rgb(0, 0, 0)',root='rgb(0, 0, 0)')  # Call unchanged function.
        sys.stdout = sys.__stdout__   # Reset redirect.
        self.assertEqual('perfectourth is not a valid attribute. It is not taken into accounts.',str(capturedOutput.getvalue()).split('\n')[0])

        F=FretBoardGtr()
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        F.set_color(perfectfourth=2,root='rgb(0, 0, 0)')  # Call unchanged function.
        sys.stdout = sys.__stdout__   # Reset redirect.
        self.assertEqual('2 (int) is not a good format for perfectfourth attribute, use str instead. Modifications are not taken into accounts.',str(capturedOutput.getvalue()).split('\n')[0])


    def test_createobjectattributs(self):
        dic={
        'wf':50, #width of fret
        'hf':70, # height of fret
        'R':20, # radius of circle
        'background_color':'rgb(255,255,255)',
        'fretcolor':'rgb(150,150,150)',
        'strings_color':'rgb(0,0,0)',
        'nut_color':'rgb(0,0,0)',
        'fretsize':3,
        'string_same_size':False,
        'string_size':3,
        'dot_color':'rgb(200,200,200)',
        'dot_color_stroke':'rgb(0,0,0)',
        'dot_width_stroke':2,
        'dot_radius':7,
        'fontsize_bottom_tuning':15,
        'fontsize_text':20,
        'fontsize_fret':20,
        'open_circle_color':'rgb(255,255,255)',
        'open_circle_stroke_color':'rgb(0,0,0)',
        'open_circle_stroke_width':3,
        'open_text_color':'rgb(0,0,0)',
        'cross_color':'rgb(0,0,0)',
        'fretted_circle_color':'rgb(0,0,0)',
        'fretted_circle_stroke_color':'rgb(0,0,0)',
        'fretted_circle_stroke_width':3,
        'fretted_text_color':'rgb(255,255,255)',
        'fontsize_cross':20,
        'nut_height':7,
        'show_nut':True,
        'first_fret':0,
        'last_fret':12,
        'show_tun':True,
        'show_ft':True,
        'color_scale':True,
        'open_color_scale':False,
        'show_note_name':False,
        'show_degree_name':True,
        'color_chord':True,
        'open_color_chord':True
        }

        F=FretBoardGtr()
        F.theme(string_size=2)
        self.assertEqual(F.string_size,2)

        F=FretBoardGtr()
        F.theme(open_color_scale=True)
        self.assertEqual(F.open_color_scale,True)


        F=FretBoardGtr()
        F.theme(open_color_scale=True,string_size=2)
        self.assertEqual(F.open_color_scale,True)
        self.assertEqual(F.string_size,2)

        F=FretBoardGtr()
        F.theme(open_color_scale=True,string_size=3,default_theme=True)
        self.assertEqual(F.open_color_scale,False)

        F=FretBoardGtr()
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        F.theme(open_coolor_scale=True,string_size=3)
        sys.stdout = sys.__stdout__   # Reset redirect.
        self.assertEqual('open_coolor_scale is not a valid attribute. It is not taken into accounts.',str(capturedOutput.getvalue()).split('\n')[0])

        F=FretBoardGtr()
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        F.theme(open_color_scale=2,string_size=3) # Call unchanged function.
        sys.stdout = sys.__stdout__   # Reset redirect.
        self.assertEqual('2 (int) is not a good format for open_color_scale attribute, use bool instead.  Modifications are not taken into accounts.',str(capturedOutput.getvalue()).split('\n')[0])


    def test_notes_names_from_fingering(self):
        F=FretBoardGtr()
        notes=F.notesname()
        self.assertEqual(notes,['E','C','E','G','C','E'])

        F=FretBoardGtr()
        F.fingering=[0,3,2,0,None,0]
        notes=F.notesname()
        self.assertEqual(notes,['E','C','E','G',None,'E'])

        F=FretBoardGtr()
        F.customtuning(["A","B",'D','E'])
        F.fingering=[0,3,2,0,None,0]
        notes=F.notesname()
        self.assertEqual(notes,['A','D','E','E'])

        F=FretBoardGtr()
        F.customtuning(["A","B",'D','E','B','G','D'])
        F.fingering=[0,3,2,0,None,0]
        with self.assertRaises(IndexError):
            notes=F.notesname()

    def test_setenharmonic(self):
        F=FretBoardGtr()
        
        self.assertEqual(FretBoardGtr.setenharmonic( ['A#', 'C', 'D', 'D#', 'F', 'G', 'A'] ) , ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'])
        self.assertEqual(FretBoardGtr.setenharmonic(["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]),['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])
        self.assertEqual(FretBoardGtr.setenharmonic(['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'F']),['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F'])

    def test_minmax(self):
        F=FretBoardGtr()
        F.fingering=[0,3,2,0,None,0]
        tupleminmax=F.minmax()
        self.assertEqual(tupleminmax,(2,3))

        F.fingering=[0,18,1,0,None,0]
        tupleminmax=F.minmax()
        self.assertEqual(tupleminmax,(1,18))

        F.fingering=[0,0,0,0,None,None]
        tupleminmax=F.minmax()
        self.assertEqual(tupleminmax,(0,0))

    def test_dist(self):
        F=FretBoardGtr()
        F.fingering=[0,3,2,0,None,0]
        distance=F.dist()
        self.assertEqual(distance,3)

        F=FretBoardGtr()
        F.fingering=[0,3,5,0,None,0]
        distance=F.dist()
        self.assertEqual(distance,3)

        F=FretBoardGtr()
        F.fingering=[0,3,8,0,None,0]
        distance=F.dist()
        self.assertEqual(distance,5)

    def test_find_intervals(self):
        intervals=FretBoardGtr.find_intervals(scale=['C','E','G'],root='C')
        self.assertEqual(intervals,['1','3','5'])

        intervals=FretBoardGtr.find_intervals(scale=['D','E','G','B'],root='D#')
        self.assertEqual(intervals,['7', 'b2', '3', 'b6'])

        intervals=FretBoardGtr.find_intervals(scale=[],root='D#')
        self.assertEqual(intervals,[])

        intervals=FretBoardGtr.find_intervals()
        self.assertEqual(intervals,['1','3','5'])


    def test_where_dot(self):
        F=FretBoardGtr()
        F.fingering=[0,18,2,0,1,0]
        tupledot=F.wheredot()
        self.assertEqual(tupledot,([2, 4, 6, 8, 11, 14, 16], [1, 1, 1, 1, 2, 1, 1]))

        F=FretBoardGtr()
        F.fingering=[0,0,0,0,0,0]
        tupledot=F.wheredot()
        self.assertEqual(tupledot,([3], [1]))

if __name__ == "__main__" :
    unittest.main()