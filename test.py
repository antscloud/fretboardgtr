from fretboardgtr import ScaleGtr, ChordGtr,ScaleFromName,ChordFromName

F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
F.customtuning(['E','A','D','G','B','E'])
F.pathname('img/scale_degree_name.svg')
F.draw()
F.save()


F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
F.customtuning(['E','A','D','G','B','E'])
F.theme(show_note_name=True,color_scale=False)
F.pathname('img/scale_note_name.svg')
F.draw()
F.save()

F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
F.customtuning(['E','A','D','G','B','E'])
F.theme(show_note_name=True)
F.pathname('img/scale_no_color.svg')
F.draw()
F.save()

F=ScaleGtr(ScaleFromName(root='F#',mode='Ionian'))
F.customtuning(['E','A','D','G','B','E'])
F.pathname('img/TestScaleName.svg')
F.theme(show_note_name=True)
F.draw()
F.save()

F=ScaleGtr(scale=['D#','F','G','G#','A#','C','D'], root='D#',enharmonic=True)
F.customtuning(['D','A','D','G','B','E'])
F.pathname('img/TestScaleNameEnhar.svg')
F.theme(show_note_name=True)
F.draw()
F.save()


F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
F.customtuning(['E','A','D','G','B','E'])
F.pathname('img/chord_degree_name.svg')
F.draw()
F.save()

F=ScaleGtr(ChordFromName(root='C',quality='M'))
F.customtuning(['D','A','D','G','A','D'])
F.pathname('img/TestChordName.svg')
F.draw()
F.save()

F=ChordGtr(fingering=[3,3,2,0,1,0],root="C",lefthand=True)
F.customtuning(['F','A','D','G','B','E'])
F.pathname('img/lefthandchord.svg')
F.draw()
F.save()

F=ChordGtr(fingering=[0,3,2,0,1,0],root="C")
F.customtuning(['F','A','D','G','B','E'])
F.pathname('img/chord_name_background.svg')
F.theme(show_note_name=True,background_color='rgb(70,70,70)')
F.draw()
F.save()