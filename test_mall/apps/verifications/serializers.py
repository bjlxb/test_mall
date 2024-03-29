from rest_framework import serializers
from django_redis import get_redis_connection

# 两种方式：
#   serializers.Serializer
#   serializers.ModelSerializer
# 因为没有模型，所以使用serializers.Serializer


class RegisterSmscodeSerializer(serializers.Serializer):
    # 用户输入的验证码
    text = serializers.CharField(max_length=4, min_length=4)
    image_code_id = serializers.UUIDField(required=True)

    """
    序列化器的验证：
    1.字段类型
    2.字段选项
    3.单个字段
    4.多个字段
    """
    def validate(self, attrs):
        # 1.获取用户提交的验证码
        text = attrs.get('text')
        # 2.获取redis的验证码
        # 2.1链接redis
        redis_conn = get_redis_connection('code')
        # 2.2获取数据
        image_id = attrs.get('image_code_id')
        redis_text = redis_conn.get('img_'+str(image_id))
        # 2.3redis的数据有时效
        if redis_text is None:
            raise serializers.ValidationError('图片验证码过期')
        # 3.比对
        # 3.1redis的数据是bytes类型
        # 3.2大小写问题
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError('输入错误')
        return attrs





















