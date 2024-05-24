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

# constrains
init_fidelity = 0.99
nodes_number = 20
lines_number = 19
qchannel_delay = 0.05
cchannel_delay = 0.05
memory_capacity = 50
send_rate = 10
number_simulation = 10


nodes_number = 10
fidelity_dict={}
throughput_dict={}
drop_dict={}

# for nodes_number in range(2, 5):

for sim in range(number_simulation):
    fidelity = []
    throughput =[]
    drop_rate=[]
    for delay in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]:
        s = Simulator(0, 30, accuracy=10000000)
        log.install(s)
        topo = LineTopology(nodes_number=10,
                            qchannel_args={"delay": 0},
                            cchannel_args={"delay": delay, "drop_rate":0},
                            memory_args=[{
                                "capacity": memory_capacity,
                                "decoherence_rate": 0.1}],
                            nodes_apps=[EntanglementDistributionApp(init_fidelity=init_fidelity)])

        net = QuantumNetwork(
            topo=topo, classic_topo=ClassicTopology.All, route=DijkstraRouteAlgorithm())
        net.build_route()

        src = net.get_node("n1")
        dst = net.get_node(f"n{nodes_number}")
        net.add_request(src=src, dest=dst, attr={"send_rate": send_rate})
        net.install(s)
        s.run()
        success_count= dst.apps[-1].success_count
        
        send_count= src.apps[0].send_count
        failed_count= send_count - success_count
        throughput.append(dst.apps[0].success_count / s.time_spend)  
   
        drop= failed_count / s.time_spend
        drop_rate.append(drop)
        # print(s.time_spend)
        fidelity.append(dst.apps[-1].success[0].fidelity)
        # log.monitor(f"{nodes_number} {fidelity[0]}")

    fidelity_dict[sim]= fidelity   
    throughput_dict[sim]=throughput
    drop_dict[sim]=drop_rate
        
# Calculate averages
averages = []

# Iterate over each index position in the lists
for i in range(len(fidelity_dict[0])):
    # Initialize sum for this index position
    index_sum = 0
    
    # Calculate sum of values at this index position across all keys
    for key in fidelity_dict:
        index_sum += fidelity_dict[key][i]
    
    # Calculate average for this index position and append to averages list
    averages.append(index_sum / len(fidelity_dict))

print(averages)


# # Plot averages
# plt.plot([0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1], avg_fidelity.values(), label='Average Fidelity')
# plt.xlabel('Delay')
# plt.ylabel('Average Fidelity')
# plt.legend()
# plt.show()

plt.plot([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1], averages, label='fidelity')
plt.xlabel('Delay')
plt.ylabel('Fidelity')
plt.legend()
plt.show()

# plt.plot([0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1], avg_drop_rate.values(), label='Average Drop Rate')
# plt.xlabel('Delay')
# plt.ylabel('Average Drop Rate')
# plt.legend()
# plt.show()






# # print(throughput_dict)
# # last_node = None
# # for node_number, drop_rate in throughput_dict.items():
# #     if last_node is None:
# #         last_node = node_number
# #     else:
# #         if node_number > last_node:
# #             last_node = node_number
# # plt.plot([0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1],drop_rate,label=f'{nodes_number} nodes' )
# # plt.xlabel('channel drop rate')
# # plt.ylabel ('Drop_rate')
# # plt.legend()


# # #  fideity vs numberde of nodes plot
# # print(drop_rate)
# # fig, ax= plt.subplots(nrows=2, ncols=2)

# # nodes_number= range(2,20)
# # ax[0,0].plot(nodes_number, fidelity)
# # # ax[0,0].xticks(nodes_number, [str(int(i)) for i in nodes_number])
# # ax[0,0].set_title( 'nodes_number vs fidelity')

# # ax[0,1].plot(nodes_number, throughput)
# # # ax[0,1].xticks(nodes_number, [str(int(i)) for i in nodes_number])
# # ax[0,1].set_title( 'nodes_number vs throughput')

# # ax[1,0].plot(nodes_number, drop_rate)
# # # ax[1,0].xticks(nodes_number, [str(int(i)) for i in nodes_number])
# # ax[1,0].set_title( 'nodes_number vs drop rate')


# # plt.subplots_adjust(wspace=0.5, hspace=0.5)

# # plt.xlabel('number of nodes in the network')
# # plt.ylabel('fidelity')
# # plt.show()

# # # throughput vs number of  nodes  in the network
# # plt.plot(nodes_number, throughput)
# # plt.xticks(nodes_number, [str(int(i)) for i in nodes_number])

# # plt.xlabel('number of nodes in the network')
# # plt.ylabel('throughput')
# # plt.show()

# # #  drop rate vs number of  nodes inthe network
# # plt.plot(nodes_number, drop_rate)
# # plt.xticks(nodes_number, [str(int(i)) for i in nodes_number])

# # plt.xlabel('number of nodes in the network')
# # plt.ylabel('drop_rate')
# # plt.show()