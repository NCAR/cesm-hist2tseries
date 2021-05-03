import typer

app = typer.Typer(
    help=(
        'Tools for converting Community Earth System Model (CESM) output '
        'from history to timeseries files.'
    )
)


def version_callback(value: bool):
    from pkg_resources import get_distribution

    __version__ = get_distribution('cesm_hist2tseries').version
    if value:
        typer.echo(f'CESM-hist2tseries CLI Version: {__version__}')
        raise typer.Exit()


@app.command()
def versions():
    """print the versions of cesm-hist2tseries dependencies."""
    import importlib
    import sys

    file = sys.stdout

    packages = [
        'xarray',
        'pandas',
        'dask',
        'numpy',
        'netCDF4',
        'typer',
    ]
    deps = [(mod, lambda mod: mod.__version__) for mod in packages]

    deps_blob = []
    for (modname, ver_f) in deps:
        try:
            if modname in sys.modules:
                mod = sys.modules[modname]
            else:
                mod = importlib.import_module(modname)
        except Exception:
            deps_blob.append((modname, None))
        else:
            try:
                ver = ver_f(mod)
                deps_blob.append((modname, ver))
            except Exception:
                deps_blob.append((modname, 'installed'))

    print('\nINSTALLED VERSIONS', file=file)
    print('------------------', file=file)

    print('', file=file)
    for k, stat in sorted(deps_blob):
        print(f'{k}: {stat}', file=file)


def main():
    typer.run(app())
