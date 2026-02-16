from OMPython import OMCSessionZMQ
omc=OMCSessionZMQ

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