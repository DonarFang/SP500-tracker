"""Production composition configuration only; no account/history writes."""
from __future__ import annotations
import json
from pathlib import Path
from e1r_engine.core import E1RCoreEngine, E1RCoreEngineConfig
from e1r_engine.lss07 import LSS07Config, VERSION

ENGINE_ID = 'FD-M3180125-SP500-TOP3-engine'
CONFIG_REL = 'config/lss07/production_v1.json'
DEPLOYMENT_ID = 'LSS07F-step-6-v1'


def load_deployment(repo_root):
    path = Path(repo_root) / CONFIG_REL
    if not path.exists():
        return None
    row = json.loads(path.read_text(encoding='utf-8'))
    if (not isinstance(row, dict) or row.get('schema_version') != '1.0'
            or row.get('deployment_id') != DEPLOYMENT_ID
            or row.get('strategy_version') != VERSION
            or row.get('tracks') != ['forward', 'live']
            or row.get('history_policy') != 'PRESERVE_NO_REPLAY'
            or row.get('live_execution') != 'RECOMMENDATION_USER_CONFIRMED'):
        raise ValueError('Invalid frozen LSS07 production deployment')
    LSS07Config(row.get('enabled'), row.get('effective_signal_date'))
    if row.get('effective_signal_date') is None:
        raise ValueError('Deployment must retain its effective signal date')
    return row


def production_engine(track, runtime_root, *, repo_root=None):
    """Only the exact official track root receives the opt-in configuration.

    Research, temporary compositions and unactivated Live retain defaults.
    Core remains the sole owner of Regime, Gate and all strategy decisions.
    """
    if track not in ('forward', 'live'):
        raise ValueError('Unknown LSS07 production track')
    root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
    official = root / 'exports/official' / ENGINE_ID / track
    if track == 'forward':
        official = official / 'runtime'
    if Path(runtime_root).resolve() != official.resolve():
        return E1RCoreEngine()
    row = load_deployment(root)
    config = LSS07Config() if row is None else LSS07Config(
        enabled=row['enabled'], effective_signal_date=row['effective_signal_date'])
    return E1RCoreEngine(E1RCoreEngineConfig(lss07=config))
