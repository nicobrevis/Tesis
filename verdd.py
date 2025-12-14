import numpy as np
data = np.load('ddm_GTV-1.npz')
print(data.files)
matriz1 = data['indices']
matriz2 = data['indptr']
matriz3 = data['format']
matriz4 = data['shape']
matriz5 = data['data']
print("Matriz indices:", matriz1)
print("Matriz indptr:", matriz2)
print("Matriz format:", matriz3)
print("Matriz shape:", matriz4)
print("Matriz data:", matriz5)
