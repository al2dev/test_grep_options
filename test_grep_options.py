import subprocess as sub
from itertools import permutations
import pytest


class Test_search_on_file:
    def setup(self):
        self.name = 'grep'
        # Mike: 2 000 USD\nJane: 1 000 USD\nKaila: 1 500 USD\nLila: 800 USD\nJone: 500 USD
        self.subject = 'experimental.txt'

    def grep(self, pattern: str, options: str = '') -> str:
        shel_command = [param for param in [self.name, options, pattern, self.subject] if param]
        grep_call = sub.Popen(shel_command, stdout=sub.PIPE, stderr=sub.PIPE, encoding='utf-8')
        output, errors = grep_call.communicate()
        grep_call.wait(5)
        if errors:
            return errors
        return output

    # Easy tests
    def test_string(self):
        assert self.grep(pattern='Jane') == 'Jane: 1 000 USD\n'

    @pytest.mark.xfail(reason='Wrong register', strict=True)
    def test_string_wrong_register(self):
        assert self.grep(pattern='JANE') == 'Jane: 1 000 USD\n'

    # 1 option string test
    @pytest.mark.parametrize('options, pattern, output', [
        ('-i', 'Kaila', 'Kaila: 1 500 USD\n'),
        ('-i', 'KAILA', 'Kaila: 1 500 USD\n'),
        ('-v', 'Kaila', 'Mike: 2 000 USD\nJane: 1 000 USD\nLila: 800 USD\nJone: 500 USD\n'),
        ('-v', 'KAILA', 'Mike: 2 000 USD\nJane: 1 000 USD\nKaila: 1 500 USD\nLila: 800 USD\nJone: 500 USD\n'),
        ('-c', 'Kaila', '1\n'),
        ('-c', 'KAILA', '0\n'),
        ('-w', 'Kaila', 'Kaila: 1 500 USD\n'),
        ('-w', 'KAILA', '')
    ])
    def test_string_1(self, options, pattern, output):
        assert self.grep(options=options, pattern=pattern) == output

    # 2 option string test
    @pytest.mark.parametrize('options, pattern, output', [
        pytest.param('-i -v', 'Kaila', 'Mike: 2 000 USD\nJane: 1 000 USD\nLila: 800 USD\nJone: 500 USD\n', marks=pytest.mark.xfail),
        pytest.param('-i -v', 'KAILA', 'Mike: 2 000 USD\nJane: 1 000 USD\nLila: 800 USD\nJone: 500 USD\n', marks=pytest.mark.xfail),
        pytest.param('-v -c', 'Kaila', '4\n', marks=pytest.mark.xfail),
        pytest.param('-v -c', 'KAILA', '5\n', marks=pytest.mark.xfail),
        pytest.param('-c -w', 'Kaila', '1\n', marks=pytest.mark.xfail),
        pytest.param('-c -w', 'KAILA', '0\n', marks=pytest.mark.xfail),
        ('-iv', 'Kaila', 'Mike: 2 000 USD\nJane: 1 000 USD\nLila: 800 USD\nJone: 500 USD\n'),
        ('-iv', 'KAILA', 'Mike: 2 000 USD\nJane: 1 000 USD\nLila: 800 USD\nJone: 500 USD\n'),
        ('-vc', 'Kaila', '4\n'),
        ('-vc', 'KAILA', '5\n'),
        ('-cw', 'Kaila', '1\n'),
        ('-cw', 'KAILA', '0\n'),
    ])
    def test_string_2(self, options, pattern, output):
        assert self.grep(options=options, pattern=pattern) == output

    # 3 option string test
    @pytest.mark.parametrize('options, pattern, output', [
        ('-ivc', 'Kaila', '4\n'),
        ('-ivc', 'KAILA', '4\n'),
        ('-ivw', 'Kaila', 'Mike: 2 000 USD\nJane: 1 000 USD\nLila: 800 USD\nJone: 500 USD\n'),
        ('-ivw', 'KAILA', 'Mike: 2 000 USD\nJane: 1 000 USD\nLila: 800 USD\nJone: 500 USD\n'),
        ('-vcw', 'Kaila', '4\n'),
        ('-vcw', 'KAILA', '5\n'),
        ('-icw', 'Kaila', '1\n'),
        ('-icw', 'KAILA', '1\n'),
    ])
    def test_string_3(self, options, pattern, output):
        assert self.grep(options=options, pattern=pattern) == output

    # 4 option string test part 1
    @pytest.mark.parametrize('options, pattern, output',
        [tuple(gen) for gen in (['-' + opt, 'Kaila', '4\n'] for opt in map(lambda x: ''.join(x), permutations('ivcw')))])
    def test_string_4_1(self, options, pattern, output):
        assert self.grep(options=options, pattern=pattern) == output

    # 4 option string test part 2
    @pytest.mark.parametrize('options, pattern, output',
        [tuple(gen) for gen in (['-' + opt, 'KAILA', '4\n'] for opt in map(lambda x: ''.join(x), permutations('ivcw')))])
    def test_string_4_2(self, options, pattern, output):
        assert self.grep(options=options, pattern=pattern) == output
