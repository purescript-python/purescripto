from typing import TextIO


def _META_ENV():
    import py_sexpr.terms as terms

    def make_pair(a, b):
        return a, b

    env = {each: getattr(terms, each) for each in terms.__all__}
    env[make_pair.__name__] = make_pair
    return env


META_ENV = _META_ENV()


def load_topdown(file_io: TextIO, env):
    readline, read = file_io.readline, file_io.read

    n_entry = int(readline()[:-1])
    ACTION_ATTR = 0
    ACTION_APP = 1
    ACTION_SEQ = 2

    object_stack = []
    actions = []
    left_stack = []
    push_object = object_stack.append
    push_left = left_stack.append
    push_action = actions.append
    pop_object = object_stack.pop
    pop_action = actions.pop
    pop_left = left_stack.pop

    def read_entry(readline=readline, read=read):
        line = readline()
        key, length = line[:-1].split()
        value = read(int(length))
        read(1)
        return key, value

    entries = dict(read_entry(readline, read) for _ in range(n_entry))
    read(1)

    def read_float(readline=readline, append=push_object):
        return append(float(readline()[:-1]))

    def read_int(readline=readline, append=push_object):
        return append(int(readline()[:-1]))

    # noinspection PyDefaultArgument
    def read_bool(
        readline=readline, mapping={"t": True, "f": False}, append=push_object,
    ):
        return append(mapping[readline()[:-1]])

    def read_nil(append=push_object):
        readline()
        return append(None)

    # noinspection PyDefaultArgument
    def read_string(readline=readline, entries=entries, append=push_object):
        append(entries[readline()[:-1]])

    # noinspection PyDefaultArgument
    def read_var(readline=readline, env=env, entries=entries, append=push_object):
        return append(env[entries[readline()[:-1]]])

    def read_acc(readline=readline, ACTION_ATTR=ACTION_ATTR):
        attr_name = readline()[:-1]
        return 1, (ACTION_ATTR, attr_name)

    # noinspection PyDefaultArgument
    def read_cons(env=env, readline=readline, entries=entries, ACTION_APP=ACTION_APP):
        length, fn = readline()[:-1].split()
        length = int(length)
        fn = env[entries[fn]]
        return length, (ACTION_APP, fn)

    def read_seq(readline=readline, ACTION_SEQ=ACTION_SEQ):
        length = int(readline()[:-1])
        return length, ACTION_SEQ

    terminal_maps = {
        "s": read_string,
        "i": read_int,
        "b": read_bool,
        "n": read_nil,
        "f": read_float,
        "v": read_var
    }
    non_term_maps = {"a": read_acc, "c": read_cons, "l": read_seq}

    left = 1

    while True:
        while left:
            left -= 1
            case = read(1)
            term = terminal_maps.get(case)
            if term:
                term()
                continue
            push_left(left)
            left, action = non_term_maps[case]()
            push_action((left, action))

        try:
            left = pop_left()
        except IndexError:
            assert not actions and len(object_stack) == 1
            return object_stack[0]
        narg, action = pop_action()
        args = [pop_object() for _ in range(narg)]
        args.reverse()
        if action is ACTION_SEQ:
            push_object(args)
            continue

        action, op = action
        if action is ACTION_APP:
            push_object(op(*args))
        else:
            assert action is ACTION_ATTR and len(args) == 1
            push_object(getattr(args[0], op))
