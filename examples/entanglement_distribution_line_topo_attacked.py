import logging
import matplotlib.pyplot as plt
import numpy as np
from qns.network.route.dijkstra import DijkstraRouteAlgorithm
from qns.network.topology.topo import ClassicTopology
from qns.simulator.simulator import Simulator
from qns.network import QuantumNetwork
from qns.network.topology import LineTopology
import qns.utils.log as log
from qns.network.protocol.entanglement_distribution import EntanglementDistributionApp


log.logger.setLevel(logging.INFO)


# # Parameters
# init_fidelity = 0.99
# nodes_number = 10
# lines_number = 9
# memory_capacity = 100
# send_rate = 50

# dUPF_QR = np.array([1, 10, 30, 20, 50, 70, 80, 100])

# avg_fidelities = []
# avg_throughputs = []
# avg_delays = []

# # Simulation loop for each nodes_number
# for nodes_number in range(2, 11):
#     delays = (dUPF_QR / 100000 + 0.0032) * (nodes_number - 1)
#     fidelities = []
#     throughputs = []
#     for delay in delays:
#         s = Simulator(0, 30, accuracy=10000000)
#         log.install(s)

#         # Create topology
#         topo = LineTopology(nodes_number=nodes_number,
#                              qchannel_args={"delay": 0, "drop_rate": 0},
#                              cchannel_args={"delay": delay, "drop_rate": 0},
#                              memory_args=[{"capacity": memory_capacity, "decoherence_rate": 5}],
#                              nodes_apps=[EntanglementDistributionApp(init_fidelity=init_fidelity)])

#         net = QuantumNetwork(
#             topo=topo, classic_topo=ClassicTopology.All, route=DijkstraRouteAlgorithm())
#         net.build_route()

#         src = net.get_node("n1")
#         dst = net.get_node(f"n{nodes_number}")
#         net.add_request(src=src, dest=dst, attr={"send_rate": send_rate})
#         net.install(s)
#         s.run()

#         # Retrieve results
#         success_count = dst.apps[-1].success_count
#         send_count = src.apps[0].send_count
#         failed_count = send_count - success_count
#         throughput = success_count / 30  # Calculate throughput

#         # Append results to lists
#         throughputs.append(throughput)
#         fidelities.append(dst.apps[-1].success[0].fidelity)

#     avg_fidelities.append(np.mean(fidelities))
#     avg_throughputs.append(np.mean(throughputs))
#     avg_delays.append(np.mean(delays))



# # Plotting
# fig, ax1 = plt.subplots(figsize=(10, 6))  # Create a larger figure

# color = 'tab:blue'
# ax1.set_xlabel('Latency',fontsize=16)
# ax1.set_ylabel('Fidelity', color=color, fontsize=16)
# ax1.plot(avg_delays, avg_fidelities , marker='o', linestyle='-', color=color, label="Fidelity vs Latency")
# ax1.tick_params(axis='y', labelcolor=color)
# ax1.grid(True)
# ax2 = ax1.twinx()  
# color = 'tab:red'
# ax2.set_ylabel('Throughput ', color=color, fontsize=16)
# ax2.plot(avg_delays, avg_throughputs, marker='s', linestyle='--', color=color, label=" Throughput vs Latency")
# ax2.tick_params(axis='y', labelcolor=color)
# # ax2.grid(True)
# # fig.tight_layout(pad=5)  
# # plt.title("Latency vs Throughput and Fidelity")
# fig.legend(loc="upper right", bbox_to_anchor=(0.8,0.85))

# plt.show()



# Parameters
init_fidelity = 0.99
nodes_number = 10
lines_number = 9
memory_capacity = 100
send_rate = 50

dUPF_QR = np.array([0.01])  # Set dUPF_QR to 100 for constant delay

fidelities = []
throughputs = []
drop_rates = (0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08,0.09, 0.1)  # Range of drop rates from 0 to 0.5

# Simulation loop for different node numbers
for nodes_number in range(4, 5):
    delays = (dUPF_QR / 100000 + 0.0032) * (nodes_number - 1)
    node_fidelities = []
    node_throughputs = []
    for drop_rate in drop_rates:
        s = Simulator(0, 30, accuracy=10000000)
        log.install(s)

        # Create topology
        topo = LineTopology(nodes_number=nodes_number,
                             qchannel_args={"delay": 0, "drop_rate": 0},
                             cchannel_args={"delay": delays, "drop_rate": drop_rate},
                             memory_args=[{"capacity": memory_capacity, "decoherence_rate": 5}],
                             nodes_apps=[EntanglementDistributionApp(init_fidelity=init_fidelity)])

        net = QuantumNetwork(
            topo=topo, classic_topo=ClassicTopology.All, route=DijkstraRouteAlgorithm())
        net.build_route()

        src = net.get_node("n1")
        dst = net.get_node(f"n{nodes_number}")
        net.add_request(src=src, dest=dst, attr={"send_rate": send_rate})
        net.install(s)
        s.run()

        # Retrieve results
        success_count = dst.apps[-1].success_count
        send_count = src.apps[0].send_count
        throughput = success_count / 30  # Calculate throughput

        node_fidelities.append(dst.apps[-1].success[0].fidelity)
        node_throughputs.append(throughput)

    fidelities.append(node_fidelities)
    throughputs.append(node_throughputs)

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))
color = 'tab:blue'
ax1.set_xlabel('Packet loss',fontsize=16)
ax1.set_ylabel('Fidelity', color=color, fontsize=16)
for i, node_fidelities in enumerate(fidelities):
    ax1.plot(drop_rates, node_fidelities, marker='o', linestyle='-', color=color, label='Fidelity')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Throughput', color=color,fontsize=16)
for i, node_throughputs in enumerate(throughputs):
    ax2.plot(drop_rates, node_throughputs, marker='s', linestyle='--', color=color, label='Throughput')
ax2.tick_params(axis='y', labelcolor=color)

# fig.tight_layout(pad=5)
# plt.title("Packet loss vs Fidelity and Throughput")
# lines1, labels1 = ax1.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()
# ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
fig.legend(loc="upper right", bbox_to_anchor=(0.8,0.85))
plt.show()






