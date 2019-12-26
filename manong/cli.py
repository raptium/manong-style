# -*- coding:utf-8 -*-
import click
import json
import yaml

from manong.specs import Pattern, Element, Series
from manong.formats import JsonFormat


@click.group()
def entry():
    pass


@click.command()
@click.argument('pattern')
@click.argument('output')
@click.option('-w', default=100, help='image width')
@click.option('-h', default=100, help='image height')
def draw(pattern, output, w, h):
    if pattern.endswith('.json'):
        with open(pattern, 'r', encoding='utf-8') as f:
            content = f.read()
            p = JsonFormat.parse(content)
    elif pattern.endswith('.yaml') or pattern.endswith('.yaml'):
        with open(pattern, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
            p = JsonFormat.parse(content)
    else:
        raise ValueError("unsupported input format")
    image = p.draw(w, h)
    image.save(output)


entry.add_command(draw)