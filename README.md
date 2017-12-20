# Requirements
- [Python ~3.6](https://www.python.org)
- [Pylambda](https://github.com/nficano/python-lambda)

# Setup
1. Follow the instructions provided at pylambda to generate the pylambda framework.
2. Change `config.yaml` to use `guildinfo.py` as the primary function.
3. Input your amazon credentials into `config.yaml`.
4. `workon YOUR_ENV_NAME` then `pip install -r requirements.txt`
5. Modify the event.json file to follow the parameters specified in `guildinfo.py` for local invocation.