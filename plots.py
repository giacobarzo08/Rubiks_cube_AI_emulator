import pyvista as pv
import logging
import sys
from cube_status import Cube

class RubikCubePlotter:
    def __init__(self, rubik_state: Cube) -> None:
        self.color_map_dict = {
            'w': (255, 255, 255), 
            'g': (0, 158, 96),    
            'r': (183, 18, 52), 
            'b': (0, 70, 173),   
            'o': (255, 88, 0),     
            'y': (255, 213, 0)     
        }

        if not isinstance(rubik_state, Cube):
            logging.error("rubik_state must be an instance of Cube.")
            raise TypeError("rubik_state must be an instance of Cube.")

        self.rubik_state = rubik_state.blocks
        self.get_color_list() # self.final_color_list will be populated here
        self.create_cube_mesh() #self.cube will be created here
    
    def get_color_list(self) -> None:
        pv_cell_to_rubik_num = ['7', '8', '9', '4', '5', '6', '1', '2', '3']
        face_prefixes = ['U', 'F', 'R', 'B', 'L', 'D']

        try:
            self.final_color_list = []
            for face_prefix in face_prefixes:
                for rubik_num in pv_cell_to_rubik_num:
                    key = face_prefix + rubik_num
                    color_char = self.rubik_state[key]
                    color_rgb = self.color_map_dict[color_char]
                    self.final_color_list.append(color_rgb)
            
            logging.info("Color list created successfully.")
        except Exception as e:
            logging.critical(f"Error in get_color_list: {e}", exc_info=True)
            sys.exit('critical error in get_color_list, exiting...')
    
    def create_cube_faces(self) -> list:
        base_face = pv.Plane(i_resolution=3, j_resolution=3)
        base_face.scale(3.0, inplace=True)
        center_offset = 1.5

        try:
            # Up (Y+)
            face_u = base_face.copy()
            face_u.rotate_x(-90, inplace=True)
            face_u.translate([0, center_offset, 0], inplace=True)

            # Front (Z+)
            face_f = base_face.copy()
            face_f.translate([0, 0, center_offset], inplace=True)

            # Right (X+)
            face_r = base_face.copy()
            face_r.rotate_y(90, inplace=True)
            face_r.translate([center_offset, 0, 0], inplace=True)

            # Back (Z-)
            face_b = base_face.copy()
            face_b.rotate_y(180, inplace=True)
            face_b.translate([0, 0, -center_offset], inplace=True)

            # Left (X-)
            face_l = base_face.copy()
            face_l.rotate_y(-90, inplace=True)
            face_l.translate([-center_offset, 0, 0], inplace=True)

            # Down (Y-)
            face_d = base_face.copy()
            face_d.rotate_x(90, inplace=True)
            face_d.translate([0, -center_offset, 0], inplace=True)

            logging.info("Cube faces created successfully.")
            return [face_u, face_f, face_r, face_b, face_l, face_d]
        except Exception as e:
            logging.critical(f"Error in create_cube_faces: {e}", exc_info=True)
            sys.exit('critical error in create_cube_faces, exiting...')

    def create_cube_mesh(self) -> None:
        try: 
            faces = self.create_cube_faces()
            self.cube = faces[0].merge(faces[1:])
            
            # Assign colors to the cube
            self.cube.cell_data['colors'] = self.final_color_list

            logging.info("Cube mesh created successfully.")
        except Exception as e:
            logging.critical(f"Error in create_cube_mesh: {e}", exc_info=True)
            sys.exit('critical error in create_cube_mesh, exiting...')
    
    def plot_cube(self, wiew_isometric: bool = False) -> None:
        if not isinstance(wiew_isometric, bool):
            logging.warning("wiew_isometric should be a boolean, not {}".format(type(wiew_isometric)))
            logging.warning("We are converting it to boolean. (Will it work?)")
            wiew_isometric = bool(wiew_isometric)

        try: 
            plotter = pv.Plotter(window_size=[800, 800])
            plotter.add_mesh(
                self.cube,
                scalars='colors',
                rgb =True,
                show_edges=True,
                edge_color='black',
                line_width=3
            )

            plotter.set_background('black')

            if wiew_isometric:
                plotter.enable_parallel_projection()
            plotter.show()
        except Exception as e:
            logging.critical(f"Error in plot_cube: {e}", exc_info=True)
            sys.exit('critical error in plot_cube, exiting...')
        finally:
            logging.info("Plotting completed, closing the plotter.")
            plotter.close()
