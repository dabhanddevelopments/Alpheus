from django.contrib import admin


class BaseMixin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(BaseMixin, self).queryset(request)
        return qs.filter(fund__classification=self.classification)


class FundMixin(BaseMixin):
    classification = 1


class EquityMixin(BaseMixin):
    classification = 5


class OptionMixin(BaseMixin):
    classification = 7


class FixedIncomeMixin(BaseMixin):
    classification = 3


class SidePocketMixin(BaseMixin):
    classification = 9


class PrivateEquityMixin(BaseMixin):
    classification = 10

