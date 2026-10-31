# Selective semantic checks

## Missing versus falsey
If an optional argument or mapping lookup behaves incorrectly, distinguish None or a missing sentinel from 0, False, an empty string, and an empty container. Check whether `x or default` incorrectly discards a valid explicit value. Test omitted, explicit None and one falsey valid value only when the API distinguishes them. Preserve documented defaults and validation errors.

## Iterators, state and ownership
Repeated iteration can consume a generator. Check whether validation, logging or length computation exhausts the stream before use. Materialize once only if the API permits eager consumption. Check whether mutable defaults or class-level containers leak state between instances; test two independent instances. Copy only at the correct ownership boundary, preserving intentional mutation and object identity where documented.

## Inheritance and dispatch
Look for an isinstance/subclass branch that incorrectly excludes a supported derived class, or a broad superclass case that shadows a more specific one. Follow the method-resolution order and existing extension hooks. When a constructor is overridden, determine which required attributes the superclass initializes. Avoid replacing polymorphic dispatch with checks for a single literal type.

## Serialization and parsing
Separate internal values from their serialized representation. Preserve aliases, explicit exclusions, nesting and encoding. Trace both encode and decode when a round trip is required. Check one ordinary case and the specific escaping, empty value, Unicode, delimiter or boundary case from the issue. Follow protocol semantics already implemented in the repository; do not normalize arbitrary user data unnecessarily.

## Async and resource lifecycle
Match synchronous and asynchronous implementations when both expose the affected API. Await awaitables in the correct layer. Verify cleanup on the documented failure path and retain exception propagation. Do not catch BaseException or suppress cancellation merely to make an example pass. Check that context-manager entry and exit own the resource being closed and that repeated close behavior matches surrounding code.

## Validation and exceptions
Validate before observable side effects when the API promises rejection. Match the established exception class, argument naming and message style. A conversion can silently accept invalid inputs or reject valid subclasses; inspect local conventions before choosing type checks. Test the requested invalid input and one nearby valid input, without expanding validation beyond the task.

## Imports and compatibility
Inspect supported Python/dependency versions before using a newer language feature or API. A change that imports a symbol only present in a different dependency release is not a portable fix. Check the actual module's __file__ if a reproducer unexpectedly passes. Prefer behavior assertions on imported source; ast.parse establishes syntax only.
