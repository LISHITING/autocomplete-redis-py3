autocomplete-redis-py3
======================

对[autocomplete-redis](https://github.com/fengli/autocomplete-redis)进行了python3的适应，并将分词由pymmseg更改为jieb结巴分词。因为pymmseg截止目前仍未支持python3。

autocomplete-redis-py3 is modified version of [autocomplete-redis](https://github.com/fengli/autocomplete-redis) to adapt python3 and using jieba for segementation instead of pymmseg (since pymmseg [can not be used for py3 yet](https://github.com/pluskid/pymmseg-cpp/issues/6)).


安装部分 Installation
---------
需要安装jieba分词，redis模块用于链接后台数据以及simplejson模块。
Need jieba for chinese NLP segementation，redis as backend db and simplejson.

* pip install jieba
* pip install simplejson
* pip install autocomplete-redis-py3： `pip install git+https://github.com/LISHITING/autocomplete-redis-py3.git`

快速入门 Quick start
----------
* 先定义一组数据用于补全的
* Assume you have few items to index.

```python
items=[{"uid":'1', "score":9, "term": "hello world, that's great"},
       {"uid":'2', "score":10, "term": "what the hell or yell"},
       {"uid":'3', "score":8.5, "term":"World is like a box of chocolate"},
      ]
```


* 然后import该包，将刚才定义的items加载进去，然后调用`search_query`来搜索
* The code for build the index and search is simple:

```python
from autocomplete import Autocomplete

#build index
au = Autocomplete ("scope")
for item in items:
  au.add_item (item)
#search
results = au.search_query ('hel')

print (results)
[{'term': 'what the hell or yell', 'score': 10, 'uid': '2'}, {'term': "hello world, that's great", 'score': 9, 'uid': '1'}]
```


API
---------------
以下部分与原项目API基本一致。
The following API discriptions remain unchanged.

* Convention: the item you pass to `autocomplete-py3` should have at least `"uid"` and `"term"`, `"score"` is optional, but it's important if you want to return based on ranking. And you could have other fields as you like.

```python
{"uid":'1', "score":9, "term": u"hello world, that's great", 'meta':"1992"}
```
  * `uid`: the unique identifier for your item
  * `score`: the returned items sorted by this value.
  * `term`: the string to be indexed.

* `def __init__ (self, scope, redisaddr="localhost", limits=5, cached=True)`

  * scope: Scope allows you to index multiple independent indexes.
  * redisaddr: your redis address
  * limits: How many results you want to get.
  * cached: Cache multiple keys combination?

* `def del_index (self)`

Delete all the indexes. Warning: all data will be deleted.

* `def add_item (self,item)`

Add item to index.

* `def del_item (self,item)`

Delete item from index.

* `def update_item (self, item)`

Update item indexed with item['uid'] with the new version.

* `def search_query (self,prefix)`

Search in database for all items that `item['term']` included `PREFIX`
