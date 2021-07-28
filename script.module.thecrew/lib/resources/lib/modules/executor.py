# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    -Mofidied by The Crew
    -Copyright (C) 2019 lambda


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import concurrent.futures
from itertools import islice
import xbmc
import threading

Executor = concurrent.futures.ThreadPoolExecutor


def execute(f, iterable, stop_flag=None, workers=10, timeout = 30):
    with Executor(max_workers=workers) as executor:
        threading.Timer(timeout, stop_flag.set)
        for future in _batched_pool_runner(executor, workers, f, iterable):

            if xbmc.abortRequested:
                break
            if stop_flag and stop_flag.isSet():
                break
            yield future.result()


def _batched_pool_runner(pool, batch_size, f, iterable):
    it = iter(iterable)

    # Submit the first batch of tasks.
    futures = set(pool.submit(f, x) for x in islice(it, batch_size))

    while futures:
        done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

        # Replenish submitted tasks up to the number that completed.
        futures.update(pool.submit(f, x) for x in islice(it, len(done)))

        for d in done:
            yield d