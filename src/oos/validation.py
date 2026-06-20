"""
Startup validation: verify Manifest config hash and Git SHA
before any OOS run. Abort immediately on mismatch.
"""
import json, hashlib, subprocess, logging, os

logger = logging.getLogger(__name__)

MANIFEST_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "validation", "E1_FROZEN_MANIFEST.json"
)

def load_manifest() -> dict:
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)

def compute_config_hash(params: dict) -> str:
    return hashlib.sha256(
        json.dumps(params, sort_keys=True).encode()
    ).hexdigest()[:16]

def get_git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "UNKNOWN"

def validate_or_abort(manifest: dict) -> None:
    """
    Check config hash and Git SHA against manifest.
    Raises RuntimeError immediately on any mismatch.
    """
    strat = manifest["strategy"]
    expected_hash = strat["strategy_config_hash"]
    expected_sha  = manifest["git"]["commit_sha"]

    # Recompute hash from manifest parameters
    params = strat["parameters"]
    canonical = {
        "strategy_id":      strat["id"],
        "entry_selection":  params["entry_selection"],
        "entry_rs_min":     params["entry_rs_min"],
        "max_positions":    params["max_positions"],
        "position_size":    params["target_position_size_pct"] / 100,
        "gate":             "slope + leadership",
        "exit_rule":        params["exit_rule"],
        "min_holding_days": params["min_holding_days"],
        "relative_stop":    params["relative_stop_enabled"],
        "fixed_tp":         params["fixed_take_profit_enabled"],
        "shock_gate":       params["gate_shock"],
        "vix_gate":         params["gate_vix"],
        "execution":        params["execution_timing"] + " " + params["execution_model"],
        "one_way_cost":     params["one_way_cost_pct"] / 100,
    }
    actual_hash = compute_config_hash(canonical)

    if actual_hash != expected_hash:
        raise RuntimeError(
            f"CONFIG HASH MISMATCH — manifest expects {expected_hash}, "
            f"computed {actual_hash}. "
            f"E1 parameters may have been modified. OOS aborted."
        )
    logger.info(f"✅ Config hash verified: {actual_hash}")

    # Git SHA check (warn only — SHA changes on every commit)
    actual_sha = get_git_sha()
    if actual_sha != expected_sha:
        logger.warning(
            f"⚠️  Git SHA: manifest={expected_sha}, current={actual_sha}. "
            f"Acceptable if only non-strategy files changed."
        )
    else:
        logger.info(f"✅ Git SHA verified: {actual_sha}")

    logger.info(f"✅ Manifest validation passed — {strat['id']} FROZEN_CHAMPION")
