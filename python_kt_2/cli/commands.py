import pathlib
from time import localtime, strftime
from typing import Literal, Annotated
import typer
import python_kt_2.use_cases as use_cases
from .parse_params import get_files_from_path_arguments

app = typer.Typer()


@app.command()
def stats(
    input: Annotated[
        pathlib.Path,
        typer.Argument(
            help="Путь к файлу для анализа", exists=True, readable=True, file_okay=True
        ),
    ],
    output: Annotated[
        pathlib.Path | None,
        typer.Option(
            "--output", "-o", help="Путь к файлу для сохранения отчета", writable=True
        ),
    ] = None,
    pos: Annotated[
        bool, typer.Option(help="Добавить к отчету анализ частей речи")
    ] = False,
): 
    
    text = input.read_text(encoding="utf-8")
    result = use_cases.stats(text)
    if output: 
        import json
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        typer.echo(f"Результат сохранён в: {output}")
    else:
        typer.echo("=" * 50)
        typer.echo("Статистика")
        typer.echo("=" * 50)
        typer.echo(f"Абзацев:    {result['tokens']['paragraphs']}")
        typer.echo(f"Предложений: {result['tokens']['sentences']}")
        typer.echo(f"Слов:       {result['tokens']['words']}")
        typer.echo("-" * 50)
        typer.echo("СИМВОЛЫ:")
        for key, value in result['symbols'].items():
            typer.echo(f"  {key:12}: {value['quantity']:6} ({value['percent']:5.2f}%)")
        
        if pos and 'pos_stats' in result:
            typer.echo("-" * 50)
            typer.echo("ЧАСТИ РЕЧИ:")
            for pos_name, count in result['pos_stats'].items():
                typer.echo(f"  {pos_name:12}: {count}")


@app.command("word-cloud")
def word_cloud(
    input: Annotated[
        pathlib.Path,
        typer.Argument(help="Исходный текстовый файл", exists=True, readable=True),
    ],
    output: pathlib.Path | None = pathlib.Path("/") / f"{strftime('%H_%M_$S', localtime())}_output.png",
    preprocess_mode: Literal["basic", "full"] = "basic",
):
    text = input.read_text(encoding="utf-8")
    result = use_cases.word_cloud(text, preprocess_mode)
    result.to_file(str(output))
    typer.echo(f"Облако слов сохранено в: {output}")



@app.command(name="top-words")
def top_words(
    input: Annotated[
        pathlib.Path,
        typer.Argument(help="Исходный текстовый файл", exists=True, readable=True),
    ],
    output: pathlib.Path | None = None,
    normalize_mode: Literal["stemming", "lemmatization"] = "stemming",
):
    text = input.read_text(encoding="utf-8")
    result = use_cases.top_words(text, normalize_mode,)

    if output:
        import json
        output_data = {
            "normalize_mode": normalize_mode,
            "n": n,
            "top_words": [{"word": word, "count": count} for word, count in result]
        }
        output.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
        typer.echo(f"Результат сохранён в: {output}")
    else:
        typer.echo("=" * 40)
        typer.echo(f"ТОП-{n} СЛОВ (режим: {normalize_mode})")
        typer.echo("=" * 40)
        for i, (word, count) in enumerate(result, 1):
            typer.echo(f"{i:3}. {word:20} - {count:4} раз")
