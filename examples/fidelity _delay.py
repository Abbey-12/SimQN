import math
import numpy as np
import matplotlib.pyplot as plt  # Corrected the alias

initial_fidelity = 0.99
decoherence_rate = 0.1
time_read_write = 2


fideliy = []
for delay in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]:
    new_fidelity = (((initial_fidelity * 4) - 1) * np.exp(-decoherence_rate*2*time_read_write * delay*9 ))/ 3
    fideliy.append(new_fidelity)

plt.plot([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1], fideliy)
plt.show()


# # Define the range for the variable x
# x_values = np.linspace(0, 4, 100)  # Example range from 0 to 10

# # Compute the corresponding exponential values
# exponential_values = np.exp(-0.3 * x_values)

# # Plot the exponential curve
# plt.plot(x_values, exponential_values, label=r'$e^{-0.3x}$')
# plt.xlabel('x')
# plt.ylabel('e^{-0.3x}')
# plt.title('Exponential Curve: e^{-0.3x}')
# plt.legend()
# plt.grid(True)
# plt.show()