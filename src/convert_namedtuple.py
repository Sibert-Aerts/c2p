import asttokens
import fileinput

for line in fileinput.input():
    line = line.strip()
    if '= NamedTuple' in line:
        atok = asttokens.ASTTokens(line, parse=True)
        module = atok.tree
        assign = module.body[0]
        name = assign.targets[0].id
        fields = assign.value.args[1].elts
        field_names = [f.elts[0].s for f in fields]
        typed_field_names = ['{0}: {1}'.format(f.elts[0].s, atok.get_text(f.elts[1])) for f in fields]
        init_string = ', '.join(['self'] + typed_field_names)
        print('class {0}(ASTNode):'.format(name))
        print('    def __init__({0}) -> None:'.format(init_string))
        for f in field_names:
            print('        self.{0} = {0}'.format(f))
        print()
        print('    def to_code(self, env: Environment) -> CodeNode:')
        print('        raise NotImplementedError()')
        print()
    else:
        print(line)


