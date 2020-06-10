from fretboardgtr import ScaleGtr, ChordGtr,ScaleFromName,ChordFromName

F=ScaleGtr(scale=["G","A","B","C","D","E","F#"],root="G")
F.customtuning(['F','A','D','G','B','E'])
F.pathname('Scale.svg')
F.draw()
F.save()

F=ScaleGtr(ScaleFromName(root='C',mode='Dorian'))
F.customtuning(['F','A','D','G','B','E'])
F.pathname('TestScaleName.svg')
F.draw()
F.save()

F=ScaleGtr(ChordFromName(root='C',quality='M'))
F.customtuning(['F','A','D','G','B','E'])
F.pathname('TestChordName.svg')
F.draw()
F.save()

F=ChordGtr(fingering=[18,3,2,0,1,0],root="C",lefthand=True)
F.customtuning(['F','A','D','G','B','E'])
F.pathname('Chord.svg')
F.draw()
F.save('pdf')