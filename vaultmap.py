from functools import reduce
import sys

"""
Converts .c file exports downloaded from www.piskelapp.com 
and prints a MAP...ENDMAP section suitable for pasting 
into Dungeon Crawl Stone Soup vault files.
"""


def get_color(code):
    """Convert 0xααBBGGRR C color code to a color name if possible."""
    default = {'0xff808080': 'Dark Gray',
               '0xffc0c0c0': 'Gray',
               '0xffffffff': 'White',
               '0xff808000': 'Dark Cyan',
               '0xffbfbf00': 'Cyan',
               '0xffffff00': 'Bright Cyan',
               '0xff404040': 'Charcoal',
               '0xff00c000': 'Green',
               '0xff008000': 'Dark Green',
               '0xff000000': 'Black',
               '0xff800000': 'Dark Blue',
               '0xffc00000': 'Blue',
               '0xff000080': 'Dark Red',
               '0xff004080': 'Dark Brown',
               '0xff0060c0': 'Brown',
               '0xffc080ff': 'Pink',
               '0xffff80c0': 'Pale Blue',
               '0xff80ff80': 'Pale Green',
               '0xff0080ff': 'Orange',
               '0xff8000c0': 'Plum',
               '0xff600080': 'Dark Plum',
               '0xffco0080': 'Purple',
               '0xff800060': 'Dark Purple',
               '0xff00dfff': 'Gold',
               '0xff00ff00': 'Bright Green',
               '0xffc000ff': 'Bright Pink',
               '0xff0000ff': 'Bright Red',
               }
    if code[:4] == '0x00':
        return 'Transparent'
    else:
        try:
            return default[code]
        except KeyError:
            code = code.upper()
            # return #RRGGBB even though C uses bbggrr
            return f'#{code[8:10]}{code[6:8]}{code[4:6]}'


def get_glyph(color):
    """Convert a color name into a glyph, suggesting default glyphs."""
    default = {'Dark Gray': ('x', 'Opaque Rock Wall'),
               'Light Gray': ('c', 'Opaque Stone Wall'),
               'White': ('X', 'Opaque Permawall'),
               'Dark Cyan': ('m', 'Transparent Rock Wall'),
               'Cyan': ('n', 'Transparent Stone Wall'),
               'Bright Cyan': ('o', 'Transparent Permawall'),
               'Charcoal': ('v', 'Metal Wall'),
               'Green': ('b', 'Crystal Wall'),
               'Dark Green': ('t', 'Tree'),
               'Black': ('.', 'Rock Floor'),
               'Dark Blue': ('w', 'Deep Water'),
               'Blue': ('W', 'Shallow Water'),
               'Dark Red': ('l', 'Lava'),
               'Dark Brown': ('+', 'Normal Door'),
               'Brown': ('=', 'Runed Door'),
               'Pink': ('G', 'Granite Statue'),
               'Pale Blue': ('T', 'Water Fountain'),
               'Pale Green': ('B', 'Altar'),
               'Orange': ('@', 'Entry Point'),
               'Plum': ('{', 'Stairs Up'),
               'Dark Plum': ('<', 'Hatch Up'),
               'Purple': ('}', 'Stairs Down'),
               'Dark Purple': ('>', 'Hatch Down'),
               'Gold': ('$', 'Gold'),
               'Bright Green': ('P', 'Undefined'),
               'Bright Pink': ('Q', 'Custom'),
               'Bright Red': ('R', 'Custom'),
               }
    try:
        if color == 'Transparent':
            return ' '
        else:
            suggest = default[color]
    except KeyError:
        glyph = ''
        while glyph == '':
            glyph = input(f'{color}: ')
        return glyph
    default_glyph, default_label = suggest
    glyph = input(f'{color} ({default_glyph} {default_label}): ')
    if glyph == '':
        glyph = default_glyph
    return glyph


def read_c_file(command_line_args):

    def add_extension(fname):
        if fname[-2:] != '.c':
            fname = fname + '.c'
        return fname

    def prompt_for_filename():
        fname = input('Enter the Piskel C file filename: ')
        return add_extension(fname)

    try:
        # filename was a command-line argument
        filename = add_extension(command_line_args[1])
    except IndexError:
        # there was no command-line argument
        filename = prompt_for_filename()
    read_successfully = False
    while not read_successfully:
        try:
            with open(filename) as c_file:
                lines = c_file.read()
                read_successfully = True
        except FileNotFoundError:
            print(f'{filename} not found.')
            filename = prompt_for_filename()
    without_header = lines.partition('{\n{\n')[-1]
    without_footer = without_header.partition('}')[0]
    without_spaces = without_footer.replace(' ', '')
    # have each row end with a comma for row[:-1] below
    add_last_comma = without_spaces[:-1] + ','
    rows = add_last_comma.split('\n')
    return [row[:-1].split(',') for row in rows]


if __name__ == '__main__':

    # Read the C file from Piskel
    codes_array = read_c_file(sys.argv)

    # Convert the color codes into color names.
    colors_array = [[get_color(code) for code in row]
                    for row in codes_array]

    # Convert the color names into glyphs.
    all_colors = reduce(set.union, [set(row) for row in colors_array])
    glyphs = {color: get_glyph(color) for color in all_colors}
    glyphs_array = [[glyphs[color] for color in row]
                    for row in colors_array]

    # Print the glyphs array as a .des MAP section
    map_string = ['MAP']
    for row in glyphs_array:
        map_string.append(''.join(row).rstrip())
    map_string.append('ENDMAP')
    print('\n'.join(map_string))
