"""Explicit identity/provider-symbol mapping registry."""

from dataclasses import replace
from typing import Dict, Iterable, List, Optional

from .contracts import MappingStatus, SecurityIdentity


class IdentityConflict(ValueError):
    pass


class IdentityRegistry:
    def __init__(self, identities: Iterable[SecurityIdentity] = ()) -> None:
        self._by_security_id: Dict[str, SecurityIdentity] = {}
        self._by_engine_symbol: Dict[str, SecurityIdentity] = {}
        self._by_yahoo_symbol: Dict[str, SecurityIdentity] = {}
        for identity in identities:
            self.add(identity)

    def add(self, identity: SecurityIdentity) -> None:
        if not identity.security_id or not identity.engine_symbol:
            raise IdentityConflict("security_id and engine_symbol are required")
        if identity.asset_type not in {"COMMON_STOCK", "INDEX"}:
            raise IdentityConflict("unsupported asset_type")
        existing = self._by_security_id.get(identity.security_id)
        if existing and existing != identity:
            raise IdentityConflict("security_id already has an active mapping")
        for mapping, key, label in (
            (self._by_engine_symbol, identity.engine_symbol, "engine_symbol"),
            (self._by_yahoo_symbol, identity.yahoo_symbol, "yahoo_symbol"),
        ):
            other = mapping.get(key)
            if other and other.security_id != identity.security_id:
                raise IdentityConflict(label + " maps to multiple security identities")
        self._by_security_id[identity.security_id] = identity
        self._by_engine_symbol[identity.engine_symbol] = identity
        self._by_yahoo_symbol[identity.yahoo_symbol] = identity

    def revise(self, security_id: str, **changes: object) -> SecurityIdentity:
        current = self._by_security_id[security_id]
        revised = replace(current, **changes)
        self.remove(security_id)
        try:
            self.add(revised)
        except Exception:
            self.add(current)
            raise
        return revised

    def remove(self, security_id: str) -> None:
        current = self._by_security_id.pop(security_id)
        self._by_engine_symbol.pop(current.engine_symbol, None)
        self._by_yahoo_symbol.pop(current.yahoo_symbol, None)

    def get_by_engine_symbol(self, symbol: str) -> Optional[SecurityIdentity]:
        return self._by_engine_symbol.get(symbol)

    def require_verified(self, symbol: str) -> SecurityIdentity:
        identity = self.get_by_engine_symbol(symbol)
        if identity is None or identity.mapping_status != MappingStatus.VERIFIED:
            raise IdentityConflict("symbol is unmapped or not verified: " + symbol)
        return identity

    def to_list(self) -> List[dict]:
        return [
            self._by_security_id[key].to_dict()
            for key in sorted(self._by_security_id)
        ]


def canonical_seed_identities() -> List[SecurityIdentity]:
    return [
        SecurityIdentity("SEC-BRK-B", "BRK.B", "BRK.B", "BRK-B", "NYSE"),
        SecurityIdentity("SEC-BF-B", "BF.B", "BF.B", "BF-B", "NYSE"),
        SecurityIdentity("IDX-SPX", "SPX", "SPX", "^GSPC", "INDEX", asset_type="INDEX"),
        SecurityIdentity("IDX-NDX", "NDX", "NDX", "^NDX", "INDEX", asset_type="INDEX"),
        SecurityIdentity("IDX-SOX", "SOX", "SOX", "^SOX", "INDEX", asset_type="INDEX"),
        SecurityIdentity("IDX-VIX", "VIX", "VIX", "^VIX", "INDEX", asset_type="INDEX"),
    ]
