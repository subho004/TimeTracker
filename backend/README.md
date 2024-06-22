# Activate venv

python3 -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate

# Install requirements

pip3 install -r requirements.txt

# Run the application

uvicorn main:app --host 0.0.0.0

# Hot Reload

uvicorn main:app --host 0.0.0.0 --reload

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. timeseries.proto

# To test

after activating venv and installing requirements do

-> python server.py

-> python client.py
