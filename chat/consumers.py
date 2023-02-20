import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
            建立连接
        Returns:

        """
        # 从路由中解析聊天室的名称
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # 聊天室组的名称-基于聊天室的名称
        self.room_group_name = f'chat_{self.room_name}'
        # 自动生成的频道名称
        # 将异步调用修改为同步调用，创建组和对应的频道
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # 接收请求
        await self.accept()

    async def disconnect(self, code):
        """
            关闭链接
        Args:
            code:

        Returns:

        """
        # 断开连接的时候关闭通道层
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """
            接收消息
        Args:
            text_data:消息内容
            bytes_data:消息的二进制内容

        Returns:

        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # 向组中发送消息
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chats_message', 'message': message}
        )

    async def chats_message(self, event):
        """
            从组中接受消息
        Args:
            event:

        Returns:

        """
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
