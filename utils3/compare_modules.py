"""
Compares two versions of conda configurations
"""

nightly = '''atomicwrites              1.2.1                    py37_0  
attrs                     18.2.0           py37h28b3542_0  
backcall                  0.1.0                    py37_0  
blas                      1.0                         mkl  
bleach                    3.0.2                    py37_0  
ca-certificates           2018.03.07                    0  
certifi                   2018.10.15               py37_0  
cycler                    0.10.0                   py37_0  
cython                    0.29             py37he6710b0_0  
dbus                      1.13.2               h714fa37_1  
decorator                 4.3.0                    py37_0  
entrypoints               0.2.3                    py37_2  
expat                     2.2.6                he6710b0_0  
fastcache                 1.0.2            py37h14c3975_2  
fontconfig                2.13.0               h9420a91_0  
freetype                  2.9.1                h8a8886c_1  
glib                      2.56.2               hd408876_0  
gmp                       6.1.2                h6c8ec71_1  
gmpy2                     2.0.8            py37h10f8cd9_2  
gst-plugins-base          1.14.0               hbbd80ab_1  
gstreamer                 1.14.0               hb453b48_1  
icu                       58.2                 h9c2bf20_1  
intel-openmp              2019.0                      118  
ipykernel                 5.0.0            py37h39e3cac_0  
ipython                   7.0.1            py37h39e3cac_0  
ipython_genutils          0.2.0                    py37_0  
ipywidgets                7.4.2                    py37_0  
jedi                      0.13.1                   py37_0  
jinja2                    2.10                     py37_0  
jpeg                      9b                   h024ee3a_2  
jsonschema                2.6.0                    py37_0  
jupyter                   1.0.0                    py37_7  
jupyter_client            5.2.3                    py37_0  
jupyter_console           6.0.0                    py37_0  
jupyter_core              4.4.0                    py37_0  
kiwisolver                1.0.1            py37hf484d3e_0  
libedit                   3.1.20170329         h6b74fdf_2  
libffi                    3.2.1                hd88cf55_4  
libgcc-ng                 8.2.0                hdf63c60_1  
libgfortran-ng            7.3.0                hdf63c60_0  
libpng                    1.6.35               hbc83047_0  
libsodium                 1.0.16               h1bed415_0  
libstdcxx-ng              8.2.0                hdf63c60_1  
libuuid                   1.0.3                h1bed415_2  
libxcb                    1.13                 h1bed415_1  
libxml2                   2.9.8                h26e45fe_1  
markupsafe                1.0              py37h14c3975_1  
matplotlib                3.0.0            py37h5429711_0  
mistune                   0.8.4            py37h7b6447c_0  
mkl                       2019.0                      118  
mkl_fft                   1.0.6            py37h7dd41cf_0  
mkl_random                1.0.1            py37h4414c95_1  
more-itertools            4.3.0                    py37_0  
mpc                       1.1.0                h10f8cd9_1  
mpfr                      4.0.1                hdf1c602_3  
mpmath                    1.0.0                    py37_2  
nbconvert                 5.3.1                    py37_0  
nbformat                  4.4.0                    py37_0  
ncurses                   6.1                  hf484d3e_0  
notebook                  5.7.0                    py37_0  
numpy                     1.15.2           py37h1d66e8a_1  
numpy-base                1.15.2           py37h81de0dd_1  
openssl                   1.0.2p               h14c3975_0  
pandas                    0.23.4           py37h04863e7_0  
pandoc                    2.2.3.2                       0  
pandocfilters             1.4.2                    py37_1  
parso                     0.3.1                    py37_0  
patsy                     0.5.0                    py37_0  
pcre                      8.42                 h439df22_0  
pexpect                   4.6.0                    py37_0  
pickleshare               0.7.5                    py37_0  
pip                       10.0.1                   py37_0  
pluggy                    0.7.1            py37h28b3542_0  
prometheus_client         0.4.2                    py37_0  
prompt_toolkit            2.0.6                    py37_0  
ptyprocess                0.6.0                    py37_0  
py                        1.7.0                    py37_0  
pygments                  2.2.0                    py37_0  
pyparsing                 2.2.2                    py37_0  
pyqt                      5.9.2            py37h05f1152_2  
pytest                    3.8.2                    py37_0  
python                    3.7.0                h6e4f718_3  
python-dateutil           2.7.3                    py37_0  
pytz                      2018.5                   py37_0  
pyzmq                     17.1.2           py37h14c3975_0  
qt                        5.9.6                h8703b6f_2  
qtconsole                 4.4.1                    py37_0  
readline                  7.0                  h7b6447c_5  
scipy                     1.1.0            py37hfa4b5c9_1  
send2trash                1.5.0                    py37_0  
setuptools                40.4.3                   py37_0  
simplegeneric             0.8.1                    py37_2  
sip                       4.19.8           py37hf484d3e_0  
six                       1.11.0                   py37_1  
sqlite                    3.25.2               h7b6447c_0  
statsmodels               0.9.0            py37h035aef0_0  
sympy                     1.3                      py37_0  
terminado                 0.8.1                    py37_1  
testpath                  0.4.2                    py37_0  
tk                        8.6.8                hbc83047_0  
tornado                   5.1.1            py37h7b6447c_0  
traitlets                 4.3.2                    py37_0  
wcwidth                   0.1.7                    py37_0  
webencodings              0.5.1                    py37_1  
wheel                     0.32.1                   py37_0  
widgetsnbextension        3.4.2                    py37_0  
xz                        5.2.4                h14c3975_4  
zeromq                    4.2.5                hf484d3e_1  
zlib                      1.2.11               ha838bed_2  
'''

