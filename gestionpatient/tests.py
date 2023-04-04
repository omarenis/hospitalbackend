from django.test import TestCase


blocks = {'0000': '1111'}
with open('generated.txt', 'w') as f:
    for i in blocks:
        f.write(f'${i}\t${blocks.get(i)}\n')
