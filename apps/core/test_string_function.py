def test_string_function(function_string, function_name) -> tuple[bool, str]:
    try:
        import requests

        exec(function_string)
        named_function = locals()[function_name]
    except NameError as ne:
        error = "NameError: %s" % ne
        return False, error
    except IndentationError as ie:
        error = "IndentationError: %s" % ie
        return False, error

    except SyntaxError as se:
        error = "SyntaxError: %s" % se
        return False, error

    except IndexError as ie:
        error = "IndexError: %s" % ie
        return False, error
    except TypeError as te:
        error = "TypeError: %s" % te
        return False, error
    except Exception as e:
        error = f"{e.__class__.__name__}: %s" % e
        return False, error
    else:
        return True, None


def test_string_function_with_paramter(
    function_string, function_name, **paramter
) -> tuple[bool, str]:
    try:
        import requests

        exec(function_string)
        named_function = locals()[function_name]
        named_function(**paramter)
    except NameError as ne:
        error = "NameError: %s" % ne
        return False, error
    except IndentationError as ie:
        error = "IndentationError: %s" % ie
        return False, error

    except SyntaxError as se:
        error = "SyntaxError: %s" % se
        return False, error

    except IndexError as ie:
        error = "IndexError: %s" % ie
        return False, error
    except TypeError as te:
        error = "TypeError: %s" % te
        return False, error
    except Exception as e:
        error = f"{e.__class__.__name__}: %s" % e
        return False, error
    else:
        return True, None
