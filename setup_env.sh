if [[ -d "venv/" ]];
then
    echo "No need to setup\nJust activate the venv\n"
else
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
fi
