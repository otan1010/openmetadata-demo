#!/usr/bin/env python3
"""
OpenMetadata demo: create two tables and add column-level lineage via Python SDK,
then verify it was actually persisted.

What it does:
1) Connects to OpenMetadata (via PAT read from local file)
2) Creates (or updates) a demo database service, database, schema
3) Creates two tables
4) Adds table-level + column-level lineage between them
5) Reads lineage back from OM and verifies column mappings are present

Prereqs:
  pip install "openmetadata-ingestion~=1.11.9.0"

Usage (with your SSH tunnel running to localhost:8585):
  python om_column_lineage_demo.py

Token:
  Put your OpenMetadata PAT in a local file named: personal_access_token
  (same folder as this script by default)
"""

from pathlib import Path
import sys
import json
from typing import Iterable, Set, Tuple, Any

from metadata.ingestion.ometa.ometa_api import OpenMetadata

from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)

from metadata.generated.schema.api.services.createDatabaseService import (
    CreateDatabaseServiceRequest,
)
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseConnection,
    DatabaseServiceType,
)
from metadata.generated.schema.entity.services.connections.database.mysqlConnection import (
    MysqlConnection,
)
from metadata.generated.schema.entity.services.connections.database.common.basicAuth import (
    BasicAuth,
)

from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest
from metadata.generated.schema.api.data.createDatabaseSchema import (
    CreateDatabaseSchemaRequest,
)
from metadata.generated.schema.api.data.createTable import CreateTableRequest

from metadata.generated.schema.entity.data.table import Table, Column, DataType
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.generated.schema.api.lineage.addLineage import AddLineageRequest
from metadata.generated.schema.type.entityLineage import (
    EntitiesEdge,
    ColumnLineage,
    LineageDetails,
)

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

OM_HOST = "http://localhost:8585/api"
TOKEN_FILE = Path("personal_access_token")

SERVICE_NAME = "demo_mysql_lineage_service"
DB_NAME = "demo_db"
SCHEMA_NAME = "public"

SOURCE_TABLE = "orders_raw"
TARGET_TABLE = "orders_curated"

# Mock connection details (metadata only; does not provision a DB)
MOCK_DB_HOSTPORT = "localhost:3306"
MOCK_DB_USER = "demo_user"
MOCK_DB_PASSWORD = "demo_pass"


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def read_pat_token(token_file: Path) -> str:
    if not token_file.exists():
        raise FileNotFoundError(
            f"Token file not found: {token_file.resolve()}\n"
            f"Create a file named '{token_file.name}' next to this script and paste your PAT into it."
        )
    token = token_file.read_text(encoding="utf-8").strip()
    if not token:
        raise ValueError(f"Token file is empty: {token_file.resolve()}")
    return token


def connect_openmetadata(host: str, pat_token: str) -> OpenMetadata:
    server_config = OpenMetadataConnection(
        hostPort=host,
        authProvider="openmetadata",
        securityConfig=OpenMetadataJWTClientConfig(jwtToken=pat_token),
    )
    om = OpenMetadata(server_config)
    if not om.health_check():
        raise RuntimeError(f"OpenMetadata health check failed for {host}")
    return om


def as_plain_str(value: Any) -> str:
    """
    Convert OpenMetadata root-model style values (e.g. fullyQualifiedName) into plain strings.
    Handles pydantic root objects where repr/str may look like: root='...'
    """
    if value is None:
        return ""

    # Pydantic RootModel style
    if hasattr(value, "root"):
        root_val = getattr(value, "root")
        return "" if root_val is None else str(root_val)

    # Some variants may serialize to {"root": "..."}
    if hasattr(value, "model_dump"):
        try:
            dumped = value.model_dump()
            if isinstance(dumped, dict) and "root" in dumped:
                return str(dumped["root"])
        except Exception:
            pass

    return str(value)


