from sympy.logic.boolalg import to_cnf

class Belief:
    
    formula: str
    cnf: str

    def __init__(self, formula: str, weight: int):
        self.formula = formula
        self.cnf = to_cnf(formula)
        self.weight = weight

    def __repr__(self):
        return self.formula

    def get_weight(self):
        return self.weight
