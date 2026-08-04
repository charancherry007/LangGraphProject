class BaseAgent:
    def validate(self,state): return True
    def execute(self,state): raise NotImplementedError
