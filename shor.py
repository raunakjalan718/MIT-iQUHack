import qiskit
from qiskit import QuantumCircuit, transpile, Aer, assemble
from qiskit.visualization import plot_histogram
import numpy as np
import time


n_qubits_x = 8  
n_qubits_fx = 2*n_qubits_x 

qc = QuantumCircuit(n_qubits_x + n_qubits_fx, n_qubits_x)


for i in range(n_qubits_x):
    qc.h(i)

for i in range(n_qubits_x):
    qc.cx(i, n_qubits_x + i) 

def qft(qc, n):
    """Creates the quantum fourier transform operation using Qiskit gates"""
    for j in range(n):
      for k in range(j):
        qc.cp(np.pi/(2**(j-k)),k,j)
      qc.h(j)
    return qc

qc = qft(qc, n_qubits_x)


for i in range(n_qubits_x):
    qc.measure(i, i)

simulator = Aer.get_backend('qasm_simulator')

start = time.time()
compiled_circuit = transpile(qc, simulator)
job = simulator.run(compiled_circuit, shots=1000)
result = job.result()
counts = result.get_counts(qc)
end = time.time()

print("counts: ", counts)
print("Time taken: ", end - start)
plot_histogram(counts).show()