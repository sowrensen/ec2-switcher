# EC2 Switcher

Easily check status and turn off or on EC2 instances from command line.

---

## Installation

Create a new virtual environment and activate it. After that, run:

```bash
pip install -r requirements.txt
```

Once all the dependencies are installed, you are ready to configure.

## Configuration

Create a `.env` file and set up the following keys:

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
EC2_INSTANCE=
```

Except `EC2_INSTANCE` all other keys are required.

## Usage

We will perform our operations using the `switch.py` file. You can run `python switch.py -h` to see available options.

The CLI structure is like following:

```
python switch.py [instances ...] (--start | --stop | --state)
```

Here you can pass multiple instance ids, _separated by space_, and one action like `--start`, `--stop`, or `--state`.

If you have set `EC2_INSTANCE` key in `.env` file, you can leave the instance ids and instead directly run:

```
python switch.py (--start | --stop | --state)
```

In this case, it will try to read the `instance` from the `.env` file. However, in this way you can set only one instance name.
