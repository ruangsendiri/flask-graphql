# 🇫​​​​​🇱​​​​​🇦​​​​​🇸​​​​​🇰​​​​​-🇬​​​​​🇷​​​​​🇦​​​​​🇵​​​​​🇭​​​​​🇶​​​​​🇱​​​​​

Flask-GraphQL is like my little project to figure out GraphQL versus REST API and to show how fast we can whip up APIs using both REST API and GraphQL with good ol' Python Flask.

## Installation

Just clone this repo.

```bash
git clone https://github.com/ruangsendiri/flask-graphql.git
```

## Usage

```bash
# install python package manager
apt-get install python3-pip

# install python virtualenv module
pip install virtualenv

# create virtual environment, named test
virtualenv test

# "jump" into test virtual environment
source test/bin/activate

# install the required python module
pip install -r requirements.txt

# clone the repo
git clone https://github.com/ruangsendiri/flask-graphql.git

# adjust host in index-graphql.py
cd flask-graphql

# run the api
python index-graphql.py
```

## Visualizing

```bash
# install tcl and graphviz visualizer
sudo apt-get install libsqlite3-tcl  tcl8.6-tdbc-sqlite3 xdot
git clone https://github.com/FredrikKarlssonSpeech/sqlite2dot.git

# generate dot file
tclsh sqlite2dot.tcl karyawan.db
tclsh sqlite2dot.tcl absen.db
tclsh sqlite2dot.tcl masuk.db
```

Use graphziz, or, copy-paste the output to: https://bit.ly/graphziv-online

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Sponsor

       __|  __|_  )
       _|  (     /   Works with Ubuntu and Amazon AMI
      ___|\___|___|

##### https://fsymbols.com/generators/carty/

