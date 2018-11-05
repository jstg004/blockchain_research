'''
test tampered data
'''

import hashlib, json, datetime


with open('test.json') as infile:
    blockchain_load = json.load(infile)

def hash_blocks(blocks):
    prev_hash = None

    for block in blocks:
        block_serialized = json.dumps(block, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(block_serialized).hexdigest()
        prev_hash = block_hash

    return prev_hash



'''
Block ef2ef582661a8b9fbca94125c4445626c30471c190ac64e82b27f61913c49139
    hashes the previous block to
    1a88b444b22bbb7f72e1a49e8478c8313592ef2a7cdbf0fea7a8a29c146dd05b

{"chain": {"prev_hash": null, "genesis": true, "data": {"name": "genesis",
"name_id": 0, "time": "2018-11-05 04:17:39.997416"}},
"aa1ef5c8fa057319d1938b053962725f790da1ea92c72bc37e1708547651b85c": {"prev_hash":
"275ae0a9baf3df186e1b256313b55fa0bfa19076834b4cdee12a4b9258fe754e", "genesis":false, "data": {"name": "dsafsda", "name_id": "asdfasd", "time": "2018-11-05
04:22:25.563387"}},
"ef2ef582661a8b9fbca94125c4445626c30471c190ac64e82b27f61913c49139": {"prev_hash":
"1a88b444b22bbb7f72e1a49e8478c8313592ef2a7cdbf0fea7a8a29c146dd05b", "genesis":
false, "data": {"name": "sdfasd", "name_id": "sadfasdfas", "time": "2018-11-05
04:22:31.580562"}}}



Block aa1ef5c8fa057319d1938b053962725f790da1ea92c72bc37e1708547651b85c
    has value of key name changed to dsadddddddfsda
    so block cc97727e151319629216c46d0b31d1654b52e22222e7535534bf0f5104b4dba6
    hashes the previous block to
    c0a1b49622fcbe35f7abc00a988068cf28d7b3c48192ef00deb174d2aedbdb7f
    when the hash is compared to the other blockchains the hash will not match
    showing that the data has been changed without having to check the data
    it self

{"chain": {"prev_hash": null, "genesis": true, "data": {"name": "genesis", "name_id": 0, "time": "2018-11-05 04:17:39.997416"}},
"aa1ef5c8fa057319d1938b053962725f790da1ea92c72bc37e1708547651b85c": {"prev_hash":
"275ae0a9baf3df186e1b256313b55fa0bfa19076834b4cdee12a4b9258fe754e", "genesis":
false, "data": {"name": "dsadddddddfsda", "name_id": "asdfasd", "time": "2018-11-05
04:22:25.563387"}},
"cc97727e151319629216c46d0b31d1654b52e22222e7535534bf0f5104b4dba6": {"prev_hash":
"c0a1b49622fcbe35f7abc00a988068cf28d7b3c48192ef00deb174d2aedbdb7f", "genesis":
false, "data": {"name": "sadfasd", "name_id": "asdfasdf", "time": "2018-11-05
04:23:18.447183"}}}


Block aa1ef5c8fa057319d1938b053962725f790da1ea92c72bc37e1708547651b85c
    has value of key name changed back to original state dsafsda
    so block aeebe7fd1028464bb98749e93d371fabc66194b5c630ac21b93369d80e7d0561
    hashes the previous block to
    1a88b444b22bbb7f72e1a49e8478c8313592ef2a7cdbf0fea7a8a29c146dd05b
    which is the correct hash for the original data

{"chain": {"prev_hash": null, "genesis": true, "data": {"name": "genesis",
"name_id": 0, "time": "2018-11-05 04:17:39.997416"}},
"aa1ef5c8fa057319d1938b053962725f790da1ea92c72bc37e1708547651b85c": {"prev_hash":
"275ae0a9baf3df186e1b256313b55fa0bfa19076834b4cdee12a4b9258fe754e", "genesis":
false, "data": {"name": "dsafsda", "name_id": "asdfasd", "time": "2018-11-05
04:22:25.563387"}},
"aeebe7fd1028464bb98749e93d371fabc66194b5c630ac21b93369d80e7d0561": {"prev_hash":
"1a88b444b22bbb7f72e1a49e8478c8313592ef2a7cdbf0fea7a8a29c146dd05b", "genesis":
false, "data": {"name": "sdfasd", "name_id": "asdfasd", "time": "2018-11-05
04:24:51.018655"}}}
'''
