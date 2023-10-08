from typing import List
from fractions import Fraction

from colorama import Fore
from sympy import symbols, Expr

M = symbols("M")

class TargetType:
    MAX = "max"
    MIN = "min"

class Sign:
    SMALLER_EQ = "<="
    GREATER_EQ = ">="
    EQ = "="

def init2DArray(columns, rows, content=None):
    arr = []
    for _ in range(rows):
        arr.append([content] * columns)
    return arr
        
def print2DArray(mat):
    for line in mat:
        print("\t".join(map(str, line)))

def auto_str(cls):
    """
    From https://stackoverflow.com/a/33800620
    """
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    cls.__repr__ = __str__
    return cls


class FullEquation:
    def __init__(self, coeffs: List[int], sign: Sign, result: int):
        self.coeffs = coeffs
        self.sign = sign
        self.result = result

    def __repr__(self):
        coeffsStr = ""
        for i, coeff in enumerate(self.coeffs):
            if coeff == 0: continue
            elif coeff == 1:
                coeffsStr += f"x{i+1} + "
            else:
                coeffsStr += f"{coeff}*x{i+1} + "


        return f"({coeffsStr[:-3]} {self.sign} {self.result})"

@auto_str
class Variable:
    def __init__(self, name: str, value: Expr, equ_values: List[int]):
        self.value = value
        self.name = name
        self.equ_values = equ_values

@auto_str
class EquationMeta:
    def __init__(self, vb: str, coeff_vb: Expr, value: int):
        self.vb = vb
        self.coeff_vb = coeff_vb
        self.value = value

