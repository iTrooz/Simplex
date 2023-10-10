import argparse

from api.simplex import Simplex

from api.simplex.sub_classes import FullEquation

from api.simplex.tools import get_target_from_string
from api.simplex.tools import get_sign_from_string

def simplex_api():
    func_obj = get_target_from_string(input("Input the objective of your objective function (Minimize or Maximise):"))
    if func_obj is None:
        print("The objective that you gave is incorrect")
        return
    obj_func_var_nb = int(input("Input the number of decision variables in your objective function:"))
    constraints_nb = int(input("Input the number of constraints in the constraint set:"))

    target = []
    for i in range(obj_func_var_nb):
        target.append(int(input(f"Enter the value for the decision variable n°{i}:")))

    full_equations = []
    for i in range(constraints_nb):
        constraint_vals = []
        for j in range(obj_func_var_nb):
            constraint_vals.append(int(input(f"Enter the variable n°{j} of the constraint n°{i}:")))
        constraint_sing = get_sign_from_string(input(f"Enter the sign of the constraint n°{i} (Between : >=, =, <=):"))
        if constraint_sing is None:
            print("The constraint that you gave is incorrect")
            return
        result = int(input(f"Enter the right-hand side values of the constraint n°{i}:"))

        full_equations.append(FullEquation(constraint_vals, constraint_sing, result))

    s = Simplex(target, func_obj, full_equations)
    s.resolve()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Maths project for different computations')
    parser.add_argument('-c', '--computation', type=str, default='simplex',
                        choices=['simplex'],
                        help="Type of computation")
    parser.add_argument('--ui', type=bool, default=False, help='Use the user interface')

    args = parser.parse_args()

    match args.computation:
        case "simplex":
            simplex_api()
        case _:
            print("The computation type selected doesnt exist")