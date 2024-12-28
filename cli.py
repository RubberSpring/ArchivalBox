import typer
from astromod import astromod

app = typer.Typer

#Submodules
app.add_typer(astromod, name="astromod")

if __name__ == "__main__":
    app()