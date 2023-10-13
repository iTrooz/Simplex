import argparse

from api.simplex import Simplex

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Maths project for different computations')
    parser.add_argument('-c', '--computation', type=str, default='simplex_cmd',
                        choices=['simplex_cmd'],
                        help="Type of computation")
    parser.add_argument('--ui', type=bool, default=False, help='Use the user interface')

    args = parser.parse_args()

    match args.computation:
        case "simplex_cmd":
            Simplex.define_simplex_from_cmd()
        case _:
            print("The computation type selected doesnt exist")