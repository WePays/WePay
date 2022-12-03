[![logo](pics/docs/Wepay-logo.png)](https://github.com/WePays/WePay)

# WePay
![Test](https://github.com/WePays/WePay/actions/workflows/django.yml/badge.svg)
![Lint](https://github.com/WePays/WePay/actions/workflows/linting.yml/badge.svg)
[![codecov](https://codecov.io/gh/WePays/WePay/branch/main/graph/badge.svg?token=0GC9E68Y6B)](https://codecov.io/gh/WePays/WePay)  
a web application for those who need to coordinate paying for a group. 


## Install and Run

### How to Install

make sure that you have [python](https://www.python.org/downloads/) in your computer

first, clone [**this repository**](https://github.com/Tezigudo/ku-polls) by type this command in your terminal at your choosen path

```sh
git clone https://github.com/WePays/WePay.git WePay
```

go to project directory

```sh
cd WePay
```

next, you have to create file name `.env` to configuration **note that you may get your secretkeys [here](https://djecrety.ir)** or you will generated using python shell command below

```py
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()
# your secret key will appear here
````

`.env` file template looks like [sample.env](sample.env) you can modify value and copy it into `.env`

by running [`setup.sh`](setup.sh) will set everythings ready for you to running the application by typing this command

you can initialize the program by

```sh
bash setup.sh
```


### How to run

#### activate the virtual environment by typing this

in mac/linux

```sh
>> source env/bin/activate
```

Windows
```sh
>> env\Scripts\activate
```

#### now to run server by type this

```sh
python manage.py runserver
```

go to `http://127.0.0.1:8000/` for application.  

## Demo Admin

| Username | Password  |
| :------: | :-------: |
|   wepay   | wepay123 |

## Project Document

You can view Project Documentation [here](https://github.com/WePays/WePay/wiki/home)

## License

The MIT License (MIT). Please see [License File](LICENSE) File for more information.
