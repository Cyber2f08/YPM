import click

@click.command("--hello")
def hello():
    print("Hello")
    