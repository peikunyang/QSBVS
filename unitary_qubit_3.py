import pennylane as qml
import numpy as np
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=3)

def recursive_amplitude_encoding(states, alpha):
    length = len(states)
    if length == 2:
        alpha0 = -2.0 * np.arctan2(states[1], states[0])
        alpha.append(alpha0)
    elif length > 2:
        half = length // 2
        norm_top = np.linalg.norm(states[:half])
        norm_bottom = np.linalg.norm(states[half:])
        alpha0 = -2.0 * np.arctan2(norm_bottom, norm_top)
        alpha.append(alpha0)
        recursive_amplitude_encoding(states[:half], alpha)
        recursive_amplitude_encoding(states[half:], alpha)

def gen_angles(states):
    n = int(np.log2(len(states)))
    alpha = []
    recursive_amplitude_encoding(states, alpha)
    return alpha

@qml.qnode(dev)
def circuit(params):
    qml.ctrl(qml.RY, control=[0,1], control_values=[0,0])(params[2], wires=2)
    qml.ctrl(qml.RY, control=[0,1], control_values=[0,1])(params[3], wires=2)
    qml.ctrl(qml.RY, control=[0,1], control_values=[1,0])(params[5], wires=2)
    qml.ctrl(qml.RY, control=[0,1], control_values=[1,1])(params[6], wires=2)
    qml.ctrl(qml.RY, control=[0], control_values=[0])(params[1], wires=1)
    qml.ctrl(qml.RY, control=[0], control_values=[1])(params[4], wires=1)
    qml.RY(params[0], wires=0)
    return qml.state()

def Out_Uni(matrix):
    real_matrix = np.real(matrix)
    with open("uni_mat.txt", "w") as file:
        for i in range(real_matrix.shape[0]):
            for j in range(real_matrix.shape[1]):
                file.write(f"{real_matrix[i, j]:9.3f} ")
                if (j + 1) % 8 == 0:  # 每行8個數值
                    file.write("\n")
            if (real_matrix.shape[1] % 8) != 0:
                file.write("\n")  # 保證每行結束後換行

def Read_states():
    with open('vector_3.txt', 'r') as file:
        first_row = np.array([float(line.strip()) for line in file])
    return first_row

def Main():
    first_row = Read_states()
    params = gen_angles(first_row)
    print('params',params)
    matrix = qml.matrix(circuit)(params)
    Out_Uni(matrix)
    drawer = qml.draw(circuit)
    print(drawer(params))
    print('first_row', first_row)

Main()

