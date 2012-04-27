from django.contrib import admin
from django import forms
from django.forms.util import ErrorList
from members.models import Member, Mat, Division, Match, Tournament
from django.http import HttpResponse, HttpResponseRedirect

class MatAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser:
            qs = self.model._default_manager.all()
        else:
            qs = self.model._default_manager.filter(user=request.user)
        return qs

def make_check_in(modeladmin, request, queryset):
    queryset.update(check_in=True)

class MemberAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def qr_code(self, obj):
        try: url = obj.qr_image.url
        except ValueError: return ''
        return '<img src="%s" alt="" />' % url
    qr_code.allow_tags = True

    exclude = ['user']
    list_display = ('first_name', 'last_name', 'dojo', 'division', 'check_in', 'qr_code')
    list_filter = ['check_in']
    ordering = ['dojo', 'last_name']
    search_fields = ['last_name', 'first_name', 'dojo']
    actions = [make_check_in]

class DivisionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'gender', 'age', 'weight', 'rank', 'mat')
    search_fields = ['mat', 'gender', 'age', 'weight', 'rank']
    filter_horizontal = ("match",)
    
class MatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        try:
            match_instance = Match.objects.filter(pk=self.instance.pk)[0]
            competitors = match_instance.competitors.all()
            if(len(competitors) > 0):
                pk_dict = {}
                for m in competitors:
                    pk_dict[m.pk] = m.__unicode__()
                tuple_list = [(0, '------')]
                for key, val in pk_dict.iteritems():
                    tuple_list.append((key, val))
                choices = tuple(tuple_list)
            else:
                choices = ( (0, 'No Competitors'), )
        except IndexError: 
            choices = ( (0, 'No Competitors'), )
        self.fields['winner'] = forms.ChoiceField(choices=choices)

class MatchAdmin(admin.ModelAdmin):
    def p1_name(self, obj):
        competitors = obj.competitors.all()
        try: return competitors[0]
        except IndexError: return ""
    p1_name.short_description = 'Competitor #1'

    def p2_name(self, obj):
        competitors = obj.competitors.all()
        try: return competitors[1]
        except IndexError: return ""
    p2_name.short_description = 'Competitor #2'

    def get_winner_name(self, obj):
        try: winner = obj.competitors.filter(pk=obj.winner)[0]
        except IndexError: winner = ''
        return winner
    get_winner_name.short_description = 'Winner'

    def match_is_finished(self, obj):
        if obj.winner == 0:
            return False
        return True
    match_is_finished.boolean = True

    def queryset(self, request):
        if request.user.is_superuser:
            qs = self.model._default_manager.all()
        else:
            qs = self.model._default_manager.filter(mat__user=request.user)
        return qs

    list_filter = ('mat',)
    _list_filter = list_filter
    def changelist_view(self, request, extra_context=None): 
        if request.user.is_superuser:
            self.list_filter = self._list_filter
        else:
            self.list_filter = None
        return super(MatchAdmin, self).changelist_view(request, extra_context)

    list_display = ('__unicode__', 'p1_name', 'p2_name', 'get_winner_name', 'match_is_finished', 'mat')
    ordering = ['mat', 'match_number']
    filter_horizontal = ("competitors",)
    form = MatchForm

class TournamentAdmin(admin.ModelAdmin):
    def add_view(self, request):
        if request.method == "POST":
            if Tournament.objects.count() >= 1:
                return HttpResponse('You only can have one tournament description at the time.')
        return super(TournamentAdmin, self).add_view(request)

admin.site.register(Member, MemberAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Mat, MatAdmin)
admin.site.register(Tournament, TournamentAdmin)