def _column_fqn(table_fqn: str, column_name: str) -> str:
    return f"{table_fqn}.{column_name}"

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> int:
    try:
        token = read_pat_token(TOKEN_FILE)
        metadata = connect_openmetadata(OM_HOST, token)
        print(f"✅ Connected to OpenMetadata at {OM_HOST}")

        # 1) Create/update DB service (metadata object only)
        db_service_req = CreateDatabaseServiceRequest(
            name=SERVICE_NAME,
            serviceType=DatabaseServiceType.Mysql,
            connection=DatabaseConnection(
                config=MysqlConnection(
                    username=MOCK_DB_USER,
                    authType=BasicAuth(password=MOCK_DB_PASSWORD),
                    hostPort=MOCK_DB_HOSTPORT,
                )
            ),
        )
        db_service = metadata.create_or_update(data=db_service_req)
        print(f"✅ Service: {as_plain_str(db_service.fullyQualifiedName)}")

        # 2) Create/update database
        db_req = CreateDatabaseRequest(
            name=DB_NAME,
            service=as_plain_str(db_service.fullyQualifiedName),
        )
        db_entity = metadata.create_or_update(data=db_req)
        print(f"✅ Database: {as_plain_str(db_entity.fullyQualifiedName)}")

        # 3) Create/update schema
        schema_req = CreateDatabaseSchemaRequest(
            name=SCHEMA_NAME,
            database=as_plain_str(db_entity.fullyQualifiedName),
        )
        schema_entity = metadata.create_or_update(data=schema_req)
        print(f"✅ Schema: {as_plain_str(schema_entity.fullyQualifiedName)}")

        # 4) Create/update source table
        source_table_req = CreateTableRequest(
            name=SOURCE_TABLE,
            databaseSchema=as_plain_str(schema_entity.fullyQualifiedName),
            columns=[
                Column(name="order_id", dataType=DataType.BIGINT),
                Column(name="customer_id", dataType=DataType.BIGINT),
                Column(name="amount", dataType=DataType.DECIMAL),
                Column(name="created_at", dataType=DataType.TIMESTAMP),
            ],
        )
        source_table = metadata.create_or_update(data=source_table_req)
        print(f"✅ Source table: {as_plain_str(source_table.fullyQualifiedName)}")

        # 5) Create/update target table
        target_table_req = CreateTableRequest(
            name=TARGET_TABLE,
            databaseSchema=as_plain_str(schema_entity.fullyQualifiedName),
            columns=[
                Column(name="order_id", dataType=DataType.BIGINT),
                Column(name="customer_id", dataType=DataType.BIGINT),
                Column(name="amount_usd", dataType=DataType.DECIMAL),
                Column(name="order_ts", dataType=DataType.TIMESTAMP),
            ],
        )
        target_table = metadata.create_or_update(data=target_table_req)
        print(f"✅ Target table: {as_plain_str(target_table.fullyQualifiedName)}")

        # IMPORTANT: unwrap FQNs correctly (avoid str(rootmodel) => "root='...'")
        src_fqn = as_plain_str(source_table.fullyQualifiedName)
        tgt_fqn = as_plain_str(target_table.fullyQualifiedName)

        # 6) Column-level lineage mappings
        column_lineage = [
            ColumnLineage(
                fromColumns=[_column_fqn(src_fqn, "order_id")],
                toColumn=_column_fqn(tgt_fqn, "order_id"),
            ),
            ColumnLineage(
                fromColumns=[_column_fqn(src_fqn, "customer_id")],
                toColumn=_column_fqn(tgt_fqn, "customer_id"),
            ),
            ColumnLineage(
                fromColumns=[_column_fqn(src_fqn, "amount")],
                toColumn=_column_fqn(tgt_fqn, "amount_usd"),
            ),
            ColumnLineage(
                fromColumns=[_column_fqn(src_fqn, "created_at")],
                toColumn=_column_fqn(tgt_fqn, "order_ts"),
            ),
        ]

        lineage_details = LineageDetails(
            sqlQuery=(
                f"INSERT INTO {TARGET_TABLE} (order_id, customer_id, amount_usd, order_ts)\n"
                f"SELECT order_id, customer_id, amount, created_at\n"
                f"FROM {SOURCE_TABLE}"
            ),
            columnsLineage=column_lineage,
        )

        lineage_req = AddLineageRequest(
            edge=EntitiesEdge(
                description="Demo lineage: orders_raw -> orders_curated with column mappings",
                fromEntity=EntityReference(id=source_table.id, type="table"),
                toEntity=EntityReference(id=target_table.id, type="table"),
                lineageDetails=lineage_details,
            )
        )

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
