from api.simplex.tools import auto_str
from api.simplex.tools import init2DArray
from api.simplex.sub_classes import TargetType
from api.simplex.sub_classes import FullEquation
from api.simplex.sub_classes import EquationMeta
from api.simplex.sub_classes import Variable
from api.simplex.sub_classes import Sign

from typing import List, Tuple
from fractions import Fraction

from colorama import Fore
from sympy import symbols, Expr
import tabulate
import copy

@auto_str
class Simplex:
    def __init__(self, target: List[int], target_type: TargetType, full_equations: List[FullEquation]):
        self.__M = symbols("M")

        self.pivot_coords: Tuple[int] = None
        self.target: List[int] = target
        self.target_type = target_type

        # Current variables and their values, including x, A, and S variables. Will be modified with each iteration
        self.variables: List[Variable] = []
        # Equations metadata. Will be modified with each iteration
        self.equations: List[EquationMeta] = []

        # Setup the sign for artificial values
        match self.target_type:
            case TargetType.MIN:
                artificial_sign = self.__M
            case TargetType.MAX:
                artificial_sign = -self.__M

        # setup x variables
        for i, value in enumerate(target):

            # get the value of the xi variable for all equations
            equ_values = []
            for equation in full_equations:
                equ_values.append(equation.coeffs[i])

            # create the variable
            self.variables.append(Variable(name=f"x{i + 1}", value=value, equ_values=equ_values))

        # setup equations, and their corresponding A and S variables
        counter = 1
        for i, equation in enumerate(full_equations):
            # create the array representing the A or S variable values
            equ_values = [0] * len(full_equations)
            equ_values[i] = 1
            match equation.sign:
                case Sign.GREATER_EQ:
                    # Create the Excess value
                    var_name = f"E{counter}"
                    # Create the corresponding E variable
                    e_values = equ_values.copy()
                    e_values[i] = -1
                    self.variables.append(Variable(name=var_name, value=0, equ_values=e_values))

                    # Create the artificial value
                    var_name = f"A{counter}"
                    # Create the equation
                    self.equations.append(EquationMeta(vb=var_name, coeff_vb=artificial_sign, value=equation.result))
                    # Create the corresponding A variable
                    self.variables.append(Variable(name=var_name, value=artificial_sign, equ_values=equ_values))
                    counter += 1
                case Sign.EQ:
                    var_name = f"A{counter}"
                    # Create the equation
                    self.equations.append(EquationMeta(vb=var_name, coeff_vb=artificial_sign, value=equation.result))
                    # Create the corresponding A variable
                    self.variables.append(Variable(name=var_name, value=artificial_sign, equ_values=equ_values))
                    counter += 1
                case Sign.SMALLER_EQ:
                    var_name = f"S{counter}"
                    # Create the equation
                    self.equations.append(EquationMeta(vb=var_name, coeff_vb=0, value=equation.result))
                    # Create the corresponding S variable
                    self.variables.append(Variable(name=var_name, value=0, equ_values=equ_values))
                    counter += 1

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

    def find_pivot(self) -> bool:
        """
        Return false is no pivot could be found, else true
        """
        reduced_costs = []
        for exp in self.reduced_costs:
            if isinstance(exp, Expr):
                reduced_costs.append(exp.evalf(subs={self.__M: 10 ** 10}))
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
            try:
                # Pivot's value should be >0
                # Meaning that if variable.equ_values[i] == 0 the value should be ignored because it can't be the pivot
                # To ignore the value we assume that it is equal to 0 (but it could be anything between ]-inf, 0])
                L.append(equation.value / variable.equ_values[i])
            except ZeroDivisionError:
                L.append(0)

        # get index of smallest value (positive only)
        row_index = L.index(sorted(filter(lambda x: x > 0, L))[0])

        self.pivot_coords = (row_index, selected_var_col)

        return True

    def show(self):
        vis = init2DArray(columns=len(self.variables) + 3, rows=len(self.equations) + 2 + 2, content="")

        # Variable metadata
        for i, var in enumerate(self.variables):
            vis[0][i + 3] = var.value
            vis[1][i + 3] = var.name

        # Equation header
        vis[1][0] = "Coeff VB"
        vis[1][1] = "VB"
        vis[1][2] = "Value"

        # Equation metadata
        for i, equation in enumerate(self.equations):
            vis[i + 2][0] = equation.coeff_vb
            vis[i + 2][1] = equation.vb
            vis[i + 2][2] = equation.value

        # variable values
        for var_n, var in enumerate(self.variables):
            for equ_n, equation in enumerate(self.equations):
                vis[equ_n + 2][var_n + 3] = var.equ_values[equ_n]

        # costs
        for i, cost in enumerate(self.costs):
            vis[-2][i + 3] = cost

        # reduced costs
        for i, reduced_cost in enumerate(self.reduced_costs):
            vis[-1][i + 3] = reduced_cost

        # set pivot color
        if self.pivot_coords:
            pivot = vis[self.pivot_coords[0] + 2][self.pivot_coords[1] + 3]
            vis[self.pivot_coords[0] + 2][self.pivot_coords[1] + 3] = f"{Fore.BLUE}{pivot}{Fore.RESET}"

        print(tabulate.tabulate(vis, tablefmt="simple_grid"))

    def update(self):
        # get pivot and pivot-related variables
        pivot_var_n = self.pivot_coords[1]
        pivot_var = self.variables[pivot_var_n]
        pivot = pivot_var.equ_values[self.pivot_coords[0]]
        pivot_equation_n = self.pivot_coords[0]
        pivot_equation = self.equations[pivot_equation_n]

        # delete exit variable if it's a A variable
        if pivot_equation.vb[0] == "A":
            for variable in self.variables:
                if variable.name == pivot_equation.vb:
                    self.variables.remove(variable)
                    break

        # Make a deepcopy for the computation of the next table
        equations_copy = copy.deepcopy(self.equations)
        variables_copy = copy.deepcopy(self.variables)

        # update equation of exit variable
        pivot_equation.vb = pivot_var.name
        pivot_equation.coeff_vb = pivot_var.value

        # Update values
        for i in range(len(self.equations)):
            if i == pivot_equation_n:
                self.equations[i].value = Fraction(self.equations[i].value, pivot)
                for variable in self.variables:
                    variable.equ_values[i] = Fraction(variable.equ_values[i], pivot)
            else:
                prod_1 = equations_copy[i].value * pivot
                prod_2 = equations_copy[pivot_equation_n].value * variables_copy[pivot_var_n].equ_values[i]
                self.equations[i].value = Fraction(prod_1 - prod_2, pivot)
                for j in range(len(self.variables)):
                    prod_1 = variables_copy[j].equ_values[i] * pivot
                    prod_2 = variables_copy[pivot_var_n].equ_values[i] * variables_copy[j].equ_values[pivot_equation_n]
                    self.variables[j].equ_values[i] = Fraction(prod_1 - prod_2, pivot)

    def step(self) -> bool:
        """
        Execute a step (one table) to resole the simplex
        return True if we should continue, False is there is no improvement possible
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
            print(f"\nTable {table_n}")
            table_n += 1
            should_continue = self.step()

        print("Resolved ! Values:")
        for var_name in self.variable_names:
            for equation in self.equations:
                if equation.vb == var_name:
                    print(f"{var_name}={equation.value}")
                    break
            else:
                print(f"{var_name}=0")
