# coding: utf-8
from datetime import date

from unipath import Path

BASE_DIR = Path(__file__).parent

TABLE1_NAME = 'tabela'

TABLE2_NAME = 'tabela2'

STATIC_ROOT = Path(BASE_DIR, 'static')

TABLES = {
    TABLE1_NAME: {
        'routes': Path(STATIC_ROOT, TABLE1_NAME, 'rotas.csv'),
        'price_per_kg': Path(BASE_DIR, 'static', 'tabela', 'preco_por_kg.csv'),
        'delimiter': ',',
        'icms': 6.0,
    },
    TABLE2_NAME: {
        'routes': Path(STATIC_ROOT, TABLE2_NAME, 'rotas.tsv'),
        'price_per_kg': Path(
            BASE_DIR, 'static', 'tabela2', 'preco_por_kg.tsv'),
        'delimiter': '\t',
    },
}

LOGGING = {
    'version': 1,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(purple)s%(asctime)s %(log_color)s%(levelname)s%(reset)s %(bg_blue)s\
[%(name)s]%(reset)-5s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/shipping_%s.log' % date.today().strftime('%Y-%m-%d'),
            'formatter': 'colored',
        },
    },
    'loggers': {
        '__main__': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'shipping': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
