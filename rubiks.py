# --- START OF FILE rubiks.py ---

"""
This script emulates a Rubik's Cube of arbitrary size,
supporting all forms of its manipulation.
Cubes are visually represented as coloured blocks in standard output.

Author: Mykel Shumay
"""

import numpy as np
import random
import time
import getopt
import sys
import importlib.util  # MODIFICA: Aggiunto import necessario

# Number of squares along each edge of the Cube.
edge_length = 3
# Unicode character used in a Cube's visual representation.
console_block = u'\u25a0'
# Default console text colour.
text_colour_white  = '\033[0m'
# Number of random rotations to make during a Cube's scrambling.
scramble_iterations = 25000

# Colour values of the Rubik's Cube.
colours = {
    'red': 0, 'white': 1, 'green': 2, 'yellow': 3, 'blue': 4, 'orange': 5,
    # MODIFICA: Aggiunti alias per il caricamento da dizionario
    'r': 0, 'w': 1, 'g': 2, 'y': 3, 'b': 4, 'o': 5
}

# MODIFICA: Mappatura per convertire il dizionario in coordinate numpy
# U->white(1), F->green(2), R->red(0), B->blue(4), L->orange(5), D->yellow(3)
cube_dict_mapping = {
    'U1': (1, 0, 0), 'U2': (1, 0, 1), 'U3': (1, 0, 2), 'U4': (1, 1, 0), 'U5': (1, 1, 1), 'U6': (1, 1, 2), 'U7': (1, 2, 0), 'U8': (1, 2, 1), 'U9': (1, 2, 2),
    'L1': (5, 0, 0), 'L2': (5, 0, 1), 'L3': (5, 0, 2), 'L4': (5, 1, 0), 'L5': (5, 1, 1), 'L6': (5, 1, 2), 'L7': (5, 2, 0), 'L8': (5, 2, 1), 'L9': (5, 2, 2),
    'F1': (2, 0, 0), 'F2': (2, 0, 1), 'F3': (2, 0, 2), 'F4': (2, 1, 0), 'F5': (2, 1, 1), 'F6': (2, 1, 2), 'F7': (2, 2, 0), 'F8': (2, 2, 1), 'F9': (2, 2, 2),
    'R1': (0, 0, 0), 'R2': (0, 0, 1), 'R3': (0, 0, 2), 'R4': (0, 1, 0), 'R5': (0, 1, 1), 'R6': (0, 1, 2), 'R7': (0, 2, 0), 'R8': (0, 2, 1), 'R9': (0, 2, 2),
    'B1': (4, 0, 0), 'B2': (4, 0, 1), 'B3': (4, 0, 2), 'B4': (4, 1, 0), 'B5': (4, 1, 1), 'B6': (4, 1, 2), 'B7': (4, 2, 0), 'B8': (4, 2, 1), 'B9': (4, 2, 2),
    'D1': (3, 0, 0), 'D2': (3, 0, 1), 'D3': (3, 0, 2), 'D4': (3, 1, 0), 'D5': (3, 1, 1), 'D6': (3, 1, 2), 'D7': (3, 2, 0), 'D8': (3, 2, 1), 'D9': (3, 2, 2),
}

# Colours for console output.
console_colours = {
    colours['red']: '\033[31m', colours['white']: '\033[37m', colours['green']: '\033[92m',
    colours['yellow']: '\033[93m', colours['blue']: '\033[94m', colours['orange']: '\033[91m',
}

