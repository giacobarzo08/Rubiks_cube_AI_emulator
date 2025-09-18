import logging

class Cube():
    def __init__(self):
        """Inizializza il cubo nel suo stato risolto."""
        self._blocks = {
            'U1': 'w', 'U2': 'w', 'U3': 'w', 'U4': 'w', 'U5': 'w', 'U6': 'w', 'U7': 'w', 'U8': 'w', 'U9': 'w',
            'F1': 'g', 'F2': 'g', 'F3': 'g', 'F4': 'g', 'F5': 'g', 'F6': 'g', 'F7': 'g', 'F8': 'g', 'F9': 'g',
            'R1': 'r', 'R2': 'r', 'R3': 'r', 'R4': 'r', 'R5': 'r', 'R6': 'r', 'R7': 'r', 'R8': 'r', 'R9': 'r',
            'B1': 'b', 'B2': 'b', 'B3': 'b', 'B4': 'b', 'B5': 'b', 'B6': 'b', 'B7': 'b', 'B8': 'b', 'B9': 'b',
            'L1': 'o', 'L2': 'o', 'L3': 'o', 'L4': 'o', 'L5': 'o', 'L6': 'o', 'L7': 'o', 'L8': 'o', 'L9': 'o',
            'D1': 'y', 'D2': 'y', 'D3': 'y', 'D4': 'y', 'D5': 'y', 'D6': 'y', 'D7': 'y', 'D8': 'y', 'D9': 'y',
        }

    @property
    def blocks(self):
        return self._blocks

    # --- Metodi Faccia Superiore (UP) ---
    def U(self):
        temp = self.blocks.copy()
        # Ruota faccia U (senso orario)
        self.blocks['U1'], self.blocks['U2'], self.blocks['U3'], self.blocks['U4'], self.blocks['U6'], self.blocks['U7'], self.blocks['U8'], self.blocks['U9'] = \
        temp['U7'], temp['U4'], temp['U1'], temp['U8'], temp['U2'], temp['U9'], temp['U6'], temp['U3']
        # Ruota lati
        self.blocks['F1'], self.blocks['F2'], self.blocks['F3'] = temp['R1'], temp['R2'], temp['R3']
        self.blocks['R1'], self.blocks['R2'], self.blocks['R3'] = temp['B1'], temp['B2'], temp['B3']
        self.blocks['B1'], self.blocks['B2'], self.blocks['B3'] = temp['L1'], temp['L2'], temp['L3']
        self.blocks['L1'], self.blocks['L2'], self.blocks['L3'] = temp['F1'], temp['F2'], temp['F3']
        logging.info("Rotated face U (clockwise) and updated adjacent sides.")

    def U_(self):
        temp = self.blocks.copy()
        # Ruota faccia U (senso antiorario)
        self.blocks['U1'], self.blocks['U2'], self.blocks['U3'], self.blocks['U4'], self.blocks['U6'], self.blocks['U7'], self.blocks['U8'], self.blocks['U9'] = \
        temp['U3'], temp['U6'], temp['U9'], temp['U2'], temp['U8'], temp['U1'], temp['U4'], temp['U7']
        # Ruota lati
        self.blocks['F1'], self.blocks['F2'], self.blocks['F3'] = temp['L1'], temp['L2'], temp['L3']
        self.blocks['L1'], self.blocks['L2'], self.blocks['L3'] = temp['B1'], temp['B2'], temp['B3']
        self.blocks['B1'], self.blocks['B2'], self.blocks['B3'] = temp['R1'], temp['R2'], temp['R3']
        self.blocks['R1'], self.blocks['R2'], self.blocks['R3'] = temp['F1'], temp['F2'], temp['F3']
        logging.info("Rotated face U (counter-clockwise) and updated adjacent sides.")

    # --- Metodi Faccia Inferiore (DOWN) ---
    def D(self):
        temp = self.blocks.copy()
        # Ruota faccia D (senso orario)
        self.blocks['D1'], self.blocks['D2'], self.blocks['D3'], self.blocks['D4'], self.blocks['D6'], self.blocks['D7'], self.blocks['D8'], self.blocks['D9'] = \
        temp['D7'], temp['D4'], temp['D1'], temp['D8'], temp['D2'], temp['D9'], temp['D6'], temp['D3']
        # Ruota lati
        self.blocks['F7'], self.blocks['F8'], self.blocks['F9'] = temp['L7'], temp['L8'], temp['L9']
        self.blocks['L7'], self.blocks['L8'], self.blocks['L9'] = temp['B7'], temp['B8'], temp['B9']
        self.blocks['B7'], self.blocks['B8'], self.blocks['B9'] = temp['R7'], temp['R8'], temp['R9']
        self.blocks['R7'], self.blocks['R8'], self.blocks['R9'] = temp['F7'], temp['F8'], temp['F9']
        logging.info("Rotated face D (clockwise) and updated adjacent sides.")

    def D_(self):
        temp = self.blocks.copy()
        # Ruota faccia D (senso antiorario)
        self.blocks['D1'], self.blocks['D2'], self.blocks['D3'], self.blocks['D4'], self.blocks['D6'], self.blocks['D7'], self.blocks['D8'], self.blocks['D9'] = \
        temp['D3'], temp['D6'], temp['D9'], temp['D2'], temp['D8'], temp['D1'], temp['D4'], temp['D7']
        # Ruota lati
        self.blocks['F7'], self.blocks['F8'], self.blocks['F9'] = temp['R7'], temp['R8'], temp['R9']
        self.blocks['R7'], self.blocks['R8'], self.blocks['R9'] = temp['B7'], temp['B8'], temp['B9']
        self.blocks['B7'], self.blocks['B8'], self.blocks['B9'] = temp['L7'], temp['L8'], temp['L9']
        self.blocks['L7'], self.blocks['L8'], self.blocks['L9'] = temp['F7'], temp['F8'], temp['F9']
        logging.info("Rotated face D (counter-clockwise) and updated adjacent sides.")

    # --- Metodi Faccia Frontale (FRONT) ---
    def F(self):
        temp = self.blocks.copy()
        # Ruota faccia F (senso orario)
        self.blocks['F1'], self.blocks['F2'], self.blocks['F3'], self.blocks['F4'], self.blocks['F6'], self.blocks['F7'], self.blocks['F8'], self.blocks['F9'] = \
        temp['F7'], temp['F4'], temp['F1'], temp['F8'], temp['F2'], temp['F9'], temp['F6'], temp['F3']
        # Ruota lati
        self.blocks['U7'], self.blocks['U8'], self.blocks['U9'] = temp['L9'], temp['L6'], temp['L3']
        self.blocks['R1'], self.blocks['R4'], self.blocks['R7'] = temp['U7'], temp['U8'], temp['U9']
        self.blocks['D1'], self.blocks['D2'], self.blocks['D3'] = temp['R7'], temp['R4'], temp['R1']
        self.blocks['L3'], self.blocks['L6'], self.blocks['L9'] = temp['D1'], temp['D2'], temp['D3']
        logging.info("Rotated face F (clockwise) and updated adjacent sides.")

    def F_(self):
        temp = self.blocks.copy()
        # Ruota faccia F (senso antiorario)
        self.blocks['F1'], self.blocks['F2'], self.blocks['F3'], self.blocks['F4'], self.blocks['F6'], self.blocks['F7'], self.blocks['F8'], self.blocks['F9'] = \
        temp['F3'], temp['F6'], temp['F9'], temp['F2'], temp['F8'], temp['F1'], temp['F4'], temp['F7']
        # Ruota lati
        self.blocks['U7'], self.blocks['U8'], self.blocks['U9'] = temp['R1'], temp['R4'], temp['R7']
        self.blocks['R1'], self.blocks['R4'], self.blocks['R7'] = temp['D3'], temp['D2'], temp['D1']
        self.blocks['D1'], self.blocks['D2'], self.blocks['D3'] = temp['L9'], temp['L6'], temp['L3']
        self.blocks['L3'], self.blocks['L6'], self.blocks['L9'] = temp['U9'], temp['U8'], temp['U7']
        logging.info("Rotated face F (counter-clockwise) and updated adjacent sides.")

    # --- Metodi Faccia Posteriore (BACK) ---
    def B(self):
        temp = self.blocks.copy()
        # Ruota faccia B (senso orario)
        self.blocks['B1'], self.blocks['B2'], self.blocks['B3'], self.blocks['B4'], self.blocks['B6'], self.blocks['B7'], self.blocks['B8'], self.blocks['B9'] = \
        temp['B7'], temp['B4'], temp['B1'], temp['B8'], temp['B2'], temp['B9'], temp['B6'], temp['B3']
        # Ruota lati
        self.blocks['U1'], self.blocks['U2'], self.blocks['U3'] = temp['R3'], temp['R6'], temp['R9']
        self.blocks['L1'], self.blocks['L4'], self.blocks['L7'] = temp['U3'], temp['U2'], temp['U1']
        self.blocks['D7'], self.blocks['D8'], self.blocks['D9'] = temp['L7'], temp['L4'], temp['L1']
        self.blocks['R3'], self.blocks['R6'], self.blocks['R9'] = temp['D9'], temp['D8'], temp['D7']
        logging.info("Rotated face B (clockwise) and updated adjacent sides.")

    def B_(self):
        temp = self.blocks.copy()
        # Ruota faccia B (senso antiorario)
        self.blocks['B1'], self.blocks['B2'], self.blocks['B3'], self.blocks['B4'], self.blocks['B6'], self.blocks['B7'], self.blocks['B8'], self.blocks['B9'] = \
        temp['B3'], temp['B6'], temp['B9'], temp['B2'], temp['B8'], temp['B1'], temp['B4'], temp['B7']
        # Ruota lati
        self.blocks['U1'], self.blocks['U2'], self.blocks['U3'] = temp['L7'], temp['L4'], temp['L1']
        self.blocks['L1'], self.blocks['L4'], self.blocks['L7'] = temp['D7'], temp['D8'], temp['D9']
        self.blocks['D7'], self.blocks['D8'], self.blocks['D9'] = temp['R9'], temp['R6'], temp['R3']
        self.blocks['R3'], self.blocks['R6'], self.blocks['R9'] = temp['U1'], temp['U2'], temp['U3']
        logging.info("Rotated face B (counter-clockwise) and updated adjacent sides.")

    # --- Metodi Faccia Destra (RIGHT) ---
    def R(self):
        temp = self.blocks.copy()
        # Ruota faccia R (senso orario)
        self.blocks['R1'], self.blocks['R2'], self.blocks['R3'], self.blocks['R4'], self.blocks['R6'], self.blocks['R7'], self.blocks['R8'], self.blocks['R9'] = \
        temp['R7'], temp['R4'], temp['R1'], temp['R8'], temp['R2'], temp['R9'], temp['R6'], temp['R3']
        # Ruota lati
        self.blocks['U3'], self.blocks['U6'], self.blocks['U9'] = temp['F3'], temp['F6'], temp['F9']
        self.blocks['F3'], self.blocks['F6'], self.blocks['F9'] = temp['D3'], temp['D6'], temp['D9']
        self.blocks['D3'], self.blocks['D6'], self.blocks['D9'] = temp['B7'], temp['B4'], temp['B1']
        self.blocks['B1'], self.blocks['B4'], self.blocks['B7'] = temp['U9'], temp['U6'], temp['U3']
        logging.info("Rotated face R (clockwise) and updated adjacent sides.")

    def R_(self):
        temp = self.blocks.copy()
        # Ruota faccia R (senso antiorario)
        self.blocks['R1'], self.blocks['R2'], self.blocks['R3'], self.blocks['R4'], self.blocks['R6'], self.blocks['R7'], self.blocks['R8'], self.blocks['R9'] = \
        temp['R3'], temp['R6'], temp['R9'], temp['R2'], temp['R8'], temp['R1'], temp['R4'], temp['R7']
        # Ruota lati
        self.blocks['U3'], self.blocks['U6'], self.blocks['U9'] = temp['B7'], temp['B4'], temp['B1']
        self.blocks['B1'], self.blocks['B4'], self.blocks['B7'] = temp['D9'], temp['D6'], temp['D3']
        self.blocks['D3'], self.blocks['D6'], self.blocks['D9'] = temp['F3'], temp['F6'], temp['F9']
        self.blocks['F3'], self.blocks['F6'], self.blocks['F9'] = temp['U3'], temp['U6'], temp['U9']
        logging.info("Rotated face R (counter-clockwise) and updated adjacent sides.")

    # --- Metodi Faccia Sinistra (LEFT) ---
    def L(self):
        temp = self.blocks.copy()
        # Ruota faccia L (senso orario)
        self.blocks['L1'], self.blocks['L2'], self.blocks['L3'], self.blocks['L4'], self.blocks['L6'], self.blocks['L7'], self.blocks['L8'], self.blocks['L9'] = \
        temp['L7'], temp['L4'], temp['L1'], temp['L8'], temp['L2'], temp['L9'], temp['L6'], temp['L3']
        # Ruota lati
        self.blocks['U1'], self.blocks['U4'], self.blocks['U7'] = temp['B9'], temp['B6'], temp['B3']
        self.blocks['B3'], self.blocks['B6'], self.blocks['B9'] = temp['D7'], temp['D4'], temp['D1']
        self.blocks['D1'], self.blocks['D4'], self.blocks['D7'] = temp['F1'], temp['F4'], temp['F7']
        self.blocks['F1'], self.blocks['F4'], self.blocks['F7'] = temp['U1'], temp['U4'], temp['U7']
        logging.info("Rotated face L (clockwise) and updated adjacent sides.")

    def L_(self):
        temp = self.blocks.copy()
        # Ruota faccia L (senso antiorario)
        self.blocks['L1'], self.blocks['L2'], self.blocks['L3'], self.blocks['L4'], self.blocks['L6'], self.blocks['L7'], self.blocks['L8'], self.blocks['L9'] = \
        temp['L3'], temp['L6'], temp['L9'], temp['L2'], temp['L8'], temp['L1'], temp['L4'], temp['L7']
        # Ruota lati
        self.blocks['U1'], self.blocks['U4'], self.blocks['U7'] = temp['F1'], temp['F4'], temp['F7']
        self.blocks['F1'], self.blocks['F4'], self.blocks['F7'] = temp['D1'], temp['D4'], temp['D7']
        self.blocks['D1'], self.blocks['D4'], self.blocks['D7'] = temp['B9'], temp['B6'], temp['B3']
        self.blocks['B3'], self.blocks['B6'], self.blocks['B9'] = temp['U7'], temp['U4'], temp['U1']
        logging.info("Rotated face L (counter-clockwise) and updated adjacent sides.")
    
    def rotate_face(self, face_number: int, counter_clockwise: bool = False) -> None:
        """
        Ruota una faccia del cubo.
        
        :param face_number: Numero della faccia da ruotare (1-6).
        :param counter_clockwise: Se True, ruota in senso antiorario.
        """
        if face_number == 1:
            self.U_() if counter_clockwise else self.U()
        elif face_number == 2:
            self.F_() if counter_clockwise else self.F()
        elif face_number == 3:
            self.R_() if counter_clockwise else self.R()
        elif face_number == 4:
            self.B_() if counter_clockwise else self.B()
        elif face_number == 5:
            self.L_() if counter_clockwise else self.L()
        elif face_number == 6:
            self.D_() if counter_clockwise else self.D()
        else:
            raise ValueError("Numero della faccia non valido. Deve essere tra 1 e 6.")