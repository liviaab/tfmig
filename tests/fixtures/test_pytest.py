def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 5

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def myfunc():
    raise ValueError("Exception 123 raised")

def test_match():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        myfunc()

# XFail: mark test functions as expected to fail
@pytest.mark.xfail(raises=IndexError)
def test_f():
    f()

def test_function():
    if not valid_config():
        pytest.xfail("failing configuration (but should work)")

@pytest.mark.xfail(sys.platform == "win32", reason="bug in a 3rd party library")
def test_function():
    ...
@pytest.mark.xfail(run=False)
def test_function():
    ...
@pytest.mark.xfail(strict=True)
def test_function():
    ...

xfail = pytest.mark.xfail

@xfail
def test_hello():
    assert 0

@xfail(run=False)
def test_hello2():
    assert 0

@xfail("hasattr(os, 'sep')")
def test_hello3():
    assert 0


@pytest.mark.fixt_data(42)
def test_fixt(fixt):
    assert fixt == 42

class Fruit:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

@pytest.fixture
def my_fruit():
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]


def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert my_fruit in fruit_basket

@pytest.fixture(scope="module")
def smtp_connection():
    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)

@pytest.fixture(scope="session")
def smtp_connection():
    # the returned fixture value will be shared for
    # all tests requesting it
    ...

@pytest.fixture(autouse=True)
def append_third(order, append_second):
    order += [3]

@pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print("finalizing {}".format(smtp_connection))
    smtp_connection.close()

@pytest.fixture(params=[0, 1], ids=["spam", "ham"])
def a(request):
    return request.param

def test_a(a):
    pass

def idfn(fixture_value):
    if fixture_value == 0:
        return "eggs"
    else:
        return None

@pytest.fixture(params=[0, 1], ids=idfn)
def b(request):
    return request.param

def test_b(b):
    pass

# Using marks with parametrized fixtures
@pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
def data_set(request):
    return request.param

def test_data(data_set):
    pass

@pytest.fixture(scope="module", params=["mod1", "mod2"])
def modarg(request):
    param = request.param
    print("  SETUP modarg", param)
    yield param
    print("  TEARDOWN modarg", param)


@pytest.fixture(scope="function", params=[1, 2])
def otherarg(request):
    param = request.param
    print("  SETUP otherarg", param)
    yield param
    print("  TEARDOWN otherarg", param)

@pytest.mark.usefixtures("cleandir")
class TestDirectoryInit:
    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
        with open("myfile", "w") as f:
            f.write("hello")

    def test_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []

@pytest.mark.usefixtures("cleandir", "anotherfixture")
def test():
    ...

import pytest

@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected

# pytest.param - Specify a parameter in pytest.mark.parametrize calls or parametrized fixtures.
@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
def test_eval(test_input, expected):
    # assert eval(test_input) == expected

@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    pass

@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown():
    ...

def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")

if not sys.platform.startswith("win"):
    pytest.skip("skipping windows-only tests", allow_module_level=True)

@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_function():
    ...
# https://docs.pytest.org/en/6.2.x/skipping.html#skipif
minversion = pytest.mark.skipif(
    mymodule.__versioninfo__ < (1, 1), reason="at least mymodule-1.1 required"
)

@minversion
def test_function():
    ...
# summarys
# Skip all tests in a module unconditionally:
pytestmark = pytest.mark.skip("all tests still WIP")

# Skip all tests in a module based on some condition:
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="tests for linux only")
