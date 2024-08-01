# fmt: off
from dagster import Definitions, load_assets_from_modules, materialize
from dagster_duckdb_pandas import DuckDBPandasIOManager

from demystifygraphrag import constants
from .assets import preprocess_documents as assets_preprocess_documents

assets = load_assets_from_modules([
    assets_preprocess_documents,
])



defs = Definitions(
    assets=[*assets],
    resources={
      "io_manager": DuckDBPandasIOManager(database=constants.DATABASE_PATH),
    },
)

materialize(assets=[assets_preprocess_documents.preprocess])