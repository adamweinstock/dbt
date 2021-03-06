from dbt.api.object import APIObject
from dbt.logger import GLOBAL_LOGGER as logger  # noqa

POSTGRES_CREDENTIALS_CONTRACT = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'dbname': {
            'type': 'string',
        },
        'host': {
            'type': 'string',
        },
        'user': {
            'type': 'string',
        },
        'pass': {
            'type': 'string',
        },
        'port': {
            'oneOf': [
                {
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 65535,
                },
                {
                    'type': 'string'
                },
            ],
        },
        'schema': {
            'type': 'string',
        },
    },
    'required': ['dbname', 'host', 'user', 'pass', 'port', 'schema'],
}

SNOWFLAKE_CREDENTIALS_CONTRACT = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'account': {
            'type': 'string',
        },
        'user': {
            'type': 'string',
        },
        'password': {
            'type': 'string',
        },
        'database': {
            'type': 'string',
        },
        'schema': {
            'type': 'string',
        },
        'warehouse': {
            'type': 'string',
        },
        'role': {
            'type': 'string',
        },
    },
    'required': ['account', 'user', 'password', 'database', 'schema'],
}

BIGQUERY_CREDENTIALS_CONTRACT = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'method': {
            'enum': ['oauth', 'service-account', 'service-account-json'],
        },
        'project': {
            'type': 'string',
        },
        'schema': {
            'type': 'string',
        },
        'keyfile': {
            'type': 'string',
        },
        'keyfile_json': {
            'type': 'object',
        },
        'timeout_seconds': {
            'type': 'integer',
        },
    },
    'required': ['method', 'project', 'schema'],
}


CONNECTION_CONTRACT = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'type': {
            'enum': ['postgres', 'redshift', 'snowflake', 'bigquery'],
        },
        'name': {
            'type': ['null', 'string'],
        },
        'state': {
            'enum': ['init', 'open', 'closed', 'fail'],
        },
        'transaction_open': {
            'type': 'boolean',
        },
        'handle': {
            'type': ['null', 'object'],
        },
        'credentials': {
            'description': (
                'The credentials object here should match the connection '
                'type. Redshift uses the Postgres connection model.'
            ),
            'oneOf': [
                POSTGRES_CREDENTIALS_CONTRACT,
                SNOWFLAKE_CREDENTIALS_CONTRACT,
                BIGQUERY_CREDENTIALS_CONTRACT,
            ],
        }
    },
    'required': [
        'type', 'name', 'state', 'transaction_open', 'handle', 'credentials'
    ],
}


class PostgresCredentials(APIObject):
    SCHEMA = POSTGRES_CREDENTIALS_CONTRACT


class SnowflakeCredentials(APIObject):
    SCHEMA = SNOWFLAKE_CREDENTIALS_CONTRACT


class BigQueryCredentials(APIObject):
    SCHEMA = BIGQUERY_CREDENTIALS_CONTRACT


CREDENTIALS_MAPPING = {
    'postgres': PostgresCredentials,
    'redshift': PostgresCredentials,
    'snowflake': SnowflakeCredentials,
    'bigquery': BigQueryCredentials,
}


class Connection(APIObject):
    SCHEMA = CONNECTION_CONTRACT

    def validate(self):
        super(Connection, self).validate()
        # make sure our credentials match our adapter type
        ContractType = CREDENTIALS_MAPPING.get(self.get('type'))
        ContractType(**self.get('credentials'))
