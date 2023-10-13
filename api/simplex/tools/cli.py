from api.simplex.sub_classes import TargetType
from api.simplex.sub_classes import FullEquation
from api.simplex.sub_classes import Sign

def define_simplex_from_cmd():
    func_obj = TargetType.from_string(
        input("Input the objective of your objective function (Minimize or Maximise):"))
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
        constraint_sing = Sign.from_string(
            input(f"Enter the sign of the constraint n°{i} (Between : >=, =, <=):"))
        if constraint_sing is None:
            print("The constraint that you gave is incorrect")
            return
        result = int(input(f"Enter the right-hand side values of the constraint n°{i}:"))

        full_equations.append(FullEquation(constraint_vals, constraint_sing, result))

    s = Simplex(target, func_obj, full_equations)
    s.resolve()