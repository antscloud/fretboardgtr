# Configuration

## `[fretboard][main]`
| Name                | Type  | Description                                         | Default |
|---------------------|-------|-----------------------------------------------------|---------|
| x_start             | float | x position for starting fretboard                   | 30.0    |
| y_start             | float | y position for starting fretboard                   | 30.0    |
| fret_height         | float | Fret height                                         | 50      |
| fret_width          | float | Fret width                                          | 70      |
| first_fret          | float | Number of the first fret to display                 | 0       |
| last_fret           | float | Number of the last fret to display                  | 12      |
| show_tuning         | bool  | Display the tuning                                  | True    |
| show_frets          | bool  | Display the frets                                   | True    |
| show_nut            | bool  | Display the nut                                     | True    |
| show_degree_name    | bool  | Display the name of degrees                         | False   |
| show_note_name      | bool  | Display the name of notes                           | True    |
| open_color_scale    | bool  | Color the open notes                                | False   |
| fretted_color_scale | bool  | Color the fretted notes                             | True    |
| enharmonic          | bool  | Preprocess the scale and trensform it to enharmonic | True    |

## `[fretboard][main][open_colors]`
See [open_colors](#open_colors)

## `[fretboard][main][fretted_colors]`
See [fretted_colors](#fretted_colors)

## `[fretboard][background]`
See [background](#background)

## `[fretboard][frets]`
See [frets](#frets)

## `[fretboard][fret_numbers]`
See [fret_numbers](#fret_numbers)

## `[fretboard][neck_dots]`
See [neck_dots](#neck_dots)

## `[fretboard][nut]`
See [nut](#nut)

## `[fretboard][strings]`
See [strings](#strings)

## `[fretboard][tuning]`
See [tuning](#tuning)

## `[fretboard][open_notes]`
See [open_notes](#open_notes)

## `[fretboard][fretted_notes]`
See [fretted_notes](#fretted_notes)


## Elements

<a name="test"></a>

## `[background]`


| Name    | Type  | Description               | Default          |
|---------|-------|---------------------------|------------------|
| color   | str   | Color of the background   | rgb(150,150,150) |
| opacity | float | Opacity of the background | 0.2              |

## `[frets]`
| Name  | Type        | Description             | Default            |
|-------|-------------|-------------------------|--------------------|
| color | str         | Color of the frets      | "rgb(150,150,150)" |
| width | int / float | Width of the frets line | 3                  |

## `[fret_numbers]`
| Name       | Type        | Description                   | Default            |
|------------|-------------|-------------------------------|--------------------|
| color      | str         | Text color of the fret number | "rgb(150,150,150)" |
| fontsize   | int / float | Font size                     | 20                 |
| fontweight | str         | Font weight                   | "bold"             |


## `[neck_dots]`
| Name         | Type        | Description          | Default            |
|--------------|-------------|----------------------|--------------------|
| color        | str         | Color of the dot     | "rgb(200,200,200)" |
| color_stroke | str         | Color of the stroke  | "rgb(0,0,0)"       |
| width_stroke | int / float | Width of the stroke  | 2                  |
| radius       | int / float | Radius of the stroke | 7                  |


## `[nut]`
| Name  | Type        | Description      | Default      |
|-------|-------------|------------------|--------------|
| color | str         | Color of the nut | "rgb(0,0,0)" |
| width | int / float | Width of the nut | 6            |


## `[strings]`
| Name  | Type        | Description              | Default      |
|-------|-------------|--------------------------|--------------|
| color | str         | Color of the strings      | "rgb(0,0,0)" |
| width | int / float | Width of the strings line | 3            |


## `[tuning]`
| Name       | Type        | Description  | Default            |
|------------|-------------|--------------|--------------------|
| color      | str         | Color of the | "rgb(150,150,150)" |
| fontsize   | int / float | Font size    | 20                 |
| fontweight | str         | Font weight  | "normal"           |


## `[open_notes]`
| Name         | Type        | Description                             | Default            |
|--------------|-------------|-----------------------------------------|--------------------|
| color        | str         | Color of the                            | "rgb(255,255,255)" |
| radius       | int / float | Radius of the note                      | 20                 |
| stroke_color | str         | Stroke color of the note                | "rgb(0,0,0)"       |
| stroke_width | int / float | Stroke width of the note                | 3                  |
| text_color   | str         | Text color of the text inside the note  | "rgb(0,0,0)"       |
| fontsize     | int / float | Font size of the text inside the note   | 20                 |
| fontweight   | str         | Font weight of the text inside the note | "bold"             |


## `[fretted_notes]`
| Name         | Type        | Description                             | Default            |
|--------------|-------------|-----------------------------------------|--------------------|
| color        | str         | Color of the                            | "rgb(255,255,255)" |
| radius       | int / float | Radius of the note                      | 20                 |
| stroke_color | str         | Stroke color of the note                | "rgb(0,0,0)"       |
| stroke_width | int / float | Stroke width of the note                | 3                  |
| text_color   | str         | Text color of the text inside the note  | "rgb(0,0,0)"       |
| fontsize     | str         | Font size of the text inside the note   | 20                 |
| fontweight   | str         | Font weight of the text inside the note | "bold"             |


## Colors

## `[open_colors]`

| Name            | Type | Description                   | Default             |
|-----------------|------|-------------------------------|---------------------|
| root            | str  | Color of the root             | "rgb(231, 0, 0)"    |
| minorsecond     | str  | Color of the minor second     | "rgb(249, 229, 0)"  |
| majorsecond     | str  | Color of the major second     | "rgb(249, 165, 0)"  |
| minorthird      | str  | Color of the minor third      | "rgb(0, 94, 0)"     |
| majorthird      | str  | Color of the major third      | "rgb(0, 108, 0)"    |
| perfectfourth   | str  | Color of the perfect fourth   | "rgb(0, 154, 0)"    |
| diminishedfifth | str  | Color of the diminished fifth | "rgb(0, 15, 65)"    |
| perfectfifth    | str  | Color of the perfect fifth    | "rgb(0, 73, 151)"   |
| minorsixth      | str  | Color of the minor sixth      | "rgb(168, 107, 98)" |
| majorsixth      | str  | Color of the major sixth      | "rgb(222, 81, 108)" |
| minorseventh    | str  | Color of the minor seventh    | "rgb(120, 37, 134)" |
| majorseventh    | str  | Color of the major seventh    | "rgb(120, 25, 98)"  |

## `[fretted_colors]`

| Name            | Type | Description                   | Default             |
|-----------------|------|-------------------------------|---------------------|
| root            | str  | Color of the root             | "rgb(231, 0, 0)"    |
| minorsecond     | str  | Color of the minor second     | "rgb(249, 229, 0)"  |
| majorsecond     | str  | Color of the major second     | "rgb(249, 165, 0)"  |
| minorthird      | str  | Color of the minor third      | "rgb(0, 94, 0)"     |
| majorthird      | str  | Color of the major third      | "rgb(0, 108, 0)"    |
| perfectfourth   | str  | Color of the perfect fourth   | "rgb(0, 154, 0)"    |
| diminishedfifth | str  | Color of the diminished fifth | "rgb(0, 15, 65)"    |
| perfectfifth    | str  | Color of the perfect fifth    | "rgb(0, 73, 151)"   |
| minorsixth      | str  | Color of the minor sixth      | "rgb(168, 107, 98)" |
| majorsixth      | str  | Color of the major sixth      | "rgb(222, 81, 108)" |
| minorseventh    | str  | Color of the minor seventh    | "rgb(120, 37, 134)" |
| majorseventh    | str  | Color of the major seventh    | "rgb(120, 25, 98)"  |