# For each face, stores the index of each adjacent face.
face_relations = {
    '_'.join([str(colours['red']), 'u']): colours['white'], '_'.join([str(colours['red']), 'l']): colours['green'], '_'.join([str(colours['red']), 'd']): colours['yellow'], '_'.join([str(colours['red']), 'r']): colours['blue'],
    '_'.join([str(colours['green']), 'u']): colours['white'], '_'.join([str(colours['green']), 'l']): colours['orange'], '_'.join([str(colours['green']), 'd']): colours['yellow'], '_'.join([str(colours['green']), 'r']): colours['red'],
    '_'.join([str(colours['orange']), 'u']): colours['white'], '_'.join([str(colours['orange']), 'l']): colours['blue'], '_'.join([str(colours['orange']), 'd']): colours['yellow'], '_'.join([str(colours['orange']), 'r']): colours['green'],
    '_'.join([str(colours['blue']), 'u']): colours['white'], '_'.join([str(colours['blue']), 'l']): colours['red'], '_'.join([str(colours['blue']), 'd']): colours['yellow'], '_'.join([str(colours['blue']), 'r']): colours['orange'],
    '_'.join([str(colours['white']), 'u']): colours['orange'], '_'.join([str(colours['white']), 'l']): colours['green'], '_'.join([str(colours['white']), 'd']): colours['red'], '_'.join([str(colours['white']), 'r']): colours['blue'],
    '_'.join([str(colours['yellow']), 'u']): colours['red'], '_'.join([str(colours['yellow']), 'l']): colours['green'], '_'.join([str(colours['yellow']), 'd']): colours['orange'], '_'.join([str(colours['yellow']), 'r']): colours['blue']
}

