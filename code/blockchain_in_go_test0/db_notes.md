# data structure

## 2 buckets to store data

1. blocks - stores metadata describing all the blocks
2. chainstate - stores the state of a chain
   - unspent transaction outputs and some metadata

- blocks are stored as separate files on disk
  - this is for performance
    - reading a single block only requires loading of that single block into
      memory - no others at the same time

## key -> value pairs in the blocks

1. 'b' + 32-byte block hash -> block index record
2. 'f' + 4-byte file number -> file information record
3. 'l' -> 4-byte file number: the last block file number used
4. 'R' -> 1-byte boolean: whether we're in the process of re-indexing
5. 'F' + 1-byte flag name length + flag name string -> 1-byte boolean:
   various flags that can be on or off
6. 't' + 32-byte transaction hash -> transaction index record

## chainstate - key -> value pairs

1. 'c' + 32-byte transaction hash -> unspent transaction output record for that
   transaction
2. 'B' -> 32-byte block hash: the block hash up to which the database represents
   the unspent transaction outputs

## key -> value pairs used in this go blockchain test

1. 32-byte block-hash -> Block structure (serialized)
2. 'l' -> the hash of the last block in a chain