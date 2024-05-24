import logging
import matplotlib.pyplot as plt

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
memory_capacity = 10
send_rate = 100

nodes_number = 10
result_dict={}

for nodes_number in range(2, 4):
    result = []
    for delay in [0.1, 0.07, 0.05, 0.03]:
        s = Simulator(0, 30, accuracy=10000000)
        log.install(s)
        topo = LineTopology(nodes_number=nodes_number,
                            qchannel_args={"delay": delay},
                            cchannel_args={"delay": delay, "drop_rate": 0.5,"bandwidth": 1000000000},
                            memory_args=[{
                                "capacity": memory_capacity,
                                "decoherence_rate": 0.9}],
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
        print(success_count)
        print(send_count)
        print(failed_count)
        result.append(dst.apps[-1].success[0].fidelity)
    result_dict[nodes_number]= result    
    # log.monitor(f"{nodes_number} {result[0]} {result[1]} {result[2]} {result[3]}")

print(result_dict)
for node_number, result in result_dict.items():

    plt.plot([0.1, 0.07, 0.05,0.03], result, label=f'{node_number} node')
    plt.xlabel('delay')
    plt.ylabel('fidelity')
    plt.show()