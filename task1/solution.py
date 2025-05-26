from functools import wraps
from typing import Callable, TypeVar, Any
import unittest


F = TypeVar('F', bound=Callable[..., Any])

def strict(func) -> F:
    annotations: dict[str, type] = dict(func.__annotations__)
    annotations.pop('return', None)

    @wraps(func)
    def wrapper(*args: Any) -> Any:
        if len(args) != len(annotations):
            raise TypeError(f"{func.__name__}() takes exactly {len(annotations)} positional arguments ({len(args)} given)")
        indx: int = 0
        for indx, (name_var, expected_type_var) in enumerate(annotations.items()):
            value = args[indx]
            if not isinstance(value, expected_type_var):
                raise TypeError(f"Argument {name_var} must be {expected_type_var.__name__}, got {type(value).__name__}")
            indx += 1
        return func(*args)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

@strict
def concat(a: str, b: str, c: str) -> int:
    return a + b + c


class TestStrictDecorator(unittest.TestCase):

    def test_correct_types(self):
        self.assertEqual(concat("Have ", "nice ", "day",), "Have nice day")
        self.assertEqual(sum_two(5, 3), 8)
        
    def test_incorrect_types(self):
        with self.assertRaises(TypeError):
            sum_two(2.3, 10)

        with self.assertRaises(TypeError):
            concat("Good ", "nice ", 4)

        with self.assertRaises(TypeError):
            concat("To many args")


if __name__ == "__main__":
    unittest.main()