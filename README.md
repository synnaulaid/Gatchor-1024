# Gatchor
Cryptographic Hash (Experimental)

gatchor hash is not published yet, but here are some preliminary results from our internal testing:

# Training Data & Tests Samples
```
➜  Gatchor git:(master) ✗ python3 test/train.py
=== Gatchor-256 Full Test Suite ===

Bit distribution test:
Total bits: 2560000, Ones: 1280800, Zeros: 1279200
Percentage of ones: 50.03% (target ~50%)

Collision test:
Samples: 50000, Collisions found: 0

Avalanche test:
Original input: hello
Average differing bits after 1-bit flip: 128.38 / 256 (~50% target)

Benchmark speed (5000 samples, length 32 chars):
Gatchor-256 time: 0.858 s
SHA-256 time:    0.044 s
Relative speed: Gatchor/ SHA-256 = 19.38

Throughput benchmark (bytes/sec)
 size 1024 bytes: gatchor 911108.89 B/s, sha    125583839.06 B/s
 size 1048576 bytes: gatchor 974512.77 B/s, sha    344706909.04 B/s
 size 10485760 bytes: gatchor 929401.58 B/s, sha    285862160.46 B/s
```

Targeting 256-bit output, Gatchor-256 shows promising randomness and collision resistance in our tests. However, it is significantly slower than SHA-256, which is expected given its experimental nature. We will continue to optimize the algorithm and conduct more extensive testing before any public release.

and complexity and security depend on the design of the gatchor algorithm so it needs to be improved again and again, and we will keep testing it with more data and more tests, and we will keep improving it until we are satisfied with the results. 

# DEMO & Test Advanced Suite
To run the demo and advanced test suite, use the following command:
```
python3 demo.py
```

**Results**

```
Gatchor-256 Demo and Testing Script
========================================

=== Gatchor-256 Hash Demo ===

Empty string:
  Input: ''
  Hash:  b8385b30191bde3030f5f15c00deffb2149b165986447d23db1dbc1ac2315bd9
.6f

Single character:
  Input: 'a'
  Hash:  4576a53d722e0278c05865fdb4247e762b857f301a195439e8db796405c8029a
.6f

Short string:
  Input: 'abc'
  Hash:  c110d6663e8a2e0f6c8dd6b24c1e3370bf94b0c0ad5218b7106415bf6baab66b
.6f

Standard test phrase:
  Input: 'The quick brown fox jumps over the lazy dog'
  Hash:  6c1298dd134210b5934c83c3dca5566f0c7c5aef58d67797fada41b4108f693b
.6f

1KB repeated 'a':
  Input: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
  Hash:  395dabba7a60da0d05081f60ad5678d5c2e62060ea0c3c215cb586d3b291ce1e
.6f

Binary data:
  Input: 00010203
  Hash:  ee3cef1d0934b6253ff0690074004471da0c1bc01be81819981f7a46c2f2639b
.6f

Unicode string:
  Input: 'Hello, 世界!'
  Hash:  426acc451847b74f70f57febe546d9581a57b8ac6b3fb12b88efc79548464ade
.6f

=== Running Verbose Test Suite ===

=============================================================== test session starts ===============================================================
platform linux -- Python 3.10.12, pytest-9.0.2, pluggy-1.6.0 -- /home/syn/Documents/Project/algo/Gatchor/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/syn/Documents/Project/algo/Gatchor
collected 11 items                                                                                                                                

test/test_gatchor_advanced.py::test_gatchor_deterministic_same_input PASSED
test/test_gatchor_advanced.py::test_gatchor_different_inputs_are_different PASSED
test/test_gatchor_advanced.py::test_gatchor_no_collision_small_random_set PASSED
test/test_gatchor_advanced.py::test_gatchor_avalanche_effect_average PASSED
test/test_gatchor_advanced.py::test_gatchor_golden_vectors PASSED
test/test_gatchor_advanced.py::test_gatchor_random_fuzz_bytes PASSED
test/test_gatchor_advanced.py::test_gatchor_type_error_for_unsupported_types PASSED
test/test_gatchor_advanced.py::test_gatchor_fuzz_various_sizes PASSED
test/test_gatchor_advanced.py::test_gatchor_avalanche_effect_strict PASSED
test/test_gatchor_advanced.py::test_gatchor_no_collisions_large_set PASSED
test/test_gatchor_advanced.py::test_gatchor_input_types PASSED

=============================================================== 11 passed in 24.40s ===============================================================

[+] All tests passed! Gatchor-256 is ready for evaluation.
```

These results demonstrate that Gatchor-256 produces consistent hashes for the same input, generates different hashes for different inputs, and shows a strong avalanche effect. The hash values are also correctly formatted as 64-character hexadecimal strings. The advanced test suite confirms that Gatchor-256 meets our expectations for randomness, collision resistance, and input handling.