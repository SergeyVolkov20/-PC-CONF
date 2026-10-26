class CompatibilityChecker:
    """Класс для проверки совместимости комплектующих в сборке."""

    def __init__(self, build):
        self.build = build
        self.components = self._collect_components()

    def _collect_components(self):
        """Собирает характеристики всех компонентов сборки по категориям."""
        components = {}
        for item in self.build.items.select_related('product__category').prefetch_related('product__specifications'):
            slug = item.product.category.slug
            specs = {s.spec_key: s.spec_value for s in item.product.specifications.all()}
            specs['_name'] = item.product.name
            components[slug] = specs
        return components

    def check_all(self):
        """Запускает все проверки. Возвращает результат и список ошибок."""
        errors = []

        if 'cpu' in self.components and 'motherboard' in self.components:
            errors += self._check_cpu_mb()

        if 'motherboard' in self.components and 'ram' in self.components:
            errors += self._check_mb_ram()

        if 'psu' in self.components:
            errors += self._check_psu()

        if 'case' in self.components:
            errors += self._check_case()

        return {
            'compatible': len(errors) == 0,
            'errors': errors
        }

    def _check_cpu_mb(self):
        errors = []
        cpu = self.components['cpu']
        mb = self.components['motherboard']
        if cpu.get('socket') != mb.get('socket'):
            errors.append(
                f"Сокет процессора {cpu['_name']} ({cpu.get('socket')}) "
                f"не совпадает с сокетом платы {mb['_name']} ({mb.get('socket')})"
            )
        return errors

    def _check_mb_ram(self):
        errors = []
        mb = self.components['motherboard']
        ram = self.components['ram']
        mb_memory = mb.get('memory_type', '')
        ram_memory = ram.get('memory_type', '')
        if ram_memory not in mb_memory:
            errors.append(
                f"Плата {mb['_name']} поддерживает {mb_memory}, "
                f"а ОЗУ {ram['_name']} — {ram_memory}"
            )
        return errors

    def _check_psu(self):
        errors = []
        psu = self.components['psu']
        psu_power = int(psu.get('power', 0))

        total_tdp = 0
        for key in ['cpu', 'gpu']:
            if key in self.components:
                total_tdp += int(self.components[key].get('tdp', 0))

        recommended = int(total_tdp * 1.3)
        if psu_power < recommended:
            errors.append(
                f"БП {psu['_name']} на {psu_power}Вт недостаточен. "
                f"Рекомендуется минимум {recommended}Вт"
            )
        return errors

    def _check_case(self):
        errors = []
        case = self.components['case']

        if 'motherboard' in self.components:
            mb = self.components['motherboard']
            supported = case.get('form_factor_support', '')
            if mb.get('form_factor') not in supported:
                errors.append(
                    f"Корпус {case['_name']} не поддерживает форм-фактор "
                    f"{mb.get('form_factor')}"
                )

        if 'gpu' in self.components:
            gpu = self.components['gpu']
            if 'length' in gpu and 'max_gpu_length' in case:
                if int(gpu['length']) > int(case['max_gpu_length']):
                    errors.append(
                        f"Видеокарта {gpu['_name']} ({gpu['length']}мм) "
                        f"не влезает в корпус (макс. {case['max_gpu_length']}мм)"
                    )
        return errors


def recalculate_build(build):
    """Пересчитывает итоговую цену и TDP сборки."""
    total_price = 0
    total_tdp = 0

    for item in build.items.select_related('product').prefetch_related('product__specifications'):
        total_price += item.product.price * item.quantity
        tdp_spec = item.product.specifications.filter(spec_key='tdp').first()
        if tdp_spec:
            total_tdp += int(tdp_spec.spec_value) * item.quantity

    build.total_price = total_price
    build.total_tdp = total_tdp
    build.save(update_fields=['total_price', 'total_tdp'])