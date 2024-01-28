# usr/bin/bash
echo "goods_crolling_start!!!!!"

python -c 'from goods_crolling import read_artistSearch; read_artistSearch()'
py.test

echo "goods_crolling_end!!!!!!"
