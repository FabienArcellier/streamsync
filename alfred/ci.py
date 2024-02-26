import os

import alfred


@alfred.command("ci", help="continuous integration pipeline")
@alfred.option('--front', '-f', help="run for frontend only", is_flag=True, default=False)
@alfred.option('--back', '-b', help="run for backend only", is_flag=True, default=False)
@alfred.option('--docs', '-d', help="run for documentation only", is_flag=True, default=False)
def ci(front, back, docs):
    run_all = (not front and not back and not docs)
    if back or run_all:
        alfred.invoke_command("ci.mypy")
        alfred.invoke_command("ci.pytest")

    if front or run_all:
        alfred.invoke_command("npm.ui.lint")
        alfred.invoke_command("npm.ui.build")

    if docs or run_all:
        alfred.invoke_command("npm.docs.build")

@alfred.command("ci.mypy", help="typing checking with mypy on ./src/streamsync")
def ci_mypy():
    alfred.run("mypy ./src/streamsync --exclude app_templates/*")


@alfred.command("ci.pytest", help="run pytest on ./tests")
def ci_test():
    os.chdir("tests")
    alfred.run("pytest")
