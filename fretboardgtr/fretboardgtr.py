import svgwrite

class FretBoardGtr():


    def __init__(self):
        self.tuning=['E','A','D','G','B','E'] # Default tuning
        self.fingering=[0,3,2,0,1,0]
        self._ol=10 # overlay
        self.square_size=500 # not important here because redefined

        self.gap=3 # minimum distance between max fret and min fret
        self.path="default.svg"

        self.dic_color={
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
        }

        self.attribute_dic={
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

        for i in self.attribute_dic.keys():
            setattr(self,i, self.attribute_dic[i])

    def pathname(self,path):
        """
        Take a parameter to set the path to save.
        >>> FretBoardGtr.pathname("test.svg")
        """
        self.path=path

    def layout(self):
        square_x=self.hf*(len(self.tuning)+2)
        pass

    def customtuning(self,tuning):
        '''
        Create a custom tuning

        >>> FretBoardGtr.customtuning(['D','A','D','G','A','D'])
        '''
        self.tuning=tuning

    def set_color(self,default_theme=False,**kwargs):
        '''
        Example :
        >>> FretboardGtr.set_color(root=rgb(0, 0, 0)')
        >>> FretboardGtr.set_color(default_theme=True)

        List of parameters : root, minorsecond, majorsecond, minorthird, majorthird,
                             perfectfourth, diminishedfifth, perfectfifth, minorsixth,
                             majorsixth,minorseventh,majorseventh
        '''

        dic_name={
        'root':"1",
        'minorsecond':'b2',
        'majorsecond':'2',
        'minorthird':'b3',
        'majorthird':"3",
        'perfectfourth':"4",
        'diminishedfifth':"b5",
        'perfectfifth':'5',
        'minorsixth':'b6',
        'majorsixth':"6",
        'minorseventh':"b7",
        'majorseventh':'7'
        }
        if default_theme:
            self.dic_color={
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
            }
        else:

            for keys in kwargs:
                    if keys in dic_name.keys():
                        self.dic_color[dic_name[keys]]=kwargs[keys]
                    else:
                        print(keys,'is not a valid attribute.')

    def theme(self,default_theme=False,**kwargs):
        '''
        Set new attributes to the fretboard
                wf = 50 (width of fret)
                hf = 70 (height of fret)
                R = 20  (radius of circle )
                background_color = 'rgb(255,255,255)'
                fretcolor = 'rgb(150,150,150)'
                strings_color = 'rgb(0,0,0)'
                nut_color = 'rgb(0,0,0)'
                fretsize = 3
                string_same_size = False (If False first string bigger than the last)
                string_size = 3
                dot_color = 'rgb(200,200,200)'
                dot_color_stroke = 'rgb(0,0,0)' (small dots on the neck)
                dot_width_stroke = 2 (small dots on the neck)
                dot_radius = 7 (small dots on the neck)
                fontsize_bottom_tuning = 15 (fontsize of the tuning)
                fontsize_text = 20 (Fontsize of text in circle)
                open_circle_color = 'rgb(255,255,255)' (for open string)
                open_circle_stroke_color = 'rgb(0,0,0)' (for open string)
                open_circle_stroke_width = 3 (for open string)
                open_text_color = 'rgb(0,0,0)' (for open string)
                cross_color = 'rgb(0,0,0)' (Cross when doesn't play string )
                fontsize_cross = 20 (Cross when doesn't play string )
                fretted_circle_color = 'rgb(0,0,0)' (for fretted string)
                fretted_circle_stroke_color = 'rgb(0,0,0)' (for fretted string)
                fretted_circle_stroke_width = 3 (for fretted string)
                fretted_text_color = 'rgb(255,255,255)' (for fretted string)
                nut_height = 7
                show_nut = True
                first_fret = 0
                last_fret = 12
                show_tun = True
                show_ft = True
                color_scale = True (for the Scale class)
                show_note_name = False (if show_not_name==True, show_degree_name is not considered )
                show_degree_name = True
                color_chord=True (for the ChordGtr class)
                open_color_chord=True (for the ChordGtr class)
            '''
        if default_theme:
            for i in self.attribute_dic.keys():
                setattr(self,i, self.attribute_dic[i])
        else:
            for keys in kwargs:
                if keys in self.attribute_dic.keys():
                    setattr(self,keys,kwargs[keys])
                else:
                    print(keys,'is not a valid attribute.')


    def notesname(self):
        '''
        Give name of note on fret depends on tunings
        >>>FretBoardGtr.notesname(fingering=[0,3,2,0,None,0])
        ['E','C','E','G',None,'E']
        '''

        notes=[0]*len(self.tuning)
        chroma=["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        alter={
            "Bb":"A#",
            "Cb":"B",
            "B#":"C",
            "Db":"C#",
            "Eb":"D#",
            "Fb":"E",
            "Gb":"F#",
            "Ab":"G#"
        }

        for i in range(0,len(self.tuning)):
            if self.fingering[i] == None:
                notes[i]=None
            else:
                ind=chroma.index(self.tuning[i])
                notes[i]=chroma[(ind+self.fingering[i])%12]

        return notes


    def minmax(self):
        '''
        Return the min and the max of fingering without None and 0.
        FretBoardGtr.minmax(fingering=[0,3,2,0,None,0])
        (2,3)
        '''
        fretfing=[0 if v == None else v for v in self.fingering]
        return min(v for v in fretfing if v > 0),max(fretfing)

    def dist(self):
        '''
        return the gap between the max fret and the min fret
        >>> FretBoardGtr.dist(fingering=[0,3,2,0,None,0])
        1
        '''
        mini,maxi = self.minmax()
        self.gap=maxi-mini
        if self.gap <=3:
            self.gap=3
        return self.gap

    @staticmethod
    def find_intervals(scale=['C','E','G'],root='C'):
        '''
        >>> find_intervals(scale=['C','E','G'],root='C')
        [1,3,5]
        '''
        chroma=["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        intervals=["1","b2","2","b3","3","4","b5","5","b6","6","b7","7"]
        intervals_dic={
                "1":"root",
                "b2":"minor second",
                "2":"major second",
                "b3":"minor third",
                "3":"major third",
                "4":"perfect fourth",
                "b5":"diminished fifth",
                "5":"perfect fifth",
                "b6":"minor sixth",
                "6":"major sixth",
                "b7":"minor seventh",
                "7":"major seventh"

            }
        notes_string=[0]*len(chroma)
        for j in range(len(chroma)):
            #start from the root and place the other notes
            notes_string[j]=chroma[(chroma.index(root)+j)%12]
        inter=[0]*len(scale)
        for i in range(len(scale)):
            if scale[i]==None:
                inter[i]==None
            else:
                inter[i]=intervals[notes_string.index(scale[i])]
        return inter



    def wheredot(self,minfret):

        ''' Find where the dot on the fretboard are depends on the minimum fret
        If the first finger is on the 2rd fret (for example a B) and there is nothing beside the function return the folowwings lists:
        dot=[1,3]
        nbdot=[1,1]
        That leads to put a dot on the second fret and the fourth fret corresponding to the third and a fifth on the guitar.
        '''

        dot_fret=[0,3,5,7,9,12]
        nbdot_fret=[2,1,1,1,1,2]

        dot=[]
        nbdot=[]

        if self.gap>=12:

            for i in range(1,(self.gap//12)*len(dot_fret)):
                dot_fret.append(dot_fret[i]+12)
                nbdot_fret.append(nbdot_fret[i])

        for i in range(len(dot_fret)):
                    if dot_fret[i]>=(minfret)%12 and dot_fret[i]<minfret%12+self.gap+1:
                        dot.append(dot_fret[i]-minfret%12)
                        nbdot.append(nbdot_fret[i])

        if minfret==0:
            dot.pop(0)
            nbdot.pop(0)

        return dot, nbdot

    def save(self):
        self.dwg.save()
