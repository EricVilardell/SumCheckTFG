import random

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def custom_polynomial(x, polynomial_str):
    return eval(polynomial_str, {}, {f"x{i+1}": x[i] for i in range(len(x))}) % FIELD_PRIME

def sum_over_boolean_hypercube(f, num_vars, polynomial_str):
    total = 0
    for i in range(2**num_vars):
        point = [(i >> j) & 1 for j in reversed(range(num_vars))]
        total = (total + f(point, polynomial_str)) % FIELD_PRIME
    return total

def interpolate_1d(vals):
    return lambda x: (vals[0] * (1 - x) + vals[1] * x) % FIELD_PRIME

def random_field_element():
    return random.randint(0, FIELD_PRIME - 1)

def main():
    while True:
        global FIELD_PRIME
        FIELD_PRIME = int(input("Enter a prime number modulus (e.g., 17): "))
        if is_prime(FIELD_PRIME):
            break
        else:
            print(f"{FIELD_PRIME} is not a prime number. Please enter a valid prime number.")

    polynomial_str = input("Enter the polynomial in terms of x1, x2, ..., xn (e.g., x1*x2 + x3 + x4): ")

    num_vars = int(input("Enter the number of variables (n): "))
    
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

if __name__ == "__main__":
    main()