from OMPython import OMCSessionZMQ
from model import Model
import matplotlib as plt
from DyMat import DyMatFile
omc=OMCSessionZMQ()


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