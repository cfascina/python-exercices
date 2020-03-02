
from nose.tools import assert_equal

class TestUniqueChars(object):

    def test_unique_chars(self, func):
        assert_equal(func(None), False)
        assert_equal(func(""), True)
        assert_equal(func("foo"), False)
        assert_equal(func("bar"), True)
        print("Tests OK.")

def main():
    test = TestUniqueChars()
    
    try:
        test.test_unique_chars(UniqueChars().is_exclusive)
    except NameError:
        pass

if __name__ == '__main__':
    main()
