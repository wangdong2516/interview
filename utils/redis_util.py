import aioredis
from typing import List


class AsyncRedisUtil(object):
    """
        异步Redis操作工具(基于aioredis实现redis的异步操作)，对于字符串类型的数据，默认会解码
    """

    def __init__(self, host, port=6379, db=0, **kwargs):
        """
            初始化方法，连接redis
        Args:
            host: redis主机地址，可以是TCP或者是UNIX地址
            port:端口号，默认是6379
            db:数据库索引，默认是0号库
            **kwargs:
                username:连接redis的用户名
                password:连接redis的密码
        """
        self.host = host
        self.port = port
        if not kwargs.get('decode_responses'):
            kwargs['decode_responses'] = True
        self.client = aioredis.from_url(
            self.host, port=self.port, db=db, **kwargs
        )
        assert self.client is not None

    async def get(self, key: str) -> str:
        """
            获取字符串类型key的值(字符串指令)
        Args:
            key: 需要获取的key

        Returns:

        """
        value = await self.client.get(key)
        return value

    async def mget(self, keys: List[str], *args) -> List[str]:
        """
            获取多个字符串类型的key对应的值(字符串指令)
        Args:
            keys: 需要获取的key组成的列表
            *args:

        Returns:
            keys中每一项对应的value组成的列表，顺序同key的顺序
        """
        values = await self.client.mget(keys, *args)
        return values

    async def set(
            self, key: str, value: str,
            ex: int = None, px: int = None, nx: bool = False, xx: bool = False,
            keepttl: bool = False
    ) -> bool:
        """
            设置一个字符串类型的key:value(字符串指令)
        Args:
            key:需要设置的key
            value:给key设置的value
            ex:给key设置的过期时间，精确到秒
            px:给key设置的过期时间，精确到毫秒
            nx:是否只有当key不存在的时候进行设置，存在的时候不做任何操作，默认为False
            xx:是否只有当key存在的时候进行设置，不存在的时候不做任何操作，默认为False
            keepttl:是否保留原来key的有效时间
        Returns:

        """
        result = await self.client.set(
            key, value, ex=ex, px=px, nx=nx, xx=xx, keepttl=keepttl
        )
        if result is None:
            return False
        return result

    async def get_range(self, key:str, start: int, end: int):
        """获取指定范围内的字符串的子串(字符串指令)"""
        return await self.client.getrange(key, start, end)

    substr = get_range

    async def incr(self, key):
        """对指定key的值进行加1操作(字符串指令)"""
        return await self.client.incr(key, amount=1)

    async def incr_by(self, key, amount):
        """对指定key的值进行加amount操作(字符串指令)"""
        if amount < 0:
            return await self.client.decrby(key, amount=abs(amount))
        return await self.client.incrby(key, amount)

    async def decr(self, key):
        """对指定key的值进行减1操作(字符串指令)"""
        return await self.client.decr(key, amount=1)

    async def decr_by(self, key, amount):
        """对指定key的值进行减amount操作(字符串指令)"""
        if amount < 0:
            return await self.client.incrby(key, abs(amount))
        return await self.client.decrby(key, amount)

    async def mset(self, mapping):
        """同时设置多个字符串类型的key:value(字符串指令)"""
        return await self.client.mset(mapping)

    async def get_del(self, key):
        """获取指定key的值之后删除key(原子性)(字符串指令)"""
        async with self.client.pipeline(transaction=True) as pipeline:
            value, success = await (pipeline.get(key).delete(key).execute())
            return value, success

    async def get_ex(self, key, ex):
        """获取指定key的值并且给key设置有效期(原子性操作)(字符串指令)"""
        async with self.client.pipeline(transaction=True) as pipeline:
            value, success = await (pipeline.get(key).expire(key, ex).execute())
            return value, success

    async def append(self, key, value):
        """key不存在则创建并且将值设置为value，当key存在在原来value的最后添加新的value(字符串指令)"""
        return await self.client.append(key, value)

    async def incr_by_float(self, key, amount):
        """给浮点数加amount(字符串指令)"""
        return await self.client.incrbyfloat(key, amount)

    async def msetnx(self, mapping):
        """同时在多个key不存在的时候设置value(字符串指令)"""
        return await self.client.msetnx(mapping)

    async def psetex(self, key, time_at, value):
        """给key设置value的同时设置key的过期时间，单位为毫秒(字符串指令)"""
        return await self.client.psetex(key, time_at, value)

    async def setex(self, key, time_at, value):
        """给key设置value的同时设置key的过期时间，单位为秒(字符串指令)"""
        return await self.client.setex(key, time_at, value)

    async def setnx(self, key, value):
        """当key不存在的时候，设置value(字符串指令)"""
        return await self.client.setnx(key, value)

    async def set_range(self, key, offset, value):
        """替换指定范围的字符串数据(字符串指令)"""
        return await self.client.setrange(key, offset, value)

    async def get_set(self, key, value):
        """获取key对应的值，并且设置新的值(字符串命令)，返回的是旧的值"""
        return await self.client.getset(key, value)

    async def lpush(self, key, *value):
        """向队首中添加元素(列表命令)"""
        return await self.client.lpush(key, *value)

    async def rpush(self, key, *value):
        """向队尾中添加元素(列表命令)"""
        return await self.client.rpush(key, *value)

    async def lpop(self, key):
        """从队首pop出一个元素(列表命令)"""
        return await self.client.lpop(key)

    async def rpop(self, key):
        """从队尾pop出一个元素(列表命令)"""
        return await self.client.rpop(key)

    async def lrange(self, key, start=0, stop=-1):
        """获取队列中的指定范围内的元素，默认获取全部元素(列表命令)"""
        return await self.client.lrange(key, start, stop)

    async def lmove(self, source, destination, move_from='left', move_to='left'):
        """将队列中的一个元素移动到另一个队列中 非原子性(列表命令)，返回移动的元素值和新队列的长度"""
        async with self.client.pipeline(transaction=True) as pipeline:
            if move_from == 'left':
                value = await pipeline.lpop(source).execute()
                if not value[0]:
                    return None, 0
                if move_to == 'left':
                    length = await (pipeline.lpush(destination, value[0]).execute())
                if move_to == 'right':
                    length = await (pipeline.rpush(destination, value[0]).execute())
            if move_from == 'right':
                value = pipeline.rpop(source).execute()
                if move_to == 'left':
                    length = (pipeline.lpush(destination, value[0]).execute())
                if move_to == 'right':
                    length = await (pipeline.rpush(destination, value[0]).execute())
            return value[0], length[0]

    async def linsert(self, key, where, refvalue, value):
        """在指定的元素前(后)插入新的值(列表命令)"""
        return await self.client.linsert(key, where, refvalue, value)

    async def lpushx(self, key, value):
        """向队首添加元素，仅在队列存在的时候执行(列表命令)"""
        return await self.client.lpushx(key, value)

    async def ltrim(self, key, start, end):
        """修剪队列(列表命令)"""
        return await self.client.ltrim(key, start, end)

    async def lindex(self, key, index):
        """从队首开始获取指定索引位置的元素(列表命令)"""
        return await self.client.lindex(key, index)

    async def lpops(self, key, value, **kwargs):
        """从队首删除指定元素，并且返回元素所在的索引(列表命令)"""
        return await self.client.lpos(key, value, **kwargs)

    async def hset(self, name, key, value, mapping):
        """写入hash值(hash命令)"""
        return await self.client.hset(name, key, value, mapping)

    async def hmset(self, name, mapping):
        """写入多个hash值(hash命令)"""
        return await self.client.hmset(name, mapping)

    async def hgetall(self, name):
        """获取hash指定name下所有field和对应的值(hash命令)"""
        return await self.client.hgetall(name)

    async def hmget(self, name, *key):
        """批量获取hash指定name的多个field(hash命令)"""
        return await self.client.hmget(name, *key)

    async def hget(self, name, key):
        """获取hash指定name的指定field(hash命令)"""
        return await self.client.hget(name, key)

    async def hincrby(self, name, key, amount):
        """将指定name下key的值加amount(hash命令)"""
        return await self.client.hincrby(name, key, amount)

    async def hexists(self, name, key):
        """判断指定name下的key是否存在(hash命令)"""
        return await self.client.hexists(name, key)

    async def hkeys(self, name):
        """获取指定name下所有的key"""
        return await self.client.hkeys(name)

    async def hvals(self, name):
        """获取指定name下所有的value"""
        return await self.client.hvals(name)

    async def hsetnx(self, name, field, value):
        """在指定name下key不存在的时候设置value"""
        return await self.client.hsetnx(name, field, value)

    async def hstrlen(self, name, key):
        """获取指定name下key对应的字符串的长度"""
        return await self.client.hstrlen(name, key)

    async def hscan(self, name, cursor=0):
        """扫描指定name，并且返回当前游标的位置"""
        return await self.client.hscan(name, cursor)

    async def sadd(self, key, *members):
        """向集合中添加元素(集合命令)"""
        return await self.client.sadd(key, *members)

    async def smembers(self, name):
        """获取集合中的所有元素(集合命令)"""
        return await self.client.smembers(name)

    async def sismember(self, name, member):
        """检查集合中是否存在某个元素(集合命令)"""
        return await self.client.sismember(name, member)

    async def sinter(self, set_name, *args):
        """获取集合的交集(集合命令)"""
        return await self.client.sinter(set_name, *args)

    async def sdiff(self, key, *keys):
        """获取第一个集合和其他集合差异的成员(集合命令)"""
        return await self.client.sdiff(key, *keys)

    async def sdiffstore(self, dist, key, *keys):
        """获取第一个集合和其他集合差异的成员，并将其存储到dist新集合中(集合命令)"""
        return await self.client.sdiffstore(dist, key, *keys)

    async def spop(self, key, count):
        """从集合中删除元素，并且返回集合中的前n条数据(集合命令)"""
        return await self.client.spop(key, count)

    async def sunion(self, key, *keys):
        """获取两个集合的并集(集合命令)"""
        return await self.client.sunion(key, *keys)

    async def len(self, key):
        """获取key对应的值的长度，支持str, list, hash, set类型"""
        data_type = await self.client.type(key)
        if data_type == 'string':
            return await self.client.strlen(key)
        if data_type == 'list':
            return await self.client.llen(key)
        if data_type == 'hash':
            return await self.client.hlen(key)
        if data_type == 'set':
            # 获取集合的大小
            return await self.client.scard(key)

    async def exists(self, key):
        """判断对应的key是否存在"""
        return await self.client.exists(key)

    async def delete(self, keys):
        """删除key，可以删除多个"""
        return await self.client.delete(keys)

    async def expire(self, key, expire_at):
        """设置key的过期时间,单位为秒"""
        return await self.client.expire(key, expire_at)

    async def get_type(self, key):
        """获取指定key对应的数据类型,返回的是redis中的数据类型而不是python的数据类型"""
        return await self.client.type(key)

    async def ttl(self, key):
        """获取key的有效期"""
        return await self.client.ttl(key)


redis_util = AsyncRedisUtil(host='redis://localhost', password=1277431229)


if __name__ == '__main__':
    import asyncio
    # print(asyncio.run(redis_util.get('name')))
    # print(asyncio.run(redis_util.mget(['name'])))
    # print(asyncio.run(redis_util.hkeys("hmset")))
    # print(asyncio.run(redis_util.hstrlen("hmset", "age")))
    # print(asyncio.run(redis_util.sadd("set_test1", 'name', "address")))
    print(asyncio.run(redis_util.sunion("set_test1", 'set_test')))
