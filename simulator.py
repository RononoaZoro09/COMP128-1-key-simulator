import random

#smaller transposition box
SBOX = [0xE, 0x4, 0xD, 0x1,
        0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC,
        0x5, 0x9, 0x0, 0x7]

def comp128_toy(ki, rand):
    #ki and rand are 16 bits each instead of 16 bytes
    # Expand to 32 bits
    A = []
    for i in range(16):
        bit_ki = (ki >> i) & 1
        bit_rand = (rand >> i) & 1
        A.append(bit_ki ^ bit_rand)

    # 4 rounds of mixing instead of 8
    for _ in range(4):
        new_A = []
        for i in range(16):
            left = A[i]
            right = A[(i + 1) % 16]

            val = (left << 1) | right
            val = SBOX[val & 0xF]

            new_A.append(val & 1)

        A = new_A

    # Compress back to 16-bit output
    out = 0
    for i in range(16):
        out |= (A[i] << i)

    return out


def recover_ki(samples):
    #by brute force
    for candidate in range(0x10000):
        match = True
        for rand, expected in samples:
            if comp128_toy(candidate, rand) != expected:
                match = False
                break
        if match:
            return candidate
    return None


def main():
    true_ki = random.getrandbits(16)

    print(f"Secret Ki: {true_ki:04x}")

    samples = []
    for _ in range(10):
        rand = random.getrandbits(16)
        out = comp128_toy(true_ki, rand)
        samples.append((rand, out))

    print("[*] Recovering Ki...")

    recovered = recover_ki(samples)

    print(f"Recovered Ki: {recovered:04x}")
    print(f"Match: {recovered == true_ki}")


if __name__ == "__main__":
    main()