@auto_str
class Simplex:
    def __init__(self, target: List[int], target_type, full_equations: List[FullEquation]):
        self.pivot_coords = None
        self.target: List[int] = target
        self.target_type: TargetType = target_type

        # Current variables and their values, including x, A, and S variables. Will be modified with each iteration
        self.variables: List[Variable] = []
        # Equations metadata. Will be modified with each iteration
        self.equations: List[EquationMeta] = []

        # setup x variables
        for i, value in enumerate(target):

            # get the value of the xi variable for all equations
            equ_values = []
            for equation in full_equations:
                equ_values.append(equation.coeffs[i])

            # create the variable
            self.variables.append(Variable(name=f"x{i+1}", value=value, equ_values=equ_values))
        
        # setup equations, and their corresponding A and S variables
        counter = 1
        for i, equation in enumerate(full_equations):
            # create the array representing the A or S variable values
            equ_values = [0] * len(full_equations)
            equ_values[i] = 1

            if equation.sign == Sign.GREATER_EQ or equation.sign == Sign.EQ:
                var_name = f"A{counter}"
                # Create the equation
                self.equations.append(EquationMeta(vb=var_name, coeff_vb=-M, value=equation.result))
                # Create the corresponding A variable
                self.variables.append(Variable(name=var_name, value=-M, equ_values=equ_values))
                counter+=1
            elif equation.sign == Sign.SMALLER_EQ:
                var_name = f"S{counter}"
                # Create the equation
                self.equations.append(EquationMeta(vb=var_name, coeff_vb=0, value=equation.result))
                # Create the corresponding S variable
                self.variables.append(Variable(name=var_name, value=0, equ_values=equ_values))
                counter+=1
        
        # Name of all variables that has been present at some point. Will not be modified during iteration
        self.variable_names = [variable.name for variable in self.variables]

    def calculateCosts(self):

        # Calculate the costs (second to last) line
        self.costs = []
        for variable in self.variables:
            res = 0
            for equ_n, equation in enumerate(self.equations):
                res += equation.coeff_vb * variable.equ_values[equ_n]
            self.costs.append(res)
        
        # Calculate the reduced costs (last) line
        self.reduced_costs = []
        for var, cost in zip(self.variables, self.costs):
            self.reduced_costs.append(var.value - cost)

    def find_pivot(self) -> False:
        """
        Return false is no pivot could be found, else true
        """
        reduced_costs = []
        for exp in self.reduced_costs:
            if isinstance(exp, Expr):
                reduced_costs.append(exp.evalf(subs={M:10**10}))
            else:
                reduced_costs.append(exp)

        # verify exit condition
        if self.target_type == TargetType.MAX:
            if max(reduced_costs) <= 0:
                self.pivot_coords = None
                return False
        elif self.target_type == TargetType.MIN:
            if min(reduced_costs) >= 0:
                self.pivot_coords = None
                return False

        if self.target_type == TargetType.MAX:
            # get index of greatest value
            selected_var_col = reduced_costs.index(sorted(reduced_costs)[-1])
        else:
            # get index of smallest value
            selected_var_col = reduced_costs.index(sorted(reduced_costs)[0])
        
        variable = self.variables[selected_var_col]
        L = []
        for i, equation in enumerate(self.equations):
            L.append(equation.value / variable.equ_values[i])

        # get index of smallest value (positive only)
        row_index = L.index(sorted(filter(lambda x: x > 0, L))[0])

        self.pivot_coords = (row_index, selected_var_col)

        return True


    def show(self):
        vis = init2DArray(columns=len(self.variables) + 3, rows=len(self.equations) + 2 + 2, content="")

        # Variable metadata
        for i, var in enumerate(self.variables):
            vis[0][i+3] = var.value
            vis[1][i+3] = var.name

        # Equation header
        vis[1][0] = "Coeff VB"
        vis[1][1] = "VB"
        vis[1][2] = "Value"

        # Equation metadata
        for i, equation in enumerate(self.equations):
            vis[i+2][0] = equation.coeff_vb
            vis[i+2][1] = equation.vb
            vis[i+2][2] = equation.value

        # variable values
        for var_n, var in enumerate(self.variables):
            for equ_n, equation in enumerate(self.equations):
                vis[equ_n+2][var_n+3] = var.equ_values[equ_n]

        # costs
        for i, cost in enumerate(self.costs):
            vis[-2][i+3] = cost

        # reduced costs
        for i, reduced_cost in enumerate(self.reduced_costs):
            vis[-1][i+3] = reduced_cost

        # set pivot color
        if self.pivot_coords:
            pivot = vis[self.pivot_coords[0]+2][self.pivot_coords[1]+3]
            vis[self.pivot_coords[0]+2][self.pivot_coords[1]+3] = f"{Fore.BLUE}{pivot}{Fore.RESET}"
        
        print2DArray(vis)

    
    def update(self):
        # get pivot and pivot-related variables
        pivot_var_n = self.pivot_coords[1]
        pivot_var = self.variables[pivot_var_n]
        pivot = pivot_var.equ_values[self.pivot_coords[0]]
        pivot_equation_n = self.pivot_coords[0]
        pivot_equation = self.equations[pivot_equation_n]

        # delete exit variable
        for variable in self.variables:
            if variable.name == pivot_equation.vb:
                self.variables.remove(variable)
                break
        
        # update equation of exit variable
        pivot_equation.vb = pivot_var.name
        pivot_equation.coeff_vb = pivot_var.value

        # update values
        for equ_n, equation in enumerate(self.equations):
            # update equation values
            if equation == pivot_equation:
                equation.value = Fraction(equation.value, pivot)
            else:
                product = pivot_equation.value * pivot_var.equ_values[equ_n]
                equation.value = equation.value - Fraction(product, pivot)
        
            # for each equation, update its variables' value
            for variable in self.variables:
                if equation == pivot_equation:
                    variable.equ_values[equ_n] = Fraction(variable.equ_values[equ_n], pivot)
                else:
                    product = variable.equ_values[pivot_equation_n] * pivot_var.equ_values[equ_n]
                    variable.equ_values[equ_n] = variable.equ_values[equ_n] - Fraction(product, pivot)
        



    def step(self) -> bool:
        """
        Execute a step (one table) to resole the simplex
        return True if we shuld continue, False is there is no improvement possible
        """

        # condition is a special case for the first iteration
        if self.pivot_coords != None:
            self.update()

        self.calculateCosts()
        should_continue = self.find_pivot()

        self.show()

        return should_continue
    
    def resolve(self):
        """
        Resolve the simplex and print the solution"
        """
        should_continue = True
        table_n = 1
        while should_continue:
            print(f"Table {table_n} " + "-"*100)
            table_n+=1
            should_continue = self.step()
        
        print("Resolved ! Values:")
        for var_name in self.variable_names:
            for equation in self.equations:
                if equation.vb == var_name:
                    print(f"{var_name}={equation.value}")
                    break
            else:
                print(f"{var_name}=0")




# ------- CONFIG

target = [5, 2]
target_type = TargetType.MAX

full_equations = [
    FullEquation([3, 4], Sign.SMALLER_EQ, 60),
    FullEquation([-1, -8], Sign.SMALLER_EQ, 22),
    FullEquation([-2, 3], Sign.EQ, 43)
]

s = Simplex(target, target_type, full_equations)
s.resolve()
