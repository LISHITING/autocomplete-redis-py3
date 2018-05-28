# -*- coding:utf-8 -*-

import redis
import simplejson
import jieba


# -*- coding:utf-8 -*-

class Autocomplete(object):
    def __init__(self, scope, redisaddr="localhost", limits=5, cached=True):
        self.r = redis.Redis(redisaddr)
        self.scope = scope
        self.cached = cached
        self.limits = limits
        self.database = "database:%s" % scope
        self.indexbase = "indexbase:%s" % scope

    #         mmseg.Dictionary.load_dictionaries ()

    def _get_index_key(self, key):
        return "%s:%s" % (self.indexbase, key)

    def del_index(self):
        prefixs = self.r.smembers(self.indexbase)
        for prefix in prefixs:
            self.r.delete(self._get_index_key(prefix))
            self.r.delete(self.indexbase)
            self.r.delete(self.database)

    def sanity_check(self, item):
        for key in ("uid", "term"):
            if key not in item:
                raise Exception("Item should have key %s" % key)

    def add_item(self, item):
        self.sanity_check(item)
        self.r.hset(self.database, item.get('uid'), simplejson.dumps(item))
        for prefix in self.prefixs_for_term(item['term']):
            self.r.sadd(self.indexbase, prefix)
            self.r.zadd(self._get_index_key(prefix), item.get('uid'), item.get('score', 0))

    def del_item(self, item):
        for prefix in self.prefixs_for_term(item['term']):
            self.r.zrem(self._get_index_key(prefix), item.get('uid'))
            if not self.r.zcard(self._get_index_key(prefix)):
                self.r.delete(self._get_index_key(prefix))
                self.r.srem(self.indexbase, prefix)

    def update_item(self, item):
        self.del_item(item)
        self.add_item(item)

    def prefixs_for_term(self, term):
        term = term.lower()
        prefixs = []
        tokens = jieba.lcut(term)
        for token in tokens:
            word = token
            for i in range(1, len(word) + 1):
                prefixs.append(word[:i])
        return prefixs

    def normalize(self, prefix):
        tokens = jieba.lcut(prefix.lower())
        return tokens

    def search_query(self, prefix):
        search_strings = self.normalize(prefix)

        if not search_strings: return []

        cache_key = self._get_index_key(('|').join(search_strings))

        if not self.cached or not self.r.exists(cache_key):
            self.r.zinterstore(cache_key, list(map(lambda x: self._get_index_key(x), search_strings)))
            self.r.expire(cache_key, 10 * 60)

        ids = self.r.zrevrange(cache_key, 0, self.limits)
        if not ids: return ids
        return list(map(lambda x: simplejson.loads(x), self.r.hmget(self.database, *ids)))

