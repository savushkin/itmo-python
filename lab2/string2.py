import re

# 1.
# ��: ������. ���� ����� > 3, �������� � ����� "ing",
# ���� � ����� ��� ��� "ing", ����� �������� "ly".


def v(s):
    if len(s) > 3:
        return '{}{}'.format(s, 'ly' if s.endswith('ing') else 'ing')
    else:
        return s

# 2.
# ��: ������. �������� ��������� �� 'not' �� 'bad'. ('bad' ����� 'not')
# �� 'good'.
# ������: So 'This music is not so bad!' -> This music is good!


def nb(s):
    return re.sub('not.*bad', 'good', s)
