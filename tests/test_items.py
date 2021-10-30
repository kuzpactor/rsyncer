from pytest import mark
from rsyncer import Item, RsyncResults

SAMPLES = [
    'cd+++++++++ кириллица'.encode('utf8'),
    b'>f+++++++++ latin',
    '.d..tp..... кириллица и пробeл'.encode('cp1251'),
    b'*deleting a',
]

ITEMS = list(Item(item) for item in SAMPLES)


@mark.parametrize(
    'input_line, attribute, value',
    [
        (SAMPLES[0], 'created', True),
        (SAMPLES[1], 'created', True),
        (SAMPLES[2], 'created', False),
        (SAMPLES[3], 'deleted', True),
    ],
)
def test_parse_item(input_line, attribute, value):
    assert getattr(Item(input_line), attribute) == value


def test_results():
    res = RsyncResults(ITEMS)
    assert res.total == 4
    assert res.deleted == 1
    assert res.updated == 2
    assert res.created == 2
    assert res.unchanged == 1
