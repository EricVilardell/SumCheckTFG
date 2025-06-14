import random

msg = "Welcome to the Sumcheck Implementation with the naive algorithm as in the report"
print(msg)

FIELD_PRIME = 17

def f(x):
    return (x[0] * x[1] + x[2] + x[3]) % FIELD_PRIME

def sum_over_boolean_hypercube(f, num_vars):
    total = 0
    for i in range(2**num_vars):
        point = [(i >> j) & 1 for j in reversed(range(num_vars))]
        total = (total + f(point)) % FIELD_PRIME
    return total

def interpolate_1d(vals):
    return lambda x: (vals[0] * (1 - x) + vals[1] * x) % FIELD_PRIME

#fixed the values so it is like the example in the report.
FIXED_R_VALUES = [6, 4, 7, 10]

def main():
    num_vars = 4
    total_sum = sum_over_boolean_hypercube(f, num_vars)
    print(f"[Prover] Claimed sum over Boolean Hypercube: {total_sum}")

    r_vals = []

    for i in range(num_vars):
        print(f"\n=== Round {i+1} ===")
        g_vals = [0, 0]
        for b in [0, 1]:
            def sub_f(y):
                point = r_vals + [b] + y
                padded_point = point + [0] * (num_vars - len(point))
                return f(padded_point)
            g_vals[b] = sum_over_boolean_hypercube(sub_f, num_vars - (i + 1))

        g = interpolate_1d(g_vals)
        print(f"[Prover] Sends univariate polynomial g_{i+1}(x): g(0) = {g_vals[0]}, g(1) = {g_vals[1]}")

        if sum(g_vals) % FIELD_PRIME != total_sum:
            print("[Verifier] Sum does not match! Abort.")
            return

        r = FIXED_R_VALUES[i]
        print(f"[Verifier] Picks fixed r_{i+1} = {r}")
        r_vals.append(r)
        total_sum = g(r)

    final_val = f(tuple(r_vals))
    print(f"\n[Verifier] Evaluates f at r = {r_vals}, gets: {final_val}")
    print(f"[Verifier] Final check passed: {final_val == total_sum}")

if __name__ == "__main__":
    main()