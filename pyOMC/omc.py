from OMPython import OMCSessionZMQ
from model import Model
from compile import Compilation
omc=OMCSessionZMQ()


model_name=input("\nEnter the model name(should be of '.mo' format): ")
model_path=input("\nEnter the path the model exists (replace '\\' with '/'): ")
model=Model(model_name,model_path)
model.load_model()
compiler=Compilation()
sim_res=compiler.compile_and_simulate(model,sim_time=(input("\nEnter simulation time (if left blank default simulation will run):")))
if isinstance(sim_res,dict):
    print("Result file:",sim_res["resultFile"])
else:
    print("Simulation error:",sim_res)
variables=list()
variables.extend(input("\nEnter the variables you need to be plotted (seperated with whitespace): ").split())
compiler.get_results(model,variables)
