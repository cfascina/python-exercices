
from nose.tools import assert_equal

class TestUniqueChars(object):

    def test_unique_chars(self, func):
        
        assert_equal(func(None), False)
        assert_equal(func(""), True)
        assert_equal(func("foo"), False)
        assert_equal(func("bar"), True)
        
        print("Tests OK.")

def main():
    
    test_class = TestUniqueChars()
    
    try:
        tested_class = UniqueChars()
        test_class.test_unique_chars(tested_class.is_unique)
    
    except NameError:
        print(f"NameError: {NameError}")

if __name__ == '__main__':

    main()
