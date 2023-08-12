# pbite

```
pip install 'pb @ git+https://github.com/cnpryer/pb.git'
```

You can add `pb` to any `venv` with
```
python -m venv .venv
./.venv/bin/pip install 'pb @ git+https://github.com/cnpryer/pb.git'
```

It's recommended to install `pb` using a package manager like `rye`.
```
rye install 'pb @ git+https://github.com/cnpryer/pb.git'
```

`pipx` will work as well.
```
pipx install 'pb @ git+https://github.com/cnpryer/pb.git'
```

Use `pb` to display project metadata contents on your file system.
```
pb on  master is 📦 v0.1.0 via 🐍 v3.11.3 
❯ pb .
Content
  Name: pb
  Version: 0.1.0
  Description: Print content info bites
  Source: /Users/chrispryer/github/pb/pyproject.toml
```