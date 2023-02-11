from __future__ import absolute_import
from fretboardgtr.fretboardgtr import FretBoardGtr #First name : main folder, second name .py file and last : class name
from fretboardgtr.constants import SCALES_DICT,CHORDS_DICT_ESSENTIAL
import svgwrite

class ScaleFromName:
    """
    Object that generate a results dictionary containing the root and
    the scale as argument from root and mode strings.

    >>> ScaleFromName(root='C',mode='Dorian').results
        {'root': 'C', 'scale': ['C', 'D', 'D#', 'F', 'G', 'A', 'A#']}

    Mode enum can also be used:

    >>> ScaleFromName(root='C',mode=Mode.DORIAN).results
        {'root': 'C', 'scale': ['C', 'D', 'D#', 'F', 'G', 'A', 'A#']}
    """
    
    def __init__(self,root='C',mode='Ionian'):
        self.root=root
        self.mode=mode
        self.findscale()

    def findscale(self):
        chroma=["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        index=chroma.index(self.root)
        modearray=SCALES_DICT[self.mode]
        scale=[0]*len(modearray)
        for i in range(len(modearray)):
            scale[i]=chroma[(index+modearray[i])%12]
        self.results={'root':self.root,'scale':scale}

class ChordFromName:
    """
    Object that generate a results dictionnary containing the root and the scale as argument from root and quality of chords strings.
    >>> ChordFromName(root='C',quality='M').results
        {'root': 'C', 'scale': ['C', 'E', 'G']}
    """
    
    def __init__(self,root='C',quality='M'):
        self.root=root
        self.quality=quality
        self.findscale()

    def findscale(self):
        chroma=["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        index=chroma.index(self.root)

        qualityarray=CHORDS_DICT_ESSENTIAL[self.quality]
        scale=[0]*len(qualityarray)
        for i in range(len(qualityarray)):
            scale[i]=chroma[(index+qualityarray[i])%12]
        self.results={'root':self.root,'scale':scale}


class ScaleGtr(FretBoardGtr):
    def __init__(self,*args,scale=['C','E','G'],root='C', enharmonic=False):
        FretBoardGtr.__init__(self)
        self.enharmonic=enharmonic
        try:
            if isinstance(args[0],ScaleFromName) or isinstance(args[0], ChordFromName):
                self.scale=args[0].results['scale']
                self.root=args[0].results['root']
        except:
            self.scale=scale
            self.root=root

        if enharmonic: 
            self.enharmonic_scale = FretBoardGtr.setenharmonic(self.scale)


    def emptybox(self):
        '''
        Create empty box and the object self.dwg
        '''

        self.dwg = svgwrite.Drawing(
        self.path,
        size=(self.hf*(self.last_fret-self.first_fret+2),self.wf*(len(self.tuning)+2)),
        profile='tiny'
        )

    def background_fill(self):
        '''
        Fill background with a color
        '''
        self.dwg.add(
            self.dwg.rect(
                insert=(self.wf+ self._ol, self.hf +self._ol),
                size=((len(self.tuning)-1)*self.wf, (len(self.tuning)-2)*self.hf), #-2 evite case du bas du tuning
                rx=None, ry=None,
                fill=self.background_color
            )
        )

    def background_fill_image(self):
        '''
        Fill background with an image
        '''
        self.dwg.add(
            self.dwg.image("wood1.jfif",
                x=self.wf+ self._ol,
                y=self.hf +self._ol,
                width=(len(self.tuning)-1)*self.wf,
                height=(len(self.tuning)-2)*self.hf, #-2 evite case du bas du tuning
                preserveAspectRatio="none",
                opacity=0.90
                )
                )

    def add_dot(self):
        '''
        Add dot up to 24 frets.
        Recalculate if the minimum fret isn't 0 or maximum fret isn't 12.
        '''

        dot=[3,5,7,9,12,15,17,19,21,24]
        dot=[dot[v] for v in range(len(dot)) if dot[v]<=self.last_fret and dot[v]>=self.first_fret]
        for i in range(len(dot)):
            if dot[i]%12==0:
                self.dwg.add(
                    self.dwg.circle(
                        ((0.5+dot[i]-self.first_fret)*self.hf+self._ol,(len(self.tuning)/2 - 1/2)*self.wf +self._ol),
                        r=self.dot_radius,
                        fill=self.dot_color,
                        stroke=self.dot_color_stroke,
                        stroke_width=self.dot_width_stroke
                    )
                )

                self.dwg.add(
                    self.dwg.circle(
                        ((0.5+dot[i]-self.first_fret)*self.hf+self._ol,(len(self.tuning)/2 + 3/2)*self.wf +self._ol),
                        r=self.dot_radius,
                        fill=self.dot_color,
                        stroke=self.dot_color_stroke,
                        stroke_width=self.dot_width_stroke
                    )
                )

            else:
                self.dwg.add(
                    self.dwg.circle(
                        ((0.5+dot[i]-self.first_fret)*self.hf+self._ol,(len(self.tuning)/2+1/2)*self.wf +self._ol),
                        r=self.dot_radius,
                        fill=self.dot_color,
                        stroke=self.dot_color_stroke,
                        stroke_width=self.dot_width_stroke))




    def createfretboard(self):
        '''
        Create an sets of lines based on tunings and the number of fret.
        '''
        string_size_list=[((self.string_size)-i/4) for i in range(len(self.tuning))]
        string_size_list=list(reversed(string_size_list))
        g=0

        if self.first_fret!=0:
            self.show_nut=False

        if self.show_nut:
            g=1
        #begin before if min fret !=0 because no open chords
        if self.first_fret!=0:
            it=0
            nb=2
        else:
            it=1
            nb=1
        for i in range(g,(self.last_fret-self.first_fret)+nb):
            self.dwg.add(
                self.dwg.line(
                    start=((self.hf)*(i+it)+self._ol,self.wf +self._ol),
                    end=((self.hf)*(i+it)+self._ol,(self.wf)*(len(self.tuning))+self._ol),
                    stroke=self.fretcolor,
                    stroke_width=self.fretsize
                )
            )

        #strings
        if self.string_same_size:
            string_size_list=[((self.string_size)) for i in range(len(self.tuning))]
        #begin before if min fret !=0 because no open chords
        if self.first_fret!=0:
            xstart=self._ol-self.fretsize/2
            xend=self._ol + ((self.last_fret-self.first_fret+1))*self.hf +self.fretsize/2
        else:
            xstart=self.hf+self._ol-self.fretsize/2
            xend=self.hf+self._ol + (self.last_fret-self.first_fret)*self.hf +self.fretsize/2

        for i in range(len(self.tuning)):

            self.dwg.add(
                self.dwg.line(
                    start=(xstart,(self.wf)*(1+i)+self._ol),
                    end=(xend,(self.wf)*(1+i)+self._ol),
                    stroke=self.strings_color,
                    stroke_width=string_size_list[i]
                )
            )

    def nut(self):
        '''
        Create nut if minimum fret == 0.

        '''
        if self.first_fret!=0:
            self.show_nut=False
        if self.show_nut:
            if self.string_same_size==False:
                self.dwg.add(
                    self.dwg.line(
                    start=((self.hf)*(1)+self._ol,self.wf +self._ol-((self.string_size)-len(self.tuning)/4)/2),
                    end=((self.hf)*(1)+self._ol,(self.wf)*(len(self.tuning))+self._ol +((self.string_size))/2 ),
                    stroke=self.nut_color,
                    stroke_width=self.nut_height
                )
            )
            else:
                self.dwg.add(
                    self.dwg.line(
                    start=((self.hf)*(1)+self._ol,self.wf +self._ol-((self.string_size))/2),
                    end=((self.hf)*(1)+self._ol,(self.wf)*(len(self.tuning))+self._ol +((self.string_size))/2 ),
                    stroke=self.nut_color,
                    stroke_width=self.nut_height
                )
            )
    def show_fret(self):
        '''
        Show text under the frets for example 3ft.
        '''
        dot=[3,5,7,9,12,15,17,19,21,24]
        dot=[dot[v] for v in range(len(dot)) if dot[v]<=self.last_fret and dot[v]>=self.first_fret]
        #self.first_fret=0
        #self.last_fret=12
        if self.show_ft:
            for j,v in enumerate(dot):
                Y=self.wf*(1+len(self.tuning))
                X=self.hf*(1/2+v-self.first_fret)+self._ol
                t=svgwrite.text.Text(str(v), insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_fret,font_weight="bold",style="text-anchor:middle")
                self.dwg.add(t)

    def show_tuning(self):
        '''
        Show  tuning at the end of the neck.
        '''

        if self.show_tun:
            reverse_tun=list(reversed(self.tuning))
            for i in range(len(self.tuning)):
                Y=self.wf*(1+i)+self._ol
                X=self.hf*(self.last_fret-self.first_fret+3/2)+self._ol

                t=svgwrite.text.Text(reverse_tun[i], insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_bottom_tuning,font_weight="normal",style="text-anchor:middle")
                self.dwg.add(t)


    def fill_with_chords(self):

        chroma=["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        intervals=["1","b2","2","b3","3","4","b5","5","b6","6","b7","7"]



        self.dist()

        fingname=self.notesname()
        fingname=list(reversed(fingname))
        fretfing=[0 if v == None else v for v in self.fingering]
        minfret = min(v for v in fretfing if v > 0)

        if max(fretfing)>12:
            return None

        fingering=[v if v==None else v-minfret+1 if v!=0 else v for v in self.fingering ]
        fingering=list(reversed(fingering))

        for i in range(0,len(self.tuning),1):

            if fingering[i]== None:
                Y=self.wf*(1+i)+self._ol
                X=self.hf*(1/2)+self._ol

                t=svgwrite.text.Text('X', insert=(X,Y),dy=["0.3em"], font_size=self.fontsize_cross,font_weight="bold",fill=self.cross_color,style="text-anchor:middle")
                self.dwg.add(t)
                #dwg.add(dwg.image("cross.svg",x=(i+1-0.3)*self.wf +self._ol,y=self.hf*(1/4-0.2)+self._ol,width=2*self.R))

            else:

                Y=self.wf*(1+i)+self._ol
                X=self.hf*(fingering[i]+1/2)+self._ol

                if fingering[i]==0:

                    self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=self.open_circle_color,stroke=self.open_circle_stroke_color,stroke_width=self.open_circle_stroke_width))
                    t=svgwrite.text.Text(fingname[i], insert=(X,Y),dy=["0.3em"], font_size=self.fontsize_text,font_weight="bold",fill=self.open_text_color,style="text-anchor:middle")
                    self.dwg.add(t)

                else:

                    self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=self.fretted_circle_color,stroke=self.fretted_circle_stroke_color,stroke_width=self.fretted_circle_stroke_width))
                    t=svgwrite.text.Text(fingname[i], insert=(X,Y),dy=["0.3em"], font_size=self.fontsize_text,fill=self.fretted_text_color,font_weight="bold",style="text-anchor:middle")
                    self.dwg.add(t)




        return self.dwg


    def fill_with_scale(self):
        '''
        Fill the neck with scale like ["C","D","E","F","G","A","B"]
        automatically calculate position and name depends on tunings and number of fret.
        '''
        chroma=["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        intervals=["1","b2","2","b3","3","4","b5","5","b6","6","b7","7"]
        notes_from_root=[0]*len(chroma)

        alter={
        "Bb":"A#",
        "Cb":"B",
        "B#":"C",
        "C":"B#",
        "Db":"C#",
        "Eb":"D#",
        "Fb":"E",
        "Gb":"F#",
        "Ab":"G#"
        }

        #inverse dictionnary
        altersharp={}
        for key, values in alter.items():
            altersharp[values]=key

        if self.first_fret!=0:
            nb=1
        else:
            nb=1
        for j in range(len(chroma)):
            #start from the root and place the other notes
            notes_from_root[j]=chroma[(chroma.index(self.root)+j)%12]

        color=self.fretted_circle_color
        color_stroke=self.open_circle_stroke_color


        for l in range(3):
            m=0

            for i in reversed(range(len(self.tuning))):

                nt=self.tuning[i]
                notes_string=[0]*12

                for j in range(12):#13 beacause add the 12th fret

                    if (12*l+j)>(self.last_fret):
                        break

                    notes_string[j]=chroma[(chroma.index(nt)+j)%12]
                for k in range(len(self.scale)):

                    try:
                        index=notes_string.index(self.scale[k])
                    except:
                        continue  #Continue return to the beginning of the loop without executing the code after (contrarly to pass)

                    Y=self.wf*(1+m)+self._ol
                    X=self.hf*(12*l+index+1/2-self.first_fret)+self._ol

                    if self.show_note_name:
                        if (index+l)==0:
                            if self.open_color_scale:
                                inter=FretBoardGtr.find_intervals(self.scale,self.root)
                                color_stroke=self.dic_color[inter[k]]
                            if self.enharmonic:
                                if notes_string[index] in list(alter.values()):
                                    if altersharp[notes_string[index]] in self.enharmonic_scale:
                                        notes_string[index] = self.enharmonic_scale[self.enharmonic_scale.index(altersharp[notes_string[index]])]



                            self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=self.open_circle_color,stroke=color_stroke,stroke_width=self.open_circle_stroke_width))
                            t=svgwrite.text.Text(notes_string[index], insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_text,font_weight="bold",fill=self.open_text_color,style="text-anchor:middle")
                            self.dwg.add(t)

                        else:
                            if self.color_scale:
                                inter=FretBoardGtr.find_intervals(self.scale,self.root)
                                color=self.dic_color[inter[k]]
                                
                            if self.enharmonic: 
                                if notes_string[index] in list(alter.values()):
                                    if altersharp[notes_string[index]] in self.enharmonic_scale:
                                        notes_string[index] = self.enharmonic_scale[self.enharmonic_scale.index(altersharp[notes_string[index]])]

                            self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=color,stroke=self.fretted_circle_stroke_color,stroke_width=self.fretted_circle_stroke_width))
                            t=svgwrite.text.Text(notes_string[index], insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_text,font_weight="bold",fill=self.fretted_text_color,style="text-anchor:middle")
                            self.dwg.add(t)

                    elif self.show_degree_name:

                        if (index+l)==0:
                            if self.open_color_scale:
                                inter=FretBoardGtr.find_intervals(self.scale,self.root)
                                color_stroke=self.dic_color[inter[k]]
                            self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=self.open_circle_color,stroke=color_stroke,stroke_width=self.open_circle_stroke_width))
                            t=svgwrite.text.Text(intervals[notes_from_root.index(notes_string[index])], insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_text,font_weight="bold",fill=self.open_text_color,style="text-anchor:middle")
                            self.dwg.add(t)

                        else:
                            if self.color_scale:
                                inter=FretBoardGtr.find_intervals(self.scale,self.root)
                                color=self.dic_color[inter[k]]

                            self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=color,stroke=self.fretted_circle_stroke_color,stroke_width=self.fretted_circle_stroke_width))
                            t=svgwrite.text.Text(intervals[notes_from_root.index(notes_string[index])], insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_text,font_weight="bold",fill=self.fretted_text_color,style="text-anchor:middle")
                            self.dwg.add(t)
                    else:

                        if (index+l)==0:
                            if self.open_color_scale:
                                inter=FretBoardGtr.find_intervals(self.scale,self.root)
                                color_stroke=self.dic_color[inter[k]]

                            self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=self.open_circle_color,stroke=color_stroke,stroke_width=self.open_circle_stroke_width))

                        else:
                            if self.color_scale:
                                inter=FretBoardGtr.find_intervals(self.scale,self.root)
                                color=self.dic_color[inter[k]]

                            self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=color,stroke=self.fretted_circle_stroke_color,stroke_width=self.fretted_circle_stroke_width))

                m+=1

        return self.dwg



    def draw(self,fingering=[]):
        """
        Execute in particular order each important methods to create the board
        """
        self.emptybox()
        self.nut()
        #self.background_fill()
        #self.background_fill_image()
        self.add_dot()
        self.createfretboard()
        self.show_fret()
        self.show_tuning()
        if len(fingering)==0:
            self.fill_with_scale()
        else:
            self.fingering=fingering
            self.fill_with_chords()

if __name__=='__main__':
    F=ScaleGtr()
    F.theme(default_theme=True)
    F.customtuning(['F','A','D','G','B','E'])
    F.set_color(root='red')
    F.draw()
    F.save()
