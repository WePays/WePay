# create virtual environment
OS="`uname`"

echo "creating virtual environment..."
case $OS in
    'Darwin')
    python3 -m venv env
    ;;
    'WindowsNT')
    python -m venv env
    ;;
    *)
    python -m venv env
esac
echo "created"

echo "activating the environment..."
case $OS in
    'Darwin')
    source env/bin/activate
    ;;
    'WindowsNT')
    env\Scripts\activate
    ;;
    *)
    source env/bin/activate
esac
echo "activated"

read -p "what iteration do you working on now(ex. Answer as iteration2): " iteration
echo pulling $iteration
git pull origin $iteration
echo installing requirements...
pip install -r requirements.txt
python manage.py loaddata data/*.json
python manage.py migrate
echo
echo everything finished
