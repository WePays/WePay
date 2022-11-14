PYTHON=${1:-python3}
echo "Checking requirements..."
# Requiring Python>=3.8 w/ venv support
if ! command -v $PYTHON > /dev/null 2>&1
then
    report_requires "Python 3"
else
    if ! $PYTHON -c "import sys; assert sys.version_info >= (3, 9)" > /dev/null 2>&1
    then
        err "Python executed was outdated!"
        report_requires "Python 3.9 or greater"
    else
        if ! $PYTHON -c "import ensurepip" > /dev/null 2>&1
        then
            err "Python's ensurepip not found!"
            report_requires "Python virtual environment support"
        fi
    fi
fi
echo "requirements met!"

# create virtual environment
OS="`uname`"

# will change to vitualenv later
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

echo installing requirements...
pip install -r requirements.txt > /dev/null 2>&1;
python manage.py migrate > /dev/null 2>&1;

python manage.py loaddata data.json > /dev/null 2>&1;

echo "setup finished"
echo "To run application, run 'python manage.py runserver' and goto '127.0.0.1:8000' in your browser"
echo
echo "Have a nice day!"