py37 = '''atomicwrites              1.2.1                    py36_0  
attrs                     18.2.0           py36h28b3542_0  
backcall                  0.1.0                    py36_0  
blas                      1.0                         mkl  
bleach                    3.0.2                    py36_0  
ca-certificates           2018.03.07                    0  
certifi                   2018.10.15               py36_0  
cycler                    0.10.0                   py36_0  
cython                    0.28.2           py36h14c3975_0  
dbus                      1.13.2               h714fa37_1  
decorator                 4.3.0                    py36_0  
entrypoints               0.2.3                    py36_2  
expat                     2.2.6                he6710b0_0  
fastcache                 1.0.2            py36h14c3975_2  
fontconfig                2.13.0               h9420a91_0  
freetype                  2.9.1                h8a8886c_1  
glib                      2.56.2               hd408876_0  
gmp                       6.1.2                h6c8ec71_1  
gmpy2                     2.0.8            py36h10f8cd9_2  
gst-plugins-base          1.14.0               hbbd80ab_1  
gstreamer                 1.14.0               hb453b48_1  
icu                       58.2                 h9c2bf20_1  
intel-openmp              2019.0                      118  
ipykernel                 5.0.0            py36h39e3cac_0  
ipython                   7.0.1            py36h39e3cac_0  
ipython_genutils          0.2.0                    py36_0  
ipywidgets                7.4.2                    py36_0  
jedi                      0.13.1                   py36_0  
jinja2                    2.10                     py36_0  
jpeg                      9b                   h024ee3a_2  
jsonschema                2.6.0                    py36_0  
jupyter                   1.0.0                    py36_7  
jupyter_client            5.2.3                    py36_0  
jupyter_console           6.0.0                    py36_0  
jupyter_core              4.4.0                    py36_0  
kiwisolver                1.0.1            py36hf484d3e_0  
libedit                   3.1.20170329         h6b74fdf_2  
libffi                    3.2.1                hd88cf55_4  
libgcc-ng                 8.2.0                hdf63c60_1  
libgfortran-ng            7.3.0                hdf63c60_0  
libpng                    1.6.35               hbc83047_0  
libsodium                 1.0.16               h1bed415_0  
libstdcxx-ng              8.2.0                hdf63c60_1  
libuuid                   1.0.3                h1bed415_2  
libxcb                    1.13                 h1bed415_1  
libxml2                   2.9.8                h26e45fe_1  
markupsafe                1.0              py36h14c3975_1  
matplotlib                2.2.3            py36hb69df0a_0  
mistune                   0.8.4            py36h7b6447c_0  
mkl                       2019.0                      118  
mkl_fft                   1.0.6            py36h7dd41cf_0  
mkl_random                1.0.1            py36h4414c95_1  
more-itertools            4.3.0                    py36_0  
mpc                       1.1.0                h10f8cd9_1  
mpfr                      4.0.1                hdf1c602_3  
mpmath                    1.0.0                    py36_2  
nbconvert                 5.3.1                    py36_0  
nbformat                  4.4.0                    py36_0  
ncurses                   6.1                  hf484d3e_0  
notebook                  5.7.0                    py36_0  
numpy                     1.15.1           py36h1d66e8a_0  
numpy-base                1.15.1           py36h81de0dd_0  
openssl                   1.0.2p               h14c3975_0  
pandas                    0.23.4           py36h04863e7_0  
pandoc                    2.2.3.2                       0  
pandocfilters             1.4.2                    py36_1  
parso                     0.3.1                    py36_0  
patsy                     0.5.0                    py36_0  
pcre                      8.42                 h439df22_0  
pexpect                   4.6.0                    py36_0  
pickleshare               0.7.5                    py36_0  
pip                       10.0.1                   py36_0  
pluggy                    0.7.1            py36h28b3542_0  
prometheus_client         0.4.2                    py36_0  
prompt_toolkit            2.0.6                    py36_0  
ptyprocess                0.6.0                    py36_0  
py                        1.7.0                    py36_0  
pygments                  2.2.0                    py36_0  
pyparsing                 2.2.2                    py36_0  
pyqt                      5.9.2            py36h05f1152_2  
pytest                    3.8.0                    py36_0  
python                    3.6.6                h6e4f718_2  
python-dateutil           2.7.3                    py36_0  
pytz                      2018.5                   py36_0  
pyzmq                     17.1.2           py36h14c3975_0  
qt                        5.9.6                h8703b6f_2  
qtconsole                 4.4.1                    py36_0  
readline                  7.0                  h7b6447c_5  
scipy                     1.1.0            py36hfa4b5c9_1  
send2trash                1.5.0                    py36_0  
setuptools                40.4.3                   py36_0  
simplegeneric             0.8.1                    py36_2  
sip                       4.19.8           py36hf484d3e_0  
six                       1.11.0                   py36_1  
sqlite                    3.25.2               h7b6447c_0  
statsmodels               0.9.0            py36h035aef0_0  
sympy                     1.1.1                    py36_0  
terminado                 0.8.1                    py36_1  
testpath                  0.4.2                    py36_0  
tk                        8.6.8                hbc83047_0  
tornado                   5.1.1            py36h7b6447c_0  
traitlets                 4.3.2                    py36_0  
wcwidth                   0.1.7                    py36_0  
webencodings              0.5.1                    py36_1  
wheel                     0.32.1                   py36_0  
widgetsnbextension        3.4.2                    py36_0  
xz                        5.2.4                h14c3975_4  
zeromq                    4.2.5                hf484d3e_1  
zlib                      1.2.11               ha838bed_2  
'''

import pprint

def main(py37, nightly):
    data = {}
    counter = 0
    for line in py37.splitlines() :
        counter += 1
        line_split = line.split()
        if 3 <= len(line_split):
            record = data.get(line_split[0], {'Version':{}, 'Build':{}})
            data[line_split[0]] = record
            record['Version']['37'] = line_split[1]
            record['Build']['37'] = line_split[2]
        else:
            raise ValueError(f"line={repr(line)}\nline_split={line_split}")

    for line in nightly.splitlines() :
        line_split = line.split()
        if 3 <= len(line_split):
            record = data.get(line_split[0], {'Version':{}, 'Build':{}})
            if not record['Version']:
                counter += 1
            if record['Version']['37'] != line_split[1]:
                data[line_split[0]] = record
                record['Version']['nightly'] = line_split[1]
                record['Build']['nightly'] = line_split[2]
            else:
                del data[line_split[0]]
        else:
            raise ValueError(f"line={repr(line)}\nline_split={line_split}")

    pprint.pprint(data)
    print(f'# Total = {counter}')
    print(f'# Unique = {len(data)}')

if "__main__" == __name__:
    main(py37, nightly)
