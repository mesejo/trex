import nox

SOURCE_FILES = (
    "setup.py",
    "noxfile.py",
    "trrex/",
)


@nox.session(reuse_venv=True)
def blacken(session):
    session.install("black")
    session.run("black", "--target-version=py36", *SOURCE_FILES)
    lint(session)


@nox.session(reuse_venv=True)
def lint(session):
    session.install("black", "flake8")
    session.run("black", "--check", "--target-version=py36", *SOURCE_FILES)
    session.run("flake8", "--ignore=E501,W503,E402,E712", *SOURCE_FILES)


@nox.session(python=["3.6"])
def test(session):
    session.run(
        "pytest", "--doctest-modules", *(session.posargs or ("trrex/",)), external=True
    )
