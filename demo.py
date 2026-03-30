#!/usr/bin/env python3
"""
Gatchor-256 Demo and Verbose Testing Script

This script demonstrates the Gatchor-256 hash algorithm and runs the full test suite
with verbose output for detailed analysis.
"""

import os
import sys
import subprocess
import time

# Ensure project root is on sys.path
project_root = os.path.dirname(__file__)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.gatchor import gatchor256

def demo_hashing():
    """Demonstrate Gatchor-256 hashing with various inputs."""
    print("=== Gatchor-256 Hash Demo ===\n")

    test_inputs = [
        ("", "Empty string"),
        ("a", "Single character"),
        ("abc", "Short string"),
        ("The quick brown fox jumps over the lazy dog", "Standard test phrase"),
        ("a" * 1000, "1KB repeated 'a'"),
        (b'\x00\x01\x02\x03', "Binary data"),
        ("Hello, 世界!", "Unicode string"),
    ]

    for input_data, description in test_inputs:
        start_time = time.time()
        hash_result = gatchor256(input_data)
        elapsed = time.time() - start_time
        print(f"{description}:")
        print(f"  Input: {repr(input_data) if isinstance(input_data, str) else input_data.hex()}")
        print(f"  Hash:  {hash_result}")
        print(".6f")
        print()

def run_verbose_tests():
    """Run the test suite with verbose output."""
    print("=== Running Verbose Test Suite ===\n")

    try:
        import pytest
    except ImportError:
        print("[X] pytest not installed. Install with: pip install pytest")
        print("Then run: python3 -m pytest -v -s test/")
        return False

    # Change to project root for pytest
    os.chdir(project_root)

    # Run pytest with verbose and no capture
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "-v",  # verbose
        "-s",  # no output capture
        "--tb=short",  # shorter tracebacks
        "test/"
    ], capture_output=False, text=True)

    return result.returncode == 0

def main():
    """Main function to run demo and tests."""
    print("Gatchor-256 Demo and Testing Script")
    print("=" * 40)
    print()

    # Run demo
    demo_hashing()

    # Run tests
    success = run_verbose_tests()

    if success:
        print("\n[+] All tests passed! Gatchor-256 is ready for evaluation.")
    else:
        print("\n[X] Some tests failed. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()