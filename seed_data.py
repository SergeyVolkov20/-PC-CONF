import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'someproject.settings')
django.setup()

from someapp.models import Category, Product, Specification

def seed():
    print("Очистка старых данных...")
    Specification.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()

    print("Создание категорий...")
    cpu_cat = Category.objects.create(name='Процессоры', slug='cpu', sort_order=1)
    mb_cat = Category.objects.create(name='Материнские платы', slug='motherboard', sort_order=2)
    ram_cat = Category.objects.create(name='Оперативная память', slug='ram', sort_order=3)
    gpu_cat = Category.objects.create(name='Видеокарты', slug='gpu', sort_order=4)
    psu_cat = Category.objects.create(name='Блоки питания', slug='psu', sort_order=5)
    case_cat = Category.objects.create(name='Корпуса', slug='case', sort_order=6)

    print("Создание товаров...")


    cpu1 = Product.objects.create(category=cpu_cat, name='Intel Core i5-13600KF', brand='Intel', price=25000, stock=10)
    Specification.objects.create(product=cpu1, spec_key='socket', spec_value='LGA1700')
    Specification.objects.create(product=cpu1, spec_key='tdp', spec_value='125')

    cpu2 = Product.objects.create(category=cpu_cat, name='AMD Ryzen 5 7600X', brand='AMD', price=22000, stock=8)
    Specification.objects.create(product=cpu2, spec_key='socket', spec_value='AM5')
    Specification.objects.create(product=cpu2, spec_key='tdp', spec_value='105')


    mb1 = Product.objects.create(category=mb_cat, name='ASUS PRIME Z790-A', brand='ASUS', price=30000, stock=5)
    Specification.objects.create(product=mb1, spec_key='socket', spec_value='LGA1700')
    Specification.objects.create(product=mb1, spec_key='memory_type', spec_value='DDR5')
    Specification.objects.create(product=mb1, spec_key='form_factor', spec_value='ATX')

    mb2 = Product.objects.create(category=mb_cat, name='MSI MAG B650 Tomahawk', brand='MSI', price=18000, stock=7)
    Specification.objects.create(product=mb2, spec_key='socket', spec_value='AM5')
    Specification.objects.create(product=mb2, spec_key='memory_type', spec_value='DDR5')
    Specification.objects.create(product=mb2, spec_key='form_factor', spec_value='ATX')


    ram1 = Product.objects.create(category=ram_cat, name='Kingston Fury DDR5 16GB', brand='Kingston', price=8000, stock=20)
    Specification.objects.create(product=ram1, spec_key='memory_type', spec_value='DDR5')


    gpu1 = Product.objects.create(category=gpu_cat, name='NVIDIA RTX 4070', brand='Palit', price=60000, stock=3)
    Specification.objects.create(product=gpu1, spec_key='tdp', spec_value='200')
    Specification.objects.create(product=gpu1, spec_key='length', spec_value='280')


    psu1 = Product.objects.create(category=psu_cat, name='БП на 650W', brand='DeepCool', price=6000, stock=15)
    Specification.objects.create(product=psu1, spec_key='power', spec_value='650')

    psu2 = Product.objects.create(category=psu_cat, name='БП на 1000W', brand='Corsair', price=15000, stock=5)
    Specification.objects.create(product=psu2, spec_key='power', spec_value='1000')


    case1 = Product.objects.create(category=case_cat, name='Zalman i3 Neo', brand='Zalman', price=4000, stock=10)
    Specification.objects.create(product=case1, spec_key='form_factor_support', spec_value='ATX, Micro-ATX')
    Specification.objects.create(product=case1, spec_key='max_gpu_length', spec_value='330')

    print("✅ Тестовые данные успешно добавлены!")

if __name__ == '__main__':
    seed()