
import os
import sys
import random
import string
import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.gatchor import gatchor256

def bit_difference(h1: str, h2: str) -> int:
    b1 = int(h1, 16)
    b2 = int(h2, 16)
    return bin(b1 ^ b2).count("1")


def random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def test_gatchor_deterministic_same_input():
    value = "The quick brown fox jumps over the lazy dog"
    h1 = gatchor256(value)
    h2 = gatchor256(value)
    assert h1 == h2
    assert len(h1) == 64
    assert all(c in '0123456789abcdef' for c in h1)


def test_gatchor_different_inputs_are_different():
    h1 = gatchor256("hello")
    h2 = gatchor256("hello ")
    h3 = gatchor256("Hello")
    assert h1 != h2
    assert h1 != h3
    assert h2 != h3


def test_gatchor_no_collision_small_random_set():
    n = 10000
    seen = set()
    for _ in range(n):
        s = random_string(20)
        h = gatchor256(s)
        assert h not in seen
        seen.add(h)


def test_gatchor_avalanche_effect_average():
    base = "gatchor"
    baseline = gatchor256(base)
    diffs = []
    total_bits = len(base) * 8
    for i in range(total_bits):
        b = bytearray(base.encode('utf-8'))
        b[i // 8] ^= (1 << (i % 8))
        h2 = gatchor256(bytes(b))
        diffs.append(bit_difference(baseline, h2))

    avg_diff = sum(diffs) / len(diffs)
    assert 96 <= avg_diff <= 160


def test_gatchor_golden_vectors():
    assert gatchor256("") == "b8385b30191bde3030f5f15c00deffb2149b165986447d23db1dbc1ac2315bd9"
    assert gatchor256("abc") == "c110d6663e8a2e0f6c8dd6b24c1e3370bf94b0c0ad5218b7106415bf6baab66b"
    assert gatchor256("The quick brown fox jumps over the lazy dog") == "6c1298dd134210b5934c83c3dca5566f0c7c5aef58d67797fada41b4108f693b"


def test_gatchor_random_fuzz_bytes():
    for size in [0, 1, 8, 64, 1024, 4096]:
        data = os.urandom(size)
        h = gatchor256(data)
        assert isinstance(h, str)
        assert len(h) == 64
        assert all(ch in '0123456789abcdef' for ch in h)


def test_gatchor_type_error_for_unsupported_types():
    with pytest.raises(TypeError):
        gatchor256(12345)  # non-str/bytes/bytearray


def test_gatchor_golden_vectors():
    """Fixed test vectors for regression testing - production critical"""
    assert gatchor256('') == 'b8385b30191bde3030f5f15c00deffb2149b165986447d23db1dbc1ac2315bd9'
    assert gatchor256('abc') == 'c110d6663e8a2e0f6c8dd6b24c1e3370bf94b0c0ad5218b7106415bf6baab66b'
    assert gatchor256('a' * 1000) == '395dabba7a60da0d05081f60ad5678d5c2e62060ea0c3c215cb586d3b291ce1e'
    assert gatchor256(b'\x00\x01\x02\x03') == 'ee3cef1d0934b6253ff0690074004471da0c1bc01be81819981f7a46c2f2639b'


def test_gatchor_fuzz_various_sizes():
    """Fuzz test with various input sizes - production robustness"""
    sizes = [0, 1, 2, 10, 64, 128, 256, 512, 1024, 2048]
    for size in sizes:
        data = os.urandom(size)
        h = gatchor256(data)
        assert len(h) == 64
        assert all(c in '0123456789abcdef' for c in h)


def test_gatchor_avalanche_effect_strict():
    """Strict avalanche effect test - production security requirement"""
    base = "gatchor"
    baseline = gatchor256(base)
    diffs = []
    total_bits = len(base) * 8
    for i in range(total_bits):
        b = bytearray(base.encode('utf-8'))
        b[i // 8] ^= (1 << (i % 8))
        h2 = gatchor256(bytes(b))
        diffs.append(bit_difference(baseline, h2))

    avg_diff = sum(diffs) / len(diffs)
    # Stricter bounds for production: expect 112-144 bits to flip (44-56% of 256)
    assert 112 <= avg_diff <= 144, f"Avalanche effect too weak/strong: {avg_diff}"


def test_gatchor_no_collisions_large_set():
    """Large collision test - production collision resistance"""
    n = 50000  # Increased for production confidence
    seen = set()
    for _ in range(n):
        s = random_string(32)  # Longer strings
        h = gatchor256(s)
        assert h not in seen, f"Collision detected for input: {s}"
        seen.add(h)


def test_gatchor_input_types():
    """Test all supported input types - production compatibility"""
    test_str = "hello world"
    test_bytes = test_str.encode('utf-8')
    test_bytearray = bytearray(test_bytes)

    h_str = gatchor256(test_str)
    h_bytes = gatchor256(test_bytes)
    h_bytearray = gatchor256(test_bytearray)

    assert h_str == h_bytes == h_bytearray
    assert len(h_str) == 64
