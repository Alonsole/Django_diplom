from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, OrderItem, \
    Contact, ConfirmEmailToken, Order
from django.db.models import Sum, F

from .signals import send_order_email


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'type')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'type')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'type', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # Добавьте эту строку для использования Baton
    change_form_template = 'baton/change_form.html'


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """list_display: Определяет столбцы, которые будут видны в списке заказов.
       list_filter: Позволяет фильтровать список заказов по полю `state` (статус заказа).
       actions: Список действий, которые могут быть выполнены над группой заказов.
    """
    list_display = ['id', 'user', 'state', 'dt', 'contact', 'get_total_sum', 'get_items']
    list_filter = ['state']
    actions = ['set_status_confirmed',
               'set_status_assembled',
               'set_status_sent',
               'set_status_delivered',
               'set_status_canceled']

    def get_total_sum(self, obj):
        return obj.ordered_items.aggregate(
            total=Sum(F('quantity') * F('product_info__price'))
        )['total']

    get_total_sum.short_description = 'Общая стоимость'

    def get_items(self, obj):
        return ", ".join([
            f"{item.product_info.product.name} (x{item.quantity})"
            for item in obj.ordered_items.all()
        ])

    get_items.short_description = 'Товары'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('ordered_items__product_info__product')

    """
    Методы `set_status_...` предназначены для выполнения соответствующих действий над выбранной группой заказов
    """

    def set_status_confirmed(self, request, queryset):
        self._set_status_and_notify(queryset, 'confirmed', request)

    set_status_confirmed.short_description = "Установить статус «Подтверждён»"

    def set_status_assembled(self, request, queryset):
        self._set_status_and_notify(queryset, 'assembled', request)

    set_status_assembled.short_description = "Установить статус «Собран»"

    def set_status_sent(self, request, queryset):
        self._set_status_and_notify(queryset, 'sent', request)

    set_status_sent.short_description = "Установить статус «Отправлен»"

    def set_status_delivered(self, request, queryset):
        self._set_status_and_notify(queryset, 'delivered', request)

    set_status_delivered.short_description = "Установить статус «Доставлен»"

    def set_status_canceled(self, request, queryset):
        self._set_status_and_notify(queryset, 'canceled', request)

    set_status_canceled.short_description = "Установить статус «Отменён»"

    def _set_status_and_notify(self, queryset, status, request):
        for order in queryset:
            order.state = status
            order.save()
            send_order_email(order.user.id, order_id=order.id, status=status)
        self.message_user(request, f"{queryset.count()} заказов были обновлены до статуса {status}.")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)
