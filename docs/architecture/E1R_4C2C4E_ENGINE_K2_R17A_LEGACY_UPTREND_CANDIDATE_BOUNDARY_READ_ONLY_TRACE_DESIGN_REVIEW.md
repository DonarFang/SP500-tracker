# E1R K2 R17A Read-Only Instrumentation Architecture

Generated UTC: 2026-07-11T11:33:11.616699+00:00

## Core rule

Instrumentation is observational only and must not participate in strategy decisions.

## Allowed snapshot operations

- tuple(collection)
- tuple(mapping.keys())
- tuple(dict(record) for record in records)
- deterministic JSON serialization
- SHA256 calculation on serialized trace payload

## Forbidden operations

- in-place sort
- append to strategy collections
- pop or remove
- update strategy dictionaries
- consume iterators
- call strategy functions twice
- mutate cash, holdings, positions, or pending orders
- alter dates or execution sequence

## Required proof before instrumentation

- Every trace point has an exact source line.
- Every trace point has a stable source variable.
- Trace-disabled and trace-enabled outputs are byte-identical.
- Maximum live holdings remains 3.
