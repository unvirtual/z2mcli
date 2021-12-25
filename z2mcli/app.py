import sys
import click
from .config import *
from .z2mclient import *

@click.group()
@click.pass_context
def main(ctx):
    config = None
    try:
        config = read_config()
    except Exception as e:
        print(e)

    if config is None:
        sys.exit(1)

    try:
        ctx.obj = Z2MClient(config)
    except ConnectionRefusedError:
        print("Connection refused to moqsuitto server at " + config["broker_host"] + ":" + str(config["broker_port"]) + ", exiting")
        sys.exit(1)

@main.command()
@click.pass_obj
def reset(z2mclient):
    z2mclient.reset()

@main.command()
@click.argument("id")
@click.argument("friendly_name")
@click.option("--ha/--no-ha", default=True, help="Update entity ID in homeassistant")
@click.pass_obj
def rename(z2mclient, ha, id, friendly_name):
    z2mclient.rename(id, friendly_name, ha)

@main.command()
@click.argument("friendly_name")
@click.option("--ha/--no-ha", default=True, help="Update entity ID in homeassistant")
@click.pass_obj
def rename_last(z2mclient, ha, friendly_name):
    z2mclient.rename_last(friendly_name, ha)

@main.command()
@click.option("--force/--no-force", default=False, help="force remove")
@click.argument("id")
@click.pass_obj
def remove(z2mclient, force, id):
    z2mclient.remove(id, force)

if __name__ == "__main__":
    main()