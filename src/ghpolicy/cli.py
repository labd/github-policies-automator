#!/usr/bin/env python3
import click
import yaml

from ghpolicy.main import run


@click.command()
@click.argument("config", type=click.File("rb"))
@click.option("--dry-run", is_flag=True)
def invoke(config: click.File, dry_run: bool):
    data = yaml.load(config, Loader=yaml.FullLoader)
    run(data, dry_run=dry_run)
