from django.contrib import admin

from .models import TokenAuthorization


class TokenAuthorizationAdmin(admin.ModelAdmin):
    """Model admin for the TokenAuthorization model."""
    list_display = ('id', 'reason', 'user', 'token', 'email_address',
                    'created_user', 'expires')
    readonly_fields = list_display + ('email_sent', 'text')
    fields = readonly_fields


admin.site.register(TokenAuthorization, TokenAuthorizationAdmin)
