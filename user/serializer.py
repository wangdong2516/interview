import re

from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    """
        用户登录序列化器
    """

    username = serializers.CharField(
        allow_null=False, required=True, error_messages={'required': '缺少用户名参数'}, max_length=16, min_length=8
    )
    password = serializers.CharField(
        allow_null=False, required=True, error_messages={'required': '缺少密码参数'}, max_length=16, min_length=8
    )

    def validate_password(self, password):
        """
            校验密码是否包含大写字母、小写字母、数字
        Args:
            password:

        Returns:

        """
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError('密码必须包含大写字母')
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError('密码必须包含小写字母')
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError('密码必须包含数字')
        return password
