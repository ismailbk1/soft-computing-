import json
from ocvrp import algorithms as algo
from ocvrp.cvrp import CVRP
from ocvrp.util import CVRPEncoder

# The path to the .ocvrp file is the problem set for this instance
cvrp = CVRP("./data/A-n54-k7.ocvrp", cxpb=0.85, ngen=50_000, pgen=True, plot=True, cx_algo=algo.cycle_xo,mt_algo=algo.inversion_mut,verbose_routes=True)

# Result contains a dict of information about the run which includes the best individual found 
result = cvrp.run()

# Save the matplotlib object to a file (only if plot=True)
result['mat_plot'].savefig("A-n54-k7-Run1.png", bbox_inches='tight')

js_res = json.dumps(obj=result, cls=CVRPEncoder, indent=2)
print(js_res)

cvrp.reset()