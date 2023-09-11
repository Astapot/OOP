from rest_framework import serializers
from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']



class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['id', 'address', 'products', 'positions']
    # настройте сериализатор для склада

    def create(self, validated_data):
        # print(validated_data)

        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        # Stock.objects.create(address=validated_data['address'])
        # stock_id = Stock.objects.all().filter(address=validated_data['address'])[0]['id']
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for i in positions:
            i['stock'] = stock
            print(i)
            StockProduct.objects.update_or_create(
                **i
            )
        return stock


    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # print(positions)
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for i in positions:
            # print(i)
            # StockProduct.objects.all().filter(product=i['product'], stock=stock).update(
            #     **i
            # )
            StockProduct.objects.update_or_create(stock=stock, product=i['product'], defaults={'price': i['price'], 'quantity': i['quantity']})
        return stock
