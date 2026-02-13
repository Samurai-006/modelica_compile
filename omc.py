from OMPython import OMCSessionZMQ
import matplotlib.pyplot as plt
from DyMat import DyMatFile

omc=OMCSessionZMQ()

class Model:
    def __init__(self,model_name:str,model_path:str):
        self.model_name=model_name
        self.model_path=model_path

    def get_model_class(self)->str:
        return self.model_cls[0]
    
    def get_model_path(self)->str:
        return self.model_path
    
    def load_model(self):
        omc.sendExpression(rf'cd("{self.get_model_path()}")')
        print("\nLoading Modelica Libraries")
        if omc.sendExpression('loadModel(Modelica)'):
            print("\nModelica loaded successfully")
        else:
            print("\nLoading Modelica libraries unsuccessful")
        print(f"\nLoading the model:{self.model_name}")
        if omc.sendExpression(f'loadFile("{self.model_name}.mo")'):
            print(f"\nLoaded model {self.model_name}")
        else:
            print(f"\nLoading model {self.model_name} unsuccessful")

        print("\nGetting class name...")
        classes=omc.sendExpression("getClassNames(recursive=true,qualified=true)")
        self.model_cls=[cls for cls in classes if omc.sendExpression(f"isModel({cls})")]
        print(f"Models:\n{self.model_cls}")
'''
    def run_cmds(self,cmds:list):
        for i, cmd in enumerate(cmds):
            print(f"{i}. "+omc.sendExpression(f"{cmd}"))

class Libraries:
    list_of_libraries=set()
    def __init__(self,list_of_libraries:List):
            for lib in self.list_of_libraries:
                 if lib not in list_of_libraries:
                    list_of_libraries.add(lib)
'''
class Compilation:
    def compile_and_simulate(self,model:Model,sim_time=""):
        print("\nInstantiating Model...")
        print("\nResults:",omc.sendExpression(f"instantiateModel({model.model_cls[0]})"))
        print("\nSimulating...")
        if not sim_time.strip():
            result=omc.sendExpression(f"simulate({model.model_cls[0]})")
        else:
            result=omc.sendExpression(f"simulate({model.model_cls[0]},stopTime={int(sim_time)})")
        return result    

    def get_results(self,model:Model,variables:list):
        res=DyMatFile(f"{model.get_model_path()}/{model.model_cls[0]}_res.mat")
        time=res.abscissa(variables[0],valuesOnly=True)
        for v in variables:
            data_v=res.data(v)
            plt.plot(time,data_v,label=v)

        plt.xlabel("Time")
        plt.ylabel("values")
        plt.legend()
        plt.show()

model_name=input("\nEnter the model name(should be of '.mo' format): ")
model_path=input("\nEnter the path the model exists (replace '\\' with '/'): ")
model=Model(model_name,model_path)
model.load_model()
'''
flag=int(("\nEnter 1 if you want to run any additional omc cmds:"))
if flag:
    cmds=list()
'''

compiler=Compilation()
sim_res=compiler.compile_and_simulate(model,sim_time=(input("\nEnter simulation time (if left blank default simulation will run):")))
if isinstance(sim_res,dict):
    print("Result file:",sim_res["resultFile"])
else:
    print("Simulation error:",sim_res)
variables=list()
variables.extend(input("\nEnter the variables you need to be plotted (seperate with whitspace): ").split())
compiler.get_results(model,variables)
