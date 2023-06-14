import datetime
from typing import Dict, Any, List, Union

from bson import ObjectId
from pymongo import MongoClient


class MongoUtil(object):
    """
    封装的mongodb工具类
    """

    def __init__(
        self,
        db_name,
        collection_name,
        host: str = None,
        port: int = 27017,
        *args,
        **kwargs,
    ):
        """
            连接MongoDB实例并且选择指定的数据库和集合
        Args:
            db_name: 数据库名称
            collection_name: 集合名称
            host: mongodb实例(集群)地址
            port: mongodb端口，默认27017
            *args: 位置参数
            **kwargs: 关键字参数
        """
        self.host = host
        self.port = port
        self.args = args
        self.kwargs = kwargs
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = self.get_client(host=host, port=port, *self.args, **self.kwargs)
        self.db = self.get_db(self.db_name)
        self.collection = self.get_collection(db_name, collection_name)

    def __str__(self):
        return f"数据库:{self.db_name}-集合:{self.collection_name}"

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
            插入单条数据并且返回插入之后的ObjectID，该ObjectID在集合中是唯一的
        Args:
            document: 需要插入的文档数据,为Python中的字典类型的数据

        Returns:
            ObjectId:插入对象的主键值->Mongo中的ObjectID
        """
        return self.collection.insert_one(
            document=document, *args, **kwargs
        ).inserted_id

    def query(
        self, document: Dict = None, skip: int = None, limit: int = None
    ) -> List[Dict]:
        """
            查询文档(多个文档), 如果查询条件匹配到的只有单个文档，也将以列表的形式返回
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

    def get_one(
        self, document: Dict = None, skip: int = None, limit: int = None
    ) -> Union[Dict, None]:
        """
            查询单个文档
        Args:
            document: 查询条件document
            skip: 希望跳过的数据数量
            limit: 希望返回的数据数量

        Returns:

        """
        if not document:
            document = dict()
        cursor = self.collection.find_one(document)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return dict(cursor) if cursor is not None else None

    def show_tables(self) -> List[str]:
        """
            获取数据库中的所有集合，以列表的形式返回
        Returns:

        """
        return self.db.list_collection_names()

    def show_databases(self) -> List[str]:
        """
            获取所有的数据库的名称，以列表的形式返回
        Returns:

        """
        return self.client.list_database_names()

    def bulk_insert(self, document: List[Dict], *args, **kwargs):
        """
            批量插入文档，返回插入成功的文档ObjectID
        Args:
            document: 文档列表
            *args: 位置参数
            **kwargs: 关键字参数
        Returns:
        """
        return self.collection.insert_many(document, *args, **kwargs).inserted_ids

    def count(self, document: Dict = None, *args, **kwargs):
        if not document:
            document = {}
        return self.collection.count_documents(document)


mongo_util = MongoUtil(db_name="wangdong", collection_name="test")
print(mongo_util)
print(mongo_util.query({"movie": "王牌替身"}))
print(f"所有的数据库:{mongo_util.show_databases()}")
print(mongo_util.show_tables())
print(mongo_util.get_one({"movie": "王牌替身"}))
print(mongo_util.get_one({"movie": "王牌替身2"}))
document = [
    {"movie": "钢铁侠", "create_time": "2020-09-09", "reviews": ["托尼屎大颗"]},
    {"movie": "钢铁侠2", "create_time": "2021-09-09", "reviews": ["精彩的对决"]},
]
# print(mongo_util.bulk_insert(document))
print(mongo_util.count())
print(mongo_util.client.dd.ss)
# print(mongo_util.insert_one({"movie": "我好喜欢你", 'create_time': datetime.datetime.now(), 'reviews': ["很心痛", "看完容易emo😯"]}))
print(mongo_util.query(document={"message": {"$regex": ".*测试.*"}}))
