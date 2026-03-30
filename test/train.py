# test/train.py
import os
import sys
import argparse

# Ensure project root is on sys.path so that `core` package can be imported when
# running this file directly. Python sets sys.path[0] to the script directory
# (test/), so the sibling `core/` folder isn't found by default.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import random
import string
import time
import hashlib
from core.gatchor import gatchor256


# -----------------------------
# Helper Functions
# -----------------------------

def bit_difference(h1: str, h2: str) -> int:
    """Count number of differing bits between two hex digests"""
    b1 = int(h1, 16)
    b2 = int(h2, 16)
    return bin(b1 ^ b2).count("1")

def random_string(length: int) -> str:
    """Generate random ASCII string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# -----------------------------
# 1. Bit distribution test
# -----------------------------

def bit_distribution_test(num_samples=10000, length=16):
    """Check uniformity of 0/1 bits in hash output"""
    ones = 0
    total_bits = 0
    for _ in range(num_samples):
        s = random_string(length)
        h = gatchor256(s)
        bits = bin(int(h, 16))[2:].zfill(256)
        ones += bits.count("1")
        total_bits += len(bits)
    print(f"Bit distribution test:")
    print(f"Total bits: {total_bits}, Ones: {ones}, Zeros: {total_bits - ones}")
    print(f"Percentage of ones: {ones / total_bits * 100:.2f}% (target ~50%)\n")

# -----------------------------
# 2. Collision test
# -----------------------------

def collision_test(num_samples=100000, length=16):
    """Check for collisions in hash outputs"""
    seen = set()
    collisions = 0
    for _ in range(num_samples):
        s = random_string(length)
        h = gatchor256(s)
        if h in seen:
            collisions += 1
        seen.add(h)
    print(f"Collision test:")
    print(f"Samples: {num_samples}, Collisions found: {collisions}\n")

# -----------------------------
# 3. Avalanche test
# -----------------------------

def avalanche_test(input_str="hello"):
    """Test avalanche effect by flipping each bit of input"""
    print(f"Avalanche test:")
    h0 = gatchor256(input_str)
    total_bits = len(input_str) * 8
    diffs = []
    for i in range(total_bits):
        b = bytearray(input_str.encode("utf-8"))
        byte_idx = i // 8
        bit_idx = i % 8
        b[byte_idx] ^= (1 << bit_idx)
        new_input = b.decode("latin1", errors="ignore")
        h1 = gatchor256(new_input)
        diffs.append(bit_difference(h0, h1))
    avg_diff = sum(diffs) / len(diffs)
    print(f"Original input: {input_str}")
    print(f"Average differing bits after 1-bit flip: {avg_diff:.2f} / 256 (~50% target)\n")

# -----------------------------
# 4. Benchmark speed
# -----------------------------

def benchmark_speed(num_samples=10000, length=32):
    """Benchmark Gatchor-256 vs SHA-256"""
    # Gatchor-256
    start = time.time()
    for _ in range(num_samples):
        s = random_string(length)
        gatchor256(s)
    t_gatchor = time.time() - start

    # SHA-256
    start = time.time()
    for _ in range(num_samples):
        s = random_string(length)
        hashlib.sha256(s.encode("utf-8")).hexdigest()
    t_sha = time.time() - start

    print(f"Benchmark speed ({num_samples} samples, length {length} chars):")
    print(f"Gatchor-256 time: {t_gatchor:.3f} s")
    print(f"SHA-256 time:    {t_sha:.3f} s")
    print(f"Relative speed: Gatchor/ SHA-256 = {t_gatchor / t_sha:.2f}\n")

# -----------------------------
# Additional Benchmarks
# -----------------------------

def benchmark_throughput(sizes=(1024, 1024*1024, 10*1024*1024), samples=5):
    """Benchmark throughput in bytes per second for various input sizes.

    Uses os.urandom to generate binary data and exercises both Gatchor-256
    and SHA-256.  This gives a more realistic idea of performance on larger
    payloads rather than many small strings.
    """
    print("Throughput benchmark (bytes/sec)")
    for size in sizes:
        data = os.urandom(size)
        start = time.time()
        for _ in range(samples):
            gatchor256(data)
        t_g = time.time() - start

        start = time.time()
        for _ in range(samples):
            hashlib.sha256(data).hexdigest()
        t_s = time.time() - start

        print(f" size {size} bytes: gatchor {size * samples / t_g:.2f} B/s, "
              f"sha    {size * samples / t_s:.2f} B/s")
    print()


def hash_directory(dir_path, algorithm='gatchor'):
    """Walk a directory and hash each file, printing timings.

    Useful for testing on real data sets rather than synthetic random
    strings.  `algorithm` can be 'gatchor' or 'sha'.
    """
    print(f"Hashing files under {dir_path} using {algorithm}")
    total_bytes = 0
    start = time.time()
    for root, _, files in os.walk(dir_path):
        for fname in files:
            path = os.path.join(root, fname)
            with open(path, 'rb') as f:
                data = f.read()
            if algorithm == 'gatchor':
                gatchor256(data)
            else:
                hashlib.sha256(data).hexdigest()
            total_bytes += len(data)
    elapsed = time.time() - start
    print(f"Processed {total_bytes} bytes in {elapsed:.3f}s ({total_bytes / elapsed:.2f} B/s)\n")


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Gatchor-256 test suite")
    parser.add_argument('--bitdist', action='store_true', help='run bit distribution test')
    parser.add_argument('--collision', action='store_true', help='run collision test')
    parser.add_argument('--avalanche', action='store_true', help='run avalanche test')
    parser.add_argument('--benchmark', action='store_true', help='run simple speed benchmark')
    parser.add_argument('--throughput', action='store_true', help='run throughput benchmark')
    parser.add_argument('--hashdir', type=str, help='hash all files in directory for timing')
    parser.add_argument('--all', action='store_true', help='run all tests/benchmarks')
    args = parser.parse_args()

    # if the user didn't specify any individual option, run everything
    if not any(vars(args).values()):
        args.all = True

    print("=== Gatchor-256 Full Test Suite ===\n")
    if args.all or args.bitdist:
        bit_distribution_test(num_samples=10000, length=16)
    if args.all or args.collision:
        collision_test(num_samples=50000, length=16)
    if args.all or args.avalanche:
        avalanche_test("hello")
    if args.all or args.benchmark:
        benchmark_speed(num_samples=5000, length=32)
    if args.all or args.throughput:
        benchmark_throughput()
    if args.hashdir:
        # run both algorithms against provided directory
        hash_directory(args.hashdir, algorithm='gatchor')
        hash_directory(args.hashdir, algorithm='sha')
