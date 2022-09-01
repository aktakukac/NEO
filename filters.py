"""Provide filters for querying close approaches and limit the generated
results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest
from the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from
    the user's options at the command line. Each one corresponds to a different
    type of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that
    occurred on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of
    `NEODatabase` because the main module directly passes this result to that
    method. For now, this can be thought of as a collection of
    `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach`
    occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach`
    occurs.
    :param distance_min: A minimum nominal approach distance for a matching
    `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching
    `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching
    `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching
    CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching
    CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching
    `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is
    potentially hazardous.
    :return: A collection of filters for use with `query`.
    """

    arguments = locals()

    filters = []

    if arguments['date']:
        filters.append({
            'filtername': 'date',
            'operator': operator.eq,
            'object': 'CA',
            'attr': 'time',
            'value': arguments['date']})
    if arguments['start_date']:
        filters.append({
            'filtername': 'start_date',
            'operator': operator.ge,
            'object': 'CA',
            'attr': 'time',
            'value': arguments['start_date']})
    if arguments['end_date']:
        filters.append({
            'filtername': 'end_date',
            'operator': operator.le,
            'object': 'CA',
            'attr': 'time',
            'value': arguments['end_date']})
    if arguments['distance_min']:
        filters.append({
            'filtername': 'distance_min',
            'operator': operator.ge,
            'object': 'CA',
            'attr': 'distance',
            'value': arguments['distance_min']})
    if arguments['distance_max']:
        filters.append({
            'filtername': 'distance_max',
            'operator': operator.le,
            'object': 'CA',
            'attr': 'distance',
            'value': arguments['distance_max']})
    if arguments['velocity_min']:
        filters.append({
            'filtername': 'velocity_min',
            'operator': operator.ge,
            'object': 'CA',
            'attr': 'velocity',
            'value': arguments['velocity_min']})
    if arguments['velocity_max']:
        filters.append({
            'filtername': 'velocity_max',
            'operator': operator.le,
            'object': 'CA',
            'attr': 'velocity',
            'value': arguments['velocity_max']})
    if arguments['diameter_min']:
        filters.append({
            'filtername': 'diameter_min',
            'operator': operator.ge,
            'object': 'NEO',
            'attr': 'diameter',
            'value': arguments['diameter_min']})
    if arguments['diameter_max']:
        filters.append({
            'filtername': 'diameter_max',
            'operator': operator.le,
            'object': 'NEO',
            'attr': 'diameter',
            'value': arguments['diameter_max']})
    if arguments['hazardous'] is not None:
        filters.append({
            'filtername': 'hazardous',
            'operator': operator.eq,
            'object': 'NEO',
            'attr': 'hazardous',
            'value': arguments['hazardous']})

    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """

    if n == 0 or n is None:
        for element in iterator:
            yield element
    else:
        for i, element in enumerate(iterator):
            if i < n:
                yield element
            else:
                break
