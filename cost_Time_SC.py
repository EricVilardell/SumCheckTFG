import random
import time
import re

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def custom_polynomial(x, polynomial_str):
    global operation_count
    operation_count += 1
    return eval(polynomial_str, {}, {f"x{i+1}": x[i] for i in range(len(x))}) % FIELD_PRIME

def sum_over_boolean_hypercube(f, num_vars, polynomial_str):
    global operation_count
    total = 0
    for i in range(2**num_vars):
        point = [(i >> j) & 1 for j in reversed(range(num_vars))]
        total = (total + f(point, polynomial_str)) % FIELD_PRIME
        operation_count += 1
    return total

def interpolate_1d(vals):
    global operation_count
    operation_count += 1
    return lambda x: (vals[0] * (1 - x) + vals[1] * x) % FIELD_PRIME

def random_field_element():
    return random.randint(0, FIELD_PRIME - 1)

def get_number_of_variables(polynomial_str):
    variables = re.findall(r'x(\d+)', polynomial_str)
    return max([int(var) for var in variables])

def main():
    global operation_count
    operation_count = 0 
    
    while True:
        global FIELD_PRIME
        FIELD_PRIME = int(input("Enter a prime number modulus (e.g., 17): "))
        if is_prime(FIELD_PRIME):
            break
        else:
            print(f"{FIELD_PRIME} is not a prime number. Please enter a valid prime number.")

    polynomial_str = input("Enter the polynomial in terms of x1, x2, ..., xn (e.g., x1*x2 + x3 + x4): ")

    num_vars = get_number_of_variables(polynomial_str)
    print(f"Automatically detected the number of variables: {num_vars}")

    start_time = time.time() 
    
    total_sum = sum_over_boolean_hypercube(custom_polynomial, num_vars, polynomial_str)
    print(f"[Prover] Claimed sum over Boolean Hypercube: {total_sum}")

    r_vals = []

    for i in range(num_vars):
        print(f"\n=== Round {i+1} ===")
        g_vals = [0, 0]
        
        for b in [0, 1]:
            def sub_f(y, polynomial_str=polynomial_str):
                point = r_vals + [b] + y
                padded_point = point + [0] * (num_vars - len(point))
                return custom_polynomial(padded_point, polynomial_str)
            
            g_vals[b] = sum_over_boolean_hypercube(sub_f, num_vars - (i + 1), polynomial_str)

        g = interpolate_1d(g_vals)
        print(f"[Prover] Sends univariate polynomial g_{i+1}(x): g(0) = {g_vals[0]}, g(1) = {g_vals[1]}")

        if sum(g_vals) % FIELD_PRIME != total_sum:
            print("[Verifier] Sum does not match! Abort.")
            return

        r = random_field_element()
        print(f"[Verifier] Picks random r_{i+1} = {r}")
        r_vals.append(r)
        total_sum = g(r)

    final_val = custom_polynomial(tuple(r_vals), polynomial_str)
    print(f"\n[Verifier] Evaluates f at r = {r_vals}, gets: {final_val}")
    print(f"[Verifier] Final check passed: {final_val == total_sum}")
    
    end_time = time.time() 
    elapsed_time = end_time - start_time 
    
    print(f"\n[Efficiency] Total operations performed: {operation_count}")
    print(f"[Efficiency] Total time taken: {elapsed_time:.4f} seconds")

if __name__ == "__main__":
    main()