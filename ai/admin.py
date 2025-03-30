from django.contrib import admin
from ai.models import AISettings, AI, Chat, Message


# AISettings Admin
@admin.register(AISettings)
class AISettingsAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]


# AI Admin
@admin.register(AI)
class AIAdmin(admin.ModelAdmin):
    list_display = ["id", "settings", "created_at", "updated_at"]
    search_fields = ["id", "settings__id"]
    list_filter = ["created_at", "updated_at"]
    raw_id_fields = ["settings"]


# Message Inline for Chat (Displays related messages in the Chat admin)
class MessageInline(admin.TabularInline):
    model = Message
    extra = 1  # allows adding one additional message inline


# Chat Admin
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "ai", "created_at", "updated_at", "created_by"]
    search_fields = ["id", "ai__id"]
    list_filter = ["created_at", "updated_at"]
    inlines = [MessageInline]


# Message Admin
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "chat", "messenger", "index", "created_at"]
    search_fields = ["id", "chat__id", "messenger"]
    list_filter = ["messenger", "created_at", "updated_at"]
    raw_id_fields = ["chat"]
