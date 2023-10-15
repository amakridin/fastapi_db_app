### Prepare
firstly install make:
```bash
apt install make
```

### Run environment
```bash
make start-env
```

### Run migrations
```bash
python3 run_migrator.py
```

### Run development
```bash
python3 run_dev.py
```

### Run prod
Before launching prodaction - update variables in config file - local.env
```bash
sh run_prod.sh
```

### Stop environment
```bash
make stop-env
```