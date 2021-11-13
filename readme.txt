make project folder
cd project
python -m venv .env
.env\Script\activate
for cuda 10.1:
    pip install tensorflow==2.2.0
    pip install keras==2.3.1      
pip install -r req.txt