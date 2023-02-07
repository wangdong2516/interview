from typing import Dict, Any

from bson import ObjectId
from pymongo import MongoClient


class MongoUtil(object):
    """
        封装的mongodb工具类
    """

    def __init__(
            self, db_name, collection_name, host: str = None, port: int = 27017,
            *args, **kwargs
    ):
        self.host = host
        self.port = port
        self.args = args
        self.kwargs = kwargs
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = self.get_client(host=host, port=port, *self.args, **self.kwargs)
        self.db = self.get_db(self.db_name)
        self.collection = self.get_collection(db_name, collection_name)

    @staticmethod
    def get_client(host: str = None, port: int = 27017, *args, **kwargs):
        """
            获取一个mongodb客户端
        Args:
            host: mongodb实例所在主机
            port: mongodb端口

        Returns:

        """
        client = MongoClient(host=host, port=port, *args, **kwargs)
        return client

    def get_db(self, db_name: str):
        """
            获取数据库
                当数据库不存在的时候，mongo会自动创建，所以当获取不存在的数据库的时候，不会报错
        Args:
            db_name: 数据库名称

        Returns:

        """
        return getattr(self.client, db_name)

    def get_collection(self, db_name, collection_name):
        """
            获取mongo中的一个集合，当集合不存在的时候，mongo会自动创建集合，所以不会报错
        Args:
            db_name: 数据库名称
            collection_name: 集合名称

        Returns:

        """
        return getattr(self.get_db(db_name), collection_name)

    def insert_one(self, document: Dict, *args, **kwargs) -> Any:
        """
            插入单条数据
        Args:
            document: 需要插入的文档数据

        Returns:
            ObjectId:插入对象的主键值->Mongo中的ObjectID
        """
        return self.collection.insert_one(
            document=document, *args, **kwargs
        ).inserted_id

    def query(self, document: Dict = None, skip: int = None, limit: int = None):
        """
            查询文档
        Args:
            document:查询条件
            skip: 希望跳过的数据数量
            limit: 希望返回的数据数量

        Returns:

        """
        # 如果没有传递查询条件，查询条件默认为空{}
        if not document:
            document = dict()
        cursor = self.collection.find(document)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)


mongo_util = MongoUtil(db_name='article', collection_name='pymongo')
print(mongo_util.query(skip=1))

