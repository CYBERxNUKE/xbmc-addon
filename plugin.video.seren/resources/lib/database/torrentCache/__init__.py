# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import collections
import datetime
import time

import xbmcgui

from resources.lib.database import Database
from resources.lib.modules.globals import g

TV_CACHE_TYPE = "tvshows"
MOVIE_CACHE_TYPE = "movies"

schema = {
    MOVIE_CACHE_TYPE: {
        "columns": collections.OrderedDict(
            [
                ("trakt_id", ["INTEGER", "NOT NULL"]),
                ("hash", ["TEXT", "NOT NULL", "UNIQUE"]),
                ("package", ["TEXT", "NOT NULL"]),
                ("torrent_object", ["PICKLE", "NOT NULL"]),
                ("expires", ["INTEGER", "NOT NULL"])
            ]
        ),
        "table_constraints": ["PRIMARY KEY(trakt_id, hash, package)"],
        "default_seed": [],
    },
    TV_CACHE_TYPE: {
        "columns": collections.OrderedDict(
            [
                ("trakt_id", ["INTEGER", "NOT NULL"]),
                ("hash", ["TEXT", "NOT NULL", "UNIQUE"]),
                ("package", ["TEXT", "NOT NULL"]),
                ("torrent_object", ["PICKLE", "NOT NULL"]),
                ("expires", ["INTEGER", "NOT NULL"])
            ]
        ),
        "table_constraints": ["PRIMARY KEY(trakt_id, hash, package)"],
        "default_seed": [],
    }
}


class TorrentCache(Database):
    def __init__(self):
        super(TorrentCache, self).__init__(g.TORRENT_CACHE, schema)
        self.enabled = g.get_bool_setting("general.torrentCache")

    @staticmethod
    def _get_item_id_keys(item_meta):
        trakt_season_id = trakt_show_id = None
        trakt_id = item_meta["trakt_id"]

        if item_meta["info"]["mediatype"] == g.MEDIA_EPISODE:
            cache_type = TV_CACHE_TYPE
            trakt_season_id = item_meta["info"]["trakt_season_id"]
            trakt_show_id = item_meta["info"]["trakt_show_id"]
        else:
            cache_type = MOVIE_CACHE_TYPE

        return cache_type, trakt_id, trakt_season_id, trakt_show_id

    def get_torrents(self, item_meta):
        if not self.enabled:
            return []

        cache_type, trakt_id, trakt_season_id, trakt_show_id = TorrentCache._get_item_id_keys(item_meta)

        if cache_type == TV_CACHE_TYPE:
            torrent_list = self.fetchall(
                "SELECT torrent_object from {} "
                "WHERE expires > {} AND "
                "   (trakt_id={} AND package='single') "
                "   OR (trakt_id={} AND package='season') "
                "   OR (trakt_id={} AND package='show') ".format(
                    cache_type,
                    time.time(),
                    trakt_id,
                    trakt_season_id,
                    trakt_show_id
                )
            )
        else:
            torrent_list = self.fetchall(
                "SELECT torrent_object from {} "
                "WHERE trakt_id={} AND expires > {}".format(
                    cache_type,
                    trakt_id,
                    time.time()
                )
            )

        return [i["torrent_object"] for i in torrent_list]

    def add_torrent(self, item_meta, torrent_objects, expiration=None):
        if not self.enabled:
            return

        if expiration is None:
            expiration = datetime.timedelta(weeks=2)

        cache_type, trakt_id, trakt_season_id, trakt_show_id = TorrentCache._get_item_id_keys(item_meta)

        self.execute_sql(
            "REPLACE INTO {} (trakt_id, hash, package, torrent_object, expires) VALUES (?, ?, ?, ?, ?)".format(
                cache_type),
            (
                (
                    (
                        trakt_show_id if cache_type == TV_CACHE_TYPE and torrent_object["package"] == "show"
                        else trakt_season_id if cache_type == TV_CACHE_TYPE and torrent_object["package"] == "season"
                        else trakt_id
                    ),
                    torrent_object["hash"],
                    torrent_object["package"],
                    torrent_object,
                    time.time() + expiration.total_seconds()
                )
                for torrent_object in torrent_objects
            ),
        )

    def clear_item(self, item_meta, clear_packs=True):
        cache_type, trakt_id, trakt_season_id, trakt_show_id = TorrentCache._get_item_id_keys(item_meta)

        if cache_type == TV_CACHE_TYPE and clear_packs:
            self.execute_sql(
                "DELETE FROM {} "
                "WHERE (trakt_id={} AND package='single') "
                "   OR (trakt_id={} AND package='season') "
                "   OR (trakt_id={} AND package='show') ".format(
                    cache_type,
                    trakt_id,
                    trakt_season_id,
                    trakt_show_id
                )
            )
        else:
            self.execute_sql(
                "DELETE FROM {} "
                "WHERE trakt_id={} AND package='single' ".format(
                    cache_type,
                    trakt_id,
                )
            )

    def do_cleanup(self):
        busy_key = "torrentcache.db.clean.busy"
        if g.get_bool_runtime_setting(busy_key):
            return
        g.set_runtime_setting(busy_key, True)

        self.execute_sql([
            "DELETE FROM {} where expires < ?".format(MOVIE_CACHE_TYPE),
            "DELETE FROM {} where expires < ?".format(TV_CACHE_TYPE)],
            (time.time(),))
        g.clear_runtime_setting(busy_key)

    def clear_all(self):
        g.show_busy_dialog()
        self.rebuild_database()
        xbmcgui.Dialog().ok(g.ADDON_NAME, g.get_language_string(30480))
        g.close_busy_dialog()
