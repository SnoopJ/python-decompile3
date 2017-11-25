import re
from uncompyle6 import PYTHON_VERSION, PYTHON3, IS_PYPY # , PYTHON_VERSION
from uncompyle6.parser import get_python_parser, python_parser
from uncompyle6.scanner import get_scanner

def test_grammar():

    def check_tokens(tokens, opcode_set):
        remain_tokens = set(tokens) - opcode_set
        remain_tokens = set([re.sub('_\d+$','', t) for t in remain_tokens])
        remain_tokens = set([re.sub('_CONT$','', t) for t in remain_tokens])
        remain_tokens = set(remain_tokens) - opcode_set
        assert remain_tokens == set([]), \
            "Remaining tokens %s\n====\n%s" % (remain_tokens, p.dump_grammar())

    p = get_python_parser(PYTHON_VERSION, is_pypy=IS_PYPY)
    (lhs, rhs, tokens,
     right_recursive, dup_rhs) = p.check_sets()
    expect_lhs = set(['expr1024', 'pos_arg'])
    unused_rhs = set(['build_list', 'call_function', 'mkfunc',
                      'mklambda',
                      'unpack',])
    expect_right_recursive = frozenset([('designList',
                                         ('designator', 'DUP_TOP', 'designList'))])
    if PYTHON3:
        expect_lhs.add('load_genexpr')

        unused_rhs = unused_rhs.union(set("""
        except_pop_except genexpr classdefdeco2 listcomp
        """.split()))
        if 3.0 <= PYTHON_VERSION:
            expect_lhs.add("annotate_arg")
            expect_lhs.add("annotate_tuple")
            unused_rhs.add("mkfunc_annotate")
            pass
    else:
        expect_lhs.add('kwarg')
    assert expect_lhs == set(lhs)
    assert unused_rhs == set(rhs)
    assert expect_right_recursive == right_recursive

    expect_dup_rhs = frozenset([('COME_FROM',), ('CONTINUE',), ('JUMP_ABSOLUTE',),
                                ('LOAD_CONST',),
                                ('JUMP_BACK',), ('JUMP_FORWARD',)])
    reduced_dup_rhs = {k: dup_rhs[k] for k in dup_rhs if k not in expect_dup_rhs}
    for k in reduced_dup_rhs:
        print(k, reduced_dup_rhs[k])
    # assert not reduced_dup_rhs, reduced_dup_rhs

    s = get_scanner(PYTHON_VERSION, IS_PYPY)
    ignore_set = set(
            """
            JUMP_BACK CONTINUE
            COME_FROM COME_FROM_EXCEPT
            COME_FROM_EXCEPT_CLAUSE
            COME_FROM_LOOP COME_FROM_WITH
            COME_FROM_FINALLY ELSE
            LOAD_GENEXPR LOAD_ASSERT LOAD_SETCOMP LOAD_DICTCOMP
            LAMBDA_MARKER
            RETURN_END_IF RETURN_END_IF_LAMBDA RETURN_VALUE_LAMBDA RETURN_LAST
            """.split())
    if 2.6 <= PYTHON_VERSION <= 2.7:
        opcode_set = set(s.opc.opname).union(ignore_set)
        check_tokens(tokens, opcode_set)
    elif PYTHON_VERSION == 3.4:
        ignore_set.add('LOAD_CLASSNAME')
        ignore_set.add('STORE_LOCALS')
        opcode_set = set(s.opc.opname).union(ignore_set)
        check_tokens(tokens, opcode_set)

def test_dup_rule():
    import inspect
    python_parser(PYTHON_VERSION, inspect.currentframe().f_code,
                  is_pypy=IS_PYPY,
                  parser_debug={
                      'dups': True, 'transition': False, 'reduce': False,
                      'rules': False, 'errorstack': None, 'context': True})
