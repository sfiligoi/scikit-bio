The Linux build was created using:
==================================
conda create -n skbio-local python=3.6 pip
conda activate skbio-local
conda install -c conda-forge gxx_linux-64=7.5.0
pip install -r ci/pip_requirements.txt
export USE_CYTHON=True
python setup.py build
python setup.py install
conda install -c conda-forge h5py
