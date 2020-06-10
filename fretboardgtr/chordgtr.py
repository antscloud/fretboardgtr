from fretboardgtr.fretboardgtr import FretBoardGtr #First name : main folder, second name .py file and last : class name
import svgwrite

class ChordGtr(FretBoardGtr):

    def __init__(self,fingering=[0,3,2,0,1,0],root='C',lefthand=False):
        FretBoardGtr.__init__(self)
        self.fingering=fingering
        self.root=root
        self.lefthand=lefthand


    def fingering(self,fingering):
        self.fingering=fingering

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


    def emptybox(self):

            self.dwg = svgwrite.Drawing(
            self.path,
            size=(self.wf*(len(self.tuning)+2),self.hf*6+self.hf*(self.gap-3)),
            profile='tiny'
        )

    def background_fill(self):
        self.dwg.add(
            self.dwg.rect(
                insert=(self.wf+ self._ol, self.hf +self._ol),
                size=((len(self.tuning)-1)*self.wf, (len(self.tuning)-2)*self.hf), #-2 evite case du bas du tuning
                rx=None, ry=None,
                fill=self.background_color
            )
        )

    def background_fill_image(self):
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

        fretfing=[0 if v == None else v for v in self.fingering]
        minfret = min(v for v in fretfing if v > 0)


        dot,nbdot = self.wheredot(minfret)
        if max(fretfing)>4:
            for i in range(len(dot)):
                if nbdot[i]==1:
                    self.dwg.add(self.dwg.circle(((len(self.tuning)/2+1/2)*self.wf +self._ol,(1.5+dot[i])*self.hf+self._ol),r=self.dot_radius,fill=self.dot_color,stroke=self.dot_color_stroke,stroke_width=self.dot_width_stroke))
                if nbdot[i]==2:
                    self.dwg.add(self.dwg.circle(((len(self.tuning)/2 - 1/2)*self.wf +self._ol,(1.5+dot[i])*self.hf+self._ol),r=self.dot_radius,fill=self.dot_color,stroke=self.dot_color_stroke,stroke_width=self.dot_width_stroke))
                    self.dwg.add(self.dwg.circle(((len(self.tuning)/2 +1.5)*self.wf +self._ol,(1.5+dot[i])*self.hf+self._ol),r=self.dot_radius,fill=self.dot_color,stroke=self.dot_color_stroke,stroke_width=self.dot_width_stroke))
        else:
                    self.dwg.add(self.dwg.circle(((len(self.tuning)/2+1/2)*self.wf +self._ol,(3.5)*self.hf+self._ol),r=self.dot_radius,fill=self.dot_color,stroke=self.dot_color_stroke,stroke_width=self.dot_width_stroke))





    def createfretboard(self):
        '''
        Create an empty set of rectangles based on tunings.
        '''
        fretfing=[0 if v == None else v for v in self.fingering]

        #Creation of fret
        if max(fretfing)>4:
            for i in range(self.gap+2):
                #self.gap +2 : two is for the beginning and the end of the fretboard
                self.dwg.add(
                    self.dwg.line(
                        start=(self.wf +self._ol, (self.hf)*(i+1)+self._ol),
                        end=((self.wf)*(len(self.tuning))+self._ol,(self.hf)*(1+i)+self._ol),
                        stroke=self.fretcolor,
                        stroke_width=self.fretsize
                    )
                )
        else:
            for i in range(self.gap+1):
                #self.gap +1 :  for  the end of the fretboard and (i+2) to avoid first fret when nut
                self.dwg.add(
                    self.dwg.line(
                        start=(self.wf +self._ol, (self.hf)*(i+2)+self._ol),
                        end=((self.wf)*(len(self.tuning))+self._ol,(self.hf)*(i+2)+self._ol),
                        stroke=self.fretcolor,
                        stroke_width=self.fretsize
                    )
                )

        #creation of strings
        if self.string_same_size==False:
            string_size_list=[((self.string_size)-i/4) for i in range(len(self.tuning))]

        elif self.string_same_size==True:
            string_size_list=[(self.string_size) for i in range(len(self.tuning))]

        for i in range(len(self.tuning)):

            self.dwg.add(
                self.dwg.line(
                    start=((self.wf)*(1+i)+self._ol, self.hf+self._ol-self.fretsize/2),
                    end=((self.wf)*(1+i)+self._ol,self.hf+self._ol + (self.gap+1)*self.hf +self.fretsize/2),
                    stroke=self.strings_color,
                    stroke_width=string_size_list[i]
                )
            )
    def nut(self):
        '''
        Create nut if condition in fillfretboard.

        '''
        if self.string_same_size==False:
            self.dwg.add(
                self.dwg.line(
                    start=(self.wf +self._ol-((self.string_size))/2,(self.hf)*(1)+self._ol),
                    end=((self.wf)*(len(self.tuning))+self._ol +((self.string_size)-len(self.tuning)/4)/2 ,(self.hf)*(1)+self._ol ),
                    stroke=self.nut_color,
                    stroke_width=self.nut_height
                )
            )
        else:
            self.dwg.add(
                self.dwg.line(
                    start=(self.wf +self._ol-((self.string_size))/2,(self.hf)*(1)+self._ol),
                    end=((self.wf)*(len(self.tuning))+self._ol +((self.string_size))/2 ,(self.hf)*(1)+self._ol ),
                    stroke=self.nut_color,
                    stroke_width=self.nut_height
                )
            )
    def show_fret(self):
        '''
        Show text under the frets for example 3ft if condition in fillfretboard
        '''
        dot=[3,5,7,9,12,15,17,19,21,24]
        dot=[dot[v] for v in range(len(dot)) if dot[v]<=self.last_fret and dot[v]>=self.first_fret]
        #self.first_fret=0
        #self.last_fret=12
        if self.show_ft:
            for j,v in enumerate(dot):
                Y=self.wf*(1+len(self.tuning))
                X=self.hf*(1/2+v-self.first_fret)+self._ol
                t=svgwrite.text.Text(str(v),dy=["0.3em"], insert=(X,Y),font_size=self.fontsize_text,font_weight="bold",style="text-anchor:middle")
                self.dwg.add(t)

    def show_tuning(self,fretfing):
        '''
        Show  tuning at the end of the neck.
        '''

        Max_after_conv=max([0 if v == None else v for v in self.fingering])
        if max(fretfing)>4:
            for i in range(len(self.tuning)):
                X=self.wf*(1+i)+self._ol
                Y=self.hf*(Max_after_conv+1/2+1)+self._ol

                t=svgwrite.text.Text(self.tuning[i], insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_bottom_tuning,font_weight="normal",style="text-anchor:middle")
                self.dwg.add(t)

        else:
            for i in range(len(self.tuning)):
                X=self.wf*(1+i)+self._ol
                Y=self.hf*(5+1/2)+self._ol

                t=svgwrite.text.Text(self.tuning[i], insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_bottom_tuning,font_weight="normal",style="text-anchor:middle")
                self.dwg.add(t)



    def fillfretboard(self):

        if self.lefthand:
            self.fingering=self.fingering[::-1] #reverse fingering array
            self.tuning=self.tuning[::-1]
        self.dist() #modify self.gap
        chroma=["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        intervals=["1","b2","2","b3","3","4","b5","5","b6","6","b7","7"]



        fingname=self.notesname()
        inter=FretBoardGtr.find_intervals(fingname,self.root)

        fretfing=[0 if v == None else v for v in self.fingering]
        minfret = min(v for v in fretfing if v > 0)

        if max(fretfing)>4:

            X=self.wf*(1+len(self.tuning))+self._ol
            Y=self.hf*(3/2)+self._ol
            t=svgwrite.text.Text(str(minfret), insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_fret,font_weight="bold",style="text-anchor:middle")
            self.dwg.add(t)

            fingering=[v if v==None else v-minfret+1 if v!=0 else v for v in self.fingering ]


        else:
            self.nut()
            fingering=self.fingering

        for i in range(0,len(self.tuning),1):

            if fingering[i]== None:
                X=self.wf*(1+i)+self._ol
                Y=self.hf*(1/2)+self._ol

                t=svgwrite.text.Text('X', insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_cross,font_weight="bold",fill=self.cross_color,style="text-anchor:middle")
                self.dwg.add(t)
                #dwg.add(dwg.image("cross.svg",x=(i+1-0.3)*self.wf +self._ol,y=self.hf*(1/4-0.2)+self._ol,width=2*self.R))

            else:
                X=self.wf*(1+i)+self._ol
                Y=self.hf*(fingering[i]+1/2)+self._ol

                if fingering[i]==0:
                    if self.open_color_chord:
                        color=self.dic_color[inter[i]]
                    else:
                        color=self.fretted_circle_color
                    if self.show_note_name:
                        name_text=fingname[i]
                    elif self.show_degree_name:
                        name_text=str(inter[i])
                    else:
                        name_text=""
                    self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=self.open_circle_color,stroke=color,stroke_width=self.open_circle_stroke_width))
                    t=svgwrite.text.Text(name_text, insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_text,font_weight="bold",fill=self.open_text_color,style="text-anchor:middle")
                    self.dwg.add(t)
                else:
                    if self.color_chord:
                        color=self.dic_color[inter[i]]
                    else:
                        color=self.fretted_circle_color
                    if self.show_note_name:
                        name_text=fingname[i]
                    elif self.show_degree_name:
                        name_text=str(inter[i])
                    else:
                        name_text=""

                    self.dwg.add(self.dwg.circle((X,Y),r=self.R,fill=color,stroke=self.fretted_circle_stroke_color,stroke_width=self.fretted_circle_stroke_width))
                    t=svgwrite.text.Text(name_text, insert=(X,Y), dy=["0.3em"], font_size=self.fontsize_text,fill=self.fretted_text_color,font_weight="bold",style="text-anchor:middle")
                    self.dwg.add(t)

            if self.show_tun:
                self.show_tuning(fretfing)


    def draw(self):
        self.dist()
        self.emptybox()
        self.background_fill()
        #self.background_fill_image()
        self.add_dot()
        self.createfretboard()
        self.fillfretboard()


        return self.dwg
