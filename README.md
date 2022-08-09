# fgen
Extensible template parser

## install

```bash
python setup.py install
```

## run

```bash
fgen [config path]
```

## config

```json
{
    "imports": ["ext.json"],
    "extractors": [
        {
            "provider": "pa.fx"
        },
        {
            "provider": "pb.fx"
        }
    ],
    "converters": [],
    "define": {
        "xx":"s"
    },
    "base": "templates",
    "dest": "out",
    "pathMappers": [
        {
            "pattern": "(.*)\\.jinja2",
            "dest": "{{1}}",
            "define": {
                "xx":"7"
            },
            "converters": [],
            "extractors": [],
            "imports": []
        }
    ]
}
```