class Cube():
    """Emulates a Rubik's Cube."""
    def __init__(self, edge_length):
        self.edge_length = edge_length
        self.faces = np.zeros([6, self.edge_length, self.edge_length], dtype=np.uint8)
        cw_rotate_take_idxs = np.arange(self.edge_length * self.edge_length)
        cw_rotate_take_idxs = cw_rotate_take_idxs.reshape(self.edge_length, self.edge_length)
        self.cw_rotate_take_idxs = np.flip(cw_rotate_take_idxs.transpose(), axis=[1])
        for face_idx in range(self.faces.shape[0]):
            self.faces[face_idx].fill(face_idx)
    
    def copy(self):
        """Returns a deep copy of the Cube."""
        clone_cube = Cube(self.edge_length)
        clone_cube.faces = np.copy(self.faces)
        return clone_cube

    # MODIFICA: Nuova funzione per caricare lo stato da un dizionario
    def load_from_dict(self, cube_dict):
        """
        Carica lo stato del cubo da un dizionario (es. my_rubiks_cube_state).
        Assume un cubo 3x3x3 per la mappatura.
        """
        if self.edge_length != 3:
            print("Avviso: La funzione load_from_dict è ottimizzata per cubi 3x3x3.")
        
        for key, color_char in cube_dict.items():
            if key in cube_dict_mapping:
                face, row, col = cube_dict_mapping[key]
                color_value = colours.get(color_char.lower())
                if color_value is not None:
                    self.faces[face, row, col] = color_value
                else:
                    print(f"Avviso: Colore '{color_char}' non riconosciuto per la chiave '{key}'.")
            else:
                print(f"Avviso: Chiave '{key}' non trovata nella mappatura. Ignorata.")

    def rotate(self, action):
        if action < 12:
            self.rotate_face(action)
            self.rotate_edges(action)
        else:
            self.rotate_middle(action)
            pass

    def rotate_face(self, action):
        face_idx = action // 2
        rotation = action % 2
        if rotation == 0:
            indices = self.cw_rotate_take_idxs
        else:
            indices = np.flip(self.cw_rotate_take_idxs.flatten(), axis=[0])
        self.faces[face_idx] = np.take(
            a=self.faces[face_idx],
            indices=indices).reshape(self.edge_length, self.edge_length)

    def rotate_edges(self, action):
        """Rotate a face's adjacent edges 90 degrees in the given direction (face not accounted for)."""
        # Face to rotate about.
        face_idx = action // 2
        # Direction to rotate (0: clockwise; 1: counter-clockwise)
        rotation = action % 2        
        ### Gather information on the affected faces.
        # Face above.
        u_face = self.faces[face_relations['_'.join([str(face_idx), 'u'])]]
        u_face_copy = np.copy(u_face)        
        # Left face.
        l_face = self.faces[face_relations['_'.join([str(face_idx), 'l'])]]
        l_face_copy = np.copy(l_face)        
        # Face below.
        d_face = self.faces[face_relations['_'.join([str(face_idx), 'd'])]]
        d_face_copy = np.copy(d_face)        
        # Right face.
        r_face = self.faces[face_relations['_'.join([str(face_idx), 'r'])]]
        r_face_copy = np.copy(r_face)        
        ### Rotate all affected edges appropriately.
        if face_idx == 0:
            # Rotate edges adjacent to face 0.
            if rotation == 0:
                # Rotate clockwise.
                u_face[-1] = np.flip(l_face_copy.transpose()[-1], axis=[0])
                l_face.transpose()[-1] = d_face_copy[0]
                d_face[0] = np.flip(r_face_copy.transpose()[0], axis=[0])
                r_face.transpose()[0] = u_face_copy[-1]
            else:
                # Rotate counter-clockwise.
                u_face[-1] = r_face_copy.transpose()[0]
                l_face.transpose()[-1] = np.flip(u_face_copy[-1], axis=[0])
                d_face[0] = l_face_copy.transpose()[-1]
                r_face.transpose()[0] = np.flip(d_face_copy[0], axis=[0])        
        elif face_idx == 1:
            # Rotate edges adjacent to face 1.
            if rotation == 0:
                # Rotate clockwise.
                u_face[0] = l_face_copy[0]
                l_face[0] = d_face_copy[0]
                d_face[0] = r_face_copy[0]
                r_face[0] = u_face_copy[0]
            else:
                # Rotate counter-clockwise.
                u_face[0] = r_face_copy[0]
                l_face[0] = u_face_copy[0]
                d_face[0] = l_face_copy[0]
                r_face[0] = d_face_copy[0]        
        elif face_idx == 2:
            # Rotate edges adjacent to face 2.
            if rotation == 0:
                # Rotate clockwise.
                u_face.transpose()[0] = np.flip(l_face_copy.transpose()[-1], axis=[0])
                l_face.transpose()[-1] = np.flip(d_face_copy.transpose()[0], axis=[0])
                d_face.transpose()[0] = r_face_copy.transpose()[0]
                r_face.transpose()[0] = u_face_copy.transpose()[0]
            else:
                # Rotate counter-clockwise.
                u_face.transpose()[0] = r_face_copy.transpose()[0]
                l_face.transpose()[-1] = np.flip(u_face_copy.transpose()[0], axis=[0])
                d_face.transpose()[0] = np.flip(l_face_copy.transpose()[-1], axis=[0])
                r_face.transpose()[0] = d_face_copy.transpose()[0]
        
        elif face_idx == 3:
            # Rotate edges adjacent to face 3.
            if rotation == 0:
                # Rotate clockwise.
                u_face[-1] = l_face_copy[-1]
                l_face[-1] = d_face_copy[-1]
                d_face[-1] = r_face_copy[-1]
                r_face[-1] = u_face_copy[-1]
            else:
                # Rotate counter-clockwise.
                u_face[-1] = r_face_copy[-1]
                l_face[-1] = u_face_copy[-1]
                d_face[-1] = l_face_copy[-1]
                r_face[-1] = d_face_copy[-1]
        
        elif face_idx == 4:
            # Rotate edges adjacent to face 4.
            if rotation == 0:
                # Rotate clockwise.
                u_face.transpose()[-1] = l_face_copy.transpose()[-1]
                l_face.transpose()[-1] = d_face_copy.transpose()[-1]
                d_face.transpose()[-1] = np.flip(r_face_copy.transpose()[0], axis=[0])
                r_face.transpose()[0] = np.flip(u_face_copy.transpose()[-1], axis=[0])
            else:
                # Rotate counter-clockwise.
                u_face.transpose()[-1] = np.flip(r_face_copy.transpose()[0], axis=[0])
                l_face.transpose()[-1] = u_face_copy.transpose()[-1]
                d_face.transpose()[-1] = l_face_copy.transpose()[-1]
                r_face.transpose()[0] = np.flip(d_face_copy.transpose()[-1], axis=[0])        
        elif face_idx == 5:
            # Rotate edges adjacent to face 5.
            if rotation == 0:
                # Rotate clockwise.
                u_face[0] = l_face_copy.transpose()[-1]
                l_face.transpose()[-1] = np.flip(d_face_copy[-1], axis=[0])
                d_face[-1] = r_face_copy.transpose()[0]
                r_face.transpose()[0] = np.flip(u_face_copy[0], axis=[0])
            else:
                # Rotate counter-clockwise.
                u_face[0] = np.flip(r_face_copy.transpose()[0], axis=[0])
                l_face.transpose()[-1] = u_face_copy[0]
                d_face[-1] = np.flip(l_face_copy.transpose()[-1], axis=[0])
                r_face.transpose()[0] = d_face_copy[-1]
                    
    def rotate_middle(self, action):
        """Rotate an inner row/column of the Cube.        
        Rotations are taken with face 0 as the front.
        """        
        # Whether to rotate left/right (0) or up/down (1).
        orientation = (action - 12) // ((self.edge_length - 2) * 2)
        # Direction to rotate (0: clockwise; 1: counter-clockwise)
        rotation = action % 2        
        ### Gather information on the affected faces.
        # Face on the front.
        f_face = self.faces[0]
        f_face_copy = np.copy(f_face)        
        # Face on the back.
        b_face = self.faces[5]
        b_face_copy = np.copy(b_face)        
        if orientation == 0:
            ### Rotate left/right.
            # Left face.
            l_face = self.faces[2]
            l_face_copy = np.copy(l_face)        
            # Right face.
            r_face = self.faces[4]
            r_face_copy = np.copy(r_face)        
            # Affected row.
            row_idx = 1 + ((action - 12) % ((self.edge_length - 2) * 2)) // 2        
            if rotation == 0:
                # Rotate rightwards.
                r_face[row_idx] = f_face_copy[row_idx]
                b_face[row_idx] = r_face_copy[row_idx]
                l_face[row_idx] = b_face_copy[row_idx]
                f_face[row_idx] = l_face_copy[row_idx]
            else:
                # Rotate leftwards.
                r_face[row_idx] = b_face_copy[row_idx]
                b_face[row_idx] = l_face_copy[row_idx]
                l_face[row_idx] = f_face_copy[row_idx]
                f_face[row_idx] = r_face_copy[row_idx]        
        else:
            ### Rotate up/down.
            # Face above.
            u_face = self.faces[1]
            u_face_copy = np.copy(u_face)        
            # Face below.
            d_face = self.faces[3]
            d_face_copy = np.copy(d_face)        
            # Affected column.
            col_idx = 1 + ((action - 12) % ((self.edge_length - 2) * 2)) // 2        
            if rotation == 0:
                # Rotate upwards.
                u_face.transpose()[col_idx] = f_face_copy.transpose()[col_idx]
                b_face.transpose()[-1-col_idx] = np.flip(u_face_copy.transpose()[col_idx])
                d_face.transpose()[col_idx] = np.flip(b_face_copy.transpose()[-1-col_idx])
                f_face.transpose()[col_idx] = d_face_copy.transpose()[col_idx]
            else:
                # Rotate downwards.
                u_face.transpose()[col_idx] = np.flip(b_face_copy.transpose()[-1-col_idx])
                b_face.transpose()[-1-col_idx] = np.flip(d_face_copy.transpose()[col_idx])
                d_face.transpose()[col_idx] = f_face_copy.transpose()[col_idx]
                f_face.transpose()[col_idx] = u_face_copy.transpose()[col_idx]

    def scramble(self, iterations=scramble_iterations):
        """Rotate the Cube randomly the specified number of times (iterations)."""
        for _ in range(iterations):
            self.random_rotation()    
    def random_rotation(self):
        """Take a random rotation action."""
        action = random.choice(range(12 + 4*(self.edge_length-2)))
        self.rotate(action)
        return action
    
    def __repr__(self):
        """Returns a coloured grid of the flattened Cube."""
        edge_length = self.edge_length
        # Gather the Cube's faces.
        red_face = self.faces[colours['red']]
        white_face = self.faces[colours['white']]
        green_face = self.faces[colours['green']]
        yellow_face = self.faces[colours['yellow']]
        blue_face = self.faces[colours['blue']]
        orange_face = self.faces[colours['orange']]
        # Concatenate the 4 middle faces together for simplicity.
        middle_faces = np.concatenate([green_face, red_face, blue_face, orange_face], axis=1)
        # Flattened lists of coloured blocks for all faces.
        white_face_blocks = [console_colours[x]+console_block+text_colour_white for x in white_face.flatten()]
        middle_faces_blocks = [console_colours[x]+console_block+text_colour_white for x in middle_faces.flatten()]
        yellow_face_blocks = [console_colours[x]+console_block+text_colour_white for x in yellow_face.flatten()]
        cube_str = ''
        # Construct the string containing the formatted coloured blocks.
        for row_idx in range(edge_length * 3):
            if row_idx % edge_length == 0:
                # Add an extra blank line between faces.
                cube_str += '\n '
            for col_idx in range(edge_length * 4):
                if col_idx % edge_length == 0:
                    # Add an extra blank column between faces.
                    cube_str += ' '
                if (row_idx < edge_length or row_idx > edge_length * 2 - 1) and \
                        (col_idx < edge_length or col_idx > edge_length * 2 - 1):
                    # Empty space in the grid.
                    cube_str += ' '
                elif row_idx < edge_length:
                    # Part of the white face.
                    position = row_idx*edge_length + col_idx%edge_length
                    colour = white_face_blocks[position]
                    cube_str += colour
                elif row_idx > edge_length * 2 - 1:
                    # Part of the yellow face.
                    position = (row_idx%edge_length)*edge_length + col_idx%edge_length
                    colour = yellow_face_blocks[position]
                    cube_str += colour
                else:
                    # Part of middle 4 faces.
                    position = (row_idx%edge_length)*edge_length*4 + col_idx%(edge_length*4)
                    colour = middle_faces_blocks[position]
                    cube_str += colour
            # Start a new row.
            cube_str += '\n '

        return cube_str

    def __eq__(self, other):
        return np.array_equal(self.faces, other.faces)
    
def main():
    global edge_length
    load_custom_cube = False
    custom_cube_data = None

    try:
        # MODIFICA: Aggiunta l'opzione --load_cube
        opts, args = getopt.getopt(sys.argv[1:], 's:h', ['size=', 'help', 'load_cube='])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('Options:')
                print(' -s N, --size=N      number of squares per Cube edge (default: 3)')
                print(' --load_cube=FILE    load initial cube state from FILE.py (e.g., cube.py)')
                print(' -h, --help          display this help page and exit')
                print('\n')
                quit()
            elif opt in ('-s', '--size'):
                try:
                    arg_val = int(arg)
                    if arg_val >= 2:
                        edge_length = arg_val
                        print(f'Cube size set to {edge_length}.')
                    else:
                        print(f'Provided cube size is not valid. Setting to default of {edge_length}.')
                        time.sleep(3)
                except ValueError:
                    print(f'Provided cube size is not valid. Setting to default of {edge_length}.')
                    time.sleep(3)
            # MODIFICA: Logica per caricare il file del cubo
            elif opt in ('--load_cube'):
                try:
                    cube_file_path = arg
                    module_name = cube_file_path.replace('.py', '')
                    spec = importlib.util.spec_from_file_location(module_name, cube_file_path)
                    if spec is None:
                        raise FileNotFoundError(f"Impossibile trovare il file: {cube_file_path}")
                    
                    cube_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(cube_module)
                    
                    # Assumiamo che la variabile si chiami 'my_rubiks_cube_state'
                    custom_cube_data = cube_module.my_rubiks_cube_state
                    load_custom_cube = True
                    print(f"Cubo personalizzato caricato con successo da {cube_file_path}")

                except (FileNotFoundError, AttributeError, ImportError) as e:
                    print(f'\nErrore durante il caricamento del cubo da {arg}: {e}')
                    print("Assicurati che il file esista e contenga una variabile 'my_rubiks_cube_state'.\n")
                    quit()

    except getopt.GetoptError as e:
        print(f'\nError: {e}')
        print("Call with option '--help' or '-h' for the help page.\n\n")
        quit()

    cube = Cube(edge_length=edge_length)
    
    if load_custom_cube:
        print('\nCaricamento dello stato del cubo dal file...')
        cube.load_from_dict(custom_cube_data)
        print('Cubo caricato:')
    else:
        print('Cubo originale:')
        print(cube)
        print('\nScrambling...')
        cube.scramble()
        print('Cubo mescolato:')
    
    print(cube)

if __name__ == '__main__':
    main()
# --- END OF FILE rubiks.py ---