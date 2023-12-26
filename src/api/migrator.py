import logging
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

log = logging.getLogger(__name__)


def run_migration(
    path: Path,
    sessionmaker: sessionmaker[Session],
    start_version: int = 1,
) -> None:
    """
    Runs the migration scripts in the given path.

    The SQL files should be named as <version>__<name>.sql

    Parameters
    ----------
    path : Path
        The path to the migration scripts
    sessionmaker : sessionmaker[Session]
        The sessionmaker
    start_version : int, optional
        The migration version to start from, by default 1
    """

    with sessionmaker() as session:
        with session.begin():
            # 1 Get all file names in the migrations folder
            files = [
                file
                for file in path.iterdir()
                if file.is_file() and file.suffix == ".sql"
            ]
            # 2 Split the file by __ delimiter
            sorted_files = sorted(files, key=lambda file: int(file.stem.split("__")[0]))
            for file in sorted_files:
                version = int(file.stem.split("__")[0])
                if version < start_version:
                    log.info(f"Skipping {file}")
                    continue
                # 3 Read the file
                with open(file, "r") as f:
                    sql = f.read()
                    log.info(f"Executing {file}")
                    session.execute(text(sql))
            session.commit()
