import alfred
import os


@alfred.command("npm.docs.build", help="build streamsync website and documentation")
def npm_docs_build():
    os.chdir("docs")
    alfred.run("npm run docs:build")

@alfred.command("npm.ui.lint", help="lint check ui code")
def npm_ui_lint():
    os.chdir("ui")
    alfred.run("npm run lint:ci")

@alfred.command("npm.ui.build", help="build ui code")
def npm_ui_build():
    os.chdir("ui")
    alfred.run("npm run build")

@alfred.command("npm.ui.build_custom_components", help="build custom components")
def npm_ui_build_custom():
    os.chdir("ui")
    alfred.run("npm run custom.build")
