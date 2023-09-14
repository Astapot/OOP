
from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        # advs = Advertisement.objects.all().filter(creator=self.context["request"].user)
        # print(advs)
        # OPENED = 0
        # for adv in advs:
        #     if adv.status == 'OPEN':
        #         OPENED += 1
        # validated_data["creator"] = self.context["request"].user
        # if OPENED >= 10:

        # код выше оставил для себя, на будущее

        # opened = Advertisement.objects.all().filter(creator=self.context["request"].user, status='OPEN').count()
        # if opened >= 10:
        #     raise ValidationError('Количество открытых объявлений не может превышать 10 штук')
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        opened = Advertisement.objects.all().filter(creator=self.context["request"].user, status='OPEN').count()
        if opened >= 10 and data.get('status') != 'CLOSED':
            raise ValidationError('Количество открытых объявлений не может превышать 10 штук')
        # TODO: добавьте требуемую валидацию
        return data

    def update(self, instance, validated_data):
        # advs = Advertisement.objects.all().filter(creator=self.context["request"].user)
        # OPENED = 0
        # for adv in advs:
        #     if adv.status == 'OPEN':
        #         OPENED += 1
        # # print(OPENED)
        # if OPENED >= 10 and validated_data.get('status') and validated_data.get('status') != 'CLOSED':


        # opened = Advertisement.objects.all().filter(creator=self.context["request"].user, status='OPEN').count()
        # if opened >= 10 and validated_data.get('status') != 'CLOSED':
        #     raise ValidationError('Количество открытых объявлений не может превышать 10 штук')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.creator = self.context["request"].user
        instance.save()
        return instance